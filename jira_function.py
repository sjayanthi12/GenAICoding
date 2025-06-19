from jira import JIRA
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
load_dotenv('.env')

JIRA_URL = os.environ.get("JIRA_INSTANCE_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

jira = JIRA(url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN)

@tool
def create_issue(summary: str, description: str, issue_type: str) -> dict:
    """
    Creates a Jira issue.
    :param summary: The issue summary
    :param description: The issue description
    :param issue_type: The issue type
    :return: The created issue
    """
    try:
        new_issue = jira.create_issue(
            fields={
                "project": {"key": os.environ.get('JIRA_PROJECT_KEY')},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        )
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "id": new_issue.id,
        "key": new_issue.key,
        "summary": new_issue.fields.summary,
        "description": new_issue.fields.description,
        "type": new_issue.fields.issuetype.name
    }

@tool
def update_issue(issue_id: str, summary: str, description: str, issue_type: str) -> dict:
    """
    Updates a Jira issue.
    :param issue_id: The issue ID
    :param summary: The issue summary
    :param description: The issue description
    :param issue_type: The issue type
    :return: The updated issue
    """
    try:
        issue = jira.issue(issue_id)

        fields = {
            "summary": summary if summary else issue.fields.summary,
            "description": description if description else issue.fields.description,
            "issuetype": {"name": issue_type if issue_type else issue.fields.issuetype.name}
        }

        issue.update(fields=fields)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "id": issue.id,
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": issue.fields.description,
        "type": issue.fields.issuetype.name
    }

@tool
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

@tool
def get_issue(issue_id: str) -> dict:
    """
    Gets a Jira issue.
    :param issue_id: The issue ID
    :return: The issue
    """
    try:
        issue = jira.issue(issue_id)
    except Exception as e:
        return {
            "error": str(e)
        }

    return {
        "id": issue.id,
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": issue.fields.description,
        "type": issue.fields.issuetype.name
    }

@tool
def get_issues(project: str) -> dict:
    """
    Gets all issues in a project.
    :param project: The project key
    :return: The issues
    """
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

@tool
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

@tool
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

@tool
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
