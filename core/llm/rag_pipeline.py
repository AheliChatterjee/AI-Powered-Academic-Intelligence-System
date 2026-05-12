from core.retrieval.pageindex_client import (
    ask_document_question
)

from core.llm.llm_client import (
    generate_response
)


# -----------------------------------
# FINAL RAG PIPELINE
# -----------------------------------

def academic_rag_pipeline(

    doc_id,

    user_question
):

    # -----------------------------------
    # RETRIEVE GROUNDED CONTEXT
    # -----------------------------------

    retrieved_context = ask_document_question(

        doc_id,

        user_question
    )

    # -----------------------------------
    # BUILD FINAL LLM PROMPT
    # -----------------------------------

    final_prompt = f"""

You are an AI academic assistant.

Your task:
- answer the student's question
- use ONLY the retrieved academic context
- explain concepts clearly
- structure answers for exam preparation
- do NOT hallucinate
- if context is insufficient, clearly say so

-----------------------------------
RETRIEVED CONTEXT
-----------------------------------

{retrieved_context}

-----------------------------------
STUDENT QUESTION
-----------------------------------

{user_question}

-----------------------------------
FINAL ANSWER
-----------------------------------

"""

    # -----------------------------------
    # GENERATE FINAL RESPONSE
    # -----------------------------------

    final_response = generate_response(
        final_prompt
    )

    return final_response