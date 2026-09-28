"""Extract MKOA all-schools rank grid (SHULE NAFASI STD4, region) -> data.json.

Region all-schools division/grade grid. Same WAV/WAS/JML triplet structure as the
primary COUNCIL schools-rank-overall report, but a REGION report so the leading text
columns are S/N | HALMASHAURI | KATA | JINA LA SHULE | UMILIKI (HALMASHAURI = council)
and there are TWO rank columns (NAFASI KIWILAYA / NAFASI KIMKOA). A summary block
(+ ASILIMIA% row) sits above the main per-school table (16 pages, all schools of the
region). The header row is located dynamically (row holding S/N + KATA + HALMASHAURI)
so the coordinate mapping is independent of the summary-block height.

Columns (main table): S/N | HALMASHAURI | KATA | JINA LA SHULE | UMILIKI
  WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D WALIOFAULU(A-D)(+%) E(+%)
  (each triplet WAV=girls WAS=boys JML=total)
  WASTANI WA SHULE /300 | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI WILAYA | NAFASI MKOA

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
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-schools-rank-overall"

SOURCES = [
    (None, "SHULE NAFASI STD4 JUMLA 2026.pdf",
     "MPANGILIO WA UFAULU WA SHULE KIMKOA - JUMLA"),
]

NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "sifanya_f", "sifanya_m", "sifanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]
# x-centres measured from THIS report's own reference (SHULE NAFASI, page 1).
NUM_CENTERS = [
    198.3, 214.8, 232.4, 250.1, 266.5, 283.0, 298.1, 311.9, 325.3,
    338.8, 352.6, 367.7, 384.1, 400.6, 417.1, 433.5, 450.0, 466.4,
    481.5, 495.3, 510.4, 526.9, 543.3, 559.8, 577.3, 593.5, 607.3, 621.1, 637.4, 663.6,
]
SN_MAX_X = 33.0
COUNCIL_MAX_X = 68.0   # HALMASHAURI (council) text: 1-2 tokens ending ~59
KATA_MAX_X = 98.0      # KATA (ward) text: single token starting ~76
SCHOOL_MAX_X = 165.0   # JINA LA SHULE text
OWN_MAX_X = 190.0
COMP_MIN_X = 685.0
NW_C = 742.8   # NAFASI WILAYA
NM_C = 760.0   # NAFASI MKOA


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
    keys = ["sn", "council", "ward", "school", "ownership", *NUM_COLS,
            "competency", "nw", "nm"]
    row = {k: "" for k in keys}
    council_parts, school_parts, comp_parts = [], [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif cx < COUNCIL_MAX_X:
            council_parts.append((x0, txt))
        elif cx < KATA_MAX_X:
            row["ward"] = txt
        elif cx < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx < OWN_MAX_X:
            row["ownership"] = txt
        elif cx >= NM_C - 8:
            row["nm"] = txt
        elif cx >= NW_C - 8:
            row["nw"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_total(line):
    keys = ["sn", "council", "ward", "school", "ownership", *NUM_COLS,
            "competency", "nw", "nm"]
    row = {k: "" for k in keys}
    comp_parts = []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if txt == "JUMLA":
            continue
        if cx < OWN_MAX_X:
            continue
        elif cx >= NM_C - 8:
            row["nm"] = txt
        elif cx >= NW_C - 8:
            row["nw"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


SUM_PCT_GROUPS = [
    ("fanya", 266.5), ("sifanya", 311.5), ("a", 353.8), ("b", 400.5),
    ("c", 449.8), ("d", 496.5), ("ad", 552.5), ("e", 616.5),
]


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


def parse_summary(words):
    row = {k: "" for k in ["shule", *NUM_COLS, "competency"]}
    comp_parts = []
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < 190:
            if _is_num(w[4]):
                row["shule"] = w[4]
        elif cx >= COMP_MIN_X and not _is_num(w[4]):
            comp_parts.append((w[0], w[4]))
        elif _is_num(w[4]):
            row[col_for(cx)] = w[4]
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_asilimia(words):
    row = {}
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < 200:
            continue
        best, bd = None, 1e9
        for name, c in SUM_PCT_GROUPS:
            if abs(cx - c) < bd:
                best, bd = name, abs(cx - c)
        row[best] = w[4]
    return row


def find_header_y(lines):
    for cy, line in lines:
        txt = {w[4] for w in line}
        if "S/N" in txt and "KATA" in txt and "UMILIKI" in txt:
            return cy
    return None


def extract(src):
    doc = pymupdf.open(src)
    rows, total, summary, pct_pass = [], None, None, None

    p0lines = group_lines(doc[0].get_text("words"))
    header_y = find_header_y(p0lines) or 165.0

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
        # WASTANI + Daraja label sit on their own line just below the values row
        for cy, line in p0lines:
            if sum_fmt_y < cy < header_y - 12:
                toks = [w[4] for w in line]
                if any("Daraja" == t for t in toks):
                    val_words += list(line)
        if val_words:
            summary = parse_summary(sorted(val_words, key=lambda w: w[0]))
        if asil_words:
            pct_pass = parse_asilimia(sorted(asil_words, key=lambda w: w[0]))

    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            first = line[0]
            text = " ".join(w[4] for w in line)
            if first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 4 and len(line) > 25:
                rows.append(parse_row(line))
            elif "JUMLA" in text and first[0] < 90 and len(line) > 25:
                total = parse_total(line)
    return rows, total, summary, pct_pass


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title in SOURCES:
        src = SRCDIR / name
        rows, total, summary, pct_pass = extract(src)
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
                "rows": rows, "total": total}
        for agg in (summary, total):
            if isinstance(agg, dict):
                agg["level"] = competency_letter(agg.get("competency"), None)
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        dst = ref / f"original{suffix}.pdf"
        dst.write_bytes(src.read_bytes())
        print(f"[{tag or 'main'}] rows={len(rows)} total={'y' if total else 'n'} "
              f"summary={'y' if summary else 'n'} -> {out.name}")
        empties = sum(1 for r in rows for k in NUM_COLS if r[k] == "")
        print(f"   empty_numeric={empties}")
        for r in rows[:2]:
            print(f"   {r['sn']} {r['council']:<14} {r['ward']:<12} {r['school']:<20} "
                  f"wastani={r['wastani']} {r['competency']} W{r['nw']} M{r['nm']}")


if __name__ == "__main__":
    main()
