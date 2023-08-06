# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgformatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pgformatter',
    'version': '0.1.4',
    'description': 'Thin Python wrapper for pgFormatter. Compatible with AWS Lambda or any environment with Perl.',
    'long_description': None,
    'author': 'Nathan Cahill',
    'author_email': 'nathan@nathancahill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
