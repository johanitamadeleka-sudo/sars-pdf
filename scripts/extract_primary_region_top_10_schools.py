"""Extract MKOA SHULE KUMI BORA (region top schools overall) -> data.json.

Region top-schools overall grid. Leading text columns:
  S/N | HALMASHAURI | JINA LA SHULE | UMILIKI
then EIGHT WAV/WAS/JML grade groups (NOTE: no WASIOFANYA group here):
  WALIOSAJILIWA WALIOFANYA A B C D WALIOFAULU(A-D)(+%) E(+%)
  WASTANI WA SHULE /300 | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI

Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-top-10-schools"

SOURCES = [
    (None, "MKOA SHULE BORA STD4 JUMLA 2026.pdf", "SHULE KUMI BORA MKOA"),
]

# 8 groups: reg fanya a b c d ad(+%) e(+%) = 26 numeric cells + wastani.
NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]
NUM_CENTERS = [
    195.4, 211.3, 227.3, 243.3, 259.2, 275.1, 291.1, 307.1, 323.0,
    339.0, 355.0, 370.9, 386.9, 402.9, 418.8, 434.8, 450.8, 466.7,
    484.4, 503.7, 522.5, 543.9, 565.9, 585.2, 604.1, 624.2, 654.0,
]
SN_MAX_X = 40.0
COUNCIL_MAX_X = 90.0
SCHOOL_MAX_X = 165.0
OWN_MAX_X = 190.0
COMP_MIN_X = 680.0
NAFASI_C = 758.6


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
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


def parse_row(line):
    keys = ["sn", "council", "school", "ownership", *NUM_COLS, "competency", "nm"]
    row = {k: "" for k in keys}
    council_parts, school_parts, comp_parts = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif cx < COUNCIL_MAX_X:
            council_parts.append((x0, txt))
        elif cx < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx < OWN_MAX_X:
            row["ownership"] = txt
        elif cx >= NAFASI_C - 10:
            row["nm"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def extract(src):
    """Walk lines in reading order across pages; a 'SHULE KUMI ...' title line starts
    a new section, its data rows follow until the next title."""
    doc = pymupdf.open(src)
    sections = []
    cur = None
    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line).strip()
            first = line[0]
            if text.startswith("SHULE KUMI"):
                cur = {"title": text, "rows": []}
                sections.append(cur)
            elif first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 3 and len(line) > 20:
                if cur is None:
                    cur = {"title": "", "rows": []}
                    sections.append(cur)
                cur["rows"].append(parse_row(line))
    return [s for s in sections if s["rows"]]


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title in SOURCES:
        src = SRCDIR / name
        sections = extract(src)
        document = {
            "page_size": "Letter-landscape",
            "ministry": [
                "OFISI YA WAZIRI MKUU",
                "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
                "MKOA WA MWANZA",
            ],
            "exam_name": "MATOKEO YA MTIHANI WA MOCK MKOA DARASA LA NNE MWEZI AGOSTI, 2026",
            "report_title": title,
        }
        data = {"document": document, "sections": sections}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        nrows = sum(len(s["rows"]) for s in sections)
        print(f"[{tag or 'main'}] sections={len(sections)} rows={nrows} -> {out.name}")
        for s in sections:
            print(f"   [{s['title']}] {len(s['rows'])} rows; first={s['rows'][0]['school']}")


if __name__ == "__main__":
    main()
