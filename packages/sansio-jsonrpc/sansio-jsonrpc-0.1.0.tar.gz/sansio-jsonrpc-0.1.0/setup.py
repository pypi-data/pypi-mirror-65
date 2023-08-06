# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sansio_jsonrpc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sansio-jsonrpc',
    'version': '0.1.0',
    'description': 'JSON-RPC v2.0 Sans I/O',
    'long_description': None,
    'author': 'Mark E. Haase',
    'author_email': 'mehaase@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
