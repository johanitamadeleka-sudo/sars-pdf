"""Extract MWANZA CC KATA RANK GRADING (primary STD4) into data.json (display strings).

Primary council per-ward (KATA) division/grade grid. A SUMMARY block sits above the
main per-KATA table (+ TOTAL/JUMLA row). Swahili/abbrev headers:
  NA | KATA | IDADI YA SHULE
  WALIOSAJILIWA(WAV WAS JML) WALIOFANYA(WAV WAS JML) WASIOFANYA(WAV WAS JML)
  A(WAV WAS JML) B(WAV WAS JML) C(WAV WAS JML) D(WAV WAS JML)
  UFAULU(A-D)(WAV WAS JML %) E(WAV WAS JML %)
  WASTANI WA UFAULU | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI KIKATA
WAV=girls, WAS=boys, JML=total. Extraction is coordinate based (pymupdf words).
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "primary_council_pdf" / "primary_council_pdf" / "MWANZA CC KATA RANK GRADING.pdf"
OUT = ROOT / "reports" / "primary" / "council" / "primary-council-wards-rank" / "data.json"

# Numeric column centres (x) measured from the header WAV/WAS/JML positions.
NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "sifanya_f", "sifanya_m", "sifanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]
NUM_CENTERS = [
    132.2, 149.4, 167.9, 186.5, 203.7, 222.1, 240.7, 257.9, 274.6,
    291.3, 308.5, 325.1, 342.0, 359.0, 375.9, 393.3, 410.5, 427.6,
    444.7, 461.9, 478.5, 495.7, 513.0, 531.7, 552.5, 570.1, 587.3, 603.9, 622.0, 650.0,
]
SN_MAX_X = 32.0
WARD_MIN_X = 32.0
WARD_MAX_X = 85.0
SHULE_MIN_X = 85.0
SHULE_MAX_X = 122.0
COMP_MIN_X = 665.0
COMP_MAX_X = 734.0
NAFASI_MIN_X = 735.0


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


def parse_grid_row(line, has_sn=True):
    keys = ["sn", "ward", "shule", *NUM_COLS, "competency", "nafasi"]
    row = {k: "" for k in keys}
    ward_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < WARD_MAX_X and cx < WARD_MAX_X:
            ward_parts.append((x0, txt))
        elif cx < SHULE_MAX_X:
            row["shule"] = txt
        elif cx >= NAFASI_MIN_X:
            row["nafasi"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["ward"] = " ".join(t for _, t in sorted(ward_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def main():
    doc = pymupdf.open(SRC)
    page = doc[0]
    lines = group_lines(page.get_text("words"))

    summary = None
    pct_pass = None
    rows = []
    total = None

    # merge the summary value row (y~149) with the WASTANI/competency line (y~151)
    summary_words = []
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        first = line[0]
        text = " ".join(w[4] for w in line)
        if 145 < cy < 155:
            summary_words += line

    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        first = line[0]
        text = " ".join(w[4] for w in line)
        if 155 < cy < 165 and "ASILIMIA" in text:
            pct_pass = parse_pct(line)
        elif first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 2 and len(line) > 20:
            rows.append(parse_grid_row(line))
        elif "JUMLA" in text and first[0] < 90 and len(line) > 20:
            total = parse_total(line)
    if summary_words:
        summary = parse_summary(sorted(summary_words, key=lambda w: w[0]))

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "OFISI YA WAZIRI MKUU",
            "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
            "MKOA WA MWANZA",
        ],
        "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
        "report_title": "MPANGILIO WA UFAULU WA KATA KIMADARAJA - MWANZA CC",
    }
    data = {"document": document, "summary": summary, "pct_pass": pct_pass,
            "rows": rows, "total": total}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} summary={'yes' if summary else 'no'} total={'yes' if total else 'no'} -> {OUT}")
    for r in rows:
        print(f"  {r['sn']} {r['ward']:<14} shule={r['shule']:>3} JML={r['reg_t']:>6} {r['competency']} #{r['nafasi']}")


def parse_summary(line):
    # summary shares the numeric geometry but has shule=169 and no sn/ward.
    keys = ["shule", *NUM_COLS, "competency"]
    row = {k: "" for k in keys}
    comp_parts = []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SHULE_MAX_X:
            row["shule"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


PCT_GROUPS = [
    ("fanya", 205.0), ("sifanya", 258.0), ("a", 308.0), ("b", 359.0),
    ("c", 410.0), ("d", 461.0), ("ad", 524.0), ("e", 596.0),
]


def parse_pct(line):
    # ASILIMIA (%) row: one value centred under each group (fanya/sifanya/A/B/C/D/AD/E).
    row = {}
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < 160:
            continue  # the "ASILIMIA (%)" label
        best, bd = None, 1e9
        for name, c in PCT_GROUPS:
            if abs(cx - c) < bd:
                best, bd = name, abs(cx - c)
        row[best] = txt
    return row


def parse_total(line):
    keys = ["shule", *NUM_COLS, "competency"]
    row = {k: "" for k in keys}
    comp_parts = []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if txt == "JUMLA":
            continue
        if cx < SHULE_MAX_X:
            row["shule"] = txt
        elif cx >= COMP_MIN_X and cx < NAFASI_MIN_X:
            comp_parts.append((x0, txt))
        elif cx < NAFASI_MIN_X:
            row[col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


if __name__ == "__main__":
    main()
