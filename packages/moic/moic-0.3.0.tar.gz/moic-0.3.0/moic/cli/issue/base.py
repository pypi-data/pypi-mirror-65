import os
import time
from datetime import datetime

import click
from rich.markdown import Markdown

from moic.cli.completion import (
    autocomplete_issues,
    autocomplete_priorities,
    autocomplete_transitions,
    autocomplete_users,
)
from moic.cli.utils import (
    get_issue_commits,
    get_template,
    print_issue,
    print_issues,
    validate_issue_key,
    validate_priority,
)
from moic.cli.utils.converter import Jira2Markdown
from moic.config import COLOR_MAP, CONF_DIR, PRIORITY_COLORS, JiraInstance, console, logger, settings

# Custom fileds
# Sprint : 10101
# Epic   : 10102
# Peer : customfield_10800


# TODO: Add change priority command
# TODO: Add change issue type command
# TODO: Manage labels
# TODO: Manage components
@click.group()
def issue():
    """Create, edit, list Jira issues"""
    pass


@issue.command()
@click.argument(
    "id", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key, required=False,
)
@click.option("--all", default=False, help="Search over all Jira Projects")
@click.option(
    "--project", default=settings.get("default_project", None), help="Project ID to scope search",
)
@click.option("--search", default=None, help="JQL query for searching issues")
@click.option("--oneline", default=False, help="Dislay issue on one line", is_flag=True)
@click.option("--subtasks", default=False, help="Dislay issue subtasks", is_flag=True)
@click.option("--commits", default=False, help="Dislay issue commits", is_flag=True)
def get(id, all, project, search, oneline, subtasks, commits):
    """Get a Jira issue"""
    logger.debug("get issue")
    if not id and not search:
        return console.print("You must specify an issue ID or a search query")
    try:
        jira = JiraInstance()
        logger.debug("build search query")
        if search:
            if project and not all and "project" not in search:
                search = f"{search} AND project = {project}"

            logger.debug(f"search: {search}")
            issues = jira.session.search_issues(search)
        else:
            issues = [jira.session.issue(id)]
        print_issues(issues, prefix="", oneline=oneline, subtasks=subtasks, commits=commits)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument("issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key)
def show(issue_key):
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        md = Jira2Markdown(issue.fields.description).render()
        for line in md:
            console.print(line)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


# TODO : Add more options : Assignee, epic, sprint, parent
# TODO : Add tests
@issue.command()
@click.argument("summary")
@click.option(
    "--project", default=settings.get("default_project", None), help="Jira project where create the issue",
)
@click.option("--issue-type", default="Story", help="Jira issue type")
@click.option("--priority", default="", help="Jira issue priority")
def new(summary, project, issue_type, priority):
    """Create new issue"""
    tpl = get_template(project, issue_type)
    if tpl:
        tpl_name = tpl.split("/")[-1:][0]
        tpl_project_target = tpl_name.split("_")[1] if tpl_name.split("_")[1] != "all" else "default"
        tpl_issue_target = tpl_name.split("_")[0]

        console.print(
            f"Using [green]{tpl_project_target}[/green] template of [green]{tpl_issue_target}[/green] project [grey70]({tpl})[/grey70]",
            highlight=False,
        )
        with open(os.path.expanduser(tpl), "r") as tpl_file:
            default_description = tpl_file.read()
    else:
        default_description = "h1. Description\n"

    description = click.edit(default_description)

    if description:
        try:
            jira = JiraInstance()
            new_issue = jira.session.create_issue(
                project=project, summary=summary, description=description, issuetype={"name": issue_type},
            )
            print_issue(new_issue, oneline=False)
        except Exception as e:
            console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.option("--comment", default=None, help="Comment to add on Jira issue")
def comment(issue_key, comment):
    """Add a comment on an issue"""
    if not comment:
        comment = click.edit("")
    try:
        jira = JiraInstance()
        jira.session.add_comment(issue_key, comment)
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.option("--last", default=None, help="Only display the last n comments")
def list_comments(issue_key, last):
    """List comments on an issue"""
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        comments = jira.session.comments(issue)
        if last:
            comments = comments[len(comments) - int(last) :]
        for comment in comments:
            console.print(
                f"[yellow]{comment.author}[/yellow] - [grey70]{datetime.strptime(comment.created.split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%m/%d/%Y %H:%M:%S')}[/grey70]"
            )
            console.line()
            md = Jira2Markdown(comment.body).render()
            for line in md:
                console.print(line)
            console.line()
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.argument("assignee", type=click.STRING, autocompletion=autocomplete_users)
def assign(issue_key, assignee):
    """Assign a Jira issue"""
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        issue.update(assignee={"name": assignee})
        console.print(
            f"Assigned [green]{assignee}[/green] on [blue]{issue_key}[/blue]", highlight=False,
        )
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.argument("peer", type=click.STRING, autocompletion=autocomplete_users)
def set_peer(issue_key, peer):
    """Define the peer user on a Jira issue"""
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        peer_user = jira.session.search_users(peer)
        if peer_user:
            issue.update(fields={settings.get("jira.custom_fields.peer"): {"name": peer}})
        console.print(
            f"Peer [green]{peer}[/green] added on [blue]{issue_key}[/blue]", highlight=False,
        )
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.option("--subtask", "-s", type=click.STRING, help="The subtask title", multiple=True)
def add_subtasks(issue_key, subtask):
    """Assign a Jira issue"""
    try:
        jira = JiraInstance()

        issue = jira.session.issue(issue_key)
        if not subtask:
            description = "# Creates one subtask per line (separate summary and description with '|'"
            subtasks_list = click.edit(description).split("\n")
            subtask = [sub for sub in subtasks_list if not sub.startswith("#")]

        for sub in subtask:
            summary = sub
            description = ""
            if "|" in sub:
                summary, description = sub.split("|")
            new_subtask = jira.session.create_issue(
                project={"key": issue.fields.project.key},
                summary=summary,
                description=description,
                issuetype={"name": "Sub-task"},
                parent={"key": issue.key},
            )
            print_issue(new_subtask, oneline=True)
            console.line()

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.argument("transition", type=click.STRING, autocompletion=autocomplete_transitions)
def move(issue_key, transition):
    """Apply a transition on a Jira issue"""
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        transition = [t for t in transitions if t["name"] == transition]
        if transition:
            transition = transition[0]
            jira.session.transition_issue(issue, transition["id"])
            console.print(
                f"Moved [green]{issue_key}[/green] to [{COLOR_MAP[transition['to']['statusCategory']['colorName']]}]{transition['name']}[/{COLOR_MAP[transition['to']['statusCategory']['colorName']]}] status",
                highlight=False,
            )
        else:
            console.print(f"[yellow]No transition available for {issue_key}[/yellow]")

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@issue.command()
@click.argument(
    "issue-key", type=click.STRING, autocompletion=autocomplete_issues, callback=validate_issue_key,
)
@click.argument("priority", type=click.STRING, autocompletion=autocomplete_priorities, callback=validate_priority)
def rank(issue_key, priority):
    try:
        jira = JiraInstance()
        issue = jira.session.issue(issue_key)
        issue.update(fields={"priority": {"name": priority}})
        console.print(f"[green]{issue_key}[/green] ranked to [{PRIORITY_COLORS[priority]}]{priority}[/]")
    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")
