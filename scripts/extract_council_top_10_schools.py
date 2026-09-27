"""Extract MWANZA CC 10 BEST SCHOOLS into data.json (display strings).

Section-centric: 6 stacked top-10 division-performance tables. Columns:
  S/NO. | SCHOOL NAME | REGISTERED(F M T) | SAT(F M T %)
  I(F M T) II(F M T) III(F M T) IV(F M T) 0(F M T %) I-III(F M T %) I-IV(F M T %)
  GPA | COMPETENCY | C/RANK
Each data row has, between SCHOOL NAME and GPA, exactly 31 numeric cells in fixed order,
then the GPA decimal, the competency label, then C/RANK. We read them positionally so no
column-centre guessing is needed. Extraction is coordinate based, never hand-typed.
"""

import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC 10 BEST SCHOOLS.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-top-10-schools" / "data.json"

SN_MAX = 34.9
SCHOOL_MAX = 92.9
CRANK_MIN = 746.0

# 31 numeric keys in order, then gpa handled separately.
NUM_KEYS = [
    "reg_f", "reg_m", "reg_t", "sat_f", "sat_m", "sat_t", "sat_pct",
    "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
    "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
    "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct",
]
GPA_RE = re.compile(r"^\d\.\d{3,5}$")


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
    row = {k: "" for k in ["sn", "school", *NUM_KEYS, "gpa", "competency", "crank"]}
    school_p, mid, comp_p = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if x0 < SN_MAX:
            row["sn"] = txt
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif cx >= CRANK_MIN:
            row["crank"] = txt
        else:
            mid.append((x0, txt))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    mid.sort()
    # split mid into: 31 numerics, gpa, competency-words
    nums, gpa, comp = [], "", []
    for x0, txt in mid:
        if not gpa and GPA_RE.match(txt):
            gpa = txt
        elif gpa:
            comp.append(txt)
        else:
            nums.append(txt)
    for k, v in zip(NUM_KEYS, nums):
        row[k] = v
    row["gpa"] = gpa
    row["competency"] = " ".join(comp)
    return row


def main():
    doc = pymupdf.open(SRC)
    sections = []
    cur = None
    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            up = text.upper()
            if ("TOP TEN" in up or "TEN LOOSER" in up) and "SCHOOL" in up \
                    and "S/NO" not in up and up != "MWANZA CC TOP TEN BEST SCHOOLS":
                title = text
                if title.upper().startswith("MWANZA CC "):
                    title = title[len("MWANZA CC "):]
                cur = {"title": title, "rows": []}
                sections.append(cur)
                continue
            if cur is None:
                continue
            first = line[0]
            if first[0] < SN_MAX and first[4].isdigit() and len(first[4]) <= 2 \
                    and len(line) > 10:
                cur["rows"].append(parse_row(line))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC TOP TEN BEST SCHOOLS",
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"sections={len(sections)} -> {OUT}")
    for s in sections:
        empt = sum(1 for r in s["rows"] for k in NUM_KEYS if r[k] == "")
        print(f"  rows={len(s['rows']):>2} empty_cells={empt}  {s['title']}")


if __name__ == "__main__":
    main()
