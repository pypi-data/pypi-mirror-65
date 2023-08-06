# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_generator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'jinja2',
 'livereload>=2.6.1,<3.0.0',
 'markdown>=3.2.1,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'arcade-generator',
    'version': '0.0.6',
    'description': 'A static site generator',
    'long_description': None,
    'author': 'Yabir Benchakhtir',
    'author_email': 'yabirg@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
