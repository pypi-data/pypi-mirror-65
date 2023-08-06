from moic.config import JiraInstance


def autocomplete_users(ctx, args, incomplete):
    """Get Jira users list completion"""
    try:
        jira = JiraInstance()
        users = jira.session.search_users(incomplete)
        return [user.name for user in users]
    except Exception:
        return []


def autocomplete_issues(ctx, args, incomplete):
    """Get Jira issues list completion"""
    try:
        jira = JiraInstance()
        if "-" in incomplete:
            issues = jira.session.search_issues(f"project = {incomplete.split('-')[0]}", 0, 100)
            return [(issue.key, issue.fields.summary) for issue in issues if issue.key.startswith(incomplete.upper())]
        else:
            return []
    except Exception:
        return []


def autocomplete_transitions(ctx, args, incomplete):
    """Get Jira translations available for an issue"""
    try:
        jira = JiraInstance()
        issue_key = args[-1:][0]
        issue = jira.session.issue(issue_key)
        transitions = jira.session.transitions(issue)
        return [t.name for t in transitions if t.name.startswith(incomplete)]
    except Exception:
        return []


def autcomplete_projects(ctx, args, incomplete):
    """Get Jira projects list completion"""
    try:
        jira = JiraInstance()
        projects = jira.session.project()
        return [p.name for p in projects if incomplete in p.name]
    except Exception:
        return []
