import re


def extract_subquestions(question_text):

    subquestions = []

    # -------------------------
    # SUBQUESTION PATTERNS
    # -------------------------

    patterns = [
        r"([a-zA-Z]\))",
        r"([ivxIVX]+\.)"
    ]

    combined_pattern = "|".join(patterns)

    splits = re.split(
        combined_pattern,
        question_text
    )

    current_label = None

    for item in splits:

        if not item:
            continue

        item = item.strip()

        # -------------------------
        # LABEL DETECTION
        # -------------------------

        if re.fullmatch(r"[a-zA-Z]\)", item):

            current_label = item

            continue

        if re.fullmatch(r"[ivxIVX]+\.", item):

            current_label = item

            continue

        # -------------------------
        # CONTENT
        # -------------------------

        if current_label:

            subquestions.append(
                {
                    "label": current_label,
                    "text": item
                }
            )

    return subquestions