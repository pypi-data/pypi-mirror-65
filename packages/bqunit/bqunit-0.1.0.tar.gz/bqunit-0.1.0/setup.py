# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqunit']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=1.24.0,<2.0.0']

setup_kwargs = {
    'name': 'bqunit',
    'version': '0.1.0',
    'description': 'Testing framework for BigQuery SQL',
    'long_description': None,
    'author': 'to-lz1',
    'author_email': 'https://github.com/to-lz1',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
