import re
from rapidfuzz import fuzz

# 🔧 Normalize
def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", text.lower().strip())

# 🧠 Expanded intent keyword dictionary
KEYWORDS = {
    "cpu_usage": ["cpu", "processor", "core", "utilization", "load average"],
    "memory_usage": ["memory", "ram", "heap", "cache", "buffer", "swap"],
    "disk_info": ["disk", "storage", "drive", "partition", "mount", "inode"],
    "uptime_status": ["uptime", "boot", "restarted", "start"],
    "network_io": ["network", "throughput", "bandwidth", "rx", "tx", "latency"],
    "error_rate": ["error", "5xx", "failures", "exceptions", "crash"],
    "pod_status": ["pod", "container", "restart", "kubernetes", "status"],
    "namespace_metrics": ["namespace", "kube-system", "default", "metrics"],
    "node_latency": ["latency", "p95", "response time", "delay", "jitter"]
}

# 🔒 Malicious detection logic
MALICIOUS_TERMS = [
    "rm -rf", "drop database", "shutdown", "format disk", "kill process", "delete everything"
]

# 🧪 Context-aware malicious check
def is_malicious_or_suspicious(prompt: str, threshold=85) -> str | None:
    prompt_norm = normalize(prompt)
    for word in MALICIOUS_TERMS:
        score = fuzz.partial_ratio(prompt_norm, word)
        if score >= threshold:
            if score > 92:
                return "blocked"  # Definitely malicious
            else:
                return "suspicious"  # Might be typo or confusion
    return None

# 🔁 Fuzzy keyword matching
def fuzzy_match(prompt: str, threshold: int = 70) -> str:
    prompt_norm = normalize(prompt)
    scores = {
        intent: max(fuzz.partial_ratio(prompt_norm, kw) for kw in keywords)
        for intent, keywords in KEYWORDS.items()
    }
    best_intent, best_score = max(scores.items(), key=lambda x: x[1])
    return best_intent if best_score >= threshold else "Sorry, no response found."

# 🔮 Final detector
def detect_intent(prompt: str) -> str:
    prompt_norm = normalize(prompt)
    status = is_malicious_or_suspicious(prompt_norm)

    if status == "blocked":
        return "Sorry, that request contains restricted operations."
    elif status == "suspicious":
        return "Did you mean something else? Please clarify your request."

    return fuzzy_match(prompt_norm)
