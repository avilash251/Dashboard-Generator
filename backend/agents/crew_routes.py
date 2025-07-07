# backend/agents/crew_router.py
from crewai import Crew, Task
from agents.crewai_agents import intent_agent, promql_agent, layout_agent, logger_agent, followup_agent

def handle_prompt_with_crew(prompt: str):
    crew = Crew(
        agents=[intent_agent, promql_agent, layout_agent, logger_agent, followup_agent],
        tasks=[
            Task(agent=intent_agent, expected_output="User intent", input=prompt),
            Task(agent=promql_agent, expected_output="PromQL query"),
            Task(agent=layout_agent, expected_output="Chart layout"),
            Task(agent=logger_agent, expected_output="Audit log updated"),
            Task(agent=followup_agent, expected_output="Follow-up suggestions as list")
        ],
        verbose=True
    )

    result = crew.run()
    followups = []

    try:
        followups = eval(result.get("Follow-up suggestions as list", "[]"))
        if not isinstance(followups, list):
            followups = []
    except:
        followups = []

    return {
        "charts": [{
            "title": "Auto-generated",
            "promql": result.get("PromQL query", "up"),
            "chart_type": "line",
            "thresholds": [70, 90]
        }],
        "followups": followups,
        "raw": result
    }
