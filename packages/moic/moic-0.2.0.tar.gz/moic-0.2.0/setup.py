# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moic',
 'moic.cli',
 'moic.cli.completion',
 'moic.cli.config',
 'moic.cli.fun',
 'moic.cli.issue',
 'moic.cli.ressources',
 'moic.cli.sprint',
 'moic.cli.template',
 'moic.cli.utils',
 'moic.jira']

package_data = \
{'': ['*']}

install_requires = \
['antidote>=0.7.0,<0.8.0',
 'click>=7.1.1,<8.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'jira',
 'keyring>=21.1.1,<22.0.0',
 'pyyaml>=5.3,<6.0',
 'rich>=0.8.1,<0.9.0']

entry_points = \
{'console_scripts': ['moic = moic.base:run']}

setup_kwargs = {
    'name': 'moic',
    'version': '0.2.0',
    'description': 'My Own Issue CLI (Jira, Gitlab etc...)',
    'long_description': None,
    'author': 'Brice Santus',
    'author_email': 'brice.santus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
