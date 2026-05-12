from core.segmentation.question_segmenter import (
    segment_questions
)

from core.topic_detection.dynamic_topic_extractor import (
    extract_dynamic_topics
)

from core.topic_detection.topic_stabilizer import (
    stabilize_topics
)

from core.topic_detection.topic_clusterer import (
    cluster_topics
)


def generate_intelligent_chunks(document):

    chunks = []

    # -----------------------------------
    # SEGMENT QUESTIONS
    # -----------------------------------

    questions = segment_questions(document)

    # -----------------------------------
    # PROCESS EACH QUESTION
    # -----------------------------------

    for question in questions:

        question_text = question[
            "question_text"
        ]

        # -----------------------------------
        # EXTRACT TOPICS
        # -----------------------------------

        raw_topics = extract_dynamic_topics(
            [question_text]
        )

        stable_topics = stabilize_topics(
            raw_topics
        )

        clustered_topics = cluster_topics(
            stable_topics
        )

        # -----------------------------------
        # BUILD CHUNK
        # -----------------------------------

        chunk = {

            "chunk_text": question_text,

            "chunk_type": "question",

            "question_number": question.get(
                "question_number"
            ),

            "marks": question.get(
                "marks"
            ),

            "source_document": document.get(
                "source_document"
            ),

            "page": document.get(
                "page"
            ),

            "topics": stable_topics,

            "topic_clusters": clustered_topics[
                "clusters"
            ]
        }

        chunks.append(chunk)

    return chunks