from rapidfuzz import fuzz

# 🔧 Predefined static context mapping
# backend/utils/static_context.py

PROMQL_CONTEXT_MAP = {
    "cpu": [
        "CPU usage (percent): avg(rate(process_cpu_seconds_total[1m])) by (instance)",
        "CPU usage for application: rate(container_cpu_usage_seconds_total{container!=\"\", pod!=\"\"}[5m])",
        "Node CPU idle: 100 - (avg by (instance)(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
        "Top CPU consumers: topk(5, rate(container_cpu_usage_seconds_total[1m]))"
    ],
    "memory": [
        "Memory usage in MB: node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes",
        "Memory usage for namespace: sum(container_memory_usage_bytes{namespace=\"kube-system\"}) by (pod)",
        "Available memory percentage: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100"
    ],
    "disk": [
        "Disk usage in percent: 100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100",
        "Disk I/O: rate(node_disk_read_bytes_total[5m])"
    ],
    "network": [
        "Network I/O rate: rate(container_network_transmit_bytes_total[5m])",
        "Pod-level network RX: sum(rate(container_network_receive_bytes_total{pod=\"your-pod\"}[5m]))"
    ],
    "http_errors": [
        "HTTP 5xx errors: sum(rate(http_requests_total{status=~\"5..\"}[5m]))",
        "Error rate by route: sum(rate(http_requests_total{status=~\"5..\"}[1m])) by (route)"
    ],
    "uptime": [
        "Instance uptime in seconds: node_time_seconds - node_boot_time_seconds",
        "Prometheus uptime: time() - process_start_time_seconds"
    ]
}

def retrieve_context(user_prompt: str) -> str:
    """
    Use fuzzy match to find the most relevant context string based on the prompt.
    """
    try:
        best_key = None
        best_score = 0

        for key, description in PROMQL_CONTEXT_MAP.items():
            score = fuzz.partial_ratio(user_prompt.lower(), key.lower())
            if score > best_score:
                best_score = score
                best_key = key

        if best_score >= 70 and best_key:
            return PROMQL_CONTEXT_MAP[best_key]
        return "No specific context found for the given prompt."
    except Exception as e:
        return f"Context resolution error: {str(e)}"
