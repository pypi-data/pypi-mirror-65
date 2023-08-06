"""
Jira Api custom calls module
"""
import json

import requests
from requests.auth import HTTPBasicAuth


def get_project_status(projectIdOrKey: str, url: str = None, login: str = None, password: str = None) -> dict:
    """
    Get project status using a given project Key or ID

    Args:
        projectIdOrKey (str): The Jira project ID or Key
        url (str): The base url of the Jira instance
        login (str): The login credential to access the API
        password (str): The passowrd credential to access the API

    Returns:
        dict: Dict of status existing for the given project
    """
    if not url and not login and not password:
        return None

    url = f"{url}/rest/api/2/project/{projectIdOrKey}/statuses"
    auth = HTTPBasicAuth(login, password)
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, auth=auth)
    return json.loads(response.text)


def get_project_story_status(projectIdOrKey: str, url: str = None, login: str = None, password: str = None) -> dict:
    """
    Get project status using a given project Key or ID which correspond to issue type stories

    Args:
        projectIdOrKey (str): The Jira project ID or Key
        url (str): The base url of the Jira instance
        login (str): The login credential to access the API
        password (str): The passowrd credential to access the API

    Returns:
        dict: Dict of status existing for the given project
    """
    return [
        st["statuses"]
        for st in get_project_status(projectIdOrKey, url=url, login=login, password=password)
        if st["name"] == "Story"
    ][0]
