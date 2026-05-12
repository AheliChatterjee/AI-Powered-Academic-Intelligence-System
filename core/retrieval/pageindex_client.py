import os
import time

from dotenv import load_dotenv

from pageindex import PageIndexClient


# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()


API_KEY = os.getenv(
    "PAGEINDEX_API_KEY"
)


# -----------------------------------
# INITIALIZE CLIENT
# -----------------------------------

pi_client = PageIndexClient(
    api_key=API_KEY
)


# -----------------------------------
# UPLOAD DOCUMENT
# -----------------------------------

def upload_document(file_path):

    result = pi_client.submit_document(
        file_path
    )

    doc_id = result["doc_id"]

    return doc_id


# -----------------------------------
# WAIT FOR PROCESSING
# -----------------------------------

def wait_for_processing(doc_id):

    while True:

        document = pi_client.get_document(
            doc_id
        )

        status = document["status"]

        print(f"Processing Status: {status}")

        if status == "completed":

            return document

        elif status == "failed":

            raise Exception(
                "PageIndex processing failed."
            )

        time.sleep(5)


# -----------------------------------
# ASK QUESTION
# -----------------------------------

def ask_document_question(
    doc_id,
    question
):

    grounded_prompt = f"""

You are an academic document assistant.

STRICT RULES:
- Answer ONLY using the uploaded documents.
- If the answer is not present in the documents, say:
  'The uploaded documents do not contain information about this.'
- Do NOT use outside knowledge.
- Do NOT hallucinate.
- Prefer grounded academic answers only.

USER QUESTION:
{question}

"""

    response = pi_client.chat_completions(

        messages=[

            {
                "role": "user",

                "content": grounded_prompt
            }
        ],

        doc_id=doc_id,

        enable_citations=True
    )

    answer = response[
        "choices"
    ][0]["message"]["content"]

    return answer