import json
import os

import click
import keyring
import requests

from moic.config import COLOR_MAP, CONF_DIR, JiraInstance, console, settings


class Board:
    def __init__(self, json_board):
        self.raw = json_board
        self.id = json_board["id"]
        self.name = json_board["name"]
        self.type = json_board["type"]


def get_issue_commits(issue_key):
    r_commits = requests.get(
        f'{settings.get("instance")}/rest/gitplugin/1.0/issues/{issue_key}/commits',
        auth=(settings.get("login"), keyring.get_password("moic", settings.get("login")),),
    )
    r_repos = requests.get(
        f'{settings.get("instance")}/rest/gitplugin/1.0/repository',
        auth=(settings.get("login"), keyring.get_password("moic", settings.get("login")),),
    )

    if r_commits.status_code == 200 and r_repos.status_code == 200:
        commits = json.loads(r_commits.content)["commits"]
        repos = json.loads(r_repos.content)["repositories"]
        for idx, commit in enumerate(commits):
            repo = [repo for repo in repos if repo["id"] == commit["repository"]["id"]][0]
            commit["repository"] = repo
            commits[idx] = commit
        return commits
    else:
        return []


def get_board_sprints(board_id, closed=False):
    """Return le sprint list of a board"""
    sprints = JiraInstance().session.sprints(board_id)
    if not closed:
        sprints = [jira_sprint for jira_sprint in sprints if jira_sprint.state != "closed"]
    ret = {"board_id": board_id, "sprints": sprints}
    return ret


def get_sprint_story_points(sprint_id):
    """Return the detailled list of story points for a given sprint Id"""

    jira = JiraInstance()
    issues = [
        issue
        for issue in jira.session.search_issues(f"Sprint = {sprint_id}")
        if settings.get("jira.custom_fields.story_points") in issue.raw["fields"].keys()
    ]

    done = [issue for issue in issues if issue.fields.status.statusCategory.key == "done"]
    todo = [issue for issue in issues if issue not in done]

    ret = {
        "sprint_id": sprint_id,
        "points": {
            "done": float(
                sum(
                    [
                        float(
                            0
                            if issue.raw["fields"][settings.get("jira.custom_fields.story_points")] is None
                            else issue.raw["fields"][settings.get("jira.custom_fields.story_points")]
                        )
                        for issue in done
                    ]
                )
            ),
            "todo": float(
                sum(
                    [
                        float(
                            0
                            if issue.raw["fields"][settings.get("jira.custom_fields.story_points")] is None
                            else issue.raw["fields"][settings.get("jira.custom_fields.story_points")]
                        )
                        for issue in todo
                    ]
                )
            ),
        },
    }
    return ret


def get_sprint_issues(sprint_id):
    jira = JiraInstance()
    return jira.session.search_issues(f"sprint = {sprint_id}")


def get_project_boards(project_key: str):
    """
    Get the board list of a given project

    This function is used waiting the 3.0.0 release of Python Jira
    which include it built-in

    Args:
        project_Key (str): The Jira project Key used to filtered

    Returns:
        boards (list): A list of boards dict
    """

    r_boards = requests.get(
        f'{settings.get("instance")}/rest/agile/latest/board/?type=scrum&projectKeyOrId={project_key}',
        auth=(settings.get("login"), keyring.get_password("moic", settings.get("login")),),
    )

    if r_boards.status_code == 200:
        boards = json.loads(r_boards.content)["values"]
        return [Board(board) for board in boards]
    else:
        return []


def validate_issue_key(ctx, param, value):
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
    try:
        if value:
            jira = JiraInstance()
            priority = [priority for priority in jira.session.priorities() if priority.name == value][0]
            return priority.name
        else:
            return ""
    except Exception:
        raise click.BadParameter("Please provide a valide priority")


def print_issues(
    issues, prefix: str = "", oneline: bool = False, commits: bool = False, subtasks: bool = False,
):
    for i in issues:
        if not oneline:
            console.print()
        print_issue(i, prefix=prefix, oneline=oneline, subtasks=subtasks, commits=commits)


# TODO: Add MR print : Can't be implemented
def print_issue(
    issue, prefix: str = "", oneline: bool = False, commits: bool = False, subtasks: bool = False,
):
    url = settings["instance"] + "/browse/"
    status_color = COLOR_MAP[issue.fields.status.statusCategory.colorName]
    if oneline:
        console.print(
            f"{prefix}[{status_color}]{issue.key}[/{status_color}] {issue.fields.summary} [bright_black]{url}{issue.key}[/bright_black]",
            highlight=False,
        )
    else:
        console.print("key".ljust(15) + f" : {issue.key}", highlight=False)
        console.print(
            "status".ljust(15) + f" : [{status_color}]{issue.fields.status.name}[/{status_color}]", highlight=False,
        )
        console.print("reporter".ljust(15) + f" : {issue.fields.reporter}", highlight=False)
        console.print("summary".ljust(15) + f" : {issue.fields.summary}", highlight=False)
        console.print("assignee".ljust(15) + f" : {issue.fields.assignee}", highlight=False)
        console.print(
            "link".ljust(15) + f" : [bright_black]{url}{issue.key}[/bright_black]", highlight=False,
        )
        if subtasks:
            console.print("subtasks".ljust(15) + " :")
            for sub in issue.fields.subtasks:
                print_issue(sub, prefix=" - ", oneline=True)
        if commits:
            commit_list = get_issue_commits(issue.key)
            console.print("commits".ljust(15) + " :")
            if commit_list:
                for commit in commit_list:
                    commit_url = commit["repository"]["changesetFormat"].replace("${rev}", commit["commitId"][:8])
                    console.print(
                        f" - ([green]{commit['commitId'][:8]}[/green]) {commit['message']}", highlight=False,
                    )
                    console.print(f"   [grey70]{commit_url}[/grey70]", highlight=False)
            else:
                console.print("[yellow]no commit found[/yellow]")


def print_status(status):
    display = [
        f"[bold {COLOR_MAP[s.statusCategory.colorName]}]{s.name}[/bold {COLOR_MAP[s.statusCategory.colorName]}]"
        for s in status
    ]
    console.print(" / ".join(display))


def get_template(project, type):
    if os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/{project}_{type}")):
        return f"{CONF_DIR}/templates/{project}_{type}"
    elif os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/all_{type}")):
        return f"{CONF_DIR}/templates/{project}_{type}"
    elif os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/all_all")):
        return f"{CONF_DIR}/templates/all_all"
    else:
        return None
