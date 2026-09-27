"""Extract MWANZA CC 10 BEST SCHOOLS ALAMA (primary STD4) into data.json (display strings).

Section-centric: stacked "SHULE KUMI BORA ..." top-10 blocks (JUMLA / ZA SERIKALI /
BINAFSI). Per school: S/N | WILAYA | JINA LA SHULE | UMILIKI | six subjects (AL average +
DRJ grade each: HISABATI, KISWAHILI, SAYANSI, ENGLISH, JIOGRAFIA NA MAZINGIRA, HISTORIA YA
TZ NA MAADILI) | WASTANI WA UFAULU/30 | WASTANI/50 | DARAJA | KUNDI LA UMAHIRI | NAFASI.

Extraction is coordinate based (pymupdf words), never hand-typed.

    python scripts/extract_primary_council_top_10_schools.py
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "primary_council_pdf" / "primary_council_pdf" / "MWANZA CC 10 BEST SCHOOLS ALAMA.pdf"
OUTDIR = ROOT / "reports" / "primary" / "council" / "primary-council-top-10-schools"

SUBJECTS = ["hisabati", "kiswahili", "sayansi", "english", "jiografia", "historia"]
SUBJ_CENTERS = [
    (257.6, 281.7), (305.6, 329.7), (353.6, 377.7),
    (401.6, 425.7), (449.6, 473.7), (497.6, 521.7),
]

SN_MAX = 80.0
WILAYA_MAX = 125.0
SCHOOL_MAX = 210.0
OWN_MAX = 245.0
SUBJ_LO = 248.0
SUBJ_HI = 533.0
UFAULU_C = 554.7    # WASTANI WA UFAULU/30
WASTANI_C = 583.0   # WASTANI/50
DARAJA_C = 609.5
COMP_LO = 630.0
COMP_HI = 705.0
NAFASI_C = 724.1


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


def subj_col(cx):
    best, bd, kind = None, 1e9, None
    for i, (al, drj) in enumerate(SUBJ_CENTERS):
        if abs(cx - al) < bd:
            best, bd, kind = i, abs(cx - al), "al"
        if abs(cx - drj) < bd:
            best, bd, kind = i, abs(cx - drj), "drj"
    return best, kind


def parse_row(line):
    row = {"sn": "", "wilaya": "", "school": "", "ownership": "",
           "ufaulu": "", "wastani": "", "daraja": "", "competency": "", "nafasi": ""}
    for s in SUBJECTS:
        row[f"{s}_al"] = ""
        row[f"{s}_g"] = ""
    wil, sch, comp = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX:
            row["sn"] = txt
        elif cx < WILAYA_MAX:
            wil.append((x0, txt))
        elif cx < SCHOOL_MAX:
            sch.append((x0, txt))
        elif cx < OWN_MAX:
            row["ownership"] = txt
        elif SUBJ_LO <= cx <= SUBJ_HI:
            i, kind = subj_col(cx)
            s = SUBJECTS[i]
            if kind == "al":
                row[f"{s}_al"] = txt
            else:
                row[f"{s}_g"] = txt
        elif cx < WASTANI_C - 10:
            row["ufaulu"] = txt
        elif cx < DARAJA_C - 10:
            row["wastani"] = txt
        elif cx < COMP_LO:
            row["daraja"] = txt
        elif cx < COMP_HI:
            comp.append((x0, txt))
        else:
            row["nafasi"] = txt
    row["wilaya"] = " ".join(t for _, t in sorted(wil))
    row["school"] = " ".join(t for _, t in sorted(sch))
    row["competency"] = " ".join(t for _, t in sorted(comp))
    return row


def extract():
    doc = pymupdf.open(SRC)
    sections = []
    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            text = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
            if "SHULE KUMI BORA" in text or "SHULE KUMI DUNI" in text:
                page_top = not any(s.get("_page") == pi for s in sections)
                sections.append({"title": text, "rows": [], "page_top": page_top, "_page": pi})
                continue
            if not sections:
                continue
            sl = sorted(line, key=lambda w: w[0])
            first = sl[0]
            if (first[0] < SN_MAX and first[4].isdigit() and len(first[4]) <= 2
                    and len(sl) > 10):
                sections[-1]["rows"].append(parse_row(sl))
    return sections


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    sections = extract()
    for s in sections:
        s.pop("_page", None)
    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "OFISI YA WAZIRI MKUU",
            "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
            "MKOA WA MWANZA",
        ],
        "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
        "report_title": "SHULE KUMI BORA - MWANZA CC",
        "subjects": [
            "HISABATI", "KISWAHILI", "SAYANSI", "ENGLISH",
            "JIOGRAFIA NA MAZINGIRA", "HISTORIA YA TZ NA MAADILI",
        ],
    }
    data = {"document": document, "sections": sections}
    (OUTDIR / "data.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ref / "original.pdf").write_bytes(SRC.read_bytes())
    print(f"sections={len(sections)} rows={[len(s['rows']) for s in sections]}")


if __name__ == "__main__":
    main()
