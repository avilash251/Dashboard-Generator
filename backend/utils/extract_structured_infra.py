import re
import spacy
from quantulum3 import parser

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_structured_infra(summary: str):
    result = {
        "statscards": [],
        "performance_alerts": {
            "high_cpu_hosts": [],
            "underutilized_hosts": []
        },
        "custom_configs": []
    }

    # Extract total servers
    match = re.search(r"health of (\d+) .*? servers", summary, re.I)
    if match:
        result["statscards"].append({
            "title": "Total Servers",
            "value": int(match.group(1)),
            "unit": "hosts"
        })

    # Extract quantities using quantulum3
    quantities = parser.parse(summary)
    cpu = memory = disk = None

    for q in quantities:
        unit = q.unit.name.lower()
        if unit in ["gigabyte", "gb"]:
            if not memory:
                memory = int(q.value)
            elif not disk:
                disk = int(q.value)
        elif unit in ["core", "cores", "processor"]:
            if not cpu:
                cpu = int(q.value)

    if cpu:
        result["statscards"].append({"title": "CPU", "value": cpu, "unit": "cores"})
    if memory:
        result["statscards"].append({"title": "Memory", "value": memory, "unit": "GB"})
    if disk:
        result["statscards"].append({"title": "Disk", "value": disk, "unit": "GB"})

    # Custom configs
    custom_matches = re.findall(r"(\d+)[ ]*core.*?(\d+)[ ]*GB.*?(\d+)[ ]*GB", summary, re.I)
    for cpu_val, mem_val, disk_val in custom_matches:
        config = {
            "cpu": int(cpu_val),
            "memory": int(mem_val),
            "disk": int(disk_val)
        }
        if config not in result["custom_configs"]:
            result["custom_configs"].append(config)

    # Extract hostnames
    high_cpu_matches = re.findall(r"high cpu.*?\b(host\w+)\b", summary, re.I)
    low_util_matches = re.findall(r"\b(host\w+)\b.*?(low cpu|underutilized|low memory)", summary, re.I)

    result["performance_alerts"]["high_cpu_hosts"] = list(set(high_cpu_matches))
    result["performance_alerts"]["underutilized_hosts"] = list(set([h[0] for h in low_util_matches]))

    return result
