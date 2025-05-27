from atlassian import Jira
from langchain_core.tools import tool

from dotenv import load_dotenv

import os

load_dotenv('.env')

JIRA_URL = os.environ.get("JIRA_INSTANCE_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")


jira = Jira(url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN)

def create_issue(summary: str, description: str, issue_type: str) -> dict:
    print("New issue is being created")
    try:
        new_issue = jira.create_issue(
            fields={
                "project": {"key": os.environ.get('JIRA_PROJECT_KEY')},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        )
        return {"id": new_issue.id, "key": new_issue.key, "message": "Issue created successfully"}
    except Exception as e:
        return {"error": str(e)}

    print(new_issue)

def update_issue(issue_id: str, summary: str, description: str, issue_type: str) -> dict:
    print(f"Updating issue {issue_id}")
    try:
        issue = jira.issue(issue_id)
        fields = {
            "summary": summary if summary else issue.fields.summary,
            "description": description if description else issue.fields.description,
            "issuetype": {"name": issue_type if issue_type else issue.fields.issuetype.name}
        }
        issue.update(fields=fields)
        return {"message": f"Issue {issue_id} updated successfully"}
    except Exception as e:
        return {"error": str(e)}
    
def delete_issue(issue_id: str) -> dict:
    """
    Deletes a Jira issue.
    :param issue_id: The issue ID
    """
    try:
        jira.issue(issue_id).delete()
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "message": "Issue deleted successfully"
    }


def get_issue(issue_id: str) -> dict:
    try:
        issue = jira.issue(issue_id)
        return {
            "id": issue.id,
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "type": issue.fields.issuetype.name
        }
    except Exception as e:
        return {"error": str(e)}

def get_issues(project: str) -> dict:

    print("Getting list of issues")

    try:
        issues = jira.search_issues(f"project={project}")
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "issues": [
            {
                "id": issue.id,
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "type": issue.fields.issuetype.name
            } for issue in issues
        ]
    }

def get_issue_comments(issue_id: str) -> dict:
    """
    Gets the comments for a Jira issue.
    :param issue_id: The issue ID
    :return: The comments
    """
    try:
        comments = jira.comments(issue_id)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        'comments': [
            {
                'id': comment.id,
                'body': comment.body
            } for comment in comments
        ]
    }

def get_issue_transitions(issue_id: str) -> dict:
    """
    Gets the transitions for a Jira issue.
    :param issue_id: The issue ID
    :return: The transitions
    """
    try:
        transitions = jira.transitions(issue_id)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        'transitions': [
            {
                'id': transition['id'],
                'name': transition['name']
            } for transition in transitions
        ]
    }

def transition_issue(issue_id: str, transition_id: str) -> dict:
    """
    Transitions a Jira issue.
    :param issue_id: The issue ID
    :param transition_id: The transition ID
    :return: The transition result
    """
    try:
        jira.transition_issue(issue_id, transition_id)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "message": "Issue transitioned successfully"
    }