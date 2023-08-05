# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parallel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-parallel',
    'version': '0.9.0',
    'description': 'Simple parallelism for the everyday developers',
    'long_description': None,
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
