"""Extract MWANZA CC 10 BEST STUDENTS (overall) into data.json (display strings).

Section-centric: multiple stacked top-10 tables, each with a title banner and columns:
  C/NO | SCHOOL NAME | CANDIDATE FULL NAME | SEX | AGGT | DIVISION | POSITION | DETAILED SUBJECTS
The DETAILED SUBJECTS free-text (e.g. "HTM - 97'A' BUSI - 80'A' ...") is preserved exactly.
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC 10 BEST STUDENTS.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-best-students-overall" / "data.json"

CNO_MAX = 66.2
SCHOOL_MAX = 135.6
CAND_MAX = 263.8
SEX_C, AGGT_C, DIV_C, POS_C = 274.1, 295.2, 316.8, 338.4
DETAIL_MIN = 349.2


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


def nearest(cx, centers):
    return min(centers, key=lambda kc: abs(cx - kc[0]))[1]


def parse_row(line):
    row = {k: "" for k in ["cno", "school", "candidate", "sex", "aggt", "division",
                            "position", "detailed"]}
    school_p, cand_p, det_p = [], [], []
    centers = [(SEX_C, "sex"), (AGGT_C, "aggt"), (DIV_C, "division"), (POS_C, "position")]
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if x0 < CNO_MAX:
            row["cno"] = (row["cno"] + " " + txt).strip()
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif x0 < CAND_MAX:
            cand_p.append((x0, txt))
        elif cx >= DETAIL_MIN:
            det_p.append((x0, txt))
        else:
            row[nearest(cx, centers)] = txt
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["candidate"] = " ".join(t for _, t in sorted(cand_p))
    row["detailed"] = " ".join(t for _, t in sorted(det_p))
    return row


def main():
    doc = pymupdf.open(SRC)
    sections = []
    cur = None
    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            if "TOP TEN" in text and "STUDENT" in text:
                title = text
                if title.startswith("MWANZA CC "):
                    title = title[len("MWANZA CC "):]
                cur = {"title": title, "banner": text.startswith("MWANZA CC "),
                       "rows": []}
                sections.append(cur)
                continue
            if cur is None:
                continue
            first = line[0]
            # data rows begin with a C/NO like "S5344-0004" or a lone "-"
            if first[0] < CNO_MAX and ("-" in first[4] or first[4].isalnum()) \
                    and len(line) > 2 and any(w[4].isdigit() for w in line):
                # position-only trailing row (candidate blank) still has POSITION digit
                row = parse_row(line)
                if row["position"] or row["candidate"] or row["cno"] not in ("", "-"):
                    cur["rows"].append(row)
            elif first[0] < CNO_MAX and first[4] == "-" and len(line) <= 3:
                cur["rows"].append(parse_row(line))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC TOP TEN BEST STUDENTS OVERALL COUNCILWISE",
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"sections={len(sections)} -> {OUT}")
    for s in sections:
        print(f"  [{ 'banner' if s['banner'] else '      ' }] rows={len(s['rows']):>2}  {s['title']}")


if __name__ == "__main__":
    main()
