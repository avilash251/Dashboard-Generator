
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

KNOWLEDGE_PATH = "./rag/promql_knowledge.txt"
INDEX_PATH = "./rag/faiss_index"

def build_faiss_index():
    if not os.path.exists(KNOWLEDGE_PATH):
        raise FileNotFoundError(f"{KNOWLEDGE_PATH} does not exist")

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    texts = CharacterTextSplitter(chunk_size=300, chunk_overlap=20).split_text(raw_text)
    docs = [Document(page_content=t) for t in texts]

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(INDEX_PATH)
    print(f"✅ FAISS index saved to {INDEX_PATH}")

if __name__ == "__main__":
    build_faiss_index()
