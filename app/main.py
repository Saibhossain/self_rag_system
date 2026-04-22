from fastapi import FastAPI
from pydantic import BaseModel
import os

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from agents.graph import build_graph
from utils.vectorstore import get_retriever
from ingestion.loader import load_documents
from ingestion.chunking import get_splitter
from utils.cleaning import deduplicate_docs
from utils.vectorstore import create_or_load_index

# ================= CONFIG =================
INDEX_PATH = "index/faiss_index"
DATA_PATH = "data"

app = FastAPI(title="Self-RAG API 🚀")


# ================= LOAD SYSTEM =================
def load_system():
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = get_retriever(vectorstore)
    rag_app = build_graph(retriever)

    return vectorstore, retriever, rag_app


vectorstore, retriever, rag_app = load_system()


# ================= SCHEMAS =================
class Query(BaseModel):
    question: str


# ================= ENDPOINTS =================

# ✅ 1. Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# ✅ 2. Ask (MAIN)
@app.post("/ask")
def ask(q: Query):
    result = rag_app.invoke({
        "question": q.question,
        "retry_count": 0
    })

    return {
        "answer": result.get("generation"),
        "valid": result.get("valid")
    }


# ✅ 3. Retrieval debug
@app.post("/retrieve")
def retrieve_debug(q: Query):
    docs = retriever.invoke(q.question)

    return {
        "count": len(docs),
        "docs": [
            {
                "content": d.page_content[:200],
                "metadata": d.metadata
            }
            for d in docs
        ]
    }


# ✅ 4. Document stats
@app.get("/documents")
def document_stats():
    return {
        "total_vectors": vectorstore.index.ntotal
    }


# ✅ 5. Reload index (rebuild)
@app.post("/reload-index")
def reload_index():
    global vectorstore, retriever, rag_app

    docs = load_documents(DATA_PATH)
    docs = deduplicate_docs(docs)

    splitter = get_splitter()
    splits = splitter.split_documents(docs)

    vectorstore = create_or_load_index(splits, INDEX_PATH)
    retriever = get_retriever(vectorstore)
    rag_app = build_graph(retriever)

    return {"status": "reloaded"}
