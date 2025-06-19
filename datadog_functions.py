from datadog import initialize, api
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv('.env')

# Initialize Datadog API keys
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")

options = {
    'api_key': DATADOG_API_KEY,
    'app_key': DATADOG_APP_KEY
}

initialize(**options)

# --- Core Functions (Free Tier) ---

def send_custom_metric(metric_name, value, tags, metric_type):
    return api.Metric.send(
        metric=metric_name,
        points=value,
        tags=tags,
        type=metric_type
    )

def log_event(title, text, alert_type, tags):
    return api.Event.create(
        title=title,
        text=text,
        alert_type=alert_type,
        tags=tags
    )

def send_service_check(check_name, status, tags):
    return api.ServiceCheck.check(
        check=check_name,
        status=status,
        tags=tags
    )

# --- Helper Function ---

def send_latency_metric(latency_seconds):
    return send_custom_metric(
        metric_name="jira.api.call.latency",
        value=latency_seconds,
        tags=["env:prod", "jira"],
        metric_type="gauge"
    )

# --- Paid Tier Functions (Commented Out) ---

# def query_metrics(query, minutes=60):
#     """
#     Query a metric time series (requires paid Datadog plan).
#     """
#     end = int(time.time())
#     start = end - (minutes * 60)
#     return api.Metric.query(start=start, end=end, query=query)

# def query_events(tags, minutes=60):
#     """
#     Query recent events filtered by tags (requires paid Datadog plan).
#     """
#     end = int(time.time())
#     start = end - (minutes * 60)
#     return api.Event.query(start=start, end=end, tags=" ".join(tags))

# def get_host_list():
#     """
#     Get list of monitored hosts (requires paid Datadog plan).
#     """
#     return api.Hosts.search()
