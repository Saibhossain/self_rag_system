#============================ rewrite user prompt ===================
REWRITE_PROMPT = """
Rewrite the question to improve retrieval.

Question: {question}
"""

#============================ retrieve decision yes or no ===============

RETRIEVE_DECISION_PROMPT = """
Do we need external knowledge to answer this?

Question: {question}

Answer ONLY: yes or no
"""
#============================ filter only most relevent ===============

DOC_FILTER_PROMPT = """
Select only relevant information for answering.

Question: {question}

Documents:
{documents}

Return ONLY relevant parts.
"""
#============================

ANSWER_PROMPT = """
Answer the question using the context.

Context:
{context}

Question:
{question}
"""
#============================

EVAL_PROMPT = """
Evaluate the answer.

Question: {question}
Answer: {answer}

Is it:
1. grounded in facts?
2. useful?

Answer ONLY: yes or no
"""
