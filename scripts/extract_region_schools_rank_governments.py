"""Extract 'Mwanza schools rank Overall' (6pp) into region-schools-rank-overall/data.json.

Region variant of the overall division grid: same F/M/T triplet grid as the council
report but the WARD column is replaced by a COUNCIL column. A SUMMARY block (+ %PASS row)
sits above the main per-school table (+ TOTAL row on the last page). Main columns:
  S/NO. | COUNCIL | SCHOOL NAME | OWNERSHIP
  REGISTERED(F M T) | SAT(F M T %)
  I(F M T) II(F M T) III(F M T) IV(F M T) 0(F M T %) I-III(F M T %) I-IV(F M T %)
  GPA | COMPETENCY | C/RANK | R/RANK
Coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza Schools Rank For Governments.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-schools-rank-governments" / "data.json"

# 40 vertical boundaries measured from the reference (main table region).
BOUNDS = [13.3, 28.1, 67.6, 126.4, 168.8, 187.2, 205.4, 223.7, 241.9, 260.2, 278.4,
          295.1, 310.2, 325.3, 340.4, 355.6, 370.7, 385.8, 400.9, 416.0, 430.0, 446.8,
          463.6, 480.4, 494.3, 508.2, 522.1, 537.0, 550.9, 569.2, 587.4, 604.1, 622.3,
          640.6, 658.8, 675.5, 701.3, 752.2, 763.4, 774.7]

NUM_KEYS = [
    "reg_f", "reg_m", "reg_t", "sat_f", "sat_m", "sat_t", "sat_pct",
    "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
    "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
    "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct", "gpa",
]
NUM_CENTERS = [(BOUNDS[i] + BOUNDS[i + 1]) / 2 for i in range(4, 36)]
SN_MAX_X = 28.1
COUNCIL_MAX_X = 67.6
SCHOOL_MAX_X = 126.4
OWN_MAX_X = 168.8
COMP_MIN_X = 701.3
CRANK_MIN_X = 752.2
RRANK_MIN_X = 763.4


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
    row = {k: "" for k in ["sn", "council", "school", "ownership", *NUM_KEYS,
                            "competency", "crank", "rrank"]}
    council_p, school_p, own_p, comp_p = [], [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < COUNCIL_MAX_X:
            council_p.append((x0, txt))
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
    row["council"] = " ".join(t for _, t in sorted(council_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["ownership"] = " ".join(t for _, t in sorted(own_p))
    row["competency"] = " ".join(t for _, t in sorted(comp_p))
    return row


def parse_numeric_only(line, min_x):
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
    rows = []
    summary = None
    pct_pass = None
    total = None
    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            first = line[0]
            if pi == 0 and cy < 112 and first[4].isdigit() and len(line) > 20:
                summary = parse_numeric_only(line, OWN_MAX_X)
                summary["no_schools"] = first[4]
            elif text.startswith("% PASS"):
                pct_pass = parse_numeric_only(line, OWN_MAX_X)
            elif text.startswith("TOTAL"):
                total = parse_numeric_only(line, OWN_MAX_X)
            else:
                hdr_limit = 120 if pi == 0 else 36
                if first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 3 \
                        and len(line) > 20 and cy > hdr_limit:
                    rows.append(parse_school_row(line))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "SCHOOL PERFORMANCE FOR GOVERNMENT SCHOOLS ONLY",
    }
    data = {"document": document, "summary": summary, "pct_pass": pct_pass,
            "rows": rows, "total": total}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    empties = sum(1 for r in rows for k in NUM_KEYS if r[k] == "")
    print(f"rows={len(rows)} empty_numeric={empties} summary_gpa={summary and summary['gpa']} "
          f"total_reg_t={total and total['reg_t']} -> {OUT}")
    for r in rows[:2] + rows[-2:]:
        print(f"  {r['sn']} {r['council']:<12} {r['school']:<24} {r['ownership']:<10} "
              f"gpa={r['gpa']} {r['competency']} C{r['crank']} R{r['rrank']}")


if __name__ == "__main__":
    main()
