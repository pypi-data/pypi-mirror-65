import json

import requests
from requests.auth import HTTPBasicAuth


def get_project_status(projectIdOrKey, url=None, login=None, password=None):
    if not url and not login and not password:
        return None

    url = f"{url}/rest/api/2/project/{projectIdOrKey}/statuses"
    auth = HTTPBasicAuth(login, password)
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, auth=auth)
    return json.loads(response.text)


def get_project_story_status(projectIdOrKey, url=None, login=None, password=None):
    return [
        st["statuses"]
        for st in get_project_status(projectIdOrKey, url=url, login=login, password=password)
        if st["name"] == "Story"
    ][0]
