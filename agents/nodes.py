import os
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from agents.prompts import *

from app.config import MAX_RETRIES

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key-just-for-drawing-the-graph"



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def rewrite(state):
    q = state["question"]

    new_q = llm.invoke(REWRITE_PROMPT.format(question=q))

    return {
        "question": new_q.content.strip(),
        "messages": state.get("messages", []) + [HumanMessage(content=q)],
        "retry_count": state.get("retry_count", 0) + 1
    }
    
    
# Decide Retrieval
def decide_retrieve(state):
    result = llm.invoke(
        RETRIEVE_DECISION_PROMPT.format(question=state["question"])
    )

    return {
        "use_retrieval": "yes" in result.content.lower()
    }


def retrieve(state, retriever):
    k = 3 if len(state["question"]) < 50 else 6
    docs = retriever.invoke(state["question"], k=k)

    return {"documents": docs}



def filter_documents(state):
    docs = state["documents"]

    combined = "\n\n".join([d.page_content for d in docs])

    filtered = llm.invoke(
        DOC_FILTER_PROMPT.format(
            question=state["question"],
            documents=combined
        )
    )

    return {
        "documents": [Document(page_content=filtered.content)]
    }


def generate(state):
    messages = state.get("messages", [])
    
    if state.get("use_retrieval") and state.get("documents"):
        docs = state.get("documents",[])
        context = "\n\n".join([d.page_content for d in docs])
        
        messages = messages+[
            HumanMessage(
                content=ANSWER_PROMPT.format(
                    context=context[:3000],
                    question=state["question"]
                )
            )
        ] 
        
    # normal massage chat with out retrival    
    else :
        messages = messages + [
            HumanMessage(content=state["question"])
        ]

    answer = llm.invoke(messages)

    return {
        "generation": answer.content,
        "messages": messages + [AIMessage(content=answer.content)]
    }


def evaluate(state):
    messages = state.get("messages", [])

    messages = messages + [
        HumanMessage(
            content=EVAL_PROMPT.format(
                question=state["question"],
                answer=state["generation"]
            )
        )
    ]

    result = llm.invoke(messages)

    return {
        "valid": "yes" in result.content.lower(),
        "messages": messages
    }
    
    
    
# ============================ Routing Logic =========================================================


def route_after_decision(state):
    return "retrieve" if state["use_retrieval"] else "generate"

def route_after_generate(state):
    if state.get("use_retrieval"):
        return "evaluate"
    return "end"


def route_after_eval(state):
    if state["valid"]:
        return "end"

    if state["retry_count"] >= MAX_RETRIES:
        return "end"

    return "rewrite"