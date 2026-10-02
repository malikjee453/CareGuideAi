"""Lightweight structure detection for healthcare documents."""

import re
from collections import Counter


def process_document(text: str) -> dict:
    clean = text.strip()
    lines = [line.strip() for line in clean.splitlines() if line.strip()]

    headings = []
    for line in lines:
        if len(line) <= 80 and (
            line.isupper()
            or line.endswith(":")
            or re.match(r"^(patient|patient name|date|diagnosis|impression|findings|results|medications|prescription|history|assessment|plan)\b", line, re.I)
        ):
            headings.append(line.rstrip(":"))

    # Surface lines that look like measured results without interpreting them.
    value_pattern = re.compile(r"\b[A-Za-z][A-Za-z /-]{1,30}\s*[:=]\s*[-+]?\d+(?:\.\d+)?\s*(?:[A-Za-z%µμ/.-]+)?\b")
    extracted_values = [line for line in lines if value_pattern.search(line)]

    word_count = len(re.findall(r"\b\w+\b", clean))
    return {
        "text": clean,
        "sections": headings[:30],
        "possible_measurement_lines": extracted_values[:50],
        "page_markers": [line for line in lines if line.startswith("[Page ")][:100],
        "word_count": word_count,
    }
