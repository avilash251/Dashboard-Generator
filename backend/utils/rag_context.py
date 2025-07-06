from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

def retrieve_context(query: str, k: int = 3) -> str:
    index_path = "backend/rag/faiss_index"
    if not os.path.exists(index_path):
        print("⚠️ RAG index not found, skipping context injection.")
        return ""

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(index_path, embeddings)
        docs = db.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"❌ Error loading RAG context: {e}")
        return ""
