# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycvesearch']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pycvesearch',
    'version': '1.0',
    'description': 'Python API for CVE search.',
    'long_description': None,
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cve-search/PyCVESearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
