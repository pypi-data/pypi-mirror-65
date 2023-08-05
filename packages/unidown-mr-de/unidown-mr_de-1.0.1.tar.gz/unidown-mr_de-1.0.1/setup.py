#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

# get long description
with Path('README.rst').open(mode='r', encoding='UTF-8') as reader:
    long_description = reader.read()

setup(
    name='unidown-mr_de',
    version='1.0.1',
    description='MR german books plugin for unidown.',
    long_description=long_description,
    author='Iceflower S',
    author_email='iceflower@gmx.de',
    license='GPLv3',
    url='https://github.com/IceflowRE/unidown-mr_de',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Natural Language :: German',
        'Environment :: Console',
    ],
    keywords='plugin unidown',
    packages=find_packages(include=['unidown_mr_de', 'unidown_mr_de.*']),
    python_requires='>=3.7',
    install_requires=[
        'unidown==2.0.1',
        'urllib3[secure]==1.25.8',
        'tqdm==4.45.0',
        'beautifulsoup4==4.8.2',
        'lxml==4.5.0',
        'certifi'
    ],
    extras_require={
        'dev': [
            'flake8==3.7.9',
            'pylint==2.4.4',
            'pyroma==2.6',
            'twine==3.1.1',
            'setuptools==46.1.3',
            'wheel==0.34.2',
        ]
    },
    package_data={

    },
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'unidown.plugin': "mr_de = unidown_mr_de.plugin:Plugin"
    },
)
