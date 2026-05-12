import re


ACADEMIC_STOPWORDS = {

    # GENERAL
    "question",
    "answer",
    "section",
    "marks",
    "attempt",
    "semester",
    "examination",
    "full",
    "time",
    "hours",
    "paper",
    "write",
    "discuss",
    "explain",

    # UNIVERSITY NOISE
    "kiit",
    "sot",
    "spring",
    "end",
    "semester",
    "examination",

    # OCR / GENERIC
    "figure",
    "required",
    "candidate",
    "candidates",
    "questions"
}


def clean_semantic_text(text):

    text = text.lower()

    # -------------------------
    # REMOVE SPECIAL CHARS
    # -------------------------

    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # -------------------------
    # REMOVE EXTRA SPACES
    # -------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    words = text.split()

    cleaned_words = []

    for word in words:

        if len(word) < 3:
            continue

        if word in ACADEMIC_STOPWORDS:
            continue

        cleaned_words.append(word)

    return " ".join(cleaned_words)