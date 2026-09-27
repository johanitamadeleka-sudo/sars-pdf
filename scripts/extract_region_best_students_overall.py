"""Extract 'Mwanza Best Students-Overall' (9pp) into region-best-students-overall/data.json.

Section-centric: 9 stacked top-10 tables (one per page). Region variant of the council
best-students-overall: adds S/NO. and COUNCIL columns.
Columns: S/NO. | COUNCIL | C/NO | SCHOOL NAME | CANDIDATE FULL NAME | SEX | AGGT
         | DIVISION | POS | DETAILED SUBJECTS
The DETAILED SUBJECTS free-text string is preserved exactly. Coordinate based (pymupdf).
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza Best Students-Overall.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-best-students-overall" / "data.json"

SNO_MAX = 42.0
COUNCIL_MAX = 92.2
CNO_MAX = 138.2
SCHOOL_MAX = 210.4
CAND_MAX = 325.1
SEX_MAX = 344.6
AGGT_MAX = 365.0
DIV_MAX = 385.4
POS_MAX = 405.8


def group_lines(words, y_tol=4.5):
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


def parse_band(words):
    row = {k: "" for k in ["sno", "council", "cno", "school", "candidate", "sex",
                            "aggt", "division", "position", "detailed"]}
    council_p, cno_p, school_p, cand_p, det_p = [], [], [], [], []
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if x0 < SNO_MAX:
            row["sno"] = txt
        elif x0 < COUNCIL_MAX:
            council_p.append((x0, txt))
        elif x0 < CNO_MAX:
            cno_p.append((x0, txt))
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif x0 < CAND_MAX:
            cand_p.append((x0, txt))
        elif cx < SEX_MAX:
            row["sex"] = txt
        elif cx < AGGT_MAX:
            row["aggt"] = txt
        elif cx < DIV_MAX:
            row["division"] = txt
        elif cx < POS_MAX:
            row["position"] = txt
        else:
            det_p.append((x0, txt))
    row["council"] = " ".join(t for _, t in sorted(council_p))
    row["cno"] = " ".join(t for _, t in sorted(cno_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["candidate"] = " ".join(t for _, t in sorted(cand_p))
    row["detailed"] = " ".join(t for _, t in sorted(det_p))
    return row


def section_title(words):
    lines = {}
    for w in words:
        y = round((w[1] + w[3]) / 2, 0)
        lines.setdefault(y, []).append(w)
    for y in sorted(lines):
        t = " ".join(x[4] for x in sorted(lines[y], key=lambda w: w[0]))
        if "BEST" in t and "STUDENT" in t and len(t) < 70:
            return t
    return ""


def main():
    doc = pymupdf.open(SRC)
    sections = []
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        title = section_title(words)
        # cluster words into row bands (a row's two text-lines sit ~2.5pt apart, rows
        # ~11.7pt apart), keep clusters that carry a leading S/NO digit below the header.
        clusters = group_lines(words, y_tol=4.5)
        rows = []
        for cy, band in clusters:
            if cy <= 151:
                continue
            has_sno = any(w[0] < SNO_MAX and w[4].isdigit() and len(w[4]) <= 2 for w in band)
            if has_sno:
                rows.append(parse_band(band))
        sections.append({"title": title, "rows": rows})

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": sections[0]["title"] if sections else "",
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for s in sections:
        blanks = sum(1 for r in s["rows"] if not r["candidate"])
        print(f"  [{s['title']}] rows={len(s['rows'])} blank_cand={blanks}")


if __name__ == "__main__":
    main()
