from atlassian import Jira
from dotenv import load_dotenv
from datadog import initialize, api
import os, time

load_dotenv('.env')

DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")

options = {
    'api_key': DATADOG_API_KEY,
    'app_key': DATADOG_APP_KEY
}

initialize(**options)

# --- Free tier useful functions ---

# Send a custom gauge metric
api.Metric.send(
    metric='my.custom.metric',
    points=100,
    tags=["env:production", "team:backend"],
    type="gauge"
)

# Send a counter metric (increment)
api.Metric.send(
    metric='jira.bugs.created',
    points=1,
    tags=['env:prod', 'jira'],
    type="count"
)

# Log an event (great for deployments, errors, milestones)
api.Event.create(
    title="Deployment successful",
    text="Version 1.2.3 deployed to production environment.",
    alert_type="success",
    tags=["env:production", "deployment"]
)

# Log an error event example
api.Event.create(
    title="Jira API Error",
    text="Failed to create Jira issue due to timeout.",
    alert_type="error",
    tags=["jira", "error"]
)

# Service check (monitor your app/service health - pass=0, warning=1, critical=2, unknown=3)
api.ServiceCheck.check(
    check="jira.service.health",
    status=0,  # OK
    tags=["env:prod"]
)

# --- Paid features (commented out, useful if you upgrade) ---

# Query metrics (requires paid plan, will give "Forbidden" on free tier)
# start_time = int(time.time()) - 3600
# end_time = int(time.time())
# result = api.Metric.query(
#     start=start_time,
#     end=end_time,
#     query='avg:system.cpu.user{*}'
# )
# print("CPU Usage (last hour):", result)

# Get list of events (useful for audit/log analysis)
# events = api.Event.query(
#     start=int(time.time()) - 3600,
#     end=int(time.time()),
#     tags="env:production"
# )
# print("Recent events:", events)

# Get host list (paid feature, useful for infra monitoring)
# hosts = api.Hosts.search()
# print("Hosts:", hosts)

# --- Helper function example ---

def send_latency_metric(latency_seconds):
    api.Metric.send(
        metric="jira.api.call.latency",
        points=latency_seconds,
        tags=["env:prod", "jira"],
        type="gauge"
    )

# Example usage
fake_latency = 0.245  # seconds
send_latency_metric(fake_latency)
