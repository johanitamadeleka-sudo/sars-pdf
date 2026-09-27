"""Extract MWANZA CC UFAULU WA MASOMO (primary STD4) into data.json (display strings).

Primary council per-subject performance grid (TATHIMINI YA UFAULU KIMASOMO). A summary
block (overall registered/sat + A-E grade split + ASILIMIA %) sits above the main
per-subject table (+ JUMLA total row). Swahili/abbrev headers, WAV=girls/WAS=boys/
JML=total triplets:
  main: NA | SOMO | A(WAV WAS JML) B(...) C(...) D(...) E(...)
        WALIOFAULU(A-D)(WAV WAS JML %) JUMLA YA WATAHINIWA(WAV WAS JML)
        WASTANI WA SOMO | NAFASI YA SOMO | KUNDI LA UMAHIRI (Daraja X (...))
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "primary_council_pdf" / "primary_council_pdf" / "MWANZA CC UFAULU WA MASOMO.pdf"
OUT = ROOT / "reports" / "primary" / "council" / "primary-council-subjects-rank" / "data.json"

# main per-subject grid numeric column centres (from the WAV/WAS/JML header row).
MAIN_COLS = [
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t",
    "d_f", "d_m", "d_t", "e_f", "e_m", "e_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "tot_f", "tot_m", "tot_t", "wastani",
]
MAIN_CENTERS = [
    204.8, 223.3, 242.2, 261.5, 284.4, 307.6, 327.2, 346.1, 364.1,
    381.8, 399.4, 416.4, 432.9, 449.3, 465.8,
    499.7, 516.6, 534.9, 482.8, 571.6, 590.2, 609.6, 629.0,
]
NA_MAX_X = 66.5
SOMO_MIN_X = 66.5
SOMO_MAX_X = 195.0
NAFASI_C = 654.5
COMP_MIN_X = 665.0


def main_col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(MAIN_COLS, MAIN_CENTERS):
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


def parse_main_row(line):
    keys = ["sn", "subject", *MAIN_COLS, "nafasi", "competency"]
    row = {k: "" for k in keys}
    somo_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < NA_MAX_X:
            row["sn"] = txt
        elif x0 < SOMO_MAX_X and cx < SOMO_MAX_X:
            somo_parts.append((x0, txt))
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        elif abs(cx - NAFASI_C) < 8:
            row["nafasi"] = txt
        else:
            row[main_col_for(cx)] = txt
    row["subject"] = " ".join(t for _, t in sorted(somo_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


# ---- top summary block geometry (distinct from the main grid) ----
SUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t", "fanya_pct",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t",
    "d_f", "d_m", "d_t", "ad_f", "ad_m", "ad_t", "e_f", "e_m", "e_t",
]
SUM_CENTERS = [
    204.8, 223.3, 242.5, 261.5, 284.4, 308.0, 326.7,
    346.1, 364.1, 381.8, 399.4, 416.4, 433.2, 449.3, 465.8, 483.1,
    500.0, 516.6, 535.0, 553.6, 571.6, 590.6, 609.5, 631.3, 654.3,
]


def sum_col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(SUM_COLS, SUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def parse_summary(line):
    keys = ["shule", *SUM_COLS]
    row = {k: "" for k in keys}
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SOMO_MAX_X:
            row["shule"] = txt
        else:
            row[sum_col_for(cx)] = txt
    return row


def main():
    doc = pymupdf.open(SRC)
    page = doc[0]
    lines = group_lines(page.get_text("words"))

    summary = None
    rows = []
    total = None

    # summary aggregate: the "169" (y~122) + the numeric values row (y~129);
    # skip the WAV/WAS/JML header labels (y~120).
    summary_words = []
    for cy, line in lines:
        for w in line:
            if w[4].replace(".", "").isdigit() and 121 < (w[1] + w[3]) / 2 < 132:
                summary_words.append(w)
    if summary_words:
        summary = parse_summary(sorted(summary_words, key=lambda w: w[0]))

    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        first = line[0]
        text = " ".join(w[4] for w in line)
        if first[0] < NA_MAX_X and first[4].isdigit() and len(first[4]) <= 2 and len(line) > 15 and cy > 195:
            rows.append(parse_main_row(line))
        elif "JUMLA" in text and first[0] < 195 and len(line) > 15 and cy > 195:
            total = parse_total(line)

    # ASILIMIA YA UFAULU(%) row: %s centred under A/B/C/D/A-D/E groups.
    asilimia = {}
    for cy, line in lines:
        for w in line:
            cx = (w[0] + w[2]) / 2
            if 133 < (w[1] + w[3]) / 2 < 140 and w[4].endswith("%") and cx > 300:
                key = {"a": 364, "b": 416, "c": 466, "d": 518, "ad": 572, "e": 632}
                best, bd = None, 1e9
                for k, c in key.items():
                    if abs(cx - c) < bd:
                        best, bd = k, abs(cx - c)
                asilimia[best] = w[4]

    # KUNDI LA UMAHIRI overall box (y~151): GPA value + Daraja label.
    overall = {"gpa": "", "competency": ""}
    for cy, line in lines:
        if 148 < cy < 155:
            comp_parts = []
            for w in line:
                cx = (w[0] + w[2]) / 2
                if w[4].replace(".", "").isdigit() and "." in w[4] and 585 < cx < 615:
                    overall["gpa"] = w[4]
                elif cx > 620:
                    comp_parts.append((w[0], w[4]))
            if comp_parts:
                overall["competency"] = " ".join(t for _, t in sorted(comp_parts))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "OFISI YA WAZIRI MKUU",
            "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
            "MKOA WA MWANZA",
        ],
        "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
        "report_title": "TATHIMINI YA UFAULU KIMASOMO - MWANZA CC",
        "section_title": "TATHIMINI YA UFAULU  MADARAJA YA KILA SOMO",
    }
    data = {"document": document, "summary": summary, "asilimia": asilimia,
            "overall": overall, "rows": rows, "total": total}
    # Stamp an explicit competency letter into the aggregate blocks so their cell
    # colour is data-driven without any shared render.py change (extraction is the
    # single source of truth).
    for agg in (summary, total):
        if isinstance(agg, dict):
            agg["level"] = competency_letter(agg.get("competency"), agg.get("gpa"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} summary={'yes' if summary else 'no'} total={'yes' if total else 'no'} -> {OUT}")
    for r in rows:
        print(f"  {r['sn']} {r['subject']:<40} JMLtot={r['tot_t']:>6} wastani={r['wastani']} {r['competency']} #{r['nafasi']}")


def parse_total(line):
    keys = ["sn", "subject", *MAIN_COLS, "nafasi", "competency"]
    row = {k: "" for k in keys}
    comp_parts = []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if txt == "JUMLA":
            continue
        if cx < SOMO_MAX_X:
            continue
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        elif abs(cx - NAFASI_C) < 8:
            row["nafasi"] = txt
        else:
            row[main_col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


if __name__ == "__main__":
    main()
