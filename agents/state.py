from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[Document]
    use_retrieval: bool
    retry_count: int
    valid: bool
