# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trellotasks']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.7.0,<6.0.0',
 'py-trello>=0.16.0,<0.17.0',
 'pyyaml>=5.3.1,<6.0.0',
 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['trellotasks = trellotasks.__main__:run']}

setup_kwargs = {
    'name': 'trellotasks',
    'version': '0.2.0',
    'description': 'A simple task scheduler built with Python and managed through Trello.',
    'long_description': None,
    'author': 'Alejandro Piad',
    'author_email': 'alepiad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
