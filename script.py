from jira_functions import create_jira_issue, get_jira_issue, update_jira_issue, transition_jira_issue

# Example usage
issue_key = create_jira_issue("Test Summary", "Test Description")
print("Created issue:", issue_key)

issue = get_jira_issue(issue_key)
print("Fetched issue:", issue)

update_jira_issue(issue_key, {"summary": "Updated Summary"})
print("Updated issue summary.")

transition_jira_issue(issue_key, "Done")
print("Transitioned issue to Done.")