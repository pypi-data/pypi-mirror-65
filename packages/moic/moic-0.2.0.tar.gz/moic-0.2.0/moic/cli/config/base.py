import click

from moic.config import JiraInstance, settings


@click.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Configure Jira cli"""
    if ctx.invoked_subcommand is None:
        JiraInstance().configure(force=True)


@config.command()
@click.option(
    "--project", default=settings.get("default_project", None), help="Provide the project you want to configure"
)
def agile(project):
    """Configure Jira Agile settings"""
    JiraInstance().configure_agile(project=project, force=True)
