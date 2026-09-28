"""Extract MWANZA CC 10 BEST STUDENTS (primary STD4) into data.json (display strings).

Section-centric: stacked "WANAFUNZI KUMI BORA ..." top-10 blocks (JUMLA / WAVULANA /
WASICHANA, and the SHULE ZA SERIKALI variants), each block holding 10 candidates. Per
candidate: S/N | WILAYA | JINA LA SHULE | UMILIKI | NAMBA YA MTAHINIWA | JINA LA
MWANAFUNZI | JINSI | six subjects (AL marks + DRJ grade each: HISABATI, KISWAHILI,
SAYANSI, ENGLISH, JIOGRAFIA NA MAZINGIRA, HISTORIA YA TZ NA MAADILI) | JUMLA | WASTANI |
DARAJA | NAFASI | KUNDI LA UMAHIRI (Daraja X (...)).

Extraction is coordinate based (pymupdf words), never hand-typed. Each subject grade is a
single letter carried as row.<subject>_g so render.py colours it via the section handling.

    python scripts/extract_primary_council_best_students_overall.py
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "primary_council_pdf" / "primary_council_pdf" / "MWANZA CC 10 BEST STUDENTS.pdf"
OUTDIR = ROOT / "reports" / "primary" / "council" / "primary-council-best-students-overall"

SUBJECTS = ["hisabati", "kiswahili", "sayansi", "english", "jiografia", "historia"]
# (al_centre, drj_centre) per subject, measured from the page-1 header AL/DRJ row.
SUBJ_CENTERS = [
    (393.6, 411.4), (429.2, 447.0), (464.7, 482.5),
    (500.2, 518.0), (535.7, 553.5), (571.3, 589.1),
]

# text/aggregate column boundaries (x-centre based)
SN_MAX = 60.0
WILAYA_MAX = 100.0
SCHOOL_MAX = 175.0
OWN_MAX = 215.0
NAMBA_MAX = 258.0
CAND_MAX = 372.0
JINSI_MAX = 388.0
SUBJ_LO = 385.0
SUBJ_HI = 600.0
JUMLA_C = 609.4
WASTANI_C = 632.5
DARAJA_C = 654.1
NAFASI_C = 674.7
COMP_MIN = 686.0


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
    """Return (subject_index, 'al'|'drj') for an x-centre in the subject band."""
    best, bd, kind = None, 1e9, None
    for i, (al, drj) in enumerate(SUBJ_CENTERS):
        if abs(cx - al) < bd:
            best, bd, kind = i, abs(cx - al), "al"
        if abs(cx - drj) < bd:
            best, bd, kind = i, abs(cx - drj), "drj"
    return best, kind


def parse_row(line):
    row = {"sn": "", "wilaya": "", "school": "", "ownership": "", "namba": "",
           "candidate": "", "jinsi": "", "jumla": "", "wastani": "", "daraja": "",
           "nafasi": "", "competency": ""}
    for s in SUBJECTS:
        row[f"{s}_al"] = ""
        row[f"{s}_g"] = ""
    wil, sch, nam, cand, comp = [], [], [], [], []
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
        elif cx < CAND_MAX and (cx < NAMBA_MAX or txt.startswith("PS")):
            nam.append((x0, txt))
        elif cx < CAND_MAX:
            cand.append((x0, txt))
        elif cx < JINSI_MAX:
            row["jinsi"] = txt
        elif SUBJ_LO <= cx <= SUBJ_HI:
            i, kind = subj_col(cx)
            s = SUBJECTS[i]
            if kind == "al":
                row[f"{s}_al"] = txt
            else:
                row[f"{s}_g"] = txt
        elif cx < WASTANI_C - 8:
            row["jumla"] = txt
        elif cx < DARAJA_C - 8:
            row["wastani"] = txt
        elif cx < NAFASI_C - 8:
            row["daraja"] = txt
        elif cx < COMP_MIN:
            row["nafasi"] = txt
        else:
            comp.append((x0, txt))
    row["wilaya"] = " ".join(t for _, t in sorted(wil))
    row["school"] = " ".join(t for _, t in sorted(sch))
    row["namba"] = " ".join(t for _, t in sorted(nam))
    row["candidate"] = " ".join(t for _, t in sorted(cand))
    row["competency"] = " ".join(t for _, t in sorted(comp))
    return row


def extract():
    doc = pymupdf.open(SRC)
    sections = []
    for pi in range(doc.page_count):
        lines = group_lines(doc[pi].get_text("words"))
        cur = None
        for cy, line in lines:
            text = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
            if "WANAFUNZI KUMI BORA" in text:
                # page_top mirrors the original's own pagination: a section starts a new
                # page when it is the FIRST section printed on its source PDF page.
                page_top = not any(s.get("_page") == pi for s in sections)
                cur = {"title": text, "rows": [], "page_top": page_top, "_page": pi}
                sections.append(cur)
                continue
            if cur is None:
                continue
            sl = sorted(line, key=lambda w: w[0])
            first = sl[0]
            # data rows begin with a 1-2 digit S/N in the far-left column and are wide.
            if (first[0] < SN_MAX and first[4].isdigit() and len(first[4]) <= 2
                    and len(sl) > 12):
                cur["rows"].append(parse_row(sl))
    return sections


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    sections = extract()
    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "OFISI YA WAZIRI MKUU",
            "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
            "MKOA WA MWANZA",
        ],
        "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
        "report_title": "WANAFUNZI KUMI BORA - MWANZA CC",
        "blocks_per_page": 2,
        "subjects": [
            "HISABATI", "KISWAHILI", "SAYANSI", "ENGLISH",
            "JIOGRAFIA NA MAZINGIRA", "HISTORIA YA TZ NA MAADILI",
        ],
    }
    for s in sections:
        s.pop("_page", None)
    data = {"document": document, "sections": sections}
    (OUTDIR / "data.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ref / "original.pdf").write_bytes(SRC.read_bytes())
    print(f"sections={len(sections)} rows={[len(s['rows']) for s in sections]}")


if __name__ == "__main__":
    main()
