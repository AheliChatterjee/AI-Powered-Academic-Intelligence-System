import re

from core.topic_detection.dynamic_topic_extractor import (
    extract_dynamic_topics
)

from core.topic_detection.topic_stabilizer import (
    stabilize_topics
)

from core.topic_detection.topic_clusterer import (
    cluster_topics
)


# -----------------------------------
# CONFIGURATION
# -----------------------------------

CHUNK_SIZE = 1200


# -----------------------------------
# SPLIT TEXT INTO PARAGRAPHS
# -----------------------------------

def split_into_paragraphs(text):

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )

    cleaned = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        # Remove tiny noisy blocks
        if len(paragraph) > 80:

            cleaned.append(paragraph)

    return cleaned


# -----------------------------------
# SPLIT LARGE PARAGRAPHS
# -----------------------------------

def split_large_paragraph(paragraph):

    chunks = []

    for i in range(
        0,
        len(paragraph),
        CHUNK_SIZE
    ):

        chunk = paragraph[
            i:i + CHUNK_SIZE
        ]

        chunks.append(chunk)

    return chunks



# -----------------------------------
# EXTRACT MARKS FROM TEXT
# -----------------------------------

def extract_marks(text):

    patterns = [

        r"\[(\d+)\]",

        r"\((\d+)\)",

        r"(\d+)\s*marks",

        r"(\d+)\s*Marks",

        r"(\d+)\s*M"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return int(
                match.group(1)
            )

    return 0

# -----------------------------------
# GENERATE SEMANTIC CHUNKS
# -----------------------------------

def generate_semantic_chunks(document):

    text = document["text"]

    # -----------------------------------
    # DOCUMENT LEVEL TOPIC EXTRACTION
    # -----------------------------------

    raw_topics = extract_dynamic_topics(
        [text]
    )

    stable_topics = stabilize_topics(
        raw_topics
    )

    clustered_topics = cluster_topics(
        stable_topics
    )

    # -----------------------------------
    # SPLIT INTO PARAGRAPHS
    # -----------------------------------

    paragraphs = split_into_paragraphs(
        text
    )

    semantic_chunks = []

    chunk_id = 1

    # -----------------------------------
    # PROCESS PARAGRAPHS
    # -----------------------------------

    for paragraph in paragraphs:

        # -----------------------------------
        # HANDLE LARGE PARAGRAPHS
        # -----------------------------------

        if len(paragraph) > CHUNK_SIZE:

            paragraph_chunks = split_large_paragraph(
                paragraph
            )

        else:

            paragraph_chunks = [paragraph]

        # -----------------------------------
        # CREATE CHUNK OBJECTS
        # -----------------------------------

        for chunk_text in paragraph_chunks:

            chunk = {

                "chunk_id": chunk_id,

                "chunk_text": chunk_text,

                "source_document": document[
                    "source_document"
                ],

                "page": document[
                    "page"
                ],

                "document_type": document.get(
                    "document_type",
                    "UNKNOWN"
                ),

                # -----------------------------------
                # DOCUMENT LEVEL SEMANTICS
                # -----------------------------------

                "topics": stable_topics,

                "topic_clusters":
                    clustered_topics["clusters"]
            }

            semantic_chunks.append(chunk)

            chunk_id += 1

    return semantic_chunks