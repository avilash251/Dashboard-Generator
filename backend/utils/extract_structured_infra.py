import re
from flashtext import KeywordProcessor

def extract_structured_infra(summary: str, known_hosts: list = []):
    result = {
        "statscards": [],
        "performance_alerts": {
            "high_cpu_hosts": [],
            "underutilized_hosts": []
        },
        "custom_configs": []
    }

    # Stats: Total servers
    match = re.search(r"health of (\d+) .*? servers", summary, re.I)
    if match:
        result["statscards"].append({
            "title": "Total Servers",
            "value": int(match.group(1)),
            "unit": "hosts"
        })

    # General resources
    cpu = re.search(r"(\d+)[ ]*core", summary)
    mem = re.search(r"(\d+)[ ]*GB memory", summary)
    disk = re.search(r"(\d+)[ ]*GB disk", summary)

    if cpu:
        result["statscards"].append({"title": "CPU", "value": int(cpu.group(1)), "unit": "cores"})
    if mem:
        result["statscards"].append({"title": "Memory", "value": int(mem.group(1)), "unit": "GB"})
    if disk:
        result["statscards"].append({"title": "Disk", "value": int(disk.group(1)), "unit": "GB"})

    # Custom configurations
    custom_matches = re.findall(r"(\d+)[ ]*core.*?(\d+)[ ]*GB.*?(\d+)[ ]*GB", summary, re.I)
    for c, m, d in custom_matches:
        result["custom_configs"].append({
            "cpu": int(c),
            "memory": int(m),
            "disk": int(d)
        })

    # Use FlashText for hostname detection (optional)
    keyword_processor = KeywordProcessor()
    for h in known_hosts:
        keyword_processor.add_keyword(h)

    found_hosts = keyword_processor.extract_keywords(summary)

    # Performance alerts
    high_cpu = re.findall(r"high cpu.*?\b(host\w+)\b", summary, re.I)
    underutil = re.findall(r"\b(host\w+)\b.*?(low cpu|underutilized|low memory)", summary, re.I)

    result["performance_alerts"]["high_cpu_hosts"] = list(set(high_cpu) | set(found_hosts))
    result["performance_alerts"]["underutilized_hosts"] = list(set(h[0] for h in underutil))

    return result
