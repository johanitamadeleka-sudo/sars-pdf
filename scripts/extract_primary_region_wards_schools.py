"""Extract MKOA KATA SHULE (region per-ward school-performance) -> data_<tag>.json.

Two source PDFs share ONE structure (data tags):
  * serikali : MKOA KATA SHULE ZA SERIKALI STD4 2026.pdf (government, 4pp)
  * binafsi  : MKOA KATA SHULE BINAFSI STD4 2026.pdf     (private, 2pp)

Flat continuous per-ward (KATA) grid running across all pages. Each row aggregates one
ward: NA. | HALMASHAURI | KATA | IDADI YA SHULE(count) then 9 WAV/WAS/JML grade groups
(WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D UFAULU(A-D)(+%) E(+%)) | WASTANI WA MKOA |
KUNDI LA UMAHIRI | NAFASI. The source STAGGERS the IDADI YA SHULE count, WASTANI and the
"Daraja X (...)" competency label onto a second physical line, so each ward row is
assembled by Y-BAND (nearest ward anchor) then X-CENTRE binning. Column centres are
derived per-page from the WAV/WAS/JML header (the grid geometry is stable here but this
keeps the extractor robust). Pagination is data-driven via WeasyPrint's automatic row
overflow with a repeating <thead>. Extraction is coordinate based, never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-wards-schools"

SOURCES = [
    ("serikali", "MKOA KATA SHULE ZA SERIKALI STD4 2026.pdf",
     "MPANGILIO WA UFAULU WA KATA SHULE ZA SERIKALI KIMKOA"),
    ("binafsi", "MKOA KATA SHULE BINAFSI STD4 2026.pdf",
     "MPANGILIO WA UFAULU WA KATA - SHULE ZISIZO ZA SERIKALI KIMKOA"),
]

# 29 grade cells in header order (7 triplets + A-D triplet+% + E triplet+%).
NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "nof_f", "nof_m", "nof_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct",
]
NA_MAX_X = 38.0
KUNDI_LABEL = "KUNDI"


def group_lines(words, y_tol=2.4):
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


def page_geometry(page):
    hdr = None
    for cy, line in group_lines(page.get_text("words")):
        if sum(1 for w in line if w[4] == "WAV") >= 6:
            hdr = sorted(line, key=lambda w: w[0])
            break
    if hdr is None:
        return None
    centers = [(w[0] + w[2]) / 2 for w in hdr if w[4] in ("WAV", "WAS", "JML", "%")]
    # locate the label header row (NA. HALMASHAURI KATA SHULE ... UFAULU KUNDI ...)
    lbl = None
    for cy, line in group_lines(page.get_text("words")):
        txts = [w[4] for w in line]
        if "KATA" in txts and "SHULE" in txts and "NA." in txts:
            lbl = sorted(line, key=lambda w: w[0])
            break
    def cx_of(name, default):
        if lbl:
            for w in lbl:
                if w[4] == name:
                    return (w[0] + w[2]) / 2
        return default
    na_c = cx_of("NA.", 25.0)
    kata_c = cx_of("KATA", 107.0)
    shule_c = cx_of("SHULE", 148.0)
    first_grade = centers[0]
    last_grade = centers[-1]
    return {
        "centers": centers,
        "na_max": na_c + 12,
        "council_max": (na_c + kata_c) / 2,
        "kata_max": (kata_c + shule_c) / 2 + 6,
        "idadi_max": first_grade - 8,
        "wastani_c": last_grade + 26,
        "comp_min": last_grade + 44,
        "nafasi_min": None,  # set below relative to comp
    }


def nearest(cx, centers):
    return min(range(len(centers)), key=lambda i: abs(cx - centers[i]))


def extract(src):
    doc = pymupdf.open(src)
    all_rows = []
    for pi in range(doc.page_count):
        page = doc[pi]
        geo = page_geometry(page)
        if geo is None:
            continue
        centers = geo["centers"]
        lines = group_lines(page.get_text("words"))
        anchors = []
        for cy, line in lines:
            line = sorted(line, key=lambda w: w[0])
            f = line[0]
            fcx = (f[0] + f[2]) / 2
            if fcx < geo["na_max"] and f[4].isdigit() and len(f[4]) <= 3 and len(line) > 22:
                anchors.append(cy)
        anchors.sort()
        if not anchors:
            continue
        lo = anchors[0] - 6
        hi = anchors[-1] + 7.0
        rows = [{"na": "", "council": "", "kata": "", "idadi": "",
                 **{k: "" for k in NUM_COLS}, "wastani": "", "competency": "", "nm": ""}
                for _ in anchors]
        council_parts = [[] for _ in anchors]
        kata_parts = [[] for _ in anchors]
        comp_parts = [[] for _ in anchors]
        nafasi_min = geo["comp_min"] + 62
        for w in page.get_text("words"):
            y = (w[1] + w[3]) / 2
            if y < lo or y > hi:
                continue
            cx = (w[0] + w[2]) / 2
            txt = w[4]
            bi = min(range(len(anchors)), key=lambda i: abs(y - anchors[i]))
            r = rows[bi]
            if cx < geo["na_max"]:
                if txt.isdigit() and len(txt) <= 3:
                    r["na"] = txt
            elif cx < geo["council_max"]:
                council_parts[bi].append((w[0], txt))
            elif cx < geo["kata_max"]:
                kata_parts[bi].append((w[0], txt))
            elif cx < geo["idadi_max"]:
                r["idadi"] = txt
            elif cx >= nafasi_min:
                r["nm"] = txt
            elif cx >= geo["comp_min"]:
                comp_parts[bi].append((w[0], txt))
            elif cx >= geo["wastani_c"] - 14:
                r["wastani"] = txt
            else:
                r[NUM_COLS[nearest(cx, centers)]] = txt
        for i, r in enumerate(rows):
            r["council"] = " ".join(t for _, t in sorted(council_parts[i]))
            r["kata"] = " ".join(t for _, t in sorted(kata_parts[i]))
            comp = " ".join(t for _, t in sorted(comp_parts[i]))
            r["competency"] = comp
            r["level"] = (competency_letter(comp) or "").upper() or None
        all_rows.extend(rows)
    return all_rows


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title in SOURCES:
        src = SRCDIR / name
        rows = extract(src)
        document = {
            "page_size": "Letter-landscape",
            "ministry": [
                "OFISI YA WAZIRI MKUU",
                "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
                "MKOA WA MWANZA",
            ],
            "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA DARASA LA IV MWEZI AGOSTI, 2026",
            "report_title": title,
        }
        data = {"document": document, "rows": rows}
        out = OUTDIR / f"data_{tag}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original_{tag}.pdf").write_bytes(src.read_bytes())
        print(f"[{tag}] rows={len(rows)} -> {out.name}")
        for r in rows[:3]:
            print(f"   {r['na']} {r['council']:<14} {r['kata']:<14} idadi={r['idadi']:>3} "
                  f"reg_t={r['reg_t']:>5} wastani={r['wastani']:>8} nm={r['nm']:>3} "
                  f"comp={r['competency']}")


if __name__ == "__main__":
    main()
