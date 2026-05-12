import re

from core.topic_detection.topic_dictionary import (
    TOPIC_KEYWORDS
)


def detect_topics(question_text):

    detected_topics = []

    cleaned_text = question_text.lower()

    cleaned_text = re.sub(
        r"\s+",
        " ",
        cleaned_text
    )

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in cleaned_text:

                detected_topics.append(topic)

                break

    return list(set(detected_topics))