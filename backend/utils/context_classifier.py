import re

# 🔐 Blocklist to prevent malicious prompts
BLOCKED_KEYWORDS = {"shutdown", "delete", "rm", "drop", "format", "exploit"}

def normalize(prompt: str) -> str:
    return re.sub(r'[^a-z0-9 ]+', '', prompt.lower())

def infer_context_role(prompt: str) -> str:
    prompt = normalize(prompt)
    if any(bad in prompt for bad in BLOCKED_KEYWORDS):
        return "Blocked Request"
    elif "cpu" in prompt or "promql" in prompt:
        return "Prometheus Dashboard Expert"
    elif "ticket" in prompt or "servicenow" in prompt:
        return "Incident Triage Assistant"
    elif "error" in prompt or "status code" in prompt:
        return "Troubleshooting Assistant"
    elif "uptime" in prompt or "latency" in prompt:
        return "System Health Monitor"
    else:
        return "Monitoring Assistant"

def infer_context_scope(prompt: str) -> str:
    prompt = normalize(prompt)
    metrics = ["cpu", "memory", "disk", "latency", "uptime", "http", "io", "error"]
    found = sum(1 for metric in metrics if metric in prompt)

    if found == 0:
        return "unknown"
    elif found == 1:
        return "narrow"
    elif found <= 3:
        return "medium"
    else:
        return "broad"
