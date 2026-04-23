from langgraph.graph import StateGraph, END
from agents.state import GraphState
from langgraph.checkpoint.memory import MemorySaver

from agents.nodes import *

import os


def build_graph(retriever):
    workflow = StateGraph(GraphState)

    workflow.add_node("rewrite", rewrite)
    workflow.add_node("decide", decide_retrieve)
    workflow.add_node("retrieve", lambda s: retrieve(s, retriever))
    workflow.add_node("filter", filter_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("evaluate", evaluate)

    workflow.set_entry_point("rewrite")

    workflow.add_edge("rewrite", "decide")

    workflow.add_conditional_edges(
        "decide",
        route_after_decision,
        {
            "retrieve": "retrieve",
            "generate": "generate"
        }
    )

    workflow.add_edge("retrieve", "filter")
    workflow.add_edge("filter", "generate")
    
    workflow.add_conditional_edges(
        "generate",
        route_after_generate,
        {
            "evaluate": "evaluate",
            "end": END
        }
    )



    workflow.add_conditional_edges(
        "evaluate",
        route_after_eval,
        {
            "rewrite": "rewrite",
            "end": END
        }
    )
    memory = MemorySaver()
    
    app = workflow.compile(checkpointer=memory)
    return app

if __name__ == "__main__":
    # Mock retriever for testing the build
    mock_retriever = {} 
    app = build_graph(mock_retriever)

    # 1. Print the raw Mermaid code (to copy-paste into mermaid.live)
    print("--- Raw Mermaid Code ---")
    print(app.get_graph().draw_mermaid())
    print("------------------------\n")

    # 2. Save it directly as a PNG image in your project folder
    try:
        image_bytes = app.get_graph().draw_mermaid_png()
        with open("self_rag_architecture.png", "wb") as f:
            f.write(image_bytes)
        print("✅ Graph successfully saved as 'self_rag_architecture.png'")
    except Exception as e:
        print(f"⚠️ Could not generate PNG. Make sure you have the required rendering dependencies installed. Error: {e}")