#============================ rewrite user prompt ===================
REWRITE_PROMPT = """
Rewrite the question only to improve clarity, grammar, or spelling.
Do NOT add new information, sub-questions, or change the meaning.

Question: {question}
"""

#============================ retrieve decision yes or no ===============

RETRIEVE_DECISION_PROMPT = """
Decide if external documents are REQUIRED to answer the question.

Rules:
- Answer "no" if the question is general knowledge.
- Answer "no" if a basic definition is enough.
- Answer "yes" only if:
  - the answer depends on specific documents
  - OR requires private, local, or up-to-date data

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
