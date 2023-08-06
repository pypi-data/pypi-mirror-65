# MOIC : My Own Issue CLI

> Inspired by https://pypi.org/project/jira-cli/


Command line utility to interact with issue manager such as Jira and Gitlab

## Getting Started

* Install moic
```bash
> pip install moic
```

* Configure moic
```bash
> moic configure
```

* Commands
```bash
> moic
Usage: moic [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  config    Configure Jira cli
  issue     Create, edit, list Jira issues
  list      List projects, issue_types, priorities, status
  template  List, edit templates
```

## Autocompletion

To activate bash autocompletion just add:
* For bash
```
# In your .bashrc
eval "$(_MOIC_COMPLETE=source_bash moic)"
```
* For zsh
```
# In your .zshrc
eval "$(_MOIC_COMPLETE=source_zsh moic)"
```

## Contribute

### Setup

* Create virtualenv
```bash
poetry shell
```
* Install dependencies
```bash
poetry install
```
* Install pre-commit
```bash
pre-commit install
```

bq. Pre-commit will check isort, black, flake8
