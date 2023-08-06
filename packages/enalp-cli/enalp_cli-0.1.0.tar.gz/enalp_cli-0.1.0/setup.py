# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enalp_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'click_help_colors>=0.8,<0.9',
 'pyfiglet>=0.8.post1,<0.9',
 'textblob>=0.15.3,<0.16.0']

entry_points = \
{'console_scripts': ['enalp_cli = enalp_cli.enalp_cli:main']}

setup_kwargs = {
    'name': 'enalp-cli',
    'version': '0.1.0',
    'description': 'Easy NAtural Language Processig CLI Tool for Tokenization, POS, Sentiment Analysis, Translations and more.',
    'long_description': '## ENALP (Easy NAtural Language Processing) CLI Tool\n+ Aim: making some basic Machine Learning activity from CLI\n+ Purpose: for tokenization, part of speech, sentiment analysis, translations, etc.\n\n### Installation\nbash\n+ pip install enalp-cli\n+ check that ".local/bin" is in your PATH \n\n### Basic usage\nbash\n+ enalp_cli --help\n+ enalp_cli about\n+ enalp_cli [COMMAND] --help\n\n### License\n+ MIT\n\n### Author\n+ Rosario Moscato\n+ https://www.linkedin.com/in/rosariomoscato',
    'author': 'Rosario Moscato',
    'author_email': 'rosario.moscato@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rosariomoscato',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
