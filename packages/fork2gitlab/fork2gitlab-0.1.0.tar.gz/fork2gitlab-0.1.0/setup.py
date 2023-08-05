# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fork2gitlab', 'fork2gitlab.commands']

package_data = \
{'': ['*']}

install_requires = \
['cliff>=3.1.0,<4.0.0', 'python-gitlab>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['f2g = fork2gitlab.main:main']}

setup_kwargs = {
    'name': 'fork2gitlab',
    'version': '0.1.0',
    'description': 'A script to help forking a project to gitlab and keeping it updated downstream',
    'long_description': None,
    'author': 'LoveIsGrief',
    'author_email': 'loveisgrief@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
