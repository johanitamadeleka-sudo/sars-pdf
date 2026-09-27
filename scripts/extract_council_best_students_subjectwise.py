"""Extract MWANZA CC 10 BEST STUDENTS SUBJECTWISE into data.json (display strings).

Section-centric: one top-10 table per subject (20 subjects on pages 1-20), followed by
10 trailing blank pages (21-30) reproduced for exact page count. Columns:
  S/NO. | ID NO. | SCHOOL | CATEGORY | CANDIDATE FULL NAME | SEX | MARKS | GRADE | POSITION
  | COMPETENCY LEVEL
Header per section 'TOP TEN BEST STUDENTS IN <SUBJECT> SUBJECT DISTRICTWISE'.
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC 10 BEST STUDENTS SUBJECTWISE.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-best-students-subjectwise" / "data.json"

SN_MAX = 86.3
ID_MAX = 153.3
SCHOOL_MAX = 247.5
CAT_MAX = 318.3
CAND_MAX = 491.7
SEX_C, MARKS_C, GRADE_C, POS_C = 504.3, 535.0, 570.9, 606.7
COMP_MIN = 624.6


def group_lines(words, y_tol=3.0):
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w)
            cy = y if cy is None else cy
        else:
            lines.append((cy, cur))
            cur, cy = [w], y
    if cur:
        lines.append((cy, cur))
    return lines


def nearest(cx, centers):
    return min(centers, key=lambda kc: abs(cx - kc[0]))[1]


def parse_row(line):
    row = {k: "" for k in ["sn", "id", "school", "category", "candidate", "sex",
                            "marks", "grade", "position", "competency"]}
    id_p, school_p, cat_p, cand_p, comp_p = [], [], [], [], []
    centers = [(SEX_C, "sex"), (MARKS_C, "marks"), (GRADE_C, "grade"), (POS_C, "position")]
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if x0 < SN_MAX:
            row["sn"] = txt
        elif x0 < ID_MAX:
            id_p.append((x0, txt))
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif x0 < CAT_MAX:
            cat_p.append((x0, txt))
        elif x0 < CAND_MAX:
            cand_p.append((x0, txt))
        elif cx >= COMP_MIN:
            comp_p.append((x0, txt))
        else:
            row[nearest(cx, centers)] = txt
    row["id"] = " ".join(t for _, t in sorted(id_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["category"] = " ".join(t for _, t in sorted(cat_p))
    row["candidate"] = " ".join(t for _, t in sorted(cand_p))
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def main():
    doc = pymupdf.open(SRC)
    sections = []
    cur = None
    blank_pages = 0
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        if not words:
            blank_pages += 1
            continue
        for cy, line in group_lines(words):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            if "TOP TEN BEST STUDENTS IN" in text and "SUBJECT" in text:
                subj = text.split("IN", 1)[1].rsplit("SUBJECT", 1)[0].strip()
                cur = {"subject": subj, "rows": []}
                sections.append(cur)
                continue
            if cur is None:
                continue
            first = line[0]
            if first[0] < SN_MAX and first[4].isdigit() and len(first[4]) <= 2 \
                    and len(line) > 4:
                cur["rows"].append(parse_row(line))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC BEST STUDENTS SUBJECTWISE",
        "trailing_blank_pages": blank_pages,
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"sections={len(sections)} blank_pages={blank_pages} -> {OUT}")
    for s in sections:
        print(f"  rows={len(s['rows']):>2}  {s['subject']}")


if __name__ == "__main__":
    main()
