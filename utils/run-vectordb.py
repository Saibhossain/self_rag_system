from ingestion.loader import load_documents
from ingestion.chunking import get_splitter
from utils.cleaning import deduplicate_docs
from utils.vectorstore import create_or_load_index, get_retriever
from app.config import DATA_PATH, INDEX_PATH



# 🔹 Load
docs = load_documents(DATA_PATH)

# 🔹 Clean
docs = deduplicate_docs(docs)

# 🔹 Chunk
splitter = get_splitter()
splits = splitter.split_documents(docs)

print(f"Total chunks: {len(splits)}")

# 🔹 Index
vectorstore = create_or_load_index(splits, INDEX_PATH)

# 🔹 Retriever
retriever = get_retriever(vectorstore)
