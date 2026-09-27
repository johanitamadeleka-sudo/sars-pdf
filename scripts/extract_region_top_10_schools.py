"""Extract 'Mwanza Top 10 Schools' (6pp) into region-top-10-schools/data.json.

Section-centric: 6 stacked top-10 division-performance sections, one per page:
  TOP 10 BEST SCHOOLS OVERALL / TOP 10 BEST GOVERNMENT SCHOOLS / TOP 10 BEST PRIVATE
  SCHOOLS / TEN LOOSER SCHOOLS OVERALL / TEN LOOSER GOVERNMENT SCHOOLS /
  TEN LOOSER PRIVATE SCHOOLS.
Region variant of the council top-10 grid: adds a COUNCIL column, rank column is R/RANK.
Columns: S/NO. | COUNCIL | SCHOOL NAME | <29 numeric cells: NUMBER OF CANDIDATES +
DIVISION PERFORMANCE + GPA> | COMPETENCY LEVEL | R/RANK.

The 29 numeric cells are placed positionally (nearest measured column centre), so no
value is hand-typed. Coordinate based (pymupdf words).
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza Top 10 Schools.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-top-10-schools" / "data.json"

BOUNDS = [138.7, 155.8, 172.8, 189.8, 206.6, 223.9, 241.0, 258.0, 275.0, 292.1, 307.9,
          322.8, 337.7, 352.6, 372.0, 391.3, 410.4, 427.9, 445.2, 462.5, 479.5, 499.2,
          518.6, 538.1, 557.2, 576.8, 597.6, 617.0, 636.4, 667.2]
NUM_CENTERS = [(BOUNDS[i] + BOUNDS[i + 1]) / 2 for i in range(len(BOUNDS) - 1)]  # 29
NUM_KEYS = [f"n{i}" for i in range(len(NUM_CENTERS))]

SN_MAX_X = 34.9
COUNCIL_MAX_X = 77.9
SCHOOL_MAX_X = 138.7
COMP_MIN_X = 667.2
RANK_MIN_X = 738.8

TITLES = {}  # discovered per page


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_KEYS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


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


def parse_row(line):
    row = {k: "" for k in ["sn", "council", "school", *NUM_KEYS, "competency", "rank"]}
    council_p, school_p, comp_p = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < COUNCIL_MAX_X:
            council_p.append((x0, txt))
        elif x0 < SCHOOL_MAX_X:
            school_p.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif x0 >= COMP_MIN_X:
            comp_p.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def find_title(words):
    lines = group_lines(words)
    for cy, line in lines:
        t = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
        if ("TOP 10" in t or "TEN LOOSER" in t) and "SCHOOL" in t:
            return t
    return ""


def main():
    doc = pymupdf.open(SRC)
    sections = []
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        title = find_title(words)
        rows = []
        for cy, line in group_lines(words):
            line = sorted(line, key=lambda w: w[0])
            first = line[0]
            if first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) == 2 \
                    and len(line) > 15 and cy > 108:
                rows.append(parse_row(line))
        sections.append({"title": title, "rows": rows})

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "TOP 10 BEST SCHOOLS OVERALL",
        "num_count": len(NUM_KEYS),
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for s in sections:
        empt = sum(1 for r in s["rows"] for k in NUM_KEYS if r[k] == "")
        print(f"  [{s['title']}] rows={len(s['rows'])} empty={empt}")


if __name__ == "__main__":
    main()
