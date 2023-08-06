# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlwrap']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'sqlwrap',
    'version': '0.0.1',
    'description': 'Easy wrapper for various SQL libraries',
    'long_description': None,
    'author': 'mitch3x3',
    'author_email': 'mitch3x3@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
