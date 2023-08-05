# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spotiflite']
install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'click>=7.1.1,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['spotiflite = spotiflite:cli']}

setup_kwargs = {
    'name': 'spotiflite',
    'version': '0.0.5',
    'description': 'scrapes spotify starting from an artist id, stores in sqlite',
    'long_description': '<img src="https://github.com/sloev/spotiflite/raw/master/assets/logo.png" width="300"/>\n\n# Spotiflite\n\n[![Build Status](https://travis-ci.org/sloev/spotiflite.svg?branch=master)](https://travis-ci.org/sloev/spotiflite) [![Latest Version](https://img.shields.io/pypi/v/spotiflite.svg)](https://pypi.python.org/pypi/spotiflite)\n\nScrapes Spotify and dumps data to a sqlite3 database.\n\n* Uses `requests` to make queries, with pythonic user-agent\n* sleeps randomly between each HTTP call\n* is *NOT* in a hurry to get anywhere\n* has nice 80\'s cli interface\n\n## Install\n\n```bash\n$ pip install spotiflite\n```\n\nthen go somewhere and setup a database:\n\n```bash\n$ spotiflite setup\n```\n\nyou can also specify the db filename:\n\n```bash\n$ spotiflite --spotifydb=this/awesome/db setup\n```\n\n## Usage\n\nFor example scrape **Frank ෴ Zappa** \n\n```bash\n$ spotiflite scrape 6ra4GIOgCZQZMOaUECftGN \ngot 44 artist ids\nextracted data for Tom Waits\nsaved data for Tom Waits\ngot 8 artist ids\nextracted data for Elmer Snowden\nsaved data for Elmer Snowden\ngot 6 artist ids\nextracted data for Wesley Willis\nsaved data for Wesley Willis\n...\n```\n\nwhile its running you can get stats in another window\n\n```bash\n$ spotiflite stats \nrows: 9882\ncompleted: 1395\njobs to do: 8487\nDB size: 48.04 MB\n```\n\n### Cli usage\n\n```bash\nUsage: spotiflite.py [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -db, --spotifydb TEXT  sqlite filename [default: spotify.db]\n  --help                 Show this message and exit.\n\nCommands:\n  scrape    starts scraping from given artist id\n  setup     creates tables\n  stats     print out db stats\n  teardown  deletes tables\n\n```',
    'author': 'sloev',
    'author_email': 'johannes.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sloev/spotiflite',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
