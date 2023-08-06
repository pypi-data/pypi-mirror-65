"""
Module for Moic configuration
"""
import json
import logging
import os
import sys

import click
import keyring
import yaml
from dynaconf import LazySettings
from jira import JIRA
from rich.console import Console

from moic.jira.api import get_project_story_status

console = Console(file=sys.__stdout__, highlight=False)

CONF_DIR = "~/.jira"

COLOR_MAP = {
    "blue-gray": "blue",
    "yellow": "yellow",
    "green": "green",
    "blue": "blue",
    "red": "red",
}

SPRINT_STATUS_COLORS = {"closed": "yellow", "active": "green", "future": "blue"}
PRIORITY_COLORS = {"Low": "grey70", "Medium": "green", "High": "dark_orange", "Critical": "red"}

settings = LazySettings(
    DEBUG_LEVEL_FOR_DYNACONF="DEBUG",
    ENVVAR_PREFIX_FOR_DYNACONF="MOIC",
    ENVVAR_FOR_DYNACONF="MOIC_SETTINGS",
    SETTINGS_FILE_FOR_DYNACONF=[os.path.expanduser(f"{CONF_DIR}/config.yaml")],
)

# Setup logger
logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger.setLevel(settings.get("LOG_LEVEL", "ERROR").upper())
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class JiraInstance:
    """
    JiraInstance class which allow you to access Jira's API using basic auth credentials
    It allows to setup several configuration such as:
    - Default project, custom fields, sprint workflow etc...
    """

    instance = None

    def __init__(self) -> None:
        """
        Init method
        """
        self.setup_home_dir()

    @property
    def session(self) -> JIRA:
        """
        Session object which represents a JIRA API session

        Returns:
            JIRA: A Jira API session
        """
        if not JiraInstance.instance:
            self.create_instance()
        return JiraInstance.instance

    def create_instance(self) -> None:
        """
        Setup the instance if it doesn't exist yet

        Returns:
            Nonte
        """
        if not settings.get("instance") or not settings.get("login"):
            self.configure()
        else:
            try:
                JiraInstance.instance = JIRA(
                    settings.get("instance"),
                    basic_auth=(settings.get("login"), keyring.get_password("moic", settings.get("login")),),
                    options={
                        "agile_rest_path": "agile",
                        "rest_api_version": "latest",
                        "agile_rest_api_version": "latest",
                    },
                )
            except Exception as e:
                console.print(f"[red]Something goes wrong {e.status_code}[/red]")
                exit(1)

    def setup_home_dir(self) -> None:
        """
        Setup configuration directory. It creates the root configuration directory
        an empty .yaml conf file and the templates directory

        Returns:
            None
        """
        if not os.path.isdir(os.path.expanduser(CONF_DIR)):
            logger.debug("Create configuration dir")
            os.makedirs(os.path.expanduser(CONF_DIR))
        if not os.path.isdir(os.path.expanduser(f"{CONF_DIR}/templates")):
            logger.debug("Create templates dir")
            os.makedirs(os.path.expanduser(f"{CONF_DIR}/templates"))
        if not os.path.isfile(os.path.expanduser(f"{CONF_DIR}/config.yaml")):
            logger.debug("Create configuration file")
            with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w") as default_config:
                default = {"default": {}}
                yaml.dump(default, default_config)

    def configure(self, force: bool = False) -> None:
        """
        Setup the main configuration and saved it:
        Instance, credentials and default project

        Args:
            force (bool): Force configuration to be setup even if it exists

        Returns:
            None
        """
        if not force:
            console.print("[yellow]No configuration found[/yellow]")
        instance = click.prompt("Your Jira Instance")

        if instance.endswith("/"):
            instance = instance[:-1]

        login = click.prompt("login")
        password = click.prompt("password", hide_input=True)
        default_project = click.prompt("Default project id")
        console.print("")
        persist = click.confirm("Would you like to persist the credentials to the local keyring?")
        if persist:
            keyring.set_password("moic", login, password)

        try:
            JiraInstance.instance = JIRA(
                instance,
                basic_auth=(login, password),
                options={"agile_rest_path": "agile", "rest_api_version": "latest", "agile_rest_api_version": "latest"},
            )
        except Exception as e:
            console.print(f"[red]Something goes wrong {e.status_code}[/red]")
            exit(1)

        conf = {"default": {"instance": instance, "login": login, "project": default_project}}
        with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w+") as conf_file:
            yaml.dump(conf, conf_file)

        console.line()
        console.print(f"[grey70]  > Configuration stored in {os.path.expanduser(CONF_DIR)}[/grey70]")
        console.line()

    def update_config(self, sub_conf: dict) -> None:
        """
        Update the local configuration merging in it a new dict of configuration

        Args:
            sub_conf (dict): The new configuration to merge into the config.yaml file

        Returns:
            None
        """
        # read configuration
        with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "r") as conf_file:
            conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        # merge configuration
        new_conf = merge_dict(sub_conf, conf)
        # write configuration
        with open(os.path.expanduser(f"{CONF_DIR}/config.yaml"), "w+") as conf_file:
            yaml.dump(new_conf, conf_file)

    def configure_agile(self, project: str, force: bool = False) -> None:
        """
        Configure the agile settings
        It configured several custom fields:
        * Story point custom field
        * Peer custom field

        Args:
            project (str): Jira Project key which should be configured
            force (bool): Force configuration to be setup even if it exists

        Returns:
            None
        """
        if not settings.get("jira.custom_fields.peer") or force:
            console.print("\n[yellow]Agile configuration: custom fields for peer is not set[/yellow]")
            fields = self.session.fields()
            candidates = [field for field in fields if "Peer" in field["name"]]
            if candidates:
                for candidate in candidates:
                    console.print(f" - [blue]{candidate['id'].ljust(20)}[/blue]: [grey70]{candidate['name']}[/grey70]")
            else:
                for field in fields:
                    console.print(f" - [blue]{field['id'].ljust(20)}[/blue]: [grey70]{field['name']}[/grey70]")
            choice = click.prompt("\nWhich custom fields correspond to the Peer value? (id)")
            if not [field for field in fields if field["id"] == choice]:
                console.print("[red]Wrong value provided, you must specify a field ID[/red]")
                exit()
            self.update_config({"default": {"jira": {"custom_fields": {"peer": choice}}}})

        if not settings.get("jira.custom_fields.story_points") or force:
            console.print("\n[yellow]Agile configuration: custom fields for story points is not set[/yellow]")
            fields = self.session.fields()
            candidates = [field for field in fields if "Story Points" in field["name"]]
            if candidates:
                for candidate in candidates:
                    console.print(f" - [blue]{candidate['id'].ljust(20)}[/blue]: [grey70]{candidate['name']}[/grey70]")
            else:
                for field in fields:
                    console.print(f" - [blue]{field['id'].ljust(20)}[/blue]: [grey70]{field['name']}[/grey70]")
            choice = click.prompt("\nWhich custom fields correspond to the Story Point value? (id)")
            if not [field for field in fields if field["id"] == choice]:
                console.print("[red]Wrong value provided, you must specify a field ID[/red]")
                exit()
            self.update_config({"default": {"jira": {"custom_fields": {"story_points": choice}}}})

        if not settings.get(f"jira.projects.{project}.workflow") or force:
            console.print("\n[yellow]Agile configuration:  workflow is not set[/yellow]")
            # Get Status for the project
            statuses = get_project_story_status(
                project,
                url=settings.get("instance"),
                login=settings.get("login"),
                password=keyring.get_password("moic", settings.get("login")),
            )
            suggest = """# You can configure the sprint command output
# Choosing the order of the issue status inside the main classes : new, inderminate, done
#
# Provide the orderd configuration you want such as this example:
#
#
# {'new': ['1', '4'], 'indeterminate': ['3', '5,6', '9'], 'done': ['8', '7']}
#
# note : use ',' to group status
#
"""
            default = {}
            for sc in ["new", "indeterminate", "done"]:
                default_status = []
                suggest = suggest + f"# {sc}\n"
                for status in statuses:
                    if status["statusCategory"]["key"] == sc:
                        suggest = suggest + f"#  - ({status['id']}) {status['name']}\n"
                        default_status.append(status["id"])
                default[sc] = default_status
            suggest = suggest + "\n" + str(default)
            response = click.edit(suggest, require_save=False)
            workflow = [line for line in response.split("\n") if not line.startswith("#") and line != ""]
            if workflow:
                workflow_config = json.loads(workflow[0].replace("'", '"'))
                self.update_config({"default": {"jira": {"projects": {project: {"workflow": workflow_config}}}}})
                console.print(workflow_config)

        console.print("[green]Agile workflow saved![/green]")
        console.line()
        console.print(f"[grey70]  > Configuration stored in {os.path.expanduser(CONF_DIR)}[/grey70]")


def merge_dict(a: dict, b: dict, path: str = None) -> dict:
    """
    Merge two dict together

    Args:
        a (dict): The main dict
        b (dict): The secondary dict which should be merged into a
        path (str): The path where to merde

    Returns:
        dict: The merged dict
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception(f"Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
