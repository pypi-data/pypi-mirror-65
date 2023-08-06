# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scan_models',
 'scan_models.management',
 'scan_models.management.commands',
 'scan_models.migrations',
 'scan_models.parser',
 'scan_models.tests',
 'scan_models.tests.parser',
 'scan_models.validators']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.4,<4.0.0', 'mysqlclient>=1.4.6,<2.0.0']

setup_kwargs = {
    'name': 'django-scan-models',
    'version': '0.2.2',
    'description': 'Django scan models: Parse django models to frontend validation',
    'long_description': None,
    'author': 'Jessie Liauw A Fong',
    'author_email': 'jessielaff@live.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
