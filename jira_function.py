from atlassian import Jira
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env')

# Environment config
JIRA_URL = os.environ.get("JIRA_INSTANCE_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# Connect to Jira
jira = Jira(url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN)

def create_issue(project: str, summary: str, description: str, issue_type: str) -> dict:
    print("New issue is being created")
    try:
        new_issue = jira.issue_create(fields={
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        })
        return {
            "key": new_issue.get("key"),
            "id": new_issue.get("id"),
            "message": "Issue created successfully"
        }
    except Exception as e:
        return {"error": str(e)}

def update_issue(issue_id=None, issue_key=None, summary=None, description=None, issue_type=None) -> dict:
    key = issue_id or issue_key
    print(f"Updating issue {key}")
    try:
        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = description
        if issue_type:
            fields["issuetype"] = {"name": issue_type}

        jira.issue_update(key, fields=fields)
        return {"message": f"Issue {key} updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def delete_issue(issue_id=None, issue_key=None) -> dict:
    key = issue_id or issue_key
    try:
        jira.issue_delete(key)
        return {"message": f"Issue {key} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_issue(issue_id=None, issue_key=None) -> dict:
    key = issue_id or issue_key
    try:
        issue = jira.issue(key)
        return {
            "id": issue.get("id"),
            "key": issue.get("key"),
            "summary": issue["fields"]["summary"],
            "description": issue["fields"]["description"],
            "type": issue["fields"]["issuetype"]["name"]
        }
    except Exception as e:
        return {"error": str(e)}

def get_issues(project: str) -> dict:
    print(f"Getting issues from project {project}")
    try:
        response = jira.jql(f"project = {project}")
        issues = response["issues"]
        return {
            "issues": [
                {
                    "id": issue["id"],
                    "key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "description": issue["fields"]["description"],
                    "type": issue["fields"]["issuetype"]["name"]
                }
                for issue in issues
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def get_issue_comments(issue_id=None, issue_key=None) -> dict:
    key = issue_id or issue_key
    try:
        comments = jira.issue_get_comments(key)
        return {
            "comments": [
                {
                    "id": comment.get("id"),
                    "body": comment.get("body")
                }
                for comment in comments
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def get_issue_transitions(issue_id=None, issue_key=None) -> dict:
    key = issue_id or issue_key
    try:
        transitions = jira.get_issue_transitions(key)
        return {
            "transitions": [
                {
                    "id": t["id"],
                    "name": t["name"]
                }
                for t in transitions
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def transition_issue(issue_id=None, issue_key=None, transition_id=None) -> dict:
    key = issue_id or issue_key
    try:
        jira.set_issue_transition(key, transition_id)
        return {"message": f"Issue {key} transitioned successfully"}
    except Exception as e:
        return {"error": str(e)}
