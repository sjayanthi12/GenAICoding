import os
import sys
import json
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError
from datadog_functions import send_custom_metric, log_event, send_service_check

load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function dispatcher
user_prompt = " ".join(str(item) for item in sys.argv[1:20])

def main():

    input_messages = [{"role": "user", "content": user_prompt}]

    response = get_openai_response(input_messages, tools)

    message = response.choices[0].message

# Execute tool call
    tool_call = message.tool_calls[0]
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"[INFO] Calling function: {name} with args: {args}")
    result = call_function(name, args)
    print(json.dumps(result, indent=2))

def call_function(name, args):

    print("From call_function ", name, args)
    functions = {
       # Datadog
            "send_custom_metric": send_custom_metric,
            "log_event": log_event,
            "send_service_check": send_service_check
    }
    func = functions.get(name)
    return func(**args) if func else {"error": f"Function {name} not found"}

# Validate input

tools = [{
    "type": "function",
    "function": {
        "name": "send_custom_metric",
        "description": "Send custom metric to Datadog",
        "parameters": {
            "type": "object",
            "properties": {
                "metric_name": {
                    "type": "string",
                    "description": "Name of the metric"
                },
                "value": {
                    "type": "number",
                    "description": "Value of the metric"
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags of the metric"
                },
                "metric_type": {
                    "type": "string",
                    "description": "Type of the metric"
                }
            },
            "required": ["metric_name", "value"],
            "additionalProperties": False
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "log_event",
        "description": "Log an event to Datadog",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the event"
                },
                "text": {
                    "type": "string",
                    "description": "Text body of the event"
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags for the event"
                },
                "alert_type": {
                    "type": "string",
                    "description": "Type of alert (info, warning, error, success)"
                }
            },
            "required": ["title", "text"],
            "additionalProperties": False
        }
    }
}]


# Get OpenAI response
def get_openai_response(messages, tools):

    print("From get_openai_response ", messages, tools)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        tools=tools
    )
    return response

if __name__ == "__main__":
    # This block ensures that main() is called only when the script is executed directly,
    # and not when it's imported as a module into another script.
    main()