from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=500,  
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
