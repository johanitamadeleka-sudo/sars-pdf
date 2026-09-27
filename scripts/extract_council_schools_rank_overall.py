"""Extract MWANZA CC SCHOOLS RANK (overall division grid) into data.json (display strings).

Wide F/M/T triplet grid. A SUMMARY block (+ %PASS row) sits above the main per-school table
(+ TOTAL row). Main columns:
  S/NO. | WARD | SCHOOL NAME | OWNERSHIP
  REGISTERED(F M T) | SAT(F M T %)
  I(F M T) II(F M T) III(F M T) IV(F M T) 0(F M T %) I-III(F M T %) I-IV(F M T %)
  GPA | COMPETENCY | C/RANK | R/RANK
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC SCHOOLS RANK.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-schools-rank-overall" / "data.json"

# 39 vertical boundaries measured from the reference (main table region).
BOUNDS = [13.3, 26.2, 64.2, 115.0, 151.8, 165.9, 182.4, 202.0, 218.5, 235.1, 251.7,
          271.1, 287.8, 301.0, 317.6, 330.8, 344.0, 363.5, 376.7, 389.9, 409.5, 426.1,
          442.6, 459.1, 478.8, 492.0, 508.5, 528.0, 544.6, 561.2, 577.8, 597.2, 613.9,
          630.5, 647.0, 666.5, 692.7, 754.0, 763.8, 779.4]

# numeric column keys in order (32 of them), from REG_F .. GPA.
NUM_KEYS = [
    "reg_f", "reg_m", "reg_t", "sat_f", "sat_m", "sat_t", "sat_pct",
    "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
    "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
    "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct", "gpa",
]
# centre of numeric columns = midpoints of BOUNDS[4..36]
NUM_CENTERS = [(BOUNDS[i] + BOUNDS[i + 1]) / 2 for i in range(4, 36)]
SN_MAX_X = 26.2
WARD_MAX_X = 64.2
SCHOOL_MAX_X = 115.0
OWN_MAX_X = 151.8
COMP_MIN_X = 692.7
CRANK_MIN_X = 754.0
RRANK_MIN_X = 763.8


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_KEYS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def group_lines(words, y_tol=2.6):
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


def parse_school_row(line):
    row = {k: "" for k in ["sn", "ward", "school", "ownership", *NUM_KEYS,
                            "competency", "crank", "rrank"]}
    ward_p, school_p, own_p, comp_p = [], [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < WARD_MAX_X:
            ward_p.append((x0, txt))
        elif x0 < SCHOOL_MAX_X:
            school_p.append((x0, txt))
        elif x0 < OWN_MAX_X:
            own_p.append((x0, txt))
        elif cx >= RRANK_MIN_X:
            row["rrank"] = txt
        elif cx >= CRANK_MIN_X:
            row["crank"] = txt
        elif cx >= COMP_MIN_X:
            comp_p.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["ward"] = " ".join(t for _, t in sorted(ward_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["ownership"] = " ".join(t for _, t in sorted(own_p))
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def parse_numeric_only(line, min_x):
    """For summary/total rows: assign numeric tokens to nearest column, keep comp/rank."""
    row = {k: "" for k in [*NUM_KEYS, "competency", "crank", "rrank"]}
    comp_p = []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < min_x:
            continue
        if cx >= RRANK_MIN_X:
            row["rrank"] = txt
        elif cx >= CRANK_MIN_X:
            row["crank"] = txt
        elif cx >= COMP_MIN_X:
            comp_p.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def main():
    doc = pymupdf.open(SRC)
    lines = group_lines(doc[0].get_text("words"))
    rows = []
    summary = None
    pct_pass = None
    total = None
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        text = " ".join(w[4] for w in line)
        first = line[0]
        if cy < 100 and first[4].isdigit() and len(line) > 20:
            summary = parse_numeric_only(line, OWN_MAX_X)
            summary["no_schools"] = first[4]  # the leading "NO. OF SCHOOLS IN COUNCIL" value
        elif text.startswith("% PASS"):
            pct_pass = parse_numeric_only(line, OWN_MAX_X)
        elif text.startswith("TOTAL"):
            total = parse_numeric_only(line, OWN_MAX_X)
            # the line starts "TOTAL 6854..." - "TOTAL" is at x<SN_MAX_X
            # and "64" is under no_schools? Actually total line has no "no_schools" value
            # just numeric data starting from reg_f
        elif first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) == 2 and cy > 140:
            rows.append(parse_school_row(line))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC SCHOOLS RANK",
    }
    data = {"document": document, "summary": summary, "pct_pass": pct_pass,
            "rows": rows, "total": total}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} -> {OUT}")
    print("summary reg_t:", summary and summary["reg_t"], "gpa:", summary and summary["gpa"])
    print("total reg_t:", total and total["reg_t"])
    empties = sum(1 for r in rows for k in NUM_KEYS if r[k] == "")
    print("empty numeric cells across rows:", empties)
    for r in rows[:3] + rows[-2:]:
        print(f"  {r['sn']} {r['ward']:<10} {r['school']:<22} {r['ownership']:<10} "
              f"gpa={r['gpa']} {r['competency']} C{r['crank']} R{r['rrank']}")


if __name__ == "__main__":
    main()
