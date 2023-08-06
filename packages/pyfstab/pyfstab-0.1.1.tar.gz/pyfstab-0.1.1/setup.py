# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfstab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfstab',
    'version': '0.1.1',
    'description': 'Fstab parsing and formatting library',
    'long_description': "**MIT-licensed libary for parsing and creating fstab files**\n\n|pypi| |docs| |license|\n\nFeatures\n========\n\n* Unlike Canonical's fstab Python library, this actually works with Python 3\n  and does not have a cancerous license (GPLv3)\n* Small\n\nContributing\n============\n\n* Send any issues to GitHub's issue tracker.\n* Before sending a pull request, format it with `Black`_ (-Sl79)\n* Any changes must be updated to the documentation\n\n\n.. _`Black`: https://github.com/psf/black\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pyfstab.svg\n    :alt: PyPI\n    :target: https://pypi.org/project/pyfstab/\n.. |docs| image:: https://readthedocs.org/projects/pyfstab/badge/?version=latest\n    :alt: Read the Docs\n    :target: http://pyfstab.readthedocs.io/en/latest/\n.. |license| image:: https://img.shields.io/github/license/b10011/pyfstab.svg\n    :alt: License\n    :target: https://github.com/b10011/pyfstab/blob/master/LICENSE\n",
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b10011/pyfstab',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
