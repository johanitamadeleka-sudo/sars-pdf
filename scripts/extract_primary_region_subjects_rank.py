"""Extract MKOA UFAULU MASOMO STD4 (region subject-performance grid) -> data.json.

Region subject-performance grid, one logical row per SUBJECT. The source STAGGERS a
subject's cells across 2-3 physical text lines (the S/N, WASTANI, NAFASI and the Swahili
"Daraja X (...)" competency label frequently wrap onto their own y-lines). We therefore
group every word of a subject into a single logical row by Y-BAND (nearest subject anchor)
and then bin each word into its column by X-CENTRE, so each subject's Daraja label is
associated exactly once (no duplication).

Columns (7 WAV/WAS/JML grade groups + trailing):
  S/N | SOMO | A(WAV/WAS/JML) | B | C | D | A-D(+%) | WASIOFAULU E(+%) | JUMLA YA WATAHINIWA
  | WASTANI WA SOMO | NAFASI YA SOMO | KUNDI LA UMAHIRI

The 1pp JUMLA source is the clean single-page KIMKOA grid used as the report. Extraction is
coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-subjects-rank"

SOURCES = [
    (None, "MKOA UFAULU MASOMO STD4 JUMLA 2026.pdf", "TATHIMINI YA UFAULU WA MASOMO KIMADARAJA KIMKOA"),
]

NUM_COLS = [
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct",
    "jml_f", "jml_m", "jml_t", "wastani", "nafasi",
]
NUM_CENTERS = [
    112.0, 136.1, 160.3, 184.3, 208.4, 232.6, 256.7, 280.8, 305.0, 329.1, 353.2, 377.3,
    401.4, 425.5, 449.7, 473.9, 497.9, 522.0, 546.2, 570.4,
    594.4, 618.5, 642.7, 666.8, 690.7,
]
SN_MAX_X = 38.0
SOMO_MAX_X = 105.0
COMP_MIN_X = 705.0


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


def nearest(cx):
    return min(range(len(NUM_CENTERS)), key=lambda i: abs(cx - NUM_CENTERS[i]))


def data_words(page):
    """All words in the data band (below header, above nothing). Header ends ~y128;
    JUMLA total row is the last band."""
    out = []
    for w in page.get_text("words"):
        y = (w[1] + w[3]) / 2
        if 130.0 <= y <= 212.0:
            out.append(w)
    return out


def find_anchors(words):
    """Subject anchor y = y of each line whose leftmost word is a 1-2 digit S/N (1..6)."""
    anchors = []
    for cy, line in group_lines(words):
        line = sorted(line, key=lambda w: w[0])
        f = line[0]
        cx = (f[0] + f[2]) / 2
        if cx < SN_MAX_X and f[4].strip().isdigit() and 1 <= int(f[4]) <= 8:
            anchors.append((int(f[4]), cy))
    anchors.sort(key=lambda a: a[1])
    return anchors


def assign(words, anchors):
    """Return {sn: {col: text, ...}} by binning each word into its nearest subject band
    (nearest anchor y) then into its column by x-centre."""
    anchor_ys = [y for _, y in anchors]
    rows = {sn: {"sn": str(sn), "somo": "", **{k: "" for k in NUM_COLS},
                 "competency": ""} for sn, _ in anchors}
    somo_parts = {sn: [] for sn, _ in anchors}
    comp_parts = {sn: [] for sn, _ in anchors}
    last_y = max(anchor_ys)
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        y = (w[1] + w[3]) / 2
        if y > last_y + 6.5:
            continue  # belongs to the JUMLA total band, handled separately
        # nearest anchor
        bi = min(range(len(anchor_ys)), key=lambda i: abs(y - anchor_ys[i]))
        sn = anchors[bi][0]
        if cx < SN_MAX_X and txt.strip().isdigit() and 1 <= int(txt) <= 8:
            continue  # the S/N marker itself
        if cx < SOMO_MAX_X:
            somo_parts[sn].append((x0, txt))
        elif cx >= COMP_MIN_X:
            comp_parts[sn].append((x0, txt))
        else:
            rows[sn][NUM_COLS[nearest(cx)]] = txt
    for sn, _ in anchors:
        rows[sn]["somo"] = " ".join(t for _, t in sorted(somo_parts[sn]))
        comp = " ".join(t for _, t in sorted(comp_parts[sn]))
        rows[sn]["competency"] = comp
        rows[sn]["level"] = (competency_letter(comp) or "").upper() or None
    return [rows[sn] for sn, _ in anchors]


def parse_total(words, anchors):
    """The JUMLA total line sits just below the last subject band; collect words with
    y greater than the last anchor + ~6 and bin by column."""
    last_y = max(y for _, y in anchors)
    tot = {k: "" for k in NUM_COLS}
    comp_parts = []
    for w in words:
        y = (w[1] + w[3]) / 2
        cx = (w[0] + w[2]) / 2
        if y <= last_y + 6.5:
            continue
        if cx < SOMO_MAX_X:
            continue
        if cx >= COMP_MIN_X:
            comp_parts.append((w[0], w[4]))
        else:
            tot[NUM_COLS[nearest(cx)]] = w[4]
    comp = " ".join(t for _, t in sorted(comp_parts))
    tot["competency"] = comp
    tot["level"] = (competency_letter(comp) or "").upper() or None
    return tot


def extract(src):
    doc = pymupdf.open(src)
    page = doc[0]
    words = data_words(page)
    anchors = find_anchors(words)
    rows = assign(words, anchors)
    total = parse_total(words, anchors)
    return rows, total


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title in SOURCES:
        src = SRCDIR / name
        rows, total = extract(src)
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
        data = {"document": document,
                "sections": [{"title": title, "rows": rows, "total": total}]}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        print(f"[{tag or 'main'}] subjects={len(rows)} -> {out.name}")
        for r in rows:
            print(f"   {r['sn']} {r['somo']:<26} jml_t={r['jml_t']:>7} "
                  f"wastani={r['wastani']:>6} nafasi={r['nafasi']:>3} comp={r['competency']}")
        print(f"   JUMLA jml_t={total['jml_t']} wastani={total['wastani']} comp={total['competency']}")


if __name__ == "__main__":
    main()
