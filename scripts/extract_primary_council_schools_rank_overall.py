"""Extract MWANZA CC SCHOOL RANK grids (primary STD4) into data*.json (display strings).

Primary council all-schools division/grade grid. A summary block sits above the main
per-school table (+ JUMLA total row). Leading text columns:
  S/N | HALMASHAURI | KATA | JINA LA SHULE | UMILIKI
then WAV/WAS/JML triplet groups (WAV=girls, WAS=boys, JML=total):
  WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D WALIOFAULU(A-D)(+%) E(+%)
  WASTANI WA SHULE /300 | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI WILAYA | NAFASI MKOA

One structure, three sources (IN GRADE = all schools; SERIKALI = government;
BINAFSI = private). They are consolidated into ONE self-contained report dir driven
by data.json + data_serikali.json + data_binafsi.json (with reference/original*.pdf).
The header row is located dynamically (the row that holds S/N + HALMASHAURI) so the
same coordinate mapping works regardless of the summary-block height.

Extraction is coordinate based (pymupdf words), never hand-typed.

    python scripts/extract_primary_council_schools_rank_overall.py           # all three
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_council_pdf" / "primary_council_pdf"
OUTDIR = ROOT / "reports" / "primary" / "council" / "primary-council-schools-rank-overall"

# (tag, source pdf name, report title). tag None -> data.json / original.pdf.
# NOTE: the SERIKALI (government-only) and BINAFSI (private-only) variants share the
# report TYPE but have a DIFFERENT physical column layout in their PDFs (different
# x-centres, no shared UMILIKI column), so they are NOT consolidated here as tags of
# this coordinate mapping - each would need its own measured header x-centres. This
# report reproduces the all-schools "IN GRADE" division/grade grid.
SOURCES = [
    (None, "MWANZA CC SCHOOL RANK IN GRADE.pdf",
     "MPANGILIO WA UFAULU WA SHULE KIMADARAJA - MWANZA CC"),
]

NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "sifanya_f", "sifanya_m", "sifanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct", "wastani",
]
NUM_CENTERS = [
    196.3, 220.3, 236.6, 253.0, 267.8, 284.2, 299.8, 313.1, 327.1,
    341.9, 356.9, 371.8, 386.6, 401.5, 416.4, 431.2, 446.2, 461.1,
    475.2, 488.5, 503.4, 517.4, 532.3, 548.7, 566.4, 582.0, 595.4, 608.4, 622.0, 641.0,
]
SN_MAX_X = 29.5
KATA_MIN_X = 58.6
KATA_MAX_X = 87.0
SCHOOL_MAX_X = 160.6
OWN_MAX_X = 179.3
COMP_MIN_X = 660.0
NW_C = 720.0
NM_C = 742.0


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
        elif x0 < KATA_MIN_X:
            council_parts.append((x0, txt))
        elif cx < KATA_MAX_X:
            row["ward"] = txt
        elif x0 < SCHOOL_MAX_X and cx < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx < OWN_MAX_X:
            row["ownership"] = txt
        elif cx >= NM_C - 6:
            row["nm"] = txt
        elif cx >= NW_C - 6:
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
        elif cx >= NM_C - 6:
            row["nm"] = txt
        elif cx >= NW_C - 6:
            row["nw"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


SUM_PCT_GROUPS = [
    ("fanya", 269.0), ("sifanya", 313.0), ("a", 357.0), ("b", 401.0),
    ("c", 446.0), ("d", 489.0), ("ad", 542.0), ("e", 602.0),
]


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


def parse_summary(words):
    row = {k: "" for k in ["shule", *NUM_COLS, "competency"]}
    comp_parts = []
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < 160:
            if _is_num(w[4]):
                row["shule"] = w[4]
        elif cx >= COMP_MIN_X and not _is_num(w[4]):
            comp_parts.append((w[0], w[4]))  # the Daraja X (...) competency label
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
    """Return the y of the header row that holds S/N and HALMASHAURI."""
    for cy, line in lines:
        txt = {w[4] for w in line}
        if "S/N" in txt and "HALMASHAURI" in txt:
            return cy
    return None


def extract(src):
    doc = pymupdf.open(src)
    rows, total, summary, pct_pass = [], None, None, None

    p0lines = group_lines(doc[0].get_text("words"))
    header_y = find_header_y(p0lines) or 165.0

    # Locate the summary block sitting ABOVE the main header band. Its own WAV/WAS/JML
    # sub-header (a line of >=15 'WAV'/'WAS'/'JML' tokens) marks its top; the numeric
    # values row is the next line, and the ASILIMIA(%) row is the line holding that label.
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
            if "ASILIMIA(%)" in toks or any(t.startswith("ASILIMIA") for t in toks):
                asil_words += [w for w in line if w[4] != "ASILIMIA(%)"
                               and not w[4].startswith("ASILIMIA")]
            elif not val_words and sum(1 for t in toks if _is_num(t)) >= 8:
                # numeric summary values row (WASTANI + Daraja label may share this line)
                val_words = list(line)
        if val_words:
            summary = parse_summary(sorted(val_words, key=lambda w: w[0]))
        if asil_words:
            pct_pass = parse_asilimia(sorted(asil_words, key=lambda w: w[0]))

    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            first = line[0]
            text = " ".join(w[4] for w in line)
            if first[0] < SN_MAX_X and first[4].isdigit() and len(first[4]) <= 3 and len(line) > 25:
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
            "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
            "report_title": title,
        }
        data = {"document": document, "summary": summary, "pct_pass": pct_pass,
                "rows": rows, "total": total}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        # place a copy of the source as the report's reference original
        dst = ref / f"original{suffix}.pdf"
        dst.write_bytes(src.read_bytes())
        print(f"[{tag or 'main'}] rows={len(rows)} total={'y' if total else 'n'} "
              f"summary={'y' if summary else 'n'} -> {out.name}")


if __name__ == "__main__":
    main()
