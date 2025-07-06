
from datetime import datetime

def run_crew():
    logs = []

    def log(agent, action, detail):
        logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent_name": agent,
            "action_type": action,
            "details": detail
        })

    log("ForecasterAgent", "forecast", "Predicted CPU peak at 85%, Memory at 78%")
    log("ConfiguratorAgent", "proposed_config", "Propose 1 extra node and increase memory limit")
    log("ApprovalAgent", "approval", "Approved: Add node, but hold on memory expansion")
    return logs
