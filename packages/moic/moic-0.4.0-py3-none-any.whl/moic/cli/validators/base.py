"""
Module for base Moic validator functions
"""
import click
from click.core import Context

from moic.config import JiraInstance


def validate_issue_key(ctx: Context, param: list, value: str) -> str:
    """
    Validate a given issue key to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the key if it's validated
    """
    try:
        if value:
            jira = JiraInstance()
            issue = jira.session.issue(value)
            return issue.key
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide issue_key")


def validate_priority(ctx, param, value):
    """
    Validate a given priority name to check if it exists in Jira

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        value (str): String input to validate

    Returns:
        str: Retrive the priority name if it's validated
    """
    try:
        if value:
            jira = JiraInstance()
            priority = [priority for priority in jira.session.priorities() if priority.name == value][0]
            return priority.name
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide priority")
