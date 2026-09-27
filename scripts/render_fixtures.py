"""Render SYNTHETIC oversized fixtures to prove volume-robustness (FEAT-003).

These fixtures are NOT part of the fidelity comparison against the real originals.
They exercise each affected report's OWN template + style.css with deliberately
oversized / edge-case data to prove that the templates are data-driven for VOLUME:

  * ties-26-rows  - a "Top 10" style block that actually holds 26 ranked rows
                    (including tied ranks) must render ALL 26 rows, not truncate at 10.
  * long-text     - very long DETAILED SUBJECTS / SCHOOL / CANDIDATE strings must WRAP
                    inside their cell (opt-in wrap policy), never silently clip/overflow.
  * 3-page        - a report whose real instance fits on ONE page must paginate to
                    exactly 3 pages when given enough rows, repeating the heading +
                    column-header band on each page and continuing S/N numbering.

The real data.json files are never overwritten. Fixture JSON lives under
reports/secondary/fixtures/ and each fixture renders to its report's own
output/fixtures/<name>.pdf (+ page PNGs) as committed proof artifacts.

    python scripts/render_fixtures.py            # generate + render + verify all fixtures

Exit status is non-zero if any built-in assertion fails.
"""

import copy
import json
import sys
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SECONDARY = ROOT / "reports" / "secondary"
FIXTURES = SECONDARY / "fixtures"
DPI = 110

BEST_STUDENTS = SECONDARY / "council" / "council-best-students-overall"
SCHOOLS_RANK = SECONDARY / "council" / "council-schools-rank-overall"


def load(report_dir):
    return json.loads((report_dir / "data.json").read_text(encoding="utf-8"))


def save_fixture(name, doc):
    FIXTURES.mkdir(parents=True, exist_ok=True)
    path = FIXTURES / f"{name}.json"
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def render(report_dir, fixture_json, out_pdf, out_html):
    """Render a fixture through a report's OWN template + style.css."""
    from sars_pdf.render import render_html
    template_dir = report_dir
    if (template_dir / "template.html.j2").exists():
        template_name = "template.html.j2"
    else:
        template_name = "report.html.j2"
    doc = json.loads(Path(fixture_json).read_text(encoding="utf-8"))
    html = render_html(doc, template_dir=template_dir, template_name=template_name)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")

    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
    font_config = FontConfiguration()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(template_dir)).write_pdf(out_pdf, font_config=font_config)


def rasterize(pdf_path, pages_dir):
    pages_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    n = len(pdf)
    for i in range(n):
        img = pdf[i].render(scale=DPI / 72).to_pil().convert("RGB")
        img.save(pages_dir / f"page_{i + 1:02d}.png")
    pdf.close()
    return n


# --------------------------------------------------------------------------- #
# fixture builders
# --------------------------------------------------------------------------- #
def build_ties_26_rows():
    """A top-10 block that actually holds 26 ranked rows incl. tied ranks."""
    doc = load(BEST_STUDENTS)
    base_rows = doc["sections"][1]["rows"]  # a plain (non-banner) top-10 section
    proto = base_rows[0]
    rows = []
    # 26 rows; ranks 1..24 with two ties (positions 5 and 12 duplicated) so the
    # printed POSITION column repeats a value - proving ties are not de-duplicated.
    ranks = list(range(1, 25))
    ranks = ranks[:4] + [5, 5] + ranks[4:10] + [12, 12] + ranks[10:]
    ranks = ranks[:26]
    for idx, pos in enumerate(ranks, start=1):
        r = copy.deepcopy(proto)
        r["cno"] = f"{idx:02d}"
        r["school"] = f"SYNTHETIC SCHOOL {idx:02d}"
        r["candidate"] = f"CANDIDATE NUMBER {idx:02d} FULLNAME"
        r["position"] = str(pos)
        rows.append(r)
    section = {
        "title": "TIES FIXTURE - TOP 10 WITH 26 TIED ROWS (SYNTHETIC)",
        "rows": rows,
    }
    doc["sections"] = [section]
    doc["document"]["exam_name"] = "SYNTHETIC FIXTURE - TIES (26 ROWS INCLUDING TIED RANKS)"
    return doc, len(rows)


def build_long_text():
    """Very long detailed-subject / school / candidate strings that must WRAP."""
    doc = load(BEST_STUDENTS)
    doc["document"]["wrap_text"] = True  # opt in to the documented wrap policy
    doc["document"]["exam_name"] = "SYNTHETIC FIXTURE - LONG TEXT (WRAP WITHIN CELL)"
    long_detail = (
        "HISTORY - 97'A' BUSINESS STUDIES - 80'A' GEOGRAPHY - 91'A' KISWAHILI - 85'A' "
        "ENGLISH LANGUAGE - 78'A' PHYSICS - 88'A' CHEMISTRY - 90'A' BIOLOGY - 84'A' "
        "BASIC MATHEMATICS - 95'A' CIVICS AND MORAL EDUCATION - 82'A' "
        "COMMERCE - 76'A' BOOKKEEPING AND ACCOUNTS - 79'A'"
    )
    long_school = "VERY LONG SYNTHETIC SECONDARY SCHOOL NAME FOR COUNCIL WRAP TEST"
    long_candidate = "MWANAHAMISI ABDALLAH RAMADHANI MOHAMEDI SULEIMANI FULLNAME"
    section = {
        "title": "LONG-TEXT FIXTURE - WRAPPING SCHOOL / CANDIDATE / DETAILED SUBJECTS (SYNTHETIC)",
        "rows": [],
    }
    proto = doc["sections"][1]["rows"][0]
    for idx in range(1, 9):
        r = copy.deepcopy(proto)
        r["cno"] = f"{idx:02d}"
        r["school"] = long_school
        r["candidate"] = long_candidate
        r["detailed"] = long_detail
        section["rows"].append(r)
    doc["sections"] = [section]
    return doc


def build_3_page():
    """A normally single-page report given enough rows to span exactly 3 pages."""
    doc = load(SCHOOLS_RANK)
    proto = doc["rows"][0]
    # The real instance is 64 rows on ONE landscape page; ~3x rows -> 3 pages.
    n = 195
    rows = []
    for idx in range(1, n + 1):
        r = copy.deepcopy(proto)
        r["sn"] = f"{idx:02d}"
        r["ward"] = f"WARD {idx:02d}"
        r["school"] = f"SYNTHETIC SCHOOL {idx:02d}"
        r["crank"] = str(idx)
        r["rrank"] = str(idx)
        rows.append(r)
    doc["rows"] = rows
    doc["document"]["exam_name"] = "SYNTHETIC FIXTURE - 3-PAGE PAGINATION (REPEATED HEADER BAND)"
    return doc, n


# --------------------------------------------------------------------------- #
# verification helpers
# --------------------------------------------------------------------------- #
def count_data_rows(pdf_path):
    """Count body rows in the ties fixture.

    Each synthetic candidate string ends in the unique token 'FULLNAME', so one
    occurrence == one rendered data row. (The C/NO and SCHOOL columns interleave in
    pdfplumber's plain-text extraction, so counting FULLNAME is the robust signal.)
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    return text.count("FULLNAME")


def text_within_bounds(pdf_path):
    """True if every char sits inside the page media box (no overflow off-page)."""
    with pdfplumber.open(pdf_path) as pdf:
        for pg in pdf.pages:
            for ch in pg.chars:
                if ch["x0"] < -0.5 or ch["x1"] > pg.width + 0.5:
                    return False, (ch["text"], ch["x0"], ch["x1"], pg.width)
    return True, None


def header_repeats_each_page(pdf_path, header_token):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [(pg.extract_text() or "") for pg in pdf.pages]
    return [header_token in t for t in pages], len(pages)


# --------------------------------------------------------------------------- #
def main():
    failures = []

    # 1) TIES ---------------------------------------------------------------
    ties_doc, ties_n = build_ties_26_rows()
    ties_json = save_fixture("council-best-students-overall__ties-26-rows", ties_doc)
    out = BEST_STUDENTS / "output" / "fixtures"
    ties_pdf = out / "ties-26-rows.pdf"
    render(BEST_STUDENTS, ties_json, ties_pdf, out / "ties-26-rows.html")
    npages = rasterize(ties_pdf, out / "ties-26-rows-pages")
    found = count_data_rows(ties_pdf)
    print(f"[ties] pages={npages} rows rendered={found} (expected {ties_n})")
    if found != ties_n:
        failures.append(f"ties: expected {ties_n} rows, found {found}")

    # 2) LONG TEXT ----------------------------------------------------------
    lt_doc = build_long_text()
    lt_json = save_fixture("council-best-students-overall__long-text", lt_doc)
    lt_pdf = out / "long-text.pdf"
    render(BEST_STUDENTS, lt_json, lt_pdf, out / "long-text.html")
    lt_pages = rasterize(lt_pdf, out / "long-text-pages")
    ok, detail = text_within_bounds(lt_pdf)
    print(f"[long-text] pages={lt_pages} text within page bounds={ok}")
    if not ok:
        failures.append(f"long-text: char outside page bounds {detail}")

    # 3) 3-PAGE PAGINATION --------------------------------------------------
    pg_doc, pg_n = build_3_page()
    pg_json = save_fixture("council-schools-rank-overall__3-page", pg_doc)
    out3 = SCHOOLS_RANK / "output" / "fixtures"
    pg_pdf = out3 / "3-page.pdf"
    render(SCHOOLS_RANK, pg_json, pg_pdf, out3 / "3-page.html")
    pg_pages = rasterize(pg_pdf, out3 / "3-page-pages")
    # The repeated column-header band carries "REGISTERED" (a header-only token; the
    # data cells never contain that word), so its presence on every page proves the
    # <thead> band repeated.
    repeats, total = header_repeats_each_page(pg_pdf, "REGISTERED")
    print(f"[3-page] pages={pg_pages} header-band on each page={repeats}")
    if pg_pages != 3:
        failures.append(f"3-page: expected 3 pages, got {pg_pages}")
    if not all(repeats):
        failures.append(f"3-page: header band missing on some page {repeats}")
    # continuous S/N numbering across page breaks: the last WARD label must appear,
    # and the S/N sequence must run unbroken 01..N (checked at line starts).
    import re
    with pdfplumber.open(pg_pdf) as pdf:
        alltext = "\n".join((p.extract_text() or "") for p in pdf.pages)
    flat = alltext.replace("\n", " ")
    # S/N appears as "NN WARD nn" at each row start; capture the S/N that is
    # immediately followed by a WARD label (this excludes the summary block's
    # "NO. OF SCHOOLS IN COUNCIL" value which is not followed by WARD).
    sns = [int(x) for x in re.findall(r"(?m)^(\d{1,3}) WARD \d", alltext)]
    if f"WARD {pg_n}" not in flat:
        failures.append(f"3-page: last row (WARD {pg_n}) not found")
    if sns != list(range(1, pg_n + 1)):
        failures.append(f"3-page: S/N numbering not continuous 1..{pg_n} (got {sns[:3]}..{sns[-3:]}, n={len(sns)})")

    print()
    if failures:
        print("=== render-fixtures FAILED ===")
        for f in failures:
            print(" -", f)
        return 1
    print("=== render-fixtures OK ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
