# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netblocks3']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'netblocks3',
    'version': '0.0.13rc1',
    'description': 'Get the Cloud Provider netblocks (Python3 version)',
    'long_description': None,
    'author': 'tomasfse',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
