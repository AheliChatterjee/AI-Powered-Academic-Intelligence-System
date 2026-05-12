from collections import Counter

import re


MIN_TOPIC_LENGTH = 3


GENERIC_WORDS = {

    "system",
    "systems",
    "question",
    "answer",
    "paper",
    "write",
    "discuss",
    "explain",
    "marks",
    "section",
    "semester",

    "kiit",
    "sot",
    "spring",
    "end"
}


def normalize_topic(topic):

    topic = topic.lower().strip()

    topic = re.sub(
        r"\s+",
        " ",
        topic
    )

    return topic


def is_valid_topic(topic):

    words = topic.split()

    # -------------------------
    # SHORT TOPIC FILTER
    # -------------------------

    if len(topic) < MIN_TOPIC_LENGTH:

        return False

    # -------------------------
    # GENERIC WORD FILTER
    # -------------------------

    if topic in GENERIC_WORDS:

        return False
    
    # -------------------------
    # REMOVE SINGLE GENERIC WORDS
    # -------------------------

    if len(words) == 1:

        if topic not in {

            "algorithm",
            "deadlock",
            "synchronization",
            "rpc",
            "lamport"
        }:

            return False

    # -------------------------
    # SINGLE CHARACTER FILTER
    # -------------------------

    if len(words) == 1 and len(words[0]) <= 2:

        return False

    return True


def stabilize_topics(extracted_topics):

    normalized_topics = []

    # -------------------------
    # NORMALIZATION
    # -------------------------

    for item in extracted_topics:

        topic = item["topic"]

        topic = normalize_topic(topic)

        if is_valid_topic(topic):

            normalized_topics.append(topic)

    # -------------------------
    # FREQUENCY COUNTING
    # -------------------------

    topic_counter = Counter(
        normalized_topics
    )

    stabilized_topics = []

    # -------------------------
    # SORT BY FREQUENCY
    # -------------------------

    for topic, freq in topic_counter.most_common():

        stabilized_topics.append(
            {
                "topic": topic.title(),

                "frequency": freq
            }
        )

    return stabilized_topics