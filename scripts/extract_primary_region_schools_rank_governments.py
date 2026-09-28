"""Extract MKOA government / private schools rank grids -> data*.json (display strings).

Two sources share ONE report TYPE (region schools rank, by ownership) but have their
own physical column x-centres, so each tag carries its own measured NUM_CENTERS:
  * SERIKALI (government, 15pp) -> data.json / original.pdf
  * BINAFSI  (private, 4pp)     -> data_binafsi.json / original_binafsi.pdf

Layout (both): S/N | HALMASHAURI | JINA LA SHULE (NO KATA, NO UMILIKI)
  WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D WALIOFAULU(A-D)(+%) E(+%)
  (each triplet WAV=girls WAS=boys JML=total)
  WASTANI WA SHULE /300 | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI KIMKOA (single rank)

A SUMMARY block (+ ASILIMIA% row) sits above the main per-school table.
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
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-schools-rank-governments"

NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "sifanya_f", "sifanya_m", "sifanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]

# Per-tag geometry measured from each source's own reference (page 1).
SERIKALI_CENTERS = [
    150.1, 168.8, 186.9, 204.4, 221.9, 239.4, 256.0, 271.2, 286.1,
    301.3, 316.6, 331.5, 347.7, 365.2, 382.7, 400.2, 417.7, 435.3,
    451.8, 467.1, 483.4, 500.9, 518.4, 535.9, 558.1, 579.4, 594.6, 609.5, 625.7, 664.5,
]
BINAFSI_CENTERS = [
    178.8, 196.3, 213.8, 231.4, 248.9, 266.4, 283.0, 298.8, 314.0,
    330.2, 347.8, 365.3, 382.8, 400.2, 417.8, 434.5, 450.2, 465.4,
    480.8, 496.5, 511.8, 528.0, 545.5, 563.0, 585.0, 606.0, 621.7, 637.0, 653.7, 678.8,
]

SOURCES = [
    (None, "SHULE SERIKALI STD4 2026.pdf",
     "MPANGILIO WA UFAULU WA SHULE ZA SERIKALI MKOA", SERIKALI_CENTERS,
     dict(SN_MAX_X=33.0, COUNCIL_MAX_X=72.0, SCHOOL_MAX_X=145.0,
          COMP_MIN_X=690.0, NAFASI_C=751.7)),
    ("binafsi", "SHULE BINAFSI STD4 2026.pdf",
     "UFAULU WA SHULE ZA BINAFSI MKOA", BINAFSI_CENTERS,
     dict(SN_MAX_X=33.0, COUNCIL_MAX_X=78.0, SCHOOL_MAX_X=170.0,
          COMP_MIN_X=700.0, NAFASI_C=760.0)),
]


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


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


class Geo:
    def __init__(self, centers, g):
        self.centers = centers
        self.__dict__.update(g)

    def col_for(self, cx):
        best, bd = None, 1e9
        for name, c in zip(NUM_COLS, self.centers):
            if abs(cx - c) < bd:
                best, bd = name, abs(cx - c)
        return best


def parse_row(line, geo):
    keys = ["sn", "council", "school", *NUM_COLS, "competency", "nm"]
    row = {k: "" for k in keys}
    council_parts, school_parts, comp_parts = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < geo.SN_MAX_X:
            row["sn"] = txt
        elif cx < geo.COUNCIL_MAX_X:
            council_parts.append((x0, txt))
        elif cx < geo.SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx >= geo.NAFASI_C - 8:
            row["nm"] = txt
        elif cx >= geo.COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[geo.col_for(cx)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_summary(words, geo):
    row = {k: "" for k in ["shule", *NUM_COLS, "competency"]}
    comp_parts = []
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < geo.centers[0] - 10:
            if _is_num(w[4]):
                row["shule"] = w[4]
        elif cx >= geo.COMP_MIN_X and not _is_num(w[4]):
            comp_parts.append((w[0], w[4]))
        elif _is_num(w[4]):
            row[geo.col_for(cx)] = w[4]
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_asilimia(words, geo):
    # % PASS row: the values sit under the fanya/sifanya/a..e groups. Use the JML
    # centre of each group as the target.
    groups = [
        ("fanya", geo.centers[5]), ("sifanya", geo.centers[8]),
        ("a", geo.centers[11]), ("b", geo.centers[14]), ("c", geo.centers[17]),
        ("d", geo.centers[20]), ("ad", geo.centers[23]), ("e", geo.centers[27]),
    ]
    row = {}
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < geo.centers[0] - 10:
            continue
        best, bd = None, 1e9
        for name, c in groups:
            if abs(cx - c) < bd:
                best, bd = name, abs(cx - c)
        row[best] = w[4]
    return row


def find_header_y(lines):
    for cy, line in lines:
        txt = {w[4] for w in line}
        if "S/N" in txt and "HALMASHAURI" in txt:
            return cy
    return None


def extract(src, geo):
    doc = pymupdf.open(src)
    rows, summary, pct_pass = [], None, None

    p0lines = group_lines(doc[0].get_text("words"))
    header_y = find_header_y(p0lines) or 190.0

    sum_fmt_y = None
    for cy, line in p0lines:
        if cy >= header_y - 12:
            continue
        toks = [w[4] for w in line]
        if toks.count("WAV") + toks.count("WAS") + toks.count("JML") >= 15:
            sum_fmt_y = cy
    if sum_fmt_y is not None:
        val_words, asil_words = [], []
        for cy, line in p0lines:
            if cy <= sum_fmt_y or cy >= header_y - 12:
                continue
            toks = [w[4] for w in line]
            if any(t.startswith("ASILIMIA") for t in toks):
                asil_words += [w for w in line if not w[4].startswith("ASILIMIA")]
            elif not val_words and sum(1 for t in toks if _is_num(t)) >= 8:
                val_words = list(line)
        for cy, line in p0lines:
            if sum_fmt_y < cy < header_y - 12:
                if any(w[4] == "Daraja" for w in line):
                    val_words += list(line)
        if val_words:
            summary = parse_summary(sorted(val_words, key=lambda w: w[0]), geo)
        if asil_words:
            pct_pass = parse_asilimia(sorted(asil_words, key=lambda w: w[0]), geo)

    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            first = line[0]
            if first[0] < geo.SN_MAX_X and first[4].isdigit() and len(first[4]) <= 4 and len(line) > 22:
                rows.append(parse_row(line, geo))
    return rows, summary, pct_pass


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title, centers, g in SOURCES:
        geo = Geo(centers, g)
        src = SRCDIR / name
        rows, summary, pct_pass = extract(src, geo)
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
        data = {"document": document, "summary": summary, "pct_pass": pct_pass,
                "rows": rows, "total": None}
        if isinstance(summary, dict):
            summary["level"] = competency_letter(summary.get("competency"), None)
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        empties = sum(1 for r in rows for k in NUM_COLS if r[k] == "")
        print(f"[{tag or 'serikali'}] rows={len(rows)} empty_num={empties} "
              f"summary={'y' if summary else 'n'} -> {out.name}")
        for r in rows[:2]:
            print(f"   {r['sn']} {r['council']:<12} {r['school']:<24} w={r['wastani']} "
                  f"{r['competency']} M{r['nm']}")


if __name__ == "__main__":
    main()
