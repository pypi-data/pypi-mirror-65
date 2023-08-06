# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytscraper', 'ytscraper.commands', 'ytscraper.helper']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'google-api-python-client>=1.8.0,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'toml>=0.10.0,<0.11.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'yt-scraper',
    'version': '0.3.0',
    'description': 'Command line utility querying the YouTube API v3.',
    'long_description': 'fetch-yt.py\n\n`-q --query STRING` \nText that is used for the search on YouTube. Needed\n\n`-o --output`\nSpecifies the output file.\n**Default:** ``data/result.sql``\n\n`-n --number INTEGER (ARRAY)`\nNumber of videos fetched per level. \nIf an array is provided, the i-th element equals \nthe number of videos fetched on the i-th level.\n**Default**: 10\n\n`-l --levels INTEGER`\nNumber of recursion steps per video.\n**Default**: 1\n\n`-v --verbose`\nPrint more information to output.\n\n\n## Known Issues\n\n- The `number` parameter is restricted to maximal 50. This can be fixed in the\nfuture by iterating through result pages.\n',
    'author': 'Michael Brauweiler',
    'author_email': 'michael.brauweiler@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
