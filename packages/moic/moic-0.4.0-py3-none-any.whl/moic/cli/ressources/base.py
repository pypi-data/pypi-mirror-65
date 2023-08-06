"""
Module for base Moic resources commands
"""
import click

from moic.config import COLOR_MAP, JiraInstance, console


# List Commands
# TODO: Add autocomplete on all commands
@click.group()
def list():
    """List projects, issue_types, priorities, status"""
    pass


@list.command()
def projects():
    """List Jira Projects"""
    jira = JiraInstance()
    projects = jira.session.projects()
    for p in projects:
        console.print(
            f"[grey70]{p.name.ljust(20)}[/grey70] : [magenta]{p.key}[/magenta]", highlight=False,
        )


@list.command()
def issue_type():
    """List Jira Issue Type"""
    jira = JiraInstance()
    issue_types = jira.session.issue_types()
    for i in issue_types:
        console.print(
            f"[grey70]{i.name.ljust(20)}[/grey70] : [green]{i.description}[/green]", highlight=False,
        )


@list.command()
def priorities():
    """List Jira Priorities"""
    jira = JiraInstance()
    priorities = jira.session.priorities()
    for p in priorities:
        console.print(
            f"[grey70]{p.name.ljust(10)}[/grey70] : [green]{p.description}[/green]", highlight=False,
        )


@list.command()
def status():
    """List Jira status"""
    jira = JiraInstance()
    statuses = jira.session.statuses()
    for s in statuses:
        color_name = COLOR_MAP[s.raw["statusCategory"]["colorName"]]
        console.print(
            f"[{color_name}]{s.name.ljust(25)}[/{color_name}] : [grey70]{s.description}[/grey70]", highlight=False,
        )
