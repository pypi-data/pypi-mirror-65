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
 'commonmark>=0.9.1,<0.10.0',
 'dynaconf>=2.2.3,<3.0.0',
 'jira',
 'keyring>=21.1.1,<22.0.0',
 'pyyaml>=5.3,<6.0',
 'rich>=0.8.1,<0.9.0',
 'tomd>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['moic = moic.base:run']}

setup_kwargs = {
    'name': 'moic',
    'version': '0.3.0',
    'description': 'My Own Issue CLI (Jira, Gitlab etc...)',
    'long_description': '# MOIC : My Own Issue CLI\n\n> Inspired by https://pypi.org/project/jira-cli/\n\n\nCommand line utility to interact with issue manager such as Jira and Gitlab\n\n## Getting Started\n\n* Install moic\n```bash\n> pip install moic\n```\n\n* Configure moic\n```bash\n> moic configure\n```\n\n* Commands\n```bash\n> moic\nUsage: moic [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  config    Configure Jira cli\n  issue     Create, edit, list Jira issues\n  list      List projects, issue_types, priorities, status\n  template  List, edit templates\n```\n\n## Autocompletion\n\nTo activate bash autocompletion just add:\n* For bash\n```\n# In your .bashrc\neval "$(_MOIC_COMPLETE=source_bash moic)"\n```\n* For zsh\n```\n# In your .zshrc\neval "$(_MOIC_COMPLETE=source_zsh moic)"\n```\n\n## Contribute\n\n### Setup\n\n* Create virtualenv\n```bash\npoetry shell\n```\n* Install dependencies\n```bash\npoetry install\n```\n* Install pre-commit\n```bash\npre-commit install\n```\n\nbq. Pre-commit will check isort, black, flake8\n',
    'author': 'Brice Santus',
    'author_email': 'brice.santus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/brice.santus/moic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
