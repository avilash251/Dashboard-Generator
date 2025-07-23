import re

def extract_structured_infra(summary: str):
    result = {
        "statscards": [],
        "performance_alerts": {
            "high_cpu_hosts": [],
            "underutilized_hosts": []
        },
        "custom_configs": []
    }

    # 🖥️ Total servers
    m = re.search(r"health of (\d+)\s+.*?servers", summary, re.I)
    if m:
        result["statscards"].append({
            "title": "Total Servers",
            "value": int(m.group(1)),
            "unit": "hosts"
        })

    # 🧠 CPU handling
    # Case 1: "8 core processors"
    match_core = re.search(r"(\d+)\s+core[s]?\s+processor[s]?", summary, re.I)

    # Case 2: "8 processors, 1 core per processor"
    match_processor_core = re.search(r"(\d+)\s+processor[s]?.*?(\d+)\s+core[s]?\s+per\s+processor", summary, re.I)

    if match_processor_core:
        cpu_total = int(match_processor_core.group(1)) * int(match_processor_core.group(2))
    elif match_core:
        cpu_total = int(match_core.group(1))
    else:
        cpu_total = None

    if cpu_total:
        result["statscards"].append({
            "title": "CPU",
            "value": cpu_total,
            "unit": "cores"
        })

    # 💾 Memory: e.g., "64GB memory", "128 GB of RAM"
    match_mem = re.search(r"(\d+)\s*GB\s*(?:memory|ram)", summary, re.I)
    if match_mem:
        result["statscards"].append({
            "title": "Memory",
            "value": int(match_mem.group(1)),
            "unit": "GB"
        })

    # 🗄️ Disk: "500GB disk", "1024 GB storage"
    match_disk = re.search(r"(\d+)\s*GB\s*(?:disk|storage)", summary, re.I)
    if match_disk:
        result["statscards"].append({
            "title": "Disk",
            "value": int(match_disk.group(1)),
            "unit": "GB"
        })

    # 📊 Custom configurations
    configs = re.findall(r"(\d+)\s*core.*?(\d+)\s*GB.*?(\d+)\s*GB", summary, re.I)
    for cpu, mem, disk in configs:
        result["custom_configs"].append({
            "cpu": int(cpu),
            "memory": int(mem),
            "disk": int(disk)
        })

    # ⚠️ Performance alerts (basic)
    result["performance_alerts"]["high_cpu_hosts"] = re.findall(r"high cpu.*?\b([a-zA-Z0-9\-_]+)\b", summary, re.I)
    result["performance_alerts"]["underutilized_hosts"] = [
        match[0] for match in re.findall(r"\b([a-zA-Z0-9\-_]+)\b.*?(underutilized|low cpu|low memory|idle)", summary, re.I)
    ]

    return result
