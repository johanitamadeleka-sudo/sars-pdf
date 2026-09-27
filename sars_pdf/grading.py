"""Competency-level rules. The competency level is the ONLY data-driven colour in the report."""

import re

# GPA upper bounds (exclusive) -> competency level. Derived from, and consistent with,
# every row of the August 2026 reference PDF (e.g. 1.5806 -> A, 1.6133 -> B,
# 2.5909 -> B, 2.6257 -> C, 3.5938 -> C, 3.6000 -> D, 4.5500 -> D, 4.6259 -> F).
GPA_BANDS = [
    (1.6, "A", "Grade A (Excellent)"),
    (2.6, "B", "Grade B (Very Good)"),
    (3.6, "C", "Grade C (Good)"),
    (4.6, "D", "Grade D (Satisfactory)"),
    (float("inf"), "F", "Grade F (Fail)"),
]

_LEVEL_RE = re.compile(r"Grade\s+([A-F])\b")


def competency_from_gpa(gpa):
    """Return (letter, label) for a GPA value."""
    g = float(gpa)
    for upper, letter, label in GPA_BANDS:
        if g < upper:
            return letter, label
    raise ValueError(gpa)


def competency_letter(competency=None, gpa=None):
    """Letter (A-F) that selects the competency background colour.

    Uses the label text if present, otherwise derives it from the GPA.
    Returns None for empty rows (no colour).
    """
    if competency:
        m = _LEVEL_RE.search(competency)
        if m:
            return m.group(1)
    if gpa not in (None, ""):
        return competency_from_gpa(gpa)[0]
    return None
