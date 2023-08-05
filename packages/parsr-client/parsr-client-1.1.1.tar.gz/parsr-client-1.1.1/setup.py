# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parsr_client']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'parsr-client',
    'version': '1.1.1',
    'description': 'Python client for Parsr - Transforms PDF, Documents and Images into Enriched Structured Data',
    'long_description': 'Parsr Client\n================\n\nProvides a python interface to the Parsr toolvia its API, which transforms PDF, documents and images into enriched, structured data.',
    'author': 'AXA Group Operations S.A.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://par.sr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
