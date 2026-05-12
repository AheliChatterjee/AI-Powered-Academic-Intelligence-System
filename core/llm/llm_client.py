import os

from dotenv import load_dotenv

from groq import Groq


# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# -----------------------------------
# INITIALIZE CLIENT
# -----------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


# -----------------------------------
# GENERATE RESPONSE
# -----------------------------------

def generate_response(prompt):

    completion = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """

You are an AI-powered academic assistant.

Your responsibilities:
- explain concepts clearly
- summarize academic content
- answer educational questions
- provide structured responses
- remain concise and accurate
- don't give answer which is not related to academics
STRICT RULES:
- Answer ONLY using the uploaded documents.
- If the answer is not present in the documents, say:
  'The uploaded documents do not contain information about this.'
- Do NOT use outside knowledge.
- Do NOT hallucinate.
- Prefer grounded academic answers only.
"""
            },

            {
                "role": "user",

                "content": prompt
            }
        ],

        temperature=0.3
    )

    response = completion.choices[
        0
    ].message.content

    return response