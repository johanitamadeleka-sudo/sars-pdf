"""Render a self-contained report folder and compare it to its reference original.

A report folder is any directory containing:
    template.html.j2   its own Jinja2 template
    style.css          its own stylesheet (fully self-contained, no shared include)
    data.json          display-string data model
    reference/original.pdf   the PDF to match
It writes artifacts into the folder's own output/ (report.pdf, report.html, pages/,
comparison/README.md + side-by-side PNGs).

    python scripts/render_and_compare.py reports/secondary/council/council-schools-rank-subjectwise

This is a thin wrapper over sars_pdf.render (with --template-dir) and scripts/compare.py,
so the exact same workflow the lakezone example uses applies to every per-report folder.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report_dir", type=Path, help="report folder (holds data.json etc.)")
    a = ap.parse_args(argv)

    rd = a.report_dir.resolve()
    data = rd / "data.json"
    original = rd / "reference" / "original.pdf"
    out = rd / "output"
    pdf = out / "report.pdf"
    html = out / "report.html"
    out.mkdir(parents=True, exist_ok=True)

    render = [sys.executable, "-m", "sars_pdf.render", str(data),
              "--template-dir", str(rd), "--pdf", str(pdf), "--html", str(html)]
    subprocess.run(render, cwd=ROOT, check=True)

    compare = [sys.executable, str(ROOT / "scripts" / "compare.py"),
               str(original), str(pdf),
               "--out", str(out / "comparison"), "--pages-out", str(out / "pages")]
    subprocess.run(compare, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
