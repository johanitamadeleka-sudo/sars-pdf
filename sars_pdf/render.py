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


def decorate_table(table, document):
    """Add computed labels and competency levels to a single subject table."""
    table["style"] = {**DEFAULT_STYLE, **table.get("style", {})}
    scope = table.get("scope", document.get("scope", "LAKEZONEWISE"))
    rank_label, overall_label = SCOPES.get(scope, ("RANK", "OVERALL  PERFORMANCE"))
    # Title line: "SCHOOL RANK IN <SUBJECT> <SCOPE>"; scope_label overrides the printed scope text.
    table["title"] = f"SCHOOL RANK IN {table['subject']} {table.get('scope_label', scope)}"
    table.setdefault("rank_label", rank_label)
    # The reference prints "ZONAL OVERALL" on every table, so an explicit document label wins.
    table.setdefault("overall_label", document.get("overall_label", overall_label))
    for row in table["rows"]:
        row["level"] = competency_letter(row.get("competency"), row.get("gpa"))
    if table.get("overall"):
        o = table["overall"]
        o["level"] = competency_letter(o.get("competency"), o.get("gpa"))
    # A subject too tall for a single page occupies its own page span in the reference
    # (the next subject starts fresh). rows_per_page is a data-driven layout hint the
    # template uses to force that break; small subjects below it stack several per page.
    rpp = document.get("rows_per_page")
    if rpp:
        table["multipage"] = len(table["rows"]) > rpp
    return table


def build_context(doc):
    document = doc["document"]
    if "pages" in doc:
        # page-centric model (lakezone success example): one or more tables per page.
        for page in doc["pages"]:
            page.setdefault("density", "normal")
            for table in page["tables"]:
                decorate_table(table, document)
    if "tables" in doc:
        # subject-centric model: a flat list of tables that flow across page breaks.
        for table in doc["tables"]:
            decorate_table(table, document)
    if "rows" in doc:
        # flat one-row-per-item model (e.g. subjects-rank / wards-rank): a single table.
        for row in doc["rows"]:
            row["level"] = competency_letter(row.get("competency"), row.get("gpa"))
    if isinstance(doc.get("overall"), dict):
        o = doc["overall"]
        o["level"] = competency_letter(o.get("competency"), o.get("gpa"))
    if "sections" in doc:
        # section-centric model (e.g. top-10 blocks, best-students-subjectwise):
        # each section has its own rows; compute competency level per row. Some section
        # reports carry a single-letter GRADE column instead of a "Grade X (...)" label -
        # use it directly when present.
        for section in doc["sections"]:
            for row in section.get("rows", []):
                grade = (row.get("grade") or "").strip().upper()
                if len(grade) == 1 and grade in "ABCDF":
                    row["level"] = grade
                else:
                    row["level"] = competency_letter(row.get("competency"), row.get("gpa"))
    return doc


def render_html(doc, template_dir=TEMPLATES, template_name="report.html.j2"):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template(template_name).render(doc=build_context(doc))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", type=Path)
    ap.add_argument("--pdf", type=Path, default=ROOT / "output" / "report.pdf")
    ap.add_argument("--html", type=Path, help="also write the rendered HTML")
    ap.add_argument("--template-dir", type=Path, default=TEMPLATES,
                    help="directory holding template.html.j2/report.html.j2 + its CSS; "
                         "base_url is set here so the report's own style.css and the shared "
                         "fonts.css resolve. Defaults to templates/ (lakezone example).")
    ap.add_argument("--template", default=None,
                    help="template file name (defaults to template.html.j2 if present in "
                         "--template-dir, else report.html.j2).")
    args = ap.parse_args(argv)

    template_dir = args.template_dir
    if args.template:
        template_name = args.template
    elif (template_dir / "template.html.j2").exists():
        template_name = "template.html.j2"
    else:
        template_name = "report.html.j2"

    doc = json.loads(args.data.read_text(encoding="utf-8"))
    html = render_html(doc, template_dir=template_dir, template_name=template_name)
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(html, encoding="utf-8")

    # imported lazily so HTML-only use needs no native libs
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration

    # CRITICAL (see fonts/README.md + FEAT-001 findings): @font-face is only honoured
    # when ONE shared FontConfiguration is passed to write_pdf. Otherwise WeasyPrint
    # silently falls back to Noto Sans instead of the registered real fonts.
    font_config = FontConfiguration()
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(template_dir)).write_pdf(args.pdf, font_config=font_config)
    print(f"wrote {args.pdf}")


if __name__ == "__main__":
    main()
