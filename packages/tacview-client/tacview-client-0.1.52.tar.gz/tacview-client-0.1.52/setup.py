# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tacview_client']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.20.1,<0.21.0',
 'sqlalchemy>=1.3.15,<2.0.0',
 'uvloop>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['tacview = tacview_client.cli:main']}

setup_kwargs = {
    'name': 'tacview-client',
    'version': '0.1.52',
    'description': '',
    'long_description': None,
    'author': 'mcdelaney',
    'author_email': 'mcdelaney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcdelaney/py-tacview-client.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
