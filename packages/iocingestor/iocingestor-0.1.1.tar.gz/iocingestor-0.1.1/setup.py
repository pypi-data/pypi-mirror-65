# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iocingestor',
 'iocingestor.extras',
 'iocingestor.ioc_fanger',
 'iocingestor.operators',
 'iocingestor.sources',
 'iocingestor.whitelists']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'aiocontextvars>=0.2.2,<0.3.0',
 'beautifulsoup4>=4.8.2,<5.0.0',
 'contextvars>=2.4,<3.0',
 'feedparser>=5.2.1,<6.0.0',
 'hug>=2.6.1,<3.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'ioc-finder>=2.1.1,<3.0.0',
 'iocextract>=1.13.1,<2.0.0',
 'ipaddress>=1.0.23,<2.0.0',
 'jsonpath-rw>=1.4.0,<2.0.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.4,<2.0',
 'pymisp>=2.4.124,<3.0.0',
 'pyparsing>=2.4.6,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sgmllib3k>=1.0.0,<2.0.0',
 'statsd>=3.3.0,<4.0.0',
 'twitter>=1.18.0,<2.0.0']

entry_points = \
{'console_scripts': ['iocingestor = iocingestor:main']}

setup_kwargs = {
    'name': 'iocingestor',
    'version': '0.1.1',
    'description': 'Extract and aggregate IOCs from threat feeds.',
    'long_description': None,
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninoseki/iocingestor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
