# backend/agents/crew_agents.py
from crewai import Agent

intent_agent = Agent(
    role="Intent Analyst",
    goal="Understand the user query and extract infrastructure context",
    backstory="Expert in prompt analysis, command extraction, and metric grouping",
    allow_delegation=True,
    verbose=True
)

promql_agent = Agent(
    role="PromQL Expert",
    goal="Generate optimized PromQL queries based on extracted intent",
    backstory="Deep knowledge of Prometheus metrics, exporters, and label filters",
    allow_delegation=False,
    verbose=True
)

layout_agent = Agent(
    role="Layout Designer",
    goal="Design dynamic dashboard layout including chart type, title, and thresholds",
    backstory="Knows how to structure UI elements for metrics display",
    allow_delegation=False,
    verbose=True
)

logger_agent = Agent(
    role="Audit Logger",
    goal="Log all query details, timestamps, and predictions for auditing",
    backstory="Maintains observability and logging pipeline for insights",
    allow_delegation=False,
    verbose=False
)

followup_agent = Agent(
    role="Follow-up Recommender",
    goal="Suggest the most likely next set of questions based on the current query",
    backstory="Understands observability workflows and user intent chaining in infrastructure monitoring.",
    allow_delegation=False,
    verbose=True
)
