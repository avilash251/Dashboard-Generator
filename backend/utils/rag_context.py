# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# import os

# def retrieve_context(query: str, k: int = 3) -> str:
#     index_path = "backend/rag/faiss_index"
#     if not os.path.exists(index_path):
#         print("⚠️ RAG index not found, skipping context injection.")
#         return ""

#     try:
#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         db = FAISS.load_local(index_path, embeddings)
#         docs = db.similarity_search(query, k=k)
#         return "\n".join([doc.page_content for doc in docs])
#     except Exception as e:
#         print(f"❌ Error loading RAG context: {e}")
#         return ""


# backend/utils/rag_context.py

from rapidfuzz import fuzz

# 🔍 Define static keyword-to-context mapping
CONTEXT_MAP = {
    "cpu": "CPU metrics can be collected using node_exporter or cAdvisor. PromQL: rate(node_cpu_seconds_total[5m])",
    "memory": "Memory usage often comes from node_memory_MemAvailable_bytes or container_memory_usage_bytes.",
    "disk": "Disk usage and I/O can be collected from node_disk_bytes_read, node_disk_io_time_seconds_total.",
    "uptime": "Uptime is tracked using node_time_seconds - node_boot_time_seconds.",
    "latency": "Use histogram_quantile for P95/P99 latency across APIs.",
    "errors": "HTTP error rates can be found using rate(http_requests_total{status=~\"5..\"}[5m])"
}

def retrieve_context(prompt: str, threshold: int = 70) -> str:
    prompt = prompt.lower()
    scores = {
        keyword: fuzz.partial_ratio(prompt, keyword) for keyword in CONTEXT_MAP
    }

    best_match = max(scores, key=scores.get)
    if scores[best_match] >= threshold:
        return CONTEXT_MAP[best_match]

    return "This system supports Prometheus queries across CPU, memory, disk, network, and uptime metrics."

