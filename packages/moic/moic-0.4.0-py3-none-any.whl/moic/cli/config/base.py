"""
Module for base Moic configuration commands
"""
import click

from moic.config import JiraInstance, settings


@click.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """
    Configure Jira cli, setting up instance, credentials etc...
    """
    if ctx.invoked_subcommand is None:
        JiraInstance().configure(force=True)


@config.command()
@click.option("--project", default=settings.get("project", None), help="Provide the project you want to configure")
def agile(project):
    """
    Configure Jira cli Agile settings, custom fields for story points, sprint workflow etc...
    """
    if not settings.get("instance"):
        JiraInstance().configure()
        project = settings.get("project")
    JiraInstance().configure_agile(project=project, force=True)
