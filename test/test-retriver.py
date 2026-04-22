import sys
import os
from dotenv import load_dotenv

# This forces Python to look in your main Self_Rag folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ingestion.embedder import get_retriever, create_or_load_index

load_dotenv()

def test_retrieval():
    index_path = "index/faiss_index"
    
    if not os.path.exists(os.path.join(index_path, "index.faiss")):
        print("❌ Error: FAISS index not found! Please run your ingestion script first.")
        return

    print("🔍 Initializing Retriever Test...")
    
    vectorstore = create_or_load_index([], index_path)
    retriever = get_retriever(vectorstore)

    test_query = "find মানুষের পথপ্রদর্শক in the documents ?"
    
    print(f"\n❓ Query: '{test_query}'\n")
    print("⏳ Searching FAISS index using MMR...\n")
    
    retrieved_docs = retriever.invoke(test_query)

    if not retrieved_docs:
        print("⚠️ No documents retrieved. Your index might be empty.")
        return

    print(f"✅ Retrieved {len(retrieved_docs)} documents:\n")
    
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"--- 📄 Result {i} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown source')}")
        print(f"Content: {doc.page_content[:300]}...\n")

if __name__ == "__main__":
    test_retrieval()