"""Extract HALMASHAURI MASOMO STD4 (region per-council subject-performance) -> data.json.

Section-centric per-council subject grid: 6 "MPANGILIO WA UFAULU WA HALMASHAURI SOMO LA
<subject>" blocks, ONE block per page over 6 pages (each block lists all councils). The
source STAGGERS the IDADI YA SHULE value and WASTANI WA SOMO / KUNDI label onto a second
physical y-line per council, so each council row is assembled by Y-BAND (nearest council
anchor) then X-CENTRE binning.

Columns: NA. | HALMASHAURI | IDADI YA SHULE
  WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D  (WAV/WAS/JML)  A-D(+%) WASIOFAULU E(+%)
  | WASTANI WA SOMO | KUNDI LA UMAHIRI

Pagination is DATA-DRIVEN (one section per page; page_top True for all but the first).
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
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-district-performance"

SOURCES = [
    (None, "HALMASHAURI MASOMO STD4 2026.pdf"),
]

# 30 numeric columns: 7 WAV/WAS/JML triplets (reg fanya nof a b c d) then A-D(+%) E(+%)
# then WASTANI WA SOMO. The WASTANI value sits under the trailing "WA SOMO" header, right
# of the last "%".
NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "nof_f", "nof_m", "nof_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct",
]


def page_geometry(page):
    """Derive per-page column centres from the WAV/WAS/JML/% header row (the source
    shifts the whole grid right on some pages, so measure it per page)."""
    hdr = None
    for cy, line in group_lines(page.get_text("words")):
        if sum(1 for w in line if w[4] == "WAV") >= 6:
            hdr = sorted(line, key=lambda w: w[0])
            break
    if hdr is None:
        return None
    centers = [(w[0] + w[2]) / 2 for w in hdr if w[4] in ("WAV", "WAS", "JML", "%")]
    # 29 grade cells (WAV/WAS/JML x7 = 21, + %(A-D) + %(E) ... but headers give 21 + 2 %).
    # Map them to the first 29 NUM_COLS by order; WASTANI is right of the last cell.
    na_c = next(((w[0] + w[2]) / 2 for w in hdr if w[4] == "NA."), 25.0)
    first_grade = centers[0]
    council_max = (na_c + first_grade) / 2 - 8
    return {"centers": centers, "na_c": na_c, "council_max": council_max}


def nearest(cx, centers):
    return min(range(len(centers)), key=lambda i: abs(cx - centers[i]))


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


def parse_block(page):
    geo = page_geometry(page)
    if geo is None:
        return []
    centers = geo["centers"]
    na_max = geo["na_c"] + 12
    council_max = geo["council_max"]
    first_grade = centers[0]
    idadi_min = council_max
    idadi_max = first_grade - 8
    last_grade = centers[-1]
    wastani_c = last_grade + 24
    comp_min = wastani_c + 18

    lines = group_lines(page.get_text("words"))
    anchors = []
    jumla_y = None
    asilimia_y = None
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        f = line[0]
        fcx = (f[0] + f[2]) / 2
        txt = " ".join(w[4] for w in line)
        if txt.startswith("JUMLA"):
            jumla_y = cy
        elif txt.startswith("ASILIMIA"):
            asilimia_y = cy
        elif fcx < na_max and f[4].isdigit() and len(f[4]) <= 2 and len(line) > 20:
            anchors.append(cy)
    anchors.sort()
    if not anchors:
        return []
    lo = anchors[0] - 5
    hi = anchors[-1] + 6.5
    rows = [{"na": "", "council": "", "idadi": "", **{k: "" for k in NUM_COLS},
             "wastani": "", "competency": ""} for _ in anchors]
    council_parts = [[] for _ in anchors]
    comp_parts = [[] for _ in anchors]
    for w in page.get_text("words"):
        x0, x1, txt = w[0], w[2], w[4]
        y = (w[1] + w[3]) / 2
        if y < lo or y > hi:
            continue
        cx = (x0 + x1) / 2
        bi = min(range(len(anchors)), key=lambda i: abs(y - anchors[i]))
        r = rows[bi]
        if cx < na_max:
            if txt.isdigit() and len(txt) <= 2:
                r["na"] = txt
        elif cx < idadi_min:
            council_parts[bi].append((x0, txt))
        elif cx < idadi_max:
            r["idadi"] = txt
        elif cx >= comp_min:
            comp_parts[bi].append((x0, txt))
        elif cx >= wastani_c - 12:
            r["wastani"] = txt
        else:
            r[NUM_COLS[nearest(cx, centers)]] = txt
    for i, r in enumerate(rows):
        r["council"] = " ".join(t for _, t in sorted(council_parts[i]))
        comp = " ".join(t for _, t in sorted(comp_parts[i]))
        r["competency"] = comp
        r["level"] = (competency_letter(comp) or "").upper() or None

    total = None
    if jumla_y is not None:
        total = _band_row(page, jumla_y, na_max, council_max, idadi_min, idadi_max,
                          wastani_c, comp_min, centers, hi_lo=anchors[-1] + 6.6)
    asilimia = None
    if asilimia_y is not None:
        asilimia = _band_row(page, asilimia_y, na_max, council_max, idadi_min, idadi_max,
                             wastani_c, comp_min, centers,
                             hi_lo=(jumla_y + 6.6) if jumla_y else anchors[-1] + 12,
                             label_prefix=True)
    return {"rows": rows, "total": total, "asilimia": asilimia}


def _band_row(page, anchor_y, na_max, council_max, idadi_min, idadi_max, wastani_c,
              comp_min, centers, hi_lo, label_prefix=False):
    """Assemble a single staggered summary row (JUMLA / ASILIMIA) whose cells span the
    lines at/after anchor_y (its label + the numeric line just below it)."""
    r = {"na": "", "council": "", "idadi": "", **{k: "" for k in NUM_COLS},
         "wastani": "", "competency": ""}
    council_parts, comp_parts = [], []
    for w in page.get_text("words"):
        y = (w[1] + w[3]) / 2
        if y < hi_lo or y > anchor_y + 6.6:
            continue
        cx = (w[0] + w[2]) / 2
        txt = w[4]
        if cx < idadi_min:
            council_parts.append((w[0], txt))
        elif cx < idadi_max:
            r["idadi"] = txt
        elif cx >= comp_min:
            comp_parts.append((w[0], txt))
        elif cx >= wastani_c - 12:
            r["wastani"] = txt
        else:
            r[NUM_COLS[nearest(cx, centers)]] = txt
    r["council"] = " ".join(t for _, t in sorted(council_parts))
    comp = " ".join(t for _, t in sorted(comp_parts))
    r["competency"] = comp
    r["level"] = (competency_letter(comp) or "").upper() or None
    return r


def block_title(page):
    for cy, line in group_lines(page.get_text("words")):
        txt = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
        if txt.startswith("MPANGILIO"):
            return txt
    return ""


def extract(src):
    doc = pymupdf.open(src)
    sections = []
    for pi in range(doc.page_count):
        parsed = parse_block(doc[pi])
        if parsed and parsed["rows"]:
            sections.append({"title": block_title(doc[pi]), "page": pi,
                             "page_top": pi > 0, "rows": parsed["rows"],
                             "total": parsed["total"], "asilimia": parsed["asilimia"]})
    return sections


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name in SOURCES:
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
            "report_title": "MPANGILIO WA UFAULU WA HALMASHAURI",
        }
        data = {"document": document, "sections": sections}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        print(f"[{tag or 'main'}] sections={len(sections)} -> {out.name}")
        for s in sections:
            tot = s["total"]
            asi = s["asilimia"]
            print(f"   p{s['page']+1} top={s['page_top']} {s['title'][:40]:<40} "
                  f"{len(s['rows'])} rows; total.jml_t={tot['reg_t'] if tot else '-'} "
                  f"total.wastani={tot['wastani'] if tot else '-'} "
                  f"asilimia.a_t={asi['a_t'] if asi else '-'}")


if __name__ == "__main__":
    main()
