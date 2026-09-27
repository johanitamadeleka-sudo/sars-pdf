"""Extract MWANZA CC Wards Rank into data.json (display strings).

Division-performance grid. A SUMMARY block (with a %PASS row) sits above the main
per-ward table (which ends with a TOTAL row). Columns of the main table:
  S/NO. | WARD | NO_SCHOOLS | REG | SAT_TOTAL SAT_PCT |
  I II III | I-III_TOTAL I-III_PCT | IV | I-IV_TOTAL I-IV_PCT | DIV0_TOTAL DIV0_PCT |
  GPA | COMPETENCY | RANK
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC Wards Rank.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-wards-rank" / "data.json"

# numeric columns (everything except sn/ward/competency), left-to-right, with centres.
NUM_COLS = ["no_schools", "reg", "sat_total", "sat_pct", "i", "ii", "iii",
            "iii_total", "iii_pct", "iv", "iv_total", "iv_pct",
            "div0_total", "div0_pct", "gpa"]
NUM_CENTERS = [142.6, 193.6, 232.8, 262.7, 290.2, 322.5, 357.8,
               390.0, 422.3, 457.7, 490.0, 522.1, 554.3, 586.6, 628.3]
SN_MAX_X = 43.1
WARD_MAX_X = 113.9
COMP_MIN_X = 652.4
RANK_MIN_X = 753.0


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
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


def parse_ward_row(line):
    row = {k: "" for k in ["sn", "ward", *NUM_COLS, "competency", "rank"]}
    ward_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < WARD_MAX_X:
            ward_parts.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["ward"] = " ".join(t for _, t in sorted(ward_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def main():
    doc = pymupdf.open(SRC)
    lines = group_lines(doc[0].get_text("words"))
    rows = []
    summary = None
    total = None
    pct_pass = None
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        text = " ".join(w[4] for w in line)
        first = line[0]
        # summary data row (18 wards..., before the main table header at y~240)
        if cy < 200 and first[4].isdigit() and len(line) > 12 and "PASS" not in text:
            summary = parse_ward_row(line)
        elif text.startswith("% PASS"):
            # %PASS row: capture the numeric cells keyed by column
            pr = {k: "" for k in NUM_COLS}
            for w in line:
                cx = (w[0] + w[2]) / 2
                if w[4] not in ("%", "PASS") and cx > WARD_MAX_X and cx < COMP_MIN_X:
                    pr[col_for(cx)] = w[4]
            pct_pass = pr
        elif first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) == 2 and cy > 240:
            rows.append(parse_ward_row(line))
        elif cy > 460 and first[4].isdigit() and len(line) > 12 and cy < 480:
            total = parse_ward_row(line)  # TOTAL row (no S/NO.)

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC WARDS PERFORMANCE",
    }
    data = {"document": document, "summary": summary, "pct_pass": pct_pass,
            "rows": rows, "total": total}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} -> {OUT}")
    print("summary:", summary)
    print("pct_pass:", pct_pass)
    print("total:", total)
    for r in rows:
        print(f"  {r['sn']} {r['ward']:<12} sch={r['no_schools']} gpa={r['gpa']} {r['competency']} #{r['rank']}")


if __name__ == "__main__":
    main()
