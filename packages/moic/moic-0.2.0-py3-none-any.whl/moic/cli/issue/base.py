import os

import click

from moic.cli.completion import autocomplete_issues, autocomplete_transitions, autocomplete_users
from moic.cli.utils import get_issue_commits, get_template, print_issue, print_issues, validate_issue_key
from moic.config import COLOR_MAP, CONF_DIR, JiraInstance, console, logger, settings

# Custom fileds
# Sprint : 10101
# Epic   : 10102


# TODO: Add set-peer command
# TODO: Add create subtasks command
# TODO: Add change priority command
# TODO: Add add/remove to sprint command
# TODO: Add change issue type command
# TODO: Manage labels
# TODO: Manage components
@click.group()
def issue():
    """Create, edit, list Jira issues"""
    pass


# TODO: Add more options (get comment, list commits)
# TODO: Add tests
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
