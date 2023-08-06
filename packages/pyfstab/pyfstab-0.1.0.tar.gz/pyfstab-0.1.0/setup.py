# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfstab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfstab',
    'version': '0.1.0',
    'description': 'Fstab parsing and formatting library',
    'long_description': None,
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
