import mimetypes
import multiprocessing
import re
import traceback
import urllib.parse as urlparse
from concurrent.futures import as_completed, ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple, List, Union

import certifi
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm
from unidown import tools
from unidown.core.settings import Settings
from unidown.plugin import APlugin, PluginInfo, LinkItemDict, LinkItem, PluginException
from urllib3.exceptions import HTTPError

from unidown_mr_de.exceptions import GetEbookLinksError
from unidown_mr_de.link_item import MrLinkItem
from unidown_mr_de.tools import sizeof_fmt


class Plugin(APlugin):
    """
    Plugin class, derived from APlugin.
    """
    _info = PluginInfo('mr_de', '1.0.0', 'www.mobileread.com')

    def __init__(self, settings: Settings, options: Dict[str, Any] = None):
        super().__init__(settings, options)
        self._unit = 'eBook'

        self.wiki_list_file = self.temp_dir.joinpath('wiki_list.html')
        self.wiki_list_link = "https://wiki.mobileread.com/wiki/Free_eBooks-de/de"

        self.threads_dir = self.temp_dir.joinpath('threads/')
        self.threads_dir.mkdir(parents=True, exist_ok=True)
        self.list_link = "/forums/showthread.php?t=31130&page="
        self.listing_dir = self.temp_dir.joinpath('list/')
        self.listing_dir.mkdir(parents=True, exist_ok=True)

        self.showthread_link = "/forums/showthread.php"
        self.attachment_link = "/forums/attachment.php"
        self.rx_invalid = re.compile(r"[^\w\s\d_.]")

    def _create_download_data(self) -> LinkItemDict:
        # delete temporary directories (should be already deleted by unidown)
        # and create them again
        tools.unlink_dir_rec(self.listing_dir)
        self.listing_dir.mkdir(parents=True, exist_ok=True)
        tools.unlink_dir_rec(self.threads_dir)
        self.threads_dir.mkdir(parents=True, exist_ok=True)

        # download first page from the listing thread to get the total page count
        self.download_as_file(self.list_link + '1', self.listing_dir.joinpath('1.html'))
        pages = self._get_page_count()

        # download all pages
        pages_dict = LinkItemDict({self.list_link + str(page): LinkItem(str(page) + '.html', datetime(1970, 1, 1)) for page in range(2, pages + 1)})
        self._download_listings(pages_dict)
        listing_success, listing_failed = self.check_download(pages_dict, self.listing_dir)
        if len(listing_failed) != 0:
            raise PluginException("No all listing threads were downloaded.")
        if not self.wiki_list_file.exists():
            raise PluginException("Failed to download the wiki list.")

        # extract links from the listing threads to get the links to the other
        thread_list, attach_list = self._extract_listing(listing_success)

        # print possible invalid links
        rx_valid_link = re.compile(r"/forums/showthread\.php\?((t=\d+)|(p=\d+)|(s=(\d|\w)+)&?)+(&page=\d+)?")
        for thread in thread_list:
            if not rx_valid_link.fullmatch(thread):
                self.log.warning(f"thread link '{thread}' may not be valid")

        # download content threads
        thread_dict = LinkItemDict({thread: LinkItem(self.rx_invalid.sub('_', thread) + '.html', datetime(1970, 1, 1)) for thread in thread_list})
        self.download(thread_dict, self.threads_dir, 'Downloading content threads', 'thread')
        content_success, _ = self.check_download(thread_dict, self.threads_dir)
        if len(content_success) == 0:
            raise PluginException("No content thread was downloaded successful.")

        # extract attachmend links
        attach_list = self._extract_content(attach_list, content_success)
        # generate attachment links, with file size and type
        attach_dict = self._create_attach_link_item_dict(attach_list)

        # print stats
        self.log.info("Found the following:")
        self._log_stats(collect_stats(attach_dict))

        # filter include, exclude from options
        for link in list(attach_dict.keys()):
            if ((self._options['include'] is not None and attach_dict[link].type not in self._options['include'])
                    or attach_dict[link].type in self._options['exclude']):
                del attach_dict[link]

        # print stats of the download
        self.log.info("Downloading the following:")
        self._log_stats(collect_stats(attach_dict))

        return attach_dict

    def _create_last_update_time(self) -> datetime:
        return datetime.now()

    def _load_default_options(self):
        if 'delay' not in self._options:
            self._options['delay'] = "10"  # set default delay to 10s
            self.log.info("Plugin option 'delay' is missing. Using 10s.")
        super(Plugin, self)._load_default_options()
        if 'include' in self._options:
            self._options['include'] = self._options['include'].split(',')
        else:
            self._options['include'] = None  # include all
        if 'exclude' in self._options:
            self._options['exclude'] = self._options['exclude'].split(',')
        else:
            self._options['exclude'] = []

    # -------------------------------------- #

    def _get_page_count(self) -> int:
        """
        Get the total page count from the listing thread.
        """
        with self.listing_dir.joinpath('1.html').open(mode='rb') as reader:
            data = reader.read()
        return int(BeautifulSoup(data, 'lxml').select(".pagenav tr td a")[-1].get('href').split('page=')[-1])

    def _download_listings(self, pages_dict: LinkItemDict):
        """
        Download the listing threads.
        """
        self.download(pages_dict, self.listing_dir, 'Downloading listing threads', 'thread')
        with urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) as https:
            with https.request('GET', self.wiki_list_link, preload_content=False, retries=urllib3.util.retry.Retry(3)) as req:
                with self.wiki_list_file.open(mode='wb') as writer:
                    writer.write(req.data)

    def _get_links_from_threads(self, files: List[Path]) -> Tuple[List[str], int]:
        """
        Get links from within a post from a thread.
        """
        job_list = []
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count() - 1) as executor:
            for file in files:
                job = executor.submit(get_links_from_thread, file)
                job_list.append(job)

            pbar = tqdm(as_completed(job_list), total=len(job_list), desc='Extract links', unit='file', mininterval=1, ncols=100, disable=self._disable_tqdm)
            for _ in pbar:
                pass

        posts = 0
        links = []
        for job in job_list:  # merge all results into one dict
            exc = job.exception()
            if exc is None:
                cur_links, cur_posts = job.result()
                links.extend(cur_links)
                posts += cur_posts
                if len(links) == 0:
                    self.log.info(f"Nothing found in {file}.")
            elif type(exc) is GetEbookLinksError:
                self.log.error(f"Something went wrong in: {file} | {exc.orig_ex}")
            else:
                self.log.error(f"Something went wrong: {exc}")

        return links, posts

    def _get_links_from_wiki(self) -> List[str]:
        """
        Get links from inside the wiki table.
        """
        with self.wiki_list_file.open(mode='rb') as reader:
            data = reader.read()
        return [url.get('href') for url in BeautifulSoup(data, 'lxml').select(".wikitable a")]

    def _filter_links(self, links: List[str]) -> List[str]:
        """
        Filter links to get only valid and links which are from mobileread.
        """
        def rewrite_link(link) -> Union[None, str]:
            # showthread.php?s=8143e4967fa6fa4f540eaf54a23a29e8 is the listing thread link, we dont want any quotations or something.
            if link is None or link.startswith("showthread.php?s=8143e4967fa6fa4f540eaf54a23a29e8") or not (
                    "attachment.php" in link or "showthread.php" in link):
                return None
            if "showthread.php" in link:
                parsed = urlparse.urlparse(link)
                query = urlparse.parse_qs(parsed.query)
                query.pop('highlight', None)
                query.pop('goto', None)
                new_query = '&'.join([f"{key}={''.join(value)}" for key, value in query.items()])
                return f"{self.showthread_link}?{new_query}".rstrip('<br />').rstrip("http://")
            if "attachment.php" in link:
                parsed = urlparse.urlparse(link)
                return f"{self.attachment_link}?{parsed.query}#{parsed.fragment}".strip('#')
            return link

        links = [rewrite_link(link) for link in links]
        return [link for link in links if link is not None]

    def _extract_listing(self, list_thread_success: LinkItemDict) -> Tuple[List[str], List[str]]:
        """
        Extract links from all listing threads.
        """
        links, posts = self._get_links_from_threads([self.listing_dir.joinpath(thread.name) for thread in list_thread_success.values()])
        self.log.info(f"found posts: {posts}")
        links.extend(self._get_links_from_wiki())
        links = self._filter_links(links)
        links = list(set(links))
        return split_thread_attach(links)

    def _extract_content(self, attach_list: List[str], content_success: LinkItemDict) -> List[str]:
        """
        Extract links from all content threads.
        """
        links, _ = self._get_links_from_threads([self.threads_dir.joinpath(thread.name) for thread in content_success.values()])
        links = self._filter_links(links)
        _, attach_list2 = split_thread_attach(links)
        attach_list.extend(attach_list2)
        attach_list = self._filter_links(attach_list)
        return list(set(attach_list))

    def _create_attach_link_item(self, link: str) -> Tuple[str, LinkItem]:
        """
        Create attachment LinkItem with additional information about file size and type.
        """
        resp = self._downloader.request('HEAD', link, preload_content=False)
        if resp.status != 200:
            raise HTTPError(f"{link} | {resp.status}")

        # make filenames valid
        rx_filename = re.compile(r'filename="(.+)"')
        filename_match = re.search(rx_filename, resp.headers.get('Content-disposition', ""))
        if filename_match is not None:
            file_name = urlparse.unquote(filename_match.group(1))
        else:
            file_name = self.rx_invalid.sub('_', link)

        modified = datetime.utcnow()
        try:
            modified = datetime.strptime(resp.headers.get('Last-Modified.', ""), '%a, %d %b %Y %H:%M:%S GMT')
        except ValueError:
            try:
                d_query = urlparse.parse_qs(urlparse.urlparse(link).query).get('d', None)
                if d_query is not None:
                    modified = datetime.utcfromtimestamp(int(''.join(d_query)))
            except Exception:
                pass

        file_size = int(resp.headers.get('Content-length', '0'))
        content_type = resp.headers.get('Content-type', '')
        # recognize some file types on our own
        file_type = mimetypes.guess_extension(content_type)
        if file_type is None:
            if 'application/x-mobipocket-ebook' == content_type:
                file_type = 'mobi'
            elif 'application/lrf' == content_type:
                file_type = 'lrf'
            elif 'plain/text' == content_type:
                file_type = 'txt'
            elif 'application/pdb' == content_type:
                file_type = 'pdb'
            elif 'application/x-ms-reader' == content_type:
                file_type = 'lit'
            elif 'application/rtf' == content_type:
                file_type = 'rtf'
            elif content_type.startswith('text/html;'):
                file_type = 'html'
            else:
                self.log.debug(f"unrecognized content-type: {content_type} - {link}")
                file_type = "unrecognized"
        else:
            file_type = file_type.lstrip('.')

        return link, MrLinkItem(file_name, modified, file_type, file_size)

    def _create_attach_link_item_dict(self, attach_list: List[str]) -> LinkItemDict:
        """
        Create attachment LinkItemDict.
        """
        job_list = []
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() - 1) as executor:
            for link in attach_list:
                job = executor.submit(self._create_attach_link_item, link)
                job_list.append(job)

            pbar = tqdm(as_completed(job_list), total=len(job_list), desc='Create attachment items', unit='item', mininterval=1, ncols=100,
                        disable=self._disable_tqdm)
            for _ in pbar:
                pass

        ebook_dict = LinkItemDict()
        for job in job_list:  # merge all results into one dict
            exc = job.exception()
            if exc is None:
                link, item = job.result()
                ebook_dict[link] = item
            else:
                self.log.error(f"Something went wrong: {exc}")
        return ebook_dict

    def _log_stats(self, stats: Dict[str, Tuple[int, int]]):
        """
        Log the LinkItemDict stats with size and type summary.
        """
        self.log.info("type | count | size")
        total = 0
        total_size = 0
        for stat in sorted(stats.items(), key=lambda kv: (kv[1], kv[0])):
            total += stat[1][0]
            total_size += stat[1][1]
            self.log.info(f"{stat[0]} | {stat[1][0]} | {sizeof_fmt(stat[1][1])}")
        self.log.info(f"total | {total} | {sizeof_fmt(total_size)}")


def split_thread_attach(links: List[str]) -> Tuple[List[str], List[str]]:
    """
    Split a list of links to showthread and attachment links
    """
    thread_links = []
    attach_links = []
    for link in links:
        if link.startswith("/forums/showthread.php"):
            thread_links.append(link)
        if link.startswith("/forums/attachment.php"):
            attach_links.append(link)
    return thread_links, attach_links


def get_links_from_thread(file: Path) -> Tuple[List[str], int]:
    """
    Get all links from a thread inside posts or attachments.
    """
    try:
        with file.open(mode='rb') as reader:
            data = reader.read()
        soup = BeautifulSoup(data, 'lxml')
        posts = soup.select("body > #container > #posts > div > div > div > div > table")
        links = []
        for post in posts:
            urls = post.select('a')
            for url in urls:
                if url.get('rel') != "nofollow":
                    links.append(url.get('href'))
    except Exception:
        raise GetEbookLinksError(file, traceback.format_exc())
    return links, len(posts)


def collect_stats(attach_dict: LinkItemDict) -> dict:
    """
    Collect stats from LinkItemDict.
    """
    stats_dict = {}
    for item in attach_dict.values():
        cur = stats_dict.get(item.type, (0, 0))
        stats_dict[item.type] = (cur[0] + 1, cur[1] + item.size)
    return stats_dict
