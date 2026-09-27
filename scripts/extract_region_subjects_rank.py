"""Extract 'Mwanza Overall Subjects Performance' into region-subjects-rank/data.json.

One row per SUBJECT (REGIONALWISE). Columns:
  S/NO. | SUBJECT NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA | COMPETENCY LEVEL | R/RANK
A "GRADE PERFORMANCE" super-header spans A..%A-D. A trailing overall block prints the
OVERALL SUBJECTS REGIONAL GPA + value + competency level.

Coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza Overall Subjects Performance.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-subjects-rank" / "data.json"

NUM_COLS = ["a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d", "gpa"]
NUM_CENTERS = [299.8, 330.5, 362.4, 395.5, 428.7, 461.8, 494.9, 527.0, 558.9, 591.0, 624.0]
SN_MAX_X = 66.0
SUBJECT_MAX_X = 240.0
COMP_MIN_X = 640.0
RANK_MIN_X = 735.0


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def parse_row(words):
    row = {k: "" for k in ["sn", "subject", *NUM_COLS, "competency", "rank"]}
    subj_parts, comp_parts = [], []
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < SUBJECT_MAX_X:
            subj_parts.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif x0 >= COMP_MIN_X:
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
        words = doc[pi].get_text("words")
        # anchors: a 2-char S/NO in the left column
        anchors = []
        for w in words:
            cx = (w[0] + w[2]) / 2
            y = (w[1] + w[3]) / 2
            # data-row S/NO anchors sit below the header band on each page
            hdr_limit = 175 if pi == 0 else 100
            if cx < SN_MAX_X and w[4].isdigit() and len(w[4]) == 2 and y > hdr_limit:
                anchors.append((y, w[4]))
        for ay, sn in anchors:
            band = [w for w in words if abs((w[1] + w[3]) / 2 - ay) <= 7.5]
            row = parse_row(band)
            row["sn"] = sn
            rows.append(row)
        # overall block (page 2)
        lines = {}
        for w in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
            y = round((w[1] + w[3]) / 2, 0)
            lines.setdefault(y, []).append(w)
        pending = None
        for y in sorted(lines):
            txt = " ".join(x[4] for x in sorted(lines[y], key=lambda w: w[0]))
            single = lines[y][0][4]
            if len(lines[y]) == 1 and single.replace(".", "").isdigit() and "." in single:
                pending = single
            elif "OVERALL" in txt and "GPA" in txt:
                overall["gpa"] = pending or overall["gpa"]
            elif txt.startswith("Grade") and len(lines[y]) >= 2:
                overall["competency"] = txt

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "SUBJECTS PERFORMANCE REGIONALWISE",
        "overall_gpa_label": "OVERALL SUBJECTS REGIONAL GPA",
        "scope": "REGIONWISE",
        "page_break_after_sn": "24",
    }
    # sort by SN numeric
    rows.sort(key=lambda r: int(r["sn"]))
    data = {"document": document, "rows": rows, "overall": overall}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} overall={overall} -> {OUT}")
    for r in rows:
        empty = [k for k in NUM_COLS if not r[k]]
        flag = f"  MISSING {empty}" if empty else ""
        print(f"  {r['sn']} {r['subject']:<40} F={r['f']:>6} GPA={r['gpa']} {r['competency']} #{r['rank']}{flag}")


if __name__ == "__main__":
    main()
