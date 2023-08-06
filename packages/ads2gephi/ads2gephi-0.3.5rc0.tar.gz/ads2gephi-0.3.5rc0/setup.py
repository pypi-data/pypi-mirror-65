# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ads2gephi']

package_data = \
{'': ['*']}

install_requires = \
['ads>=0.12.3,<0.13.0',
 'click>=7.0,<8.0',
 'configparser>=3.7,<4.0',
 'python-igraph>=0.7.1,<0.8.0',
 'sqlalchemy>=1.3,<2.0',
 'tqdm>=4.32,<5.0',
 'yaspin>=0.14.3,<0.15.0']

entry_points = \
{'console_scripts': ['ads2gephi = ads2gephi.cli:main']}

setup_kwargs = {
    'name': 'ads2gephi',
    'version': '0.3.5rc0',
    'description': 'A command line tool for querying and modeling citation networks from the Astrophysical Data System (ADS) in a format compatible with Gephi',
    'long_description': "[![PyPI version](https://badge.fury.io/py/ads2gephi.svg)](https://badge.fury.io/py/ads2gephi)\n![build](https://api.travis-ci.org/03b8/ads2gephi.svg?branch=master)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n# ads2gephi\n\nis a command line tool for querying and modeling citation networks from the Astrophysical Data System (ADS) in a format compatible with Gephi, a popular network visualization tool. ads2gephi has been developed at the history of science department of TU Berlin as part of a research project on the history of extragalactic astronomy.\n\nYou can install `ads2gephi` from PyPI:\n```\npip install ads2gephi\n```\n\n### Usage\n\nWhen using the tool for the first time to model a network, you will be prompted to enter your ADS API key. Your key will then be stored in a configuration file under ~/.ads2gephi.\n\nIn order to sample an initial citation network, you need to provide ads2gephi with a plain text file with bibcodes (ADS unique identifiers), one per line, as input. The queried network will be output in a SQLite database stored in the current directory:\n\n```\nads2gephi -c bibcodes_example.txt -d my_fancy_netzwerk.db\n```\n\nAfterwards you can extend the queried network by providing the existing database file and using the additional sampling options. For example, you can extend the network by querying all the items cited in every publication previously queried:\n\n```\nads2gephi -s ref -d my_fancy_netzwerk.db\n```\n\nFinally you might want to also generate the edges of the network. There are several options for generating edges. For example you can use a semantic similarity measure like bibliographic coupling or co-citation:\n```\nads2gephi -e bibcp -d my_fancy_netzwerk.db\n```\n\nYou can also do everything at once:\n```\nads2gephi -c bibcodes_example.txt -s ref -e bibcp -d my_fancy_netzwerk.db\n```\n\nAll other querying and modelling options are described in the help page:\n```\nads2gephi --help\n```\n\nOnce you've finished querying and modeling, the database file can be directly imported in Gephi for network visualization and analysis.\n\n## Special thanks to\n\n* Edwin Henneken\n",
    'author': 'Theo Costea',
    'author_email': 'theo.costea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/03b8/ads2gephi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
