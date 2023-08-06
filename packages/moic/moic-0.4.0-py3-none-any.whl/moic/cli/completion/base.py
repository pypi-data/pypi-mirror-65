"""
Base module for completion functions
It includes all function used for autocomplete click options and arguments
"""
from click.core import Context
from jira.client import ResultList

from moic.config import JiraInstance


def autocomplete_users(ctx: Context, args: list, incomplete: str) -> ResultList:
    """
    Get Jira users list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        jira.client.ResultList: List of users corresponding to the incomplete input
    """
    try:
        jira = JiraInstance()
        users = jira.session.search_users(incomplete)
        return [user.name for user in users]
    except Exception:
        return []


def autocomplete_priorities(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira priorities name list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of priorities name corresponding to the incomplete input
    """
    try:
        jira = JiraInstance()
        return [priority.name for priority in jira.session.priorities() if incomplete in priority.name]
    except Exception:
        return []


def autocomplete_issues(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira issues list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of tuples (issue.key, issue.fields.summary) of issues corresponding to the incomplete input
    """
    try:
        jira = JiraInstance()
        if "-" in incomplete:
            issues = jira.session.search_issues(f"project = {incomplete.split('-')[0]}", 0, 100)
            return [(issue.key, issue.fields.summary) for issue in issues if issue.key.startswith(incomplete.upper())]
        else:
            return []
    except Exception:
        return []


def autocomplete_transitions(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira translations available for an issue

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of translation names corresponding to the incomplete input
    """
    try:
        jira = JiraInstance()
        issue_key = args[-1:][0]
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        return [t.name for t in transitions if t.name.startswith(incomplete)]
    except Exception:
        return []


def autcomplete_projects(ctx: Context, args: list, incomplete: str) -> list:
    """
    Get Jira projects list completion

    Args:
        ctx (click.core.Context): click.core.Context of the given command
        args (list): List of commands args
        incomplete (str): String input to autocomplete

    Returns:
        list: List of project names corresponding to the incomplete input
    """
    try:
        jira = JiraInstance()
        projects = jira.session.project()
        return [p.name for p in projects if incomplete in p.name]
    except Exception:
        return []
