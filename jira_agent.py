import os
from dotenv import load_dotenv
from agents import Agent, Runner
from atlassian import Jira
import json, sys
from openai import OpenAI
from jira_functions import create_issue, update_issue, delete_issue, get_issue, get_issues, get_issue_comments, transition_issue

# Load environment variables from .env file
load_dotenv()

# Access your API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

JIRA_URL = os.environ.get("JIRA_INSTANCE_URL")
JIRA_USERNAME = os.environ.get("JIRA_USERNAME")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")


jira = Jira(url=JIRA_URL, username=JIRA_USERNAME, password=JIRA_API_TOKEN)


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def call_function(name, args):
    functions = {
        "create_issue": create_issue,
        "get_issues": get_issues,
        "update_issue": update_issue,
        "get_issue": get_issue,
        "delete_issue": delete_issue,
        "transition_issue": transition_issue,
    }
    func = functions.get(name)
    return func(**args) if func else {"error": f"Function {name} not found"}
   
   
if len(sys.argv) < 2:
    print("Please provide a prompt.")
    sys.exit(1)

user_prompt = sys.argv[1]

tools = [{
	"type": "function",
    "name": "get_issues",
    "description": "get list of all issues in project",
    "parameters": {
        "type": "object",
        "properties": {
            "project": {"type": "string"}
        },
        "required": ["project"],
        "additionalProperties": False
    },
    "strict": True
},

{
    "type": "function",
    "name": "update_issue",
    "description": "Update a existing issue in jira project",
    "parameters": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "description": {"type": "string"},
		   "issue_type": {"type": "string"}
        },
        "required": ["summary", "description", "issue_type"],
        "additionalProperties": False
    },
    "strict": True
},

{
	"type": "function",
    "name": "create_issue",
    "description": "Create a new issue in jira project",
    "parameters": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "description": {"type": "string"},
		   "issue_type": {"type": "string"}
        },
        "required": ["summary", "description", "issue_type"],
        "additionalProperties": False
    },
    "strict": True
}]

input_messages = [{"role": "user", "content": user_prompt}]

response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)

tool_call = response.output[0]

name=tool_call.name
args = json.loads(tool_call.arguments)

print(f"This is new {tool_call.arguments}  {name}")


result = call_function(name, args)

print(result) 