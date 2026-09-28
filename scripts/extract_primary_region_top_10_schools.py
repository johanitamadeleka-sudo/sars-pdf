"""Extract MKOA SHULE KUMI BORA / DUNI (region top-schools) -> data.json.

This region source packs TWO "SHULE KUMI ..." blocks onto every page (10 blocks over
5 pages) and MIXES two physical layouts:

  * "grid" layout (source pages 1-3, 6 blocks): the WAV/WAS/JML division grid
      S/N | HALMASHAURI | JINA LA SHULE | UMILIKI
      + 8 WAV/WAS/JML grade groups (NO WASIOFANYA) + WASTANI /300 + KUNDI + NAFASI
  * "subj" layout (source pages 4-5, 4 blocks): the per-subject AL/DRJ marks grid
      S/N | WILAYA | KATA | JINA LA SHULE | UMILIKI
      + 6 subjects (AL avg + DRJ) + WASTANI WA UFAULU/300 + WASTANI/50 + DARAJA
      + KUNDI LA UMAHIRI + NAFASI

Pagination is DATA-DRIVEN: each section carries its source-page index and a `page_top`
hint (True only for the first block on each source page) so the template reproduces the
original's block-to-page grouping EXACTLY (5 pages, 2 blocks each), instead of forcing one
block per page. Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter  # noqa: F401  (kept for parity/future use)

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-top-10-schools"

SOURCES = [
    (None, "MKOA SHULE BORA STD4 JUMLA 2026.pdf", "SHULE KUMI BORA MKOA"),
]

# ---------------------------------------------------------------- grid layout
GRID_NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]
GRID_NUM_CENTERS = [
    195.4, 211.3, 227.3, 243.3, 259.2, 275.1, 291.1, 307.1, 323.0,
    339.0, 355.0, 370.9, 386.9, 402.9, 418.8, 434.8, 450.8, 466.7,
    484.4, 503.7, 522.5, 543.9, 565.9, 585.2, 604.1, 624.2, 654.0,
]
GRID_SN_MAX_X = 40.0
GRID_COUNCIL_MAX_X = 90.0
GRID_SCHOOL_MAX_X = 165.0
GRID_OWN_MAX_X = 190.0
GRID_COMP_MIN_X = 680.0
GRID_NAFASI_C = 758.6

# ---------------------------------------------------------------- subj layout
SUBJ_KEYS = ["hisabati", "kiswahili", "sayansi", "english", "jiografia", "historia"]
# AL / DRJ x-centres measured from source pages 4-5.
SUBJ_AL_C = [309.0, 351.0, 393.0, 435.0, 474.0, 516.0]
SUBJ_DRJ_C = [330.0, 372.0, 414.0, 453.0, 495.0, 537.0]
SUBJ_SN_MAX_X = 72.0
SUBJ_WILAYA_MAX_X = 135.0
SUBJ_KATA_MAX_X = 175.0
SUBJ_SCHOOL_MAX_X = 255.0
SUBJ_OWN_MAX_X = 295.0
SUBJ_UFAULU_C = 564.0
SUBJ_WASTANI_C = 594.0
SUBJ_DARAJA_C = 615.0
SUBJ_COMP_MIN_X = 628.0
SUBJ_NAFASI_C = 717.0


def nearest(cx, names, centers):
    best, bd = None, 1e9
    for name, c in zip(names, centers):
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


def parse_grid_row(line):
    keys = ["sn", "council", "school", "ownership", *GRID_NUM_COLS, "competency", "nm"]
    row = {k: "" for k in keys}
    council_parts, school_parts, comp_parts = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < GRID_SN_MAX_X:
            row["sn"] = txt
        elif cx < GRID_COUNCIL_MAX_X:
            council_parts.append((x0, txt))
        elif cx < GRID_SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx < GRID_OWN_MAX_X:
            row["ownership"] = txt
        elif cx >= GRID_NAFASI_C - 10:
            row["nm"] = txt
        elif cx >= GRID_COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[nearest(cx, GRID_NUM_COLS, GRID_NUM_CENTERS)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    row["level"] = _level_of(row["competency"])
    return row


def parse_subj_row(line):
    keys = ["sn", "wilaya", "kata", "school", "ownership"]
    for k in SUBJ_KEYS:
        keys += [k + "_al", k + "_g"]
    keys += ["ufaulu", "wastani", "daraja", "competency", "nm"]
    row = {k: "" for k in keys}
    wil_parts, kata_parts, school_parts, comp_parts = [], [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SUBJ_SN_MAX_X:
            row["sn"] = txt
        elif cx < SUBJ_WILAYA_MAX_X:
            wil_parts.append((x0, txt))
        elif cx < SUBJ_KATA_MAX_X:
            kata_parts.append((x0, txt))
        elif cx < SUBJ_SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx < SUBJ_OWN_MAX_X:
            row["ownership"] = txt
        elif cx < SUBJ_UFAULU_C - 12:
            # a subject AL or DRJ cell
            ai = _idx(cx, SUBJ_AL_C)
            di = _idx(cx, SUBJ_DRJ_C)
            if abs(cx - SUBJ_AL_C[ai]) <= abs(cx - SUBJ_DRJ_C[di]):
                row[SUBJ_KEYS[ai] + "_al"] = txt
            else:
                row[SUBJ_KEYS[di] + "_g"] = txt
        elif cx < SUBJ_WASTANI_C - 10:
            row["ufaulu"] = txt
        elif cx < SUBJ_DARAJA_C - 8:
            row["wastani"] = txt
        elif cx < SUBJ_COMP_MIN_X:
            row["daraja"] = txt
        elif cx >= SUBJ_NAFASI_C - 12:
            row["nm"] = txt
        else:
            comp_parts.append((x0, txt))
    row["wilaya"] = " ".join(t for _, t in sorted(wil_parts))
    row["kata"] = " ".join(t for _, t in sorted(kata_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    row["level"] = _level_of(row["competency"])
    return row


def _idx(cx, centers):
    return min(range(len(centers)), key=lambda i: abs(cx - centers[i]))


def _level_of(comp):
    """Stamp an explicit single-letter competency level from the Swahili 'Daraja X (...)'
    label so the data-driven KUNDI LA UMAHIRI colour is correct even on aggregate rows."""
    try:
        return (competency_letter(comp) or "").upper() or None
    except Exception:
        return None


def extract(src):
    """Walk lines page-by-page. A 'SHULE KUMI ...' title starts a new section; the section's
    layout is decided by the S/N x-position of its first data row (grid S/N ~x24 vs subj
    S/N ~x58). page_top is True for the first block on each page."""
    doc = pymupdf.open(src)
    sections = []
    cur = None
    for pi in range(doc.page_count):
        page_started = False
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line).strip()
            first = line[0]
            if text.startswith("SHULE KUMI"):
                cur = {"title": text, "page": pi, "page_top": not page_started, "rows": []}
                page_started = True
                sections.append(cur)
            elif first[0] < 72.0 and first[4].isdigit() and len(first[4]) <= 3 and len(line) > 15:
                if cur is None:
                    continue
                if first[0] < GRID_SN_MAX_X:
                    cur["layout"] = "grid"
                    cur["rows"].append(parse_grid_row(line))
                else:
                    cur["layout"] = "subj"
                    cur["rows"].append(parse_subj_row(line))
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
            "subjects": ["HISABATI", "KISWAHILI", "SAYANSI", "ENGLISH",
                         "JIOGRAFIA & MAZINGIRA", "HISTORIA YA TZ & MAADILI"],
        }
        data = {"document": document, "sections": sections}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        nrows = sum(len(s["rows"]) for s in sections)
        print(f"[{tag or 'main'}] sections={len(sections)} rows={nrows} -> {out.name}")
        for s in sections:
            print(f"   p{s['page']+1} top={s['page_top']} [{s.get('layout')}] "
                  f"{s['title']} :: {len(s['rows'])} rows; first={s['rows'][0]['school']}")


if __name__ == "__main__":
    main()
