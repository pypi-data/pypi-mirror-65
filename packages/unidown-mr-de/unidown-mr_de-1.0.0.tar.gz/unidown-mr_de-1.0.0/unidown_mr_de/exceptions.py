"""
mr_de specific module exceptions.
"""
from pathlib import Path

from unidown.plugin.exceptions import PluginException


class GetEbookLinksError(PluginException):
    """
    Something wents wrong while parsing an thread.
    Has default values due to python bug: https://bugs.python.org/issue37208
    """

    def __init__(self, file: Path, orig_ex: Exception = None):
        super().__init__()
        self.file = file
        self.orig_ex = orig_ex
