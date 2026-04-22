from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os


def create_or_load_index(docs, path):
    embeddings = OpenAIEmbeddings()

    if os.path.exists(path) and os.listdir(path):
        print("Loading existing FAISS index...")
        return FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    print("⚡ Creating new FAISS index...")

    vectorstore = FAISS.from_documents(docs, embeddings)

    os.makedirs(path, exist_ok=True)
    vectorstore.save_local(path)

    return vectorstore


def get_retriever(vectorstore, k=5):
    return vectorstore.as_retriever(
        search_kwargs={"k": k}
    )
