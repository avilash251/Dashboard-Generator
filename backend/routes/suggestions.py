from fastapi import APIRouter

router = APIRouter()

# Static suggestions to assist in search autocompletion
PREDEFINED_SUGGESTIONS = [
    "CPU usage for server1",
    "Memory usage trends for node1",
    "Disk IO stats for cluster",
    "Kubernetes namespace status",
    "Top pods by CPU consumption",
    "Network traffic comparison across nodes",
    "Errors logged today",
    "Overall health of OCP cluster"
]

@router.get("/suggestions")
def get_suggestions():
    return {"suggestions": PREDEFINED_SUGGESTIONS}
