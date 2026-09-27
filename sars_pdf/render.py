"""Render the report: JSON data -> Jinja2 HTML -> WeasyPrint PDF.

    python -m sars_pdf.render data/lakezone_f2_mock_aug2026.json --pdf output/report.pdf --html output/report.html

Geometry, borders, fonts and fixed fills are the same for every report. Per table,
the data may override the measured layout (`layout`), thick-border exceptions
(`borders`) and a few typographic variants (`style`), see README.
"""

import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .grading import competency_letter
from .layout import COLS, DEFAULT_LAYOUT, DEFAULT_THICK, THICK, THIN, TITLE_CENTER, TITLE_PITCH, X

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

SCOPES = {
    "LAKEZONEWISE": "Z/RANK",
    "ZONEWISE": "Z/RANK",
    "REGIONWISE": "R/RANK",
    "COUNCILWISE": "C/RANK",
    "WARDWISE": "W/RANK",
}

DEFAULT_STYLE = {
    "header_narrow": False,        # S/N..SCHOOL NAME headers in Arial Narrow Bold (page 1)
    "comp_header_align": "left",   # COMPENTENCY LEVEL header alignment
    "page1_fills": False,          # page-1 palette: S/N header, GPA header, coloured overall row
    "rank_label_font": "bold",     # rotated Z/RANK: "bold" (Arial Bold 5.27) | "narrow" (Arial Narrow Bold 6.11)
    "overall_label_size": 5.27,
    "centre_align": "center",
    "total_bold": True,
    "competency_font": "narrow",   # school-row competency text: "narrow" | "bold"
    "overall_competency": {"size": 5.75, "align": "center"},
}

# Fixed fills (never data dependent).
F = {
    "avh": "#ffffcc", "av": "#ebf1de", "abcdh": "#d8e4bc", "fh": "#fabf8f", "f": "#fcd5b4",
    "totalh": "#b7dee8", "ach": "#65ffab", "ac": "#ccffff", "adh": "#ccffff", "ad": "#b7dee8",
    "gpah": "#daeef3", "gpah1": "#d2fce6", "rankh": "#fde9d9",
    "ov_abcd": "#daeef3", "ov_total": "#f2dcdb", "ov_gpa": "#d2fce6",
}
# Competency level fills: the only conditional colour.
LEVEL = {"A": "#00b050", "B": "#92d050", "C": "#ffff00", "D": "#ffc000", "F": "#ff0000"}

BODY_FILL = {5: "av", 6: "av", 11: "f", 13: "ac", 14: "ac", 15: "ad", 16: "ad"}


def cell(col, span=1, rowspan=1, text="", font="R", size=6.11, align="center", fill=None, cls=""):
    return {"col": col, "span": span, "rowspan": rowspan, "text": text, "font": font, "size": size,
            "align": align, "fill": fill, "cls": cls}


def header_rows(t, s):
    nb = "NB" if s["header_narrow"] else "B"
    h1 = [cell(0, rowspan=2, text="S/N", font=nb, fill=F["rankh"] if s["page1_fills"] else None)]
    for c, label in ((1, "REGION"), (2, "COUNCIL"), (3, "CENTRE NO."), (4, "SCHOOL NAME")):
        align = "left" if c == 3 and s["centre_align"] == "left" else "center"
        h1.append(cell(c, rowspan=2, text=label, font=nb, align=align))
    h1 += [cell(5, rowspan=2, text="AV", font="B", fill=F["avh"]),
           cell(6, rowspan=2, text="GRD", font="B", fill=F["avh"]),
           cell(7, span=10, text="GRADING PERFORMANCE", font="B"),
           cell(17, rowspan=2, text="GPA", font="B", fill=F["gpah1"] if s["page1_fills"] else F["gpah"]),
           cell(18, rowspan=2, text="COMPENTENCY LEVEL", font="NB", size=5.75, align=s["comp_header_align"]),
           cell(19, rowspan=2, text=t["rank_label"], font="B", fill=F["rankh"], cls="rank-h")]
    h2 = [cell(c, text=x, font="B", fill=F["abcdh"]) for c, x in zip(range(7, 11), "ABCD")]
    h2 += [cell(11, text="F", font="B", fill=F["fh"]),
           cell(12, text="TOTAL", font="NB", size=5.27, fill=F["totalh"]),
           cell(13, text="A-C", font="B", fill=F["ach"]), cell(14, text="%A-C", font="B", fill=F["ach"]),
           cell(15, text="A-D", font="B", fill=F["adh"]), cell(16, text="%A-D", font="B", fill=F["adh"])]
    return [("h1", h1), ("h2", h2)]


def body_row(r, s):
    cells = []
    for c, key in enumerate(COLS):
        v = r.get(key, "") or ""
        if c <= 4:
            font, size = "R", 5.27
            align = "left" if c in (1, 2, 4) else ("left" if c == 3 and s["centre_align"] == "left" else "center")
        elif c in (7, 8, 9, 10):
            font, size, align = "R", 6.11, "center"
        elif c == 12:
            font, size, align = ("B" if s["total_bold"] else "R"), 6.11, "center"
        elif c == 18:
            font = "NB" if s["competency_font"] == "narrow" else "B"
            size, align = 5.75, "left"
        elif c == 19:
            font, size, align = "B", 5.27, "center"
        else:
            font, size, align = "B", 6.11, "center"
        fill = F[BODY_FILL[c]] if c in BODY_FILL else None
        if c == 18 and r.get("level"):
            fill = LEVEL[r["level"]]
        cells.append(cell(c, text=v, font=font, size=size, align=align, fill=fill))
    return cells


def overall_row(o, t, s):
    p1 = s["page1_fills"]
    oc = {**DEFAULT_STYLE["overall_competency"], **s.get("overall_competency", {})}
    cells = [cell(0, span=5, text=t["overall_label"], font="B", size=s["overall_label_size"])]
    fills = {5: F["av"], 6: F["av"]}
    if p1:
        fills.update({7: F["ov_abcd"], 8: F["ov_abcd"], 9: F["ov_abcd"], 10: F["ov_abcd"], 11: F["f"],
                      12: F["ov_total"], 13: F["ac"], 14: F["ac"], 15: F["ad"], 16: F["ad"], 17: F["ov_gpa"]})
    for c in range(5, 18):
        cells.append(cell(c, text=o.get(COLS[c], ""), font="B", fill=fills.get(c)))
    cells.append(cell(18, span=2, text=o.get("competency", ""), font="B", size=oc["size"], align=oc["align"],
                      fill=LEVEL.get(o.get("level"))))
    return cells


def thick_set(t):
    s = set(DEFAULT_THICK)
    b = t.get("borders") or {}
    s -= set(b.get("remove", []))
    s |= set(b.get("add", []))
    return s


def h_thick(thick, line, c0, c1):
    """Is the horizontal line `line` thick over the column range c0..c1 (grid indices)?"""
    for seg in thick:
        if seg.startswith(f"H{line}:"):
            a, b = map(int, seg.split(":")[1].split("-"))
            if a <= c0 and c1 <= b:
                return True
    return False


def apply_borders(rows, thick, last_band):
    """Set border widths on every cell from the thick-segment set (THIN elsewhere)."""
    for i, (band, cells) in enumerate(rows):
        for c in cells:
            c0, c1 = c["col"], c["col"] + c["span"]
            bands = [band] + (["h2"] if c["rowspan"] == 2 else [])
            lb = "h1" if c["rowspan"] == 2 else band

            def v(k, bs):
                return THICK if all(f"V{k}:{b}" in thick for b in bs) else THIN

            # rowspan header cells: a vertical line may be thick only in h2; that part is drawn by the h2 neighbour
            c["bl"] = v(c0, [lb] if c["rowspan"] == 1 else bands)
            c["br"] = v(c1, [lb] if c["rowspan"] == 1 else bands)
            top_line = {"h1": "top", "h2": "h1b", "body": None, "ov": "ovt"}[band]
            if i > 0 and band == "body" and rows[i - 1][0] != "body":
                top_line = "hb"
            c["bt"] = THICK if top_line and h_thick(thick, top_line, c0, c1) else THIN
            bottom = None
            if c["rowspan"] == 2 or band == "h2":
                bottom = "hb"
            elif band == "h1":
                bottom = "h1b"
            elif i == len(rows) - 1:
                bottom = "bot"
            elif rows[i + 1][0] == "ov":
                bottom = "ovt"
            c["bb"] = THICK if bottom and h_thick(thick, bottom, c0, c1) else THIN
    # vertical segments thick only in h2 next to a rowspan cell (e.g. V7, V17 on most pages)
    for band, cells in rows:
        if band == "h2":
            for c in cells:
                c["bl"] = THICK if f"V{c['col']}:h2" in thick else c["bl"]
                c["br"] = THICK if f"V{c['col'] + c['span']}:h2" in thick else c["br"]


def build_table(t, doc):
    s = {**DEFAULT_STYLE, **t.get("style", {})}
    t["style"] = s
    scope = t.get("scope", "LAKEZONEWISE")
    t.setdefault("rank_label", SCOPES.get(scope, "RANK"))
    t.setdefault("title", f"SCHOOL RANK IN {t['subject']}  {t.get('scope_label', scope)}")
    t.setdefault("overall_label", doc["document"].get("overall_label", "ZONAL OVERALL  PERFORMANCE"))
    lay = {**DEFAULT_LAYOUT, **t.get("layout", {})}
    rh = list(lay["rows"])
    t["layout"] = lay

    for r in t["rows"]:
        r["level"] = competency_letter(r.get("competency"), r.get("gpa"))
    rows = header_rows(t, s) + [("body", body_row(r, s)) for r in t["rows"]]
    if t.get("overall"):
        o = t["overall"]
        o["level"] = competency_letter(o.get("competency"), o.get("gpa"))
        rows.append(("ov", overall_row(o, t, s)))
    apply_borders(rows, thick_set(t), rows[-1][0])
    heights = {"h1": rh[0], "h2": rh[1], "body": rh[2], "ov": rh[3] or rh[2]}
    t["grid"] = [{"band": b, "height": heights[b], "cells": cs,
                  # Excel lifts the text of the row sitting on the thick overall line by 0.48pt
                  "last": b == "body" and i + 1 < len(rows) and rows[i + 1][0] == "ov"}
                 for i, (b, cs) in enumerate(rows)]
    t["heads"] = [*doc["document"]["ministry"], doc["document"]["exam_board"], doc["document"]["exam_name"]]
    if t.get("scope_area"):
        t["heads"].append(t["scope_area"])
    return t


def build_context(doc):
    for page in doc["pages"]:
        for t in page["tables"]:
            build_table(t, doc)
    doc["geo"] = {"X": X, "widths": [round(b - a, 3) for a, b in zip(X, X[1:])], "pitch": TITLE_PITCH,
                  "center": TITLE_CENTER}
    return doc


def render_html(doc):
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html", "j2"]),
                      trim_blocks=True, lstrip_blocks=True)
    return env.get_template("report.html.j2").render(doc=build_context(doc))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", type=Path)
    ap.add_argument("--pdf", type=Path, default=ROOT / "output" / "report.pdf")
    ap.add_argument("--html", type=Path, help="also write the rendered HTML")
    args = ap.parse_args(argv)

    html = render_html(json.loads(args.data.read_text(encoding="utf-8")))
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(html, encoding="utf-8")

    from weasyprint import HTML

    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(TEMPLATES)).write_pdf(args.pdf)
    print(f"wrote {args.pdf}")


if __name__ == "__main__":
    main()
