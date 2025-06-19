import os
import sys
import json
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError
from datadog import initialize as dd_initialize
from datadog_functions import send_custom_metric, log_event, send_service_check
from jira_functions import create_issue, update_issue, delete_issue, get_issue, get_issues, transition_issue

load_dotenv()

# Initialize Datadog
dd_initialize(
    api_key=os.getenv("DATADOG_API_KEY"),
    app_key=os.getenv("DATADOG_APP_KEY")
)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function dispatcher
def call_function(name, args):
    try:
        functions = {
            # Datadog
            "send_custom_metric": send_custom_metric,
            "log_event": log_event,
            "send_service_check": send_service_check,
            # Jira
            "create_issue": create_issue,
            "update_issue": update_issue,
            "delete_issue": delete_issue,
            "get_issue": get_issue,
            "get_issues": get_issues,
            "transition_issue": transition_issue
        }
        func = functions.get(name)
        if func is None:
            return {"error": f"Unknown function '{name}'"}
        start = time.perf_counter()
        result = func(**args)
        duration = time.perf_counter() - start
        send_custom_metric("jira.api.call.latency", duration, ["env:prod", name], "gauge")
        return result
    except Exception as e:
        log_event(
            title=f"Function '{name}' execution failed",
            text=str(e),
            alert_type="error",
            tags=["error", name]
        )
        return {"error": str(e)}

# Validate input
if len(sys.argv) < 2:
    print("Usage: python main.py \"<your prompt>\"")
    sys.exit(1)

user_prompt = sys.argv[1]

# Tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_issue",
            "description": "Create a new issue in a Jira project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "summary": {"type": "string"},
                    "description": {"type": "string"},
                    "issue_type": {"type": "string"}
                },
                "required": ["project", "summary", "description", "issue_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_issue",
            "description": "Update an existing Jira issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"},
                    "summary": {"type": "string"},
                    "description": {"type": "string"},
                    "issue_type": {"type": "string"}
                },
                "required": ["issue_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_issue",
            "description": "Delete a Jira issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"}
                },
                "required": ["issue_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_issue",
            "description": "Retrieve a Jira issue by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"}
                },
                "required": ["issue_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_issues",
            "description": "Retrieve all issues for a Jira project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string"}
                },
                "required": ["project"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_issue_comments",
            "description": "Retrieve comments from a Jira issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"}
                },
                "required": ["issue_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_issue_transitions",
            "description": "Retrieve available transitions for a Jira issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"}
                },
                "required": ["issue_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transition_issue",
            "description": "Transition a Jira issue to a different state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"},
                    "transition_id": {"type": "string"}
                },
                "required": ["issue_id", "transition_id"]
            }
        }
    }
]


# Get OpenAI response
def get_openai_response(messages, tools):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=messages,
                tools=tools
            )
            return response
        except RateLimitError:
            print(f"[WARN] Rate limit hit. Retrying in 5 seconds... ({attempt + 1}/3)")
            time.sleep(5)
        except OpenAIError as e:
            print(f"[ERROR] OpenAI error: {e}")
            sys.exit(1)
    print("[FATAL] Rate limit persisted after retries. Exiting.")
    sys.exit(1)

# Prompt to OpenAI
input_messages = [
    {
        "role": "system",
        "content": (
            "You are an AI assistant integrated with Jira and Datadog. "
            "If the user asks to create, update, delete, or log anything, "
            "you must call the appropriate tool function. "
            "Do not just reply with helpful text unless explicitly asked. "
            "Always prefer tool use over plain responses when possible."
        )
    },
    {"role": "user", "content": user_prompt}
]

response = get_openai_response(input_messages, TOOLS)
message = response.choices[0].message

# Defensive check
if not hasattr(message, "tool_calls") or message.tool_calls is None:
    print("[ERROR] No tool call was returned by the model. Try rephrasing your prompt.")
    print("AI replied with:", message.content)
    sys.exit(1)

# Execute tool call
tool_call = message.tool_calls[0]
name = tool_call.function.name
args = json.loads(tool_call.function.arguments)

print(f"[INFO] Calling function: {name} with args: {args}")
result = call_function(name, args)
print(json.dumps(result, indent=2))
