"""
Module for base Moic template commands
"""
import os

import click

from moic.config import CONF_DIR, console


@click.group()
def template():
    """List, edit templates"""
    pass


@template.command()
@click.option("--project", default="all", help="The project Id for your template")
@click.option("--issue-type", default="all", help="The issue type for the template")
def edit(project, issue_type):
    """Edit a template"""
    template_name = f"{project}_{issue_type}"

    if os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/{template_name}")):
        click.edit(filename=os.path.expanduser(f"{CONF_DIR}/templates/{template_name}"))
    else:
        message = click.edit("Create your template here\n")
        with open(os.path.expanduser(f"{CONF_DIR}/templates/{template_name}"), "w") as template_file:
            template_file.write(message)

    console.print(f"Your [grey70]template[/grey70] has been saved in [green]{CONF_DIR}/templates[/green]")


@template.command()
def list():
    """List existing templates"""
    f = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.expanduser(f"{CONF_DIR}/templates")):
        f.extend(filenames)
        break

    for template in filenames:
        project, issue_type = template.split("_")
        console.print(
            f"{issue_type.ljust(10)}" + f"[green]{project.ljust(10)}[/green]" + f": {CONF_DIR}/templates/{template}",
            highlight=False,
        )
