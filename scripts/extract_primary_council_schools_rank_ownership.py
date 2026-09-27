"""Extract MWANZA CC SCHOOL RANK SERIKALI / BINAFSI (primary STD4) into data*.json.

Same division/grade grid TYPE as primary-council-schools-rank-overall, but filtered by
ownership: SERIKALI = government schools only, BINAFSI = private schools only. The two
source PDFs share the report structure but have DIFFERENT physical column layouts (the
SERIKALI grid carries a KATA column; the BINAFSI grid omits it, and every numeric x-centre
is shifted), so each ownership tag gets its OWN measured header x-centres here. They are
consolidated into ONE self-contained report dir driven by data_serikali.json +
data_binafsi.json (with reference/original_serikali.pdf + original_binafsi.pdf).

Leading text columns (per tag): S/N | HALMASHAURI | [KATA] | JINA LA SHULE
then 29 numeric columns (WAV=girls, WAS=boys, JML=total triplets):
  WALIOSAJILIWA WALIOFANYA WASIOFANYA A B C D WALIOFAULU(A-D)(+%) E(+%)
then WASTANI WA SHULE /300 | KUNDI LA UMAHIRI (Daraja X (...)) | NAFASI

Extraction is coordinate based (pymupdf words), never hand-typed.

    python scripts/extract_primary_council_schools_rank_ownership.py
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_council_pdf" / "primary_council_pdf"
OUTDIR = ROOT / "reports" / "primary" / "council" / "primary-council-schools-rank-ownership"

NUM_COLS = [
    "reg_f", "reg_m", "reg_t", "fanya_f", "fanya_m", "fanya_t",
    "sifanya_f", "sifanya_m", "sifanya_t",
    "a_f", "a_m", "a_t", "b_f", "b_m", "b_t", "c_f", "c_m", "c_t", "d_f", "d_m", "d_t",
    "ad_f", "ad_m", "ad_t", "ad_pct", "e_f", "e_m", "e_t", "e_pct",
]

# Per-tag measured layout. num_centers = the 29 numeric header x-centres (WAV/WAS/JML...%).
# has_kata: SERIKALI grid has a KATA column, BINAFSI does not.
SERIKALI_NUM = [
    169.8, 191.8, 209.4, 226.9, 243.5, 261.1, 278.7, 295.2, 311.4, 327.5, 344.1,
    360.2, 376.4, 392.9, 409.1, 425.2, 441.8, 457.9, 474.1, 490.6, 506.8, 522.9,
    539.5, 557.0, 575.8, 593.3, 609.8, 626.0, 641.7,
]
BINAFSI_NUM = [
    154.8, 175.5, 194.1, 212.7, 231.3, 249.9, 267.6, 284.3, 300.5, 316.8, 333.5,
    351.1, 368.8, 385.5, 403.1, 420.8, 437.4, 453.6, 470.0, 486.6, 502.8, 520.1,
    538.7, 557.3, 577.9, 596.9, 613.0, 628.9, 646.3,
]

SOURCES = [
    ("serikali", "MWANZA CC SCHOOL RANK SERIKALI.pdf",
     "MPANGILIO WA UFAULU WA SHULE ZA SERIKALI KIMADARAJA - MWANZA CC",
     dict(num=SERIKALI_NUM, has_kata=True,
          sn_max=40.0, council_max=78.0, kata_max=103.0, school_max=160.0,
          wastani_c=665.2, comp_min=680.0, nafasi_min=745.0)),
    ("binafsi", "MWANZA CC SCHOOL RANK BINAFSI.pdf",
     "MPANGILIO WA UFAULU WA SHULE ZA BINAFSI KIMADARAJA - MWANZA CC",
     dict(num=BINAFSI_NUM, has_kata=False,
          sn_max=40.0, council_max=78.0, school_max=145.0,
          wastani_c=671.3, comp_min=686.0, nafasi_min=750.0)),
]


def col_for(cx, centers):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, centers):
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


def parse_row(line, cfg):
    keys = ["sn", "council", "ward", "school", *NUM_COLS, "wastani", "competency", "nafasi"]
    row = {k: "" for k in keys}
    council_parts, school_parts, comp_parts = [], [], []
    num_lo = cfg["num"][0] - 8
    num_hi = cfg["num"][-1] + 8
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < cfg["sn_max"]:
            row["sn"] = txt
        elif cx < cfg["council_max"]:
            council_parts.append((x0, txt))
        elif cfg["has_kata"] and cx < cfg["kata_max"]:
            row["ward"] = txt
        elif cx < cfg["school_max"]:
            school_parts.append((x0, txt))
        elif num_lo <= cx <= num_hi:
            row[col_for(cx, cfg["num"])] = txt
        elif cx < cfg["comp_min"]:
            row["wastani"] = txt
        elif cx >= cfg["nafasi_min"]:
            row["nafasi"] = txt
        else:
            comp_parts.append((x0, txt))
    row["council"] = " ".join(t for _, t in sorted(council_parts))
    row["school"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


def parse_total(line, cfg):
    keys = ["sn", "council", "ward", "school", *NUM_COLS, "wastani", "competency", "nafasi"]
    row = {k: "" for k in keys}
    comp_parts = []
    num_lo = cfg["num"][0] - 8
    num_hi = cfg["num"][-1] + 8
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if txt == "JUMLA":
            continue
        if num_lo <= cx <= num_hi:
            row[col_for(cx, cfg["num"])] = txt
        elif cfg["comp_min"] <= cx < cfg["nafasi_min"] and not _is_num(txt):
            comp_parts.append((x0, txt))
        elif cx < cfg["comp_min"] and cx >= num_hi:
            row["wastani"] = txt
        elif cx < num_lo and not _is_num(txt):
            comp_parts.append((x0, txt))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


# summary block sits above the main header band (IDADI YA SHULE ... values ... ASILIMIA(%))
SUM_PCT_GROUPS = [
    ("fanya", 3), ("sifanya", 4), ("a", 5), ("b", 6),
    ("c", 7), ("d", 8), ("ad", 9), ("e", 11),
]


def find_main_header_y(lines):
    for cy, line in lines:
        txt = {w[4] for w in line}
        if "S/N" in txt and "HALMASHAURI" in txt:
            return cy
    return None


def parse_summary(words, cfg):
    row = {k: "" for k in ["shule", *NUM_COLS, "wastani", "competency"]}
    comp_parts = []
    num_lo = cfg["num"][0] - 8
    num_hi = cfg["num"][-1] + 8
    for w in words:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < num_lo:
            if _is_num(txt):
                row["shule"] = txt
        elif num_lo <= cx <= num_hi:
            row[col_for(cx, cfg["num"])] = txt
        elif not _is_num(txt):
            comp_parts.append((x0, txt))
        elif _is_num(txt):
            row["wastani"] = txt
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_asilimia(words, cfg):
    # % values line up under the group JML columns; approximate by nearest group JML centre.
    group_jml = {
        "fanya": cfg["num"][5], "sifanya": cfg["num"][8], "a": cfg["num"][11],
        "b": cfg["num"][14], "c": cfg["num"][17], "d": cfg["num"][20],
        "ad": cfg["num"][23], "e": cfg["num"][27],
    }
    row = {}
    for w in words:
        cx = (w[0] + w[2]) / 2
        if cx < cfg["num"][0] - 8:
            continue
        best, bd = None, 1e9
        for name, c in group_jml.items():
            if abs(cx - c) < bd:
                best, bd = name, abs(cx - c)
        row[best] = w[4]
    return row


def extract(src, cfg):
    doc = pymupdf.open(src)
    rows, total, summary, pct_pass = [], None, None, None

    p0lines = group_lines(doc[0].get_text("words"))
    header_y = find_main_header_y(p0lines) or 199.0

    # summary block: its WAV/WAS/JML sub-header line, then values row, then ASILIMIA(%) row.
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
            elif val_words and not asil_words and any("Daraja" == t for t in toks):
                # the WASTANI + 'Daraja X (...)' competency sit on their own line, just
                # below the main numeric summary row; merge them into the summary.
                val_words += list(line)
        if val_words:
            summary = parse_summary(sorted(val_words, key=lambda w: w[0]), cfg)
        if asil_words:
            pct_pass = parse_asilimia(sorted(asil_words, key=lambda w: w[0]), cfg)

    for pi in range(doc.page_count):
        for cy, line in group_lines(doc[pi].get_text("words")):
            line = sorted(line, key=lambda w: w[0])
            first = line[0]
            text = " ".join(w[4] for w in line)
            if (first[0] < cfg["sn_max"] and first[4].isdigit()
                    and len(first[4]) <= 3 and len(line) > 25):
                rows.append(parse_row(line, cfg))
            elif "JUMLA" in text and len(line) > 25:
                total = parse_total(line, cfg)
    return rows, total, summary, pct_pass


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name, title, cfg in SOURCES:
        src = SRCDIR / name
        rows, total, summary, pct_pass = extract(src, cfg)
        document = {
            "page_size": "Letter-landscape",
            "ministry": [
                "OFISI YA WAZIRI MKUU",
                "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
                "MKOA WA MWANZA",
            ],
            "exam_name": "MATOKEO YA MTIHANI WA UTAMILIFU(MOCK) MKOA  DARASA LA IV MWEZI AGOSTI, 2026",
            "report_title": title,
            "has_kata": cfg["has_kata"],
        }
        data = {"document": document, "summary": summary, "pct_pass": pct_pass,
                "rows": rows, "total": total}
        # Stamp an explicit competency letter into the aggregate blocks so their
        # cell colour is data-driven with no shared render.py change (extraction is
        # the single source of truth).
        for agg in (summary, total):
            if isinstance(agg, dict):
                agg["level"] = competency_letter(agg.get("competency"), agg.get("gpa"))
        out = OUTDIR / f"data_{tag}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        dst = ref / f"original_{tag}.pdf"
        dst.write_bytes(src.read_bytes())
        print(f"[{tag}] rows={len(rows)} total={'y' if total else 'n'} "
              f"summary={'y' if summary else 'n'} pct={'y' if pct_pass else 'n'} -> {out.name}")


if __name__ == "__main__":
    main()
