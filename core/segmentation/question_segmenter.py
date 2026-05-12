import re

from core.preprocessing.text_cleaner import (
    clean_exam_text
)


def segment_questions(document):

    raw_text = document["text"]

    text = clean_exam_text(raw_text)

    segmented_questions = []

    # -------------------------
    # NORMALIZE SPACES
    # -------------------------

    text = re.sub(r"\s+", " ", text)

    # -------------------------
    # QUESTION START DETECTION
    # -------------------------

    question_pattern = r"(?=(\d+\s*\[.*?\]))"

    matches = list(
        re.finditer(question_pattern, text)
    )

    for i in range(len(matches)):

        start = matches[i].start()

        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(text)
        )

        question_block = text[start:end].strip()

        # -------------------------
        # QUESTION NUMBER
        # -------------------------

        number_match = re.match(
            r"(\d+)",
            question_block
        )

        question_number = None

        if number_match:

            question_number = number_match.group(1)

        # -------------------------
        # MARKS
        # -------------------------

        marks_match = re.search(
            r"\[(.*?)\]",
            question_block
        )

        marks = None

        if marks_match:

            marks = marks_match.group(1)

        # -------------------------
        # SECTION
        # -------------------------

        section_match = re.search(
            r"(SECTION[-\s][A-Z])",
            text,
            re.IGNORECASE
        )

        section = None

        if section_match:

            section = section_match.group(1)

        segmented_questions.append(
            {
                "question_number": question_number,

                "question_text": question_block,

                "marks": marks,

                "section": section,

                "source_document": document[
                    "source_document"
                ],

                "page": document["page"],

                "extraction_method": document[
                    "extraction_method"
                ]
            }
        )

    return segmented_questions