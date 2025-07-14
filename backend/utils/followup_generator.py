from utils.intent_detector import detect_intent

FOLLOWUP_TEMPLATES = {
    "cpu_usage": [
        "Show CPU usage by pod",
        "Show CPU usage by node",
        "Show CPU usage by namespace",
        "Show CPU usage by server"
    ],
    "memory_usage": [
        "Show memory usage by pod",
        "Show memory usage by node",
        "Show memory usage by namespace",
        "Show memory usage by server"
    ],
    "disk_info": [
        "Show disk usage by node",
        "Show disk usage by server"
    ],
    "uptime_status": [
        "Show uptime per node",
        "Show uptime per cluster"
    ]
}

def generate_followup(prompt: str) -> list:
    intent = detect_intent(prompt)
    if intent == "unknown":
        return [
            "Please specify the scope: pod, node, namespace, or server?",
            "Example: Show memory usage by pod",
            "Example: Show CPU usage for server1"
        ]
    return FOLLOWUP_TEMPLATES.get(intent, [])
