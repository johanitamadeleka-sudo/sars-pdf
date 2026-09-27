"""Derive the TRUE cell grid of a report page from its thin gridline rects.

Diagnostic groundwork that quantifies the "borders not straight" and "cell sizes
differ" complaints. In these originals the gridlines are drawn as thin RECTS, not
pdfplumber lines (page.lines is empty), so column/row boundaries must be derived
from page.rects edges:

  * thin VERTICAL rects (width < 2pt, height > 3pt) collapse to column-boundary
    x positions;
  * thin HORIZONTAL rects (height < 2pt, width > 3pt) collapse to row-boundary
    y positions.

Boundaries within ~1.5pt of each other are clustered into a single line. The
script prints the sorted column boundaries, sorted row boundaries, page
width/height and rect/line counts for BOTH the original and the generated PDF so
a coder can compare column x-positions and row heights directly.

    python scripts/measure_grid.py reports/secondary/council/council-schools-rank-overall
    python scripts/measure_grid.py reports/secondary/council/council-schools-rank-overall --page 1
    python scripts/measure_grid.py path/to/some.pdf --page 0

Accepts a report directory (resolves original + generated PDFs like
scripts/build_all.py jobs_for()) OR a direct PDF path. Diagnostic only; it never
modifies any report source.
"""

import argparse
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent

THIN = 2.0     # a rect edge thinner than this (pt) is treated as a gridline
LONG = 3.0     # ...and longer than this in the other axis
CLUSTER = 1.5  # boundaries within this many pt collapse to one line


def cluster(values, tol=CLUSTER):
    """Collapse near-equal coordinates into single representative boundaries."""
    out = []
    for v in sorted(values):
        if out and abs(v - out[-1]) <= tol:
            continue
        out.append(v)
    return out


def grid(page):
    """Return (col_x_boundaries, row_y_boundaries, n_rects, n_lines) for a page.

    Column boundaries come from thin vertical rects (their x-centre), row
    boundaries from thin horizontal rects (their y-centre, in top-origin coords).

    In these originals gridlines are drawn as thin RECTS and page.lines is empty.
    Generated (WeasyPrint) PDFs instead emit real page.lines for the same
    borders, so we also fold vertical/horizontal lines in when present, letting a
    coder compare the true grid of BOTH sources on the same axes.
    """
    cols, rows = [], []
    for r in page.rects:
        w = abs(r["x1"] - r["x0"])
        h = abs(r["bottom"] - r["top"])
        if w < THIN and h > LONG:
            cols.append((r["x0"] + r["x1"]) / 2.0)
        elif h < THIN and w > LONG:
            rows.append((r["top"] + r["bottom"]) / 2.0)
    for ln in page.lines:
        w = abs(ln["x1"] - ln["x0"])
        h = abs(ln["bottom"] - ln["top"])
        if w < THIN and h > LONG:
            cols.append((ln["x0"] + ln["x1"]) / 2.0)
        elif h < THIN and w > LONG:
            rows.append((ln["top"] + ln["bottom"]) / 2.0)
    return cluster(cols), cluster(rows), len(page.rects), len(page.lines)


def _fmt(vals):
    return " ".join(f"{v:.1f}" for v in vals)


def report_grid(pdf_path: Path, page_index, label: str):
    print(f"\n=== {label} ===")
    print(f"pdf: {pdf_path.relative_to(ROOT) if pdf_path.is_relative_to(ROOT) else pdf_path}")
    if not pdf_path.exists():
        print("!!! PDF missing")
        return
    with pdfplumber.open(pdf_path) as pdf:
        pages = range(len(pdf.pages)) if page_index is None else [page_index]
        for i in pages:
            if i >= len(pdf.pages):
                print(f"!!! page {i} out of range (pdf has {len(pdf.pages)} pages)")
                continue
            page = pdf.pages[i]
            cols, rows, n_rects, n_lines = grid(page)
            print(f"\n-- page {i} (0-indexed) --")
            print(f"  page size   : width {page.width:.1f} x height {page.height:.1f}")
            print(f"  rects/lines : {n_rects} rects, {n_lines} lines")
            print(f"  columns ({len(cols)}) x: {_fmt(cols)}")
            print(f"  rows ({len(rows)}) y: {_fmt(rows)}")


def jobs_for(rd: Path):
    """(tag, original_pdf, generated_pdf) tuples for a report dir (mirrors build_all)."""
    ref = rd / "reference"
    out = rd / "output"
    if (rd / "data.json").is_file() and (ref / "original.pdf").is_file():
        return [(None, ref / "original.pdf", out / "report.pdf")]
    jobs = []
    for data in sorted(rd.glob("data_*.json")):
        tag = data.stem[len("data_"):]
        original = ref / f"original_{tag}.pdf"
        if original.is_file():
            jobs.append((tag, original, out / f"report_{tag}.pdf"))
    return jobs


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", type=Path,
                    help="report directory OR a direct PDF path")
    ap.add_argument("--page", type=int, default=None,
                    help="0-indexed page to inspect (default: all pages)")
    a = ap.parse_args(argv)

    target = a.target if a.target.is_absolute() else (ROOT / a.target)
    target = target.resolve()

    if target.is_file() and target.suffix.lower() == ".pdf":
        report_grid(target, a.page, target.name)
        return 0

    if target.is_dir():
        jobs = jobs_for(target)
        if not jobs:
            print(f"no original/generated PDF pairs found under {a.target}")
            return 1
        for tag, original, generated in jobs:
            suffix = f" [{tag}]" if tag else ""
            report_grid(original, a.page, f"{target.name}{suffix} ORIGINAL")
            report_grid(generated, a.page, f"{target.name}{suffix} GENERATED")
        return 0

    print(f"not a PDF file or report directory: {a.target}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
