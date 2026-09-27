"""Extract 'Mwanza f2 District Performance' (5pp) into
region-district-performance/data.json.

Region-only report. Section-centric: 5 stacked per-council/district division grids (one
per page): DISTRICT PERFORMANCE OVERALL / FOR GOVERNMENT SCHOOLS ONLY / FOR PRIVATE
SCHOOLS ONLY / BY PERCENTAGE / BY KPI. Each grid:
  S/N | DISTRICT | NO. OF SCHOOLS | NUMBER OF CANDIDATES(REGISTERED F M T, SAT F M T %)
      | DIVISION PERFORMANCE(I,II,III,IV,0,I-III,I-IV as F/M/T + %) | GPA
      | COMPETENCY LEVEL | RANK, plus a TOTAL row.

Each page's own measured vertical boundaries bucket every numeric token into a column, so
rows are captured positionally as ordered cell lists (never hand-typed). The template
renders each section with its own column widths. Coordinate based (pymupdf + pdfplumber).
"""

import json
from pathlib import Path

import pdfplumber
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza f2 District Performance.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-district-performance" / "data.json"


def boundaries(page):
    xs = sorted(set(round(e["x0"], 1) for e in page.edges if e["orientation"] == "v"))
    cl = []
    for x in xs:
        if not cl or x - cl[-1] > 2:
            cl.append(x)
    return cl


def group_lines(words, y_tol=4.0):
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w)
            cy = y if cy is None else (cy * (len(cur) - 1) + y) / len(cur)
        else:
            lines.append((cy, cur))
            cur, cy = [w], y
    if cur:
        lines.append((cy, cur))
    return lines


# named numeric columns, in order, for the two layouts.
COLS_FULL = ["schools", "reg_f", "reg_m", "reg_t", "sat_f", "sat_m", "sat_t", "sat_pct",
             "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
             "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
             "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct",
             "gpa", "competency", "rank", "_pad"]
COLS_PCT = ["schools", "sat_f", "sat_m", "sat_t", "sat_pct",
            "i_f", "i_m", "i_t", "ii_f", "ii_m", "ii_t", "iii_f", "iii_m", "iii_t",
            "iv_f", "iv_m", "iv_t", "z_f", "z_m", "z_t", "z_pct",
            "d3_f", "d3_m", "d3_t", "d3_pct", "d4_f", "d4_m", "d4_t", "d4_pct",
            "gpa", "competency", "rank", "_pad"]


def bucket(band, bounds):
    """Return sn, district (text), and a raw ordered cell list for numeric columns 2..end."""
    ncell = len(bounds) - 1
    cells = [""] * ncell
    district_p = []
    sn = ""
    for w in band:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < bounds[1]:
            sn = txt
            continue
        if bounds[1] <= cx < bounds[2]:
            district_p.append((x0, txt))
            continue
        for i in range(2, ncell):
            if bounds[i] <= cx < bounds[i + 1]:
                cells[i] = (cells[i] + " " + txt).strip() if cells[i] else txt
                break
    district = " ".join(t for _, t in sorted(district_p))
    return {"sn": sn, "district": district, "cells": cells[2:]}


def name_cells(row, ncols):
    keys = COLS_FULL if ncols == 38 else COLS_PCT
    cells = row["cells"]
    named = {"sn": row["sn"], "district": row["district"]}
    for i, k in enumerate(keys):
        named[k] = cells[i] if i < len(cells) else ""
    return named


def main():
    fdoc = pymupdf.open(SRC)
    pdf = pdfplumber.open(SRC)
    sections = []
    for pi in range(fdoc.page_count):
        page = pdf.pages[pi]
        bounds = boundaries(page)
        words = fdoc[pi].get_text("words")
        # section title (line just below the exam name, y ~ 90-100)
        title = ""
        for cy, band in group_lines(words):
            if 88 < cy < 102:
                title = " ".join(w[4] for w in sorted(band, key=lambda w: w[0]))
                break
        # capture the header band verbatim (group titles + F/M/T labels), as a single
        # centred string per text-line, so the rendered header matches word-for-word.
        header_lines = []
        for cy, band in group_lines(words, y_tol=2.2):
            if 100 < cy < 129:
                txt = " ".join(w[4] for w in sorted(band, key=lambda w: w[0]))
                header_lines.append(txt)
        rows = []
        total = None
        for cy, band in group_lines(words):
            if cy <= 125:
                continue
            first = min(band, key=lambda w: w[0])
            text_first = first[4]
            # a data row has a leading S/N and many numeric tokens (header/label lines don't)
            numeric = sum(1 for w in band if w[4].replace(".", "").replace("-", "").isdigit())
            if first[0] < bounds[1] and text_first.isdigit() and len(text_first) <= 2 \
                    and numeric >= 10:
                rows.append(bucket(band, bounds))
            elif any(w[4] == "TOTAL" for w in band):
                total = bucket(band, bounds)
                total["district"] = "TOTAL"
        ncols = len(bounds) - 1
        rows = [name_cells(r, ncols) for r in rows]
        if total:
            total = name_cells(total, ncols)
            total["district"] = "TOTAL"
        sections.append({
            "title": title,
            "bounds": bounds,
            "ncols": len(bounds) - 1,
            "has_registered": (len(bounds) - 1) == 38,
            "rows": rows,
            "total": total,
        })

    document = {
        "page_size": "Letter-landscape",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
    }
    data = {"document": document, "sections": sections}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for s in sections:
        print(f"  [{s['title']}] ncols={s['ncols']} rows={len(s['rows'])} total={'y' if s['total'] else 'n'}")


if __name__ == "__main__":
    main()
