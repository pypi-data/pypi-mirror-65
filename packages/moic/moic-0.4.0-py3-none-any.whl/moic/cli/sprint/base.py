"""
Module for base Moic sprint commands
"""
import concurrent.futures
import os
import time
from datetime import datetime

import click
from rich.progress import track

from moic.cli.completion import autcomplete_projects
from moic.cli.utils import (
    get_board_sprints,
    get_project_boards,
    get_sprint_issues,
    get_sprint_story_points,
    print_issues,
    print_status,
)
from moic.config import COLOR_MAP, SPRINT_STATUS_COLORS, JiraInstance, console, settings

STEPS = ["new", "indeterminate", "done"]


# TODO: Add 'add' and 'remove' from sprint
@click.group()
def sprint():
    """Create, edit, list Jira Sprints"""
    if not settings.get("jira.custom_fields.story_points"):
        JiraInstance().configure_agile(settings.get("project"))
        return


@sprint.command()
# TODO: Add autocomplete
@click.option("--board", default=None, help="Specify Jira Board name")
@click.option(
    "--project",
    default=settings.get("project", None),
    help="Specify a project key",
    autocompletion=autcomplete_projects,
)
@click.option("--closed", default=False, help="Dislay closed sprints", is_flag=True)
def list(board, project, closed):
    """List Jira Sprints"""
    try:
        jira = JiraInstance()
        if not board:
            if project and project != "all":
                # This function is used waiting the 3.0.0 release of Python Jira
                # which include it built-in
                # jira_boards = jira.session.boards(type="scrum", projectKeyOrID=project)
                jira_boards = get_project_boards(project)
            else:
                jira_boards = jira.session.boards(type="scrum")
        else:
            jira_boards = jira.session.boards(name=board)

        data = {}
        output = ""

        # Building data
        for jira_board in track(jira_boards, description="Building output..."):
            # Get board sprints
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(get_board_sprints, jira_board.id, closed) for jira_board in jira_boards]

                for idx, future in enumerate(concurrent.futures.as_completed(futures, timeout=180.0)):
                    res = future.result()
                    data[res["board_id"]] = {
                        "board": [jb for jb in jira_boards if jb.id == res["board_id"]][0],
                        "sprints": res["sprints"],
                    }

            # Get sprint points
            points = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(get_sprint_story_points, js.id) for js in data[jira_board.id]["sprints"]]
                for idx, future in enumerate(concurrent.futures.as_completed(futures, timeout=180.0)):
                    res = future.result()
                    points[res["sprint_id"]] = res["points"]

            output = output + f"[blue]{jira_board.name}[/blue] [grey70]({jira_board.id})[/grey70]\n"
            for jira_sprint in data[jira_board.id]["sprints"]:
                goal = jira_sprint.goal if hasattr(jira_sprint, "goal") else ""
                startDate = (
                    datetime.strptime(jira_sprint.startDate.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y")
                    if hasattr(jira_sprint, "startDate")
                    else ""
                )
                endDate = (
                    datetime.strptime(jira_sprint.endDate.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y")
                    if hasattr(jira_sprint, "endDate")
                    else ""
                )
                sprint_color = COLOR_MAP[SPRINT_STATUS_COLORS[jira_sprint.state]]
                points_values = f"( {points[jira_sprint.id]['done']} / {points[jira_sprint.id]['done'] + points[jira_sprint.id]['todo']} )"
                output = (
                    output
                    + f" - [grey70]({jira_sprint.id})[/grey70] [{sprint_color}]{jira_sprint.name}[/{sprint_color}] {points_values}\n"
                )
                output = output + f"    Goal  : {goal}\n"
                output = output + f"    Dates : [grey70]{startDate} - {endDate}[/grey70]\n"

        console.print(output)

    except Exception as e:
        console.print(f"[red]Something goes wrong {e}[/red]")


@sprint.command()
# TODO: Add autocomplete
@click.option("--board", default=None, help="Specify Jira Board name")
@click.option("--sprint", default=None, help="Specify Jira Sprint id")
@click.option(
    "--project",
    default=settings.get("project", None),
    help="Specify a project key",
    autocompletion=autcomplete_projects,
)
@click.option("--subtasks", default=False, help="Display story subtask", is_flag=True)
def get(board, sprint, project, subtasks):
    """Get Jira sprints link to a board"""
    if not settings.get(f"jira.projects.{project}.workflow"):
        JiraInstance().configure_agile(project)

    jira = JiraInstance()
    if not board and not sprint:
        # This function is used waiting the 3.0.0 release of Python Jira
        # which include it built-in
        # jira_boards = jira.session.boards(type="scrum", projectKeyOrID=project)[0]
        board = get_project_boards(project)[0]
        sprints = jira.session.sprints(board.id, state="active")
    elif sprint:
        sprints = [jira.session.sprint(sprint)]

    jira_statuses = jira.session.statuses()
    if sprints:
        for sprint in sprints:
            console.print()
            console.print(f"[grey70]({sprint.id})[/grey70] {sprint.name} : {sprint.goal}")
            console.print()
            issues = get_sprint_issues(sprint.id)

            workflow = settings.get(f"jira.projects.{project}.workflow")

            for step in STEPS:
                statuses = workflow.get(step).to_list()
                for status_id in statuses:
                    if "," not in status_id:
                        status = [s for s in jira_statuses if s.id == status_id][0]
                        issues_to_display = [
                            issue
                            for issue in issues
                            if issue.fields.status.name == status.name
                            and (issue.fields.issuetype.name == "Story" or subtasks)
                        ]
                        if issues_to_display:
                            print_status([status])
                            print_issues(issues_to_display, prefix=" - ", oneline=True)
                    else:
                        status_for_step = [s for s in jira_statuses if s.id in status_id.split(",")]
                        issues_to_display = [
                            issue
                            for issue in issues
                            if issue.fields.status.name in [status.name for status in status_for_step]
                            and issue.fields.issuetype.name == "Story"
                        ]
                        if issues_to_display:
                            print_status(status_for_step)
                            print_issues(issues_to_display, prefix=" - ", oneline=True)
    else:
        console.print("[yellow]No sprint found[/yellow]")
