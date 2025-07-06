from crewai import Crew, Agent, Task
from utils.rag_context import retrieve_context
from utils.gemini_wrapper import ask_gemini

PlannerAgent = Agent("Planner", "Understand and decompose user prompt", "Observability expert", verbose=True)
RetrieverAgent = Agent("Retriever", "Get related metric context", "RAG-enhanced retriever", tools=[retrieve_context])
PromQLAgent = Agent("PromQLAgent", "Convert prompt to PromQL", "PromQL builder", tools=[ask_gemini])
LayoutAgent = Agent("LayoutAgent", "Build dashboard layout", "UI layout creator", tools=[ask_gemini])

crew_task = Task("Generate PromQL + layout JSON", expected_output="dashboard spec", agent=PlannerAgent)

DashboardCrew = Crew([PlannerAgent, RetrieverAgent, PromQLAgent, LayoutAgent], [crew_task], verbose=True)

def build_dashboard_with_agents(prompt: str):
    return DashboardCrew.run(prompt)
