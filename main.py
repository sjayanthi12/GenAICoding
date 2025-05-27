import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
from datadog import initialize as dd_initialize, api as dd_api

from jira_functions import create_issue, update_issue, delete_issue, get_issue, get_issues, get_issue_comments, transition_issue

load_dotenv()

# Set up Datadog
dd_initialize(
    api_key=os.getenv("DATADOG_API_KEY"),
    app_key=os.getenv("DATADOG_APP_KEY")
)

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function dispatcher
def call_function(name, args):
    try:
        if name == "create_issue":
            result = create_issue(**args)
        elif name == "update_issue":
            result = update_issue(**args)
        elif name == "delete_issue":
            result = delete_issue(**args)
        elif name == "get_issue":
            result = get_issue(**args)
        elif name == "get_issues":
            result = get_issues(**args)
        elif name == "get_issue_comments":
            result = get_issue_comments(**args)
        elif name == "transition_issue":
            result = transition_issue(**args)
        else:
            return {"error": f"Unknown function '{name}'"}

        # Log success to Datadog
        dd_api.Event.create(
            title=f"Function '{name}' executed successfully",
            text=json.dumps(args, indent=2),
            alert_type="info",
            tags=["jira", name]
        )
        return result
    except Exception as e:
        # Log error to Datadog
        dd_api.Event.create(
            title=f"Function '{name}' execution failed",
            text=str(e),
            alert_type="error",
            tags=["jira", "error", name]
        )
        return {"error": str(e)}

# Validate input
if len(sys.argv) < 2:
    print("Usage: python main.py \"<your prompt>\"")
    sys.exit(1)

user_prompt = sys.argv[1]

# Define available tools
tools = [
    {
        "type": "function",
        "name": "create_issue",
        "description": "Create a new issue in Jira project",
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
        "name": "get_issues",
        "description": "Get list of all issues in a project",
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
        "description": "Update an existing issue",
        "parameters": {
            "type": "object",
            "properties": {
                "issue_id": {"type": "string"},
                "summary": {"type": "string"},
                "description": {"type": "string"},
                "issue_type": {"type": "string"}
            },
            "required": ["issue_id", "summary", "description", "issue_type"],
            "additionalProperties": False
        },
        "strict": True
    }
]

# Get AI tool recommendation
input_messages = [{"role": "user", "content": user_prompt}]
response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools
)

# Extract and run the tool
tool_call = response.output[0]
name = tool_call.name
args = json.loads(tool_call.arguments)

print(f"[INFO] Calling function: {name} with args: {args}")
result = call_function(name, args)
print(json.dumps(result, indent=2))
import os

def load_dotenv(path=".env"):
    """
    Load environment variables from a .env file into os.environ
    """
    if not os.path.exists(path):
        print(f"[WARN] No .env file found at {path}")
        return {}

    loaded_vars = {}

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("export "):
                line = line.replace("export ", "", 1)

            if "=" not in line:
                print(f"[WARN] Skipping malformed line: {line}")
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.split(" #")[0].strip().strip('"').strip("'")

            if key not in os.environ:
                os.environ[key] = value
                loaded_vars[key] = value

    print(f"[INFO] Loaded {len(loaded_vars)} environment variables from {path}")
    return loaded_vars