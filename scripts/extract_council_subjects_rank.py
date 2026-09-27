"""Extract MWANZA CC SUBJECTS RANK into data.json (display strings).

One row per SUBJECT. Columns:
  S/NO. | SUBJECT NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA | COMPETENCY LEVEL | RANK
A "GRADE PERFORMANCE" super-header spans A..%A-D. A trailing overall block prints the
OVERALL SUBJECTS COUNCIL GPA + value + competency level.

Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC SUBJECTS RANK.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-subjects-rank" / "data.json"

# column centres measured from the header row of the reference
NUM_COLS = ["a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d", "gpa"]
NUM_CENTERS = [234, 269, 301, 333, 369, 407, 443, 480, 517, 553, 592]
SN_MAX_X = 70.0
SUBJECT_MAX_X = 220.0
COMP_MIN_X = 611.0
RANK_MIN_X = 735.0


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


def parse_row(line):
    row = {k: "" for k in ["sn", "subject", *NUM_COLS, "competency", "rank"]}
    subj_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < SUBJECT_MAX_X:
            subj_parts.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["subject"] = " ".join(t for _, t in sorted(subj_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def main():
    doc = pymupdf.open(SRC)
    rows = []
    overall = {"gpa": "", "competency": ""}
    for pi in range(doc.page_count):
        lines = group_lines(doc[pi].get_text("words"))
        pending_gpa = None
        for cy, line in lines:
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            first = line[0]
            if first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 2 and len(line) > 5:
                rows.append(parse_row(line))
            elif text.replace(".", "").isdigit() and "." in text and len(line) == 1:
                pending_gpa = text  # lone GPA number above the overall label
            elif "OVERALL" in text and "GPA" in text:
                overall["gpa"] = pending_gpa or ""
            elif "Grade" in text and "COMPETENCY" not in text and first[0] > 200:
                overall["competency"] = " ".join(w[4] for w in line)

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC ALL SUBJECTS PERFOMANCE",
        "overall_gpa_label": "OVERALL SUBJECTS COUNCIL GPA",
    }
    data = {"document": document, "rows": rows, "overall": overall}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} overall={overall} -> {OUT}")
    for r in rows:
        print(f"  {r['sn']} {r['subject']:<26} F={r['f']:>5} GPA={r['gpa']} {r['competency']} #{r['rank']}")


if __name__ == "__main__":
    main()
