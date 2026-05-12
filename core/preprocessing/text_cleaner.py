import re


def clean_text(text):

    # Remove excessive newlines
    text = re.sub(r"\n+", " ", text)

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    # Remove broken unicode spaces
    text = text.replace("\u00a0", " ")

    # Strip leading/trailing spaces
    text = text.strip()

    return text

import re


def clean_exam_text(text):

    # -------------------------
    # REMOVE EXTRA SPACES
    # -------------------------

    text = re.sub(r"\s+", " ", text)

    # -------------------------
    # REMOVE HEADER AREA
    # -------------------------

    header_patterns = [
        r"SPRING END SEMESTER EXAMINATION-\d+",
        r"Time:\s*\d+\s*Hours",
        r"Full Marks:\s*\d+",
        r"Candidates are required.*?only:",
        r"KIIT-DU.*?Examination-\d+",
        r"KIIT-DU.*",
        r"Page\s*\d+",
        r"Semester\s*B\.?Tech.*",
        r"DISTRIBUTED OPERATING SYSTEMS.*"
    ]

    for pattern in header_patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
                    )

    return text.strip()