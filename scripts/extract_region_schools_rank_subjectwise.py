"""Extract the two region school-rank-by-subject PDFs into data files.

Sources (region-level, PORTRAIT):
  'Mwanza School Rank-EDK.pdf'              (1pp) -> data_edk.json
  'Mwanza School Rank-English Language.pdf' (6pp) -> data_english.json

Region variant of the subjectwise-rank shape: adds a COUNCIL column and BOTH
C/RANK and R/RANK columns. Columns:
  S/N | COUNCIL | SCHOOL NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA
      | COMPETENCY LEVEL | C/RANK | R/RANK
'GRADING PERFORMANCE' super-header spans A..%A-D. A trailing COUNCIL OVERALL
PERFORMANCE row closes each subject. Coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "region_pdf" / "region_pdf"
OUTDIR = ROOT / "reports" / "secondary" / "region" / "region-schools-rank-subjectwise"

NUM_COLS = ["a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d", "gpa"]
NUM_CENTERS = [200.8, 224.1, 247.5, 270.9, 294.3, 320.3, 346.3, 372.5, 398.4, 424.5, 460.5]
SN_MAX_X = 55.0
COUNCIL_MAX_X = 110.0
SCHOOL_MAX_X = 195.0
COMP_MIN_X = 480.0
CRANK_MIN_X = 556.0
RRANK_MIN_X = 573.0


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def parse_row(words):
    row = {k: "" for k in ["sn", "council", "school", *NUM_COLS, "competency", "c_rank", "rank"]}
    council_parts, school_parts, comp_parts = [], [], []
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < COUNCIL_MAX_X:
            council_parts.append((x0, txt))
        elif x0 < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx >= RRANK_MIN_X:
            row["rank"] = txt
        elif cx >= CRANK_MIN_X:
            row["c_rank"] = txt
        elif x0 >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def extract(src, subject, scope_note):
    doc = pymupdf.open(src)
    rows = []
    overall = None
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        anchors = []
        for w in words:
            cx = (w[0] + w[2]) / 2
            y = (w[1] + w[3]) / 2
            hdr_limit = 144 if pi == 0 else 90
            if cx < SN_MAX_X and w[4].isdigit() and len(w[4]) == 3 and y > hdr_limit:
                anchors.append((y, w[4]))
        for ay, sn in anchors:
            band = [w for w in words if abs((w[1] + w[3]) / 2 - ay) <= 5.0]
            row = parse_row(band)
            row["sn"] = sn
            rows.append(row)
        # overall row: "COUNCIL OVERALL PERFORMANCE ..."
        lines = {}
        for w in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
            y = round((w[1] + w[3]) / 2, 0)
            lines.setdefault(y, []).append(w)
        pending_grade = None
        for y in sorted(lines):
            ws = sorted(lines[y], key=lambda w: w[0])
            txt = " ".join(x[4] for x in ws)
            if "OVERALL PERFORMANCE" in txt:
                nums = [x[4] for x in ws if _isnum(x[4])]
                overall = {
                    "label": " ".join(x[4] for x in ws if not _isnum(x[4])),
                    "a": nums[0], "b": nums[1], "c": nums[2], "d": nums[3], "f": nums[4],
                    "total": nums[5], "a_c": nums[6], "pct_a_c": nums[7],
                    "a_d": nums[8], "pct_a_d": nums[9], "gpa": nums[10],
                    "competency": "",
                }
            elif overall is not None and not overall["competency"] and txt.startswith("Grade"):
                overall["competency"] = txt
    table = {"subject": subject, "scope": "REGIONWISE", "scope_label": "SUBJECT REGIONALWISE",
             "rows": rows, "overall": overall}
    return table


def _isnum(s):
    return s.replace(".", "").replace("-", "").isdigit()


def build(src_name, out_name, subject):
    src = SRCDIR / src_name
    table = extract(src, subject, None)
    document = {
        "page_size": "Letter-portrait",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO ASSESSMENT RESULTS, JULY 2026",
        "scope": "REGIONWISE",
    }
    data = {"document": document, "tables": [table]}
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / out_name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    empty = sum(1 for r in table["rows"] for k in NUM_COLS if not r[k])
    print(f"{src_name}: rows={len(table['rows'])} empty_cells={empty} overall={table['overall']['gpa'] if table['overall'] else None} -> {out_name}")
    return table


def main():
    build("Mwanza School Rank-EDK.pdf", "data_edk.json", "ELIMU YA DINI YA KIISLAMU")
    build("Mwanza School Rank-English Language.pdf", "data_english.json", "ENGLISH LANGUAGE")


if __name__ == "__main__":
    main()
