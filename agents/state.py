from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    question: str
    generation: str
    messages: List[BaseMessage] 
    documents: List[Document]
    use_retrieval: bool
    retry_count: int
    valid: bool
