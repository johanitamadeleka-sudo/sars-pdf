"""Render the report: JSON data -> Jinja2 HTML -> WeasyPrint PDF.

Usage:
    python -m sars_pdf.render data/lakezone_f2_mock_aug2026.json \
        --pdf output/report.pdf --html output/report.html
"""

import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

# Defaults for the per-table presentation quirks of the original (see README).
DEFAULT_STYLE = {
    "title_size": "normal",          # "large" on page 1
    "sn_header_fill": False,         # peach S/N header cell (page 1 only)
    "centre_align": "center",        # CENTRE NO. alignment: "center" | "left"
    "total_bold": True,              # TOTAL column bold
    "competency_size": "small",      # competency text in school rows: "small" | "large"
    "overall_competency_size": "normal",
}


# Ranking scope -> rank column label and overall-row label.
SCOPES = {
    "LAKEZONEWISE": ("Z/RANK", "ZONAL OVERALL  PERFORMANCE"),
    "ZONEWISE": ("Z/RANK", "ZONAL OVERALL  PERFORMANCE"),
    "REGIONWISE": ("R/RANK", "REGIONAL OVERALL  PERFORMANCE"),
    "COUNCILWISE": ("C/RANK", "COUNCIL OVERALL  PERFORMANCE"),
    "WARDWISE": ("W/RANK", "WARD OVERALL  PERFORMANCE"),
}


def build_context(doc):
    for page in doc["pages"]:
        page.setdefault("density", "normal")
        for table in page["tables"]:
            table["style"] = {**DEFAULT_STYLE, **table.get("style", {})}
            scope = table.get("scope", "LAKEZONEWISE")
            rank_label, overall_label = SCOPES.get(scope, ("RANK", "OVERALL  PERFORMANCE"))
            # Title line: "SCHOOL RANK IN <SUBJECT> <SCOPE>"; scope_label overrides the printed scope text.
            table["title"] = f"SCHOOL RANK IN {table['subject']} {table.get('scope_label', scope)}"
            table.setdefault("rank_label", rank_label)
            # The reference prints "ZONAL OVERALL" on every table, so an explicit document label wins.
            table.setdefault("overall_label", doc["document"].get("overall_label", overall_label))
            for row in table["rows"]:
                row["level"] = competency_letter(row.get("competency"), row.get("gpa"))
            if table.get("overall"):
                o = table["overall"]
                o["level"] = competency_letter(o.get("competency"), o.get("gpa"))
    return doc


def render_html(doc):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template("report.html.j2").render(doc=build_context(doc))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", type=Path)
    ap.add_argument("--pdf", type=Path, default=ROOT / "output" / "report.pdf")
    ap.add_argument("--html", type=Path, help="also write the rendered HTML")
    args = ap.parse_args(argv)

    doc = json.loads(args.data.read_text(encoding="utf-8"))
    html = render_html(doc)
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(html, encoding="utf-8")

    from weasyprint import HTML  # imported lazily so HTML-only use needs no native libs

    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(TEMPLATES)).write_pdf(args.pdf)
    print(f"wrote {args.pdf}")


if __name__ == "__main__":
    main()
