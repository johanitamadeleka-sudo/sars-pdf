"""One-off extraction of MWANZA CC SCHOOLS RANK SUBJECTWISE into data.json (display strings).

The report is subject-centric: each subject has a header block + one table whose rows
flow across page breaks (continuation pages do NOT repeat the header). Small subjects
stack several-per-page at the end. We therefore model ONE table per subject (in document
order) and let the HTML/CSS paginate to reproduce the 24-page layout.

Column layout (NO region/council/centre/av/grd):
  S/N | SCHOOL NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA | COMPETENCY LEVEL | C/RANK
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC SCHOOLS RANK SUBJECTWISE.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-schools-rank-subjectwise" / "data.json"

NUM_COLS = ["a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d", "gpa"]
NUM_CENTERS = [197, 220, 244, 268, 295, 324, 352, 379, 406, 434, 466]
SCHOOL_MAX_X = 175.0
COMP_MIN_X = 478.0
RANK_MIN_X = 570.0
SN_MAX_X = 55.0


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


def group_lines(words, y_tol=3.0):
    """Group words into visual lines by y-centre."""
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


def parse_data_row(line):
    row = {k: "" for k in ["sn", "school_name", *NUM_COLS, "competency", "rank"]}
    school_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["school_name"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_overall_row(line):
    row = {k: "" for k in [*NUM_COLS, "competency"]}
    label_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx >= COMP_MIN_X and not _is_num(txt):
            comp_parts.append((x0, txt))
        elif _is_num(txt) and cx > SN_MAX_X:
            row[col_for(cx)] = txt
        else:
            label_parts.append((x0, txt))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return " ".join(t for _, t in sorted(label_parts)), row


def main():
    doc = pymupdf.open(SRC)
    subjects = []  # each: {subject, start_page, rows, overall, overall_label}
    cur = None
    for pi in range(doc.page_count):
        page = doc[pi]
        lines = group_lines(page.get_text("words"))
        for cy, line in lines:
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            if "SCHOOL RANK IN" in text and "COUNCILWISE" in text:
                subj = text.split("SCHOOL RANK IN", 1)[1].rsplit("COUNCILWISE", 1)[0].strip()
                cur = {"subject": subj, "start_page": pi + 1, "rows": [],
                       "overall": None, "overall_label": None}
                subjects.append(cur)
                continue
            if cur is None:
                continue
            if "OVERALL" in text and "PERFORMANCE" in text:
                lbl, orow = parse_overall_row(line)
                cur["overall_label"] = lbl
                cur["overall"] = orow
                continue
            first = line[0]
            if first[0] < SN_MAX_X and first[4].isdigit():
                cur["rows"].append(parse_data_row(line))

    document = {
        "page_size": "Letter",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC SCHOOLS RANK SUBJECTWISE",
        "scope": "COUNCILWISE",
        "rows_per_page": 54,
        "trailing_blank_page": True,
    }
    tables = []
    for s in subjects:
        tab = {"subject": s["subject"], "scope": "COUNCILWISE", "rows": s["rows"]}
        if s["overall"]:
            tab["overall"] = s["overall"]
            tab["overall_label"] = s["overall_label"]
        tables.append(tab)

    data = {"document": document, "tables": tables}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(len(t["rows"]) for t in tables)
    print(f"subjects={len(tables)} rows={total} -> {OUT}")
    for t in tables:
        print(f"  {t['subject']:<28} rows={len(t['rows']):>3} "
              f"overall={t.get('overall_label') or '-'}")


if __name__ == "__main__":
    main()
