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
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.pdftext import column_x, page_words  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza schools rank Overall.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-schools-rank-overall" / "data.json"

# 40 vertical boundaries measured from the reference (main table region).
BOUNDS = [13.2, 28.9, 67.2, 129.6, 164.9, 182.8, 200.5, 218.3, 236.0, 253.8, 271.6,
          287.9, 302.6, 317.4, 332.2, 346.9, 361.7, 376.4, 391.2, 406.0, 420.7, 438.6,
          456.5, 474.4, 489.1, 503.9, 518.6, 534.5, 549.2, 567.0, 584.8, 601.1, 618.8,
          636.6, 654.4, 670.7, 692.0, 746.2, 758.2, 770.0]

NUM_KEYS = [
    "reg_f", "reg_m", "reg_t", "sat_f", "sat_m", "sat_t", "sat_pct",
    "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
    "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
    "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct", "gpa",
]
NUM_CENTERS = [(BOUNDS[i] + BOUNDS[i + 1]) / 2 for i in range(4, 36)]
SN_MAX_X = 28.9
COUNCIL_MAX_X = 67.2
SCHOOL_MAX_X = 129.6
OWN_MAX_X = 164.9
COMP_MIN_X = 692.0
CRANK_MIN_X = 746.2
RRANK_MIN_X = 758.2


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
    # Words drawn past their cell edge stay in the cell they were typed into
    # (sars_pdf/pdftext.py), e.g. "STAR REACHERS GIRLS AND BOYS" over OWNERSHIP's "PRIVATE".
    colx = column_x(line)
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        col_x = colx[id(w)]
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif col_x < COUNCIL_MAX_X:
            council_p.append((x0, txt))
        elif col_x < SCHOOL_MAX_X:
            school_p.append((x0, txt))
        elif col_x < OWN_MAX_X:
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


# % PASS row: one value per division group, keyed by the group it is centred in.
PASS_GROUPS = [("i", 288.06, 332.34), ("ii", 332.34, 376.62), ("iii", 376.62, 420.9),
               ("iv", 420.9, 474.54), ("z", 474.54, 534.66), ("d3", 534.66, 601.26),
               ("d4", 601.26, 670.86)]


def parse_pct_pass(line):
    out = {k: "" for k, _, _ in PASS_GROUPS}
    for w in line:
        cx = (w[0] + w[2]) / 2
        for key, lo, hi in PASS_GROUPS:
            if lo <= cx < hi:
                out[key] = w[4]
    return out


def main():
    doc = pymupdf.open(SRC)
    rows = []
    summary = None
    pct_pass = None
    total = None
    for pi in range(doc.page_count):
        for cy, line in group_lines(page_words(doc[pi])):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            first = line[0]
            if pi == 0 and cy < 112 and first[4].isdigit() and len(line) > 20:
                summary = parse_numeric_only(line, OWN_MAX_X)
                summary["no_schools"] = first[4]
            elif text.startswith("% PASS"):
                pct_pass = parse_pct_pass(line)
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
        "report_title": "SCHOOL PERFORMANCE OVERALL",
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
