# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astrosql', 'astrosql.deprecated']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'numpy>=1.18.2,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'peewee>=3.13.2,<4.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'requests>=2.23.0,<3.0.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'astrosql',
    'version': '1.0.1',
    'description': 'SQL database introspection and methods in Python to access existing astronomy databases.',
    'long_description': None,
    'author': 'Keto Zhang',
    'author_email': 'keto.zhang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
