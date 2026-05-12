import re


def parse_document_structure(text):

    structure = {
        "chapters": [],
        "sections": [],
        "questions": []
    }

    # -------------------------
    # CHAPTER DETECTION
    # -------------------------

    chapter_patterns = re.findall(
        r"(chapter\s+\d+[:\-\s]*[A-Za-z ]+)",
        text,
        re.IGNORECASE
    )

    uppercase_headings = re.findall(
        r"\b([A-Z][A-Z\s]{8,})\b",
        text
    )

# Remove short uppercase noise
    uppercase_headings = [
        heading.strip()
        for heading in uppercase_headings
        if len(heading.split()) >= 2
    ]

    structure["chapters"].extend(chapter_patterns)
    structure["chapters"].extend(uppercase_headings)

    # -------------------------
    # SECTION DETECTION
    # -------------------------

    section_patterns = re.findall(
        r"(\d+\.\d+\s+[A-Za-z][A-Za-z\s]+)",
        text
    )

    numbered_headings = re.findall(
        r"(\d+\s+[A-Z][A-Za-z\s]+)",
        text
    )

    structure["sections"].extend(section_patterns)
    structure["sections"].extend(numbered_headings)

    # -------------------------
    # QUESTION DETECTION
    # -------------------------

    question_patterns = re.findall(
        r"(Q\.?\s?\d+.*?[\?\n])",
        text,
        re.IGNORECASE
    )

    # Detect WH-type academic questions
    wh_questions = re.findall(
        r"((What|Explain|Define|Discuss|Describe|Compare)[^.?\n]*\?)",
        text,
        re.IGNORECASE
    )

    extracted_wh_questions = [q[0] for q in wh_questions]

    structure["questions"].extend(question_patterns)
    structure["questions"].extend(extracted_wh_questions)

    # -------------------------
    # REMOVE DUPLICATES
    # -------------------------

    structure["chapters"] = list(set(structure["chapters"]))
    structure["sections"] = list(set(structure["sections"]))
    structure["questions"] = list(set(structure["questions"]))

    return structure