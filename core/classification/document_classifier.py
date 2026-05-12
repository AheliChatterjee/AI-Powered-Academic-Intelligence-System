import re


def classify_document(text):

    text_lower = text.lower()

    pyq_score = 0
    book_score = 0
    notes_score = 0

    # -------------------------
    # PYQ SIGNALS
    # -------------------------

    year_patterns = re.findall(r"\b(20\d{2})\b", text)

    question_patterns = re.findall(
        r"(q\.?\s?\d+|question\s+\d+)",
        text_lower
    )

    marks_patterns = re.findall(
        r"(\d+\s*marks?)",
        text_lower
    )

    pyq_keywords = [
        "previous year",
        "university question",
        "mid sem",
        "end sem",
        "semester exam"
    ]

    for keyword in pyq_keywords:
        if keyword in text_lower:
            pyq_score += 5

    pyq_score += len(year_patterns) * 3
    pyq_score += len(question_patterns) * 4
    pyq_score += len(marks_patterns) * 3

    # -------------------------
    # BOOK SIGNALS
    # -------------------------

    chapter_patterns = re.findall(
        r"(chapter\s+\d+)",
        text_lower
    )

    section_patterns = re.findall(
        r"(\d+\.\d+)",
        text_lower
    )

    academic_keywords = [
        "introduction",
        "conclusion",
        "definition",
        "example",
        "figure",
        "table"
    ]

    for keyword in academic_keywords:
        if keyword in text_lower:
            book_score += 2

    book_score += len(chapter_patterns) * 5
    book_score += len(section_patterns) * 2

    # -------------------------
    # NOTES SIGNALS
    # -------------------------

    bullet_patterns = re.findall(
        r"(•|- |\*)",
        text
    )

    short_line_patterns = re.findall(
        r"([A-Za-z ]{3,40}:)",
        text
    )

    notes_score += len(bullet_patterns) * 2
    notes_score += len(short_line_patterns)

    # -------------------------
    # FALLBACK HANDLING
    # -------------------------

    scores = {
        "PYQ": pyq_score,
        "BOOK": book_score,
        "NOTES": notes_score
    }

    max_score = max(scores.values())

    if max_score == 0:
        predicted_type = "UNKNOWN"
    else:
        predicted_type = max(scores, key=scores.get)

    return {
        "document_type": predicted_type,
        "scores": scores
    }