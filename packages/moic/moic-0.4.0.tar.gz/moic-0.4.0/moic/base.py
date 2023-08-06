"""
Moic cli definition base module
"""
import click

from moic.cli.config import config
from moic.cli.fun import rabbit
from moic.cli.issue import issue
from moic.cli.ressources import list
from moic.cli.sprint import sprint
from moic.cli.template import template


@click.group()
def cli():
    pass


# Register sub command
cli.add_command(template)
cli.add_command(config)
cli.add_command(issue)
cli.add_command(list)
cli.add_command(sprint)
cli.add_command(rabbit)
# TODO : Add version command group


def run():
    """
    Run the cli application
    """
    cli()


if __name__ == "__main__":
    """
    Main method of the module
    """
    cli()
