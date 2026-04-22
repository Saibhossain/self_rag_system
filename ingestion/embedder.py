from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import sys
import os
# Add the parent directory (Self_Rag) to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def create_or_load_index(docs, path):
    embeddings = OpenAIEmbeddings()

    os.makedirs(path, exist_ok=True)
    index_file = os.path.join(path, "index.faiss")
    print("🔥 NEW VECTORSTORE CODE LOADED")

    if os.path.exists(index_file):
        print("📦 Loading existing FAISS index...")
        return FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    print("⚡ Creating new FAISS index...")

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(path)

    return vectorstore

def get_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 15
        }
    )