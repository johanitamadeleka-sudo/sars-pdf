"""Extract MKOA SHULE 10 BORA (region top-10 schools per subject) -> data.json / data_<tag>.

Two source PDFs share ONE structure (data tags):
  * jumla    : MKOA SHULE BORA MASOMO STD4 JUMLA 2026.pdf  (all schools)
  * serikali : MKOA SHULE BORA MASOMO SERIKALI STD4 2026.pdf (government schools)

Each is a section-centric grid: 6 "SHULE 10 BORA ... SOMO LA <subject>" blocks (one per
subject), TWO blocks per page over 3 pages. Pagination is DATA-DRIVEN via s.page_top
(True only for the first block on each source page), reproducing the 2-blocks-per-page
grouping EXACTLY (3 pages).

Columns: S/N | HALMASHAURI | JINA LA SHULE | UMILIKI
  IDADI YA WATAHINIWA (WALIOSAJILIWA, WALIOFANYA) + UFAULU WA MADARAJA (A B C D E(+%) A-D(+%))
  each WAV/WAS/JML | WASTANI WA SOMO (ALAMA + DRJ) | NAFASI

Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter  # noqa: F401

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-top-10-schools-subjectwise"

SOURCES = [
    ("jumla", "MKOA SHULE BORA MASOMO STD4 JUMLA 2026.pdf"),
    ("serikali", "MKOA SHULE BORA MASOMO SERIKALI STD4 2026.pdf"),
]

NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "e_f", "e_m", "e_t", "e_pct", "ad_f", "ad_m", "ad_t", "ad_pct",
    "alama", "drj",
]

# Per-layout measured geometry. The JUMLA source has an UMILIKI column; the SERIKALI
# source does NOT (its numerics start ~37pt further left).
LAYOUTS = {
    "jumla": {
        "has_own": True,
        "num_centers": [
            229.1, 250.0, 270.8, 291.7, 312.6, 333.5, 353.1, 371.3, 389.5,
            407.8, 426.0, 444.2, 462.5, 480.8, 499.0, 517.3, 535.5, 553.7,
            572.0, 590.2, 608.4, 626.8, 644.9, 663.2, 681.4, 699.7,
            725.8, 753.2,
        ],
        "sn_max_x": 40.0, "council_max_x": 100.0, "school_max_x": 190.0,
        "own_max_x": 218.0, "nafasi_c": 772.8,
    },
    "serikali": {
        "has_own": False,
        "num_centers": [
            192.0, 213.8, 235.7, 257.5, 279.4, 301.2, 321.5, 340.5, 359.5,
            378.4, 397.4, 416.4, 435.3, 454.3, 473.3, 492.2, 511.2, 530.2,
            549.1, 568.1, 587.1, 606.0, 624.9, 643.9, 662.9, 684.4,
            713.9, 742.6,
        ],
        "sn_max_x": 42.0, "council_max_x": 105.0, "school_max_x": 182.0,
        "own_max_x": 182.0, "nafasi_c": 765.0,
    },
}


def nearest(cx, centers):
    return min(range(len(centers)), key=lambda i: abs(cx - centers[i]))


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


def parse_row(line, cfg):
    keys = ["sn", "council", "school", "ownership", *NUM_COLS, "nm"]
    row = {k: "" for k in keys}
    council_parts, school_parts = [], []
    centers = cfg["num_centers"]
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < cfg["sn_max_x"]:
            row["sn"] = txt
        elif cx < cfg["council_max_x"]:
            council_parts.append((x0, txt))
        elif cx < cfg["school_max_x"]:
            school_parts.append((x0, txt))
        elif cfg["has_own"] and cx < cfg["own_max_x"]:
            row["ownership"] = txt
        elif cx >= cfg["nafasi_c"] - 12:
            row["nm"] = txt
        else:
            row[NUM_COLS[nearest(cx, centers)]] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    return row


def extract(src, cfg):
    doc = pymupdf.open(src)
    sections = []
    cur = None
    for pi in range(doc.page_count):
        page_started = False
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line).strip()
            first = line[0]
            fcx = (first[0] + first[2]) / 2
            if text.startswith("SHULE 10 BORA"):
                cur = {"title": text, "page": pi, "page_top": not page_started,
                       "has_own": cfg["has_own"], "rows": []}
                page_started = True
                sections.append(cur)
            elif (fcx < cfg["sn_max_x"] and first[4].isdigit() and len(first[4]) <= 2
                  and len(line) > 18 and cur is not None):
                cur["rows"].append(parse_row(line, cfg))
    return [s for s in sections if s["rows"]]


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name in SOURCES:
        src = SRCDIR / name
        cfg = LAYOUTS[tag]
        sections = extract(src, cfg)
        title = "SHULE 10 BORA ZA SERIKALI MKOA" if tag == "serikali" else "SHULE 10 BORA MKOA"
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
            print(f"   p{s['page']+1} top={s['page_top']} {s['title'][:48]:<48} "
                  f"{len(s['rows'])} rows; first={s['rows'][0]['school']}")


if __name__ == "__main__":
    main()
