import re
from flashtext import KeywordProcessor

def extract_structured_infra(summary):
    result = {
        "statscards": [],
        "performance_alerts": {
            "high_cpu_hosts": [],
            "underutilized_hosts": []
        },
        "custom_configs": []
    }

    # Extract total servers
    m = re.search(r"health of (\d+) .*? servers", summary, re.I)
    if m:
        result["statscards"].append({"title": "Total Servers", "value": int(m.group(1)), "unit": "hosts"})

    # Quantities (CPU, memory, disk)
    cpu = re.search(r"(\d+)[ ]*core", summary)
    mem = re.search(r"(\d+)[ ]*GB memory", summary)
    disk = re.search(r"(\d+)[ ]*GB disk", summary)
    if cpu: result["statscards"].append({"title": "CPU", "value": int(cpu.group(1)), "unit": "cores"})
    if mem: result["statscards"].append({"title": "Memory", "value": int(mem.group(1)), "unit": "GB"})
    if disk: result["statscards"].append({"title": "Disk", "value": int(disk.group(1)), "unit": "GB"})

    # Custom configs
    matches = re.findall(r"(\d+)[ ]*core.*?(\d+)[ ]*GB.*?(\d+)[ ]*GB", summary)
    for cpu, mem, disk in matches:
        result["custom_configs"].append({
            "cpu": int(cpu),
            "memory": int(mem),
            "disk": int(disk)
        })

    # Hostname matching
    result["performance_alerts"]["high_cpu_hosts"] = re.findall(r"high cpu.*?\b(host\w+)\b", summary, re.I)
    result["performance_alerts"]["underutilized_hosts"] = [
        m[0] for m in re.findall(r"\b(host\w+)\b.*?(low cpu|underutilized|low memory)", summary, re.I)
    ]

    return result
