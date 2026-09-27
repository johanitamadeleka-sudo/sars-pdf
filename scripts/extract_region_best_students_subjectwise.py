"""Extract 'Mwanza Best students-Subjectwise' (23pp) into
region-best-students-subjectwise/data.json.

Section-centric: 23 stacked top-10-per-subject tables (one section per page). Region
variant of the council best-students-subjectwise: adds a COUNCIL column.
Columns: S/NO. | COUNCIL | SCHOOL | CATEGORY | CANDIDATE FULL NAME | SEX | MARKS | GRADE
         | POSITION | COMPETENCY LEVEL
The single-letter GRADE drives the competency-level background (via grading.py in render).
Coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza Best students-Subjectwise.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-best-students-subjectwise" / "data.json"

SNO_MAX = 84.8
COUNCIL_MAX = 155.5
SCHOOL_MAX = 244.6
CAT_MAX = 322.3
CAND_MAX = 488.5
SEX_MAX = 512.5
MARKS_MAX = 547.1
GRADE_MAX = 581.3
POS_MAX = 615.5


def group_lines(words, y_tol=4.0):
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w)
            cy = y if cy is None else (cy * (len(cur) - 1) + y) / len(cur)
        else:
            lines.append((cy, cur))
            cur, cy = [w], y
    if cur:
        lines.append((cy, cur))
    return lines


def parse_row(words):
    row = {k: "" for k in ["sno", "council", "school", "category", "candidate", "sex",
                            "marks", "grade", "position", "competency"]}
    council_p, school_p, cat_p, cand_p, comp_p = [], [], [], [], []
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if x0 < SNO_MAX:
            row["sno"] = txt
        elif x0 < COUNCIL_MAX:
            council_p.append((x0, txt))
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif x0 < CAT_MAX:
            cat_p.append((x0, txt))
        elif x0 < CAND_MAX:
            cand_p.append((x0, txt))
        elif cx < SEX_MAX:
            row["sex"] = txt
        elif cx < MARKS_MAX:
            row["marks"] = txt
        elif cx < GRADE_MAX:
            row["grade"] = txt
        elif cx < POS_MAX:
            row["position"] = txt
        else:
            comp_p.append((x0, txt))
    row["council"] = " ".join(t for _, t in sorted(council_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["category"] = " ".join(t for _, t in sorted(cat_p))
    row["candidate"] = " ".join(t for _, t in sorted(cand_p))
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def section_title(words):
    lines = {}
    for w in words:
        y = round((w[1] + w[3]) / 2, 0)
        lines.setdefault(y, []).append(w)
    for y in sorted(lines):
        t = " ".join(x[4] for x in sorted(lines[y], key=lambda w: w[0]))
        if "BEST STUDENTS IN" in t:
            return t
    return ""


def main():
    doc = pymupdf.open(SRC)
    sections = []
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        title = section_title(words)
        rows = []
        for cy, band in group_lines(words):
            if cy <= 184:
                continue
            first = min(band, key=lambda w: w[0])
            if first[0] < SNO_MAX and first[4].isdigit() and len(first[4]) <= 2:
                rows.append(parse_row(band))
        sections.append({"title": title, "rows": rows})

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "",
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"sections={len(sections)}")
    for s in sections:
        blanks = sum(1 for r in s["rows"] if not r["candidate"])
        print(f"  rows={len(s['rows'])} blank={blanks}  [{s['title'][:55]}]")


if __name__ == "__main__":
    main()
