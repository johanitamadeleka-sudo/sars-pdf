"""Measure fill colours per page from a report's OWN original vs its generated PDF.

Diagnostic groundwork for the colour-correction work: for a given report
directory it opens BOTH the reference original PDF and the generated output PDF
with pdfplumber and prints, per page, the fill-colour Counter for each, plus the
set differences (colours only in the original, colours only in the generated).
This lets the palette be corrected PER REPORT from measured values instead of a
generalized/copied palette.

    python scripts/measure_fills.py reports/secondary/council/council-schools-rank-subjectwise

It reuses the EXACT fills() logic from scripts/compare.py (page.rects with fill
and non_stroking_color, normalized to #rrggbb, dropping #ffffff) and mirrors the
report-dir resolution of scripts/build_all.py jobs_for(), so it handles both the
single-source shape (data.json / reference/original.pdf / output/report.pdf) and
the dual-source shape (data_<tag>.json / reference/original_<tag>.pdf /
output/report_<tag>.pdf).

This script NEVER modifies any report source; it only reads PDFs.
"""

import argparse
from collections import Counter
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent


def fills(page):
    """Fill colours on a page as #rrggbb, dropping white. Copied from compare.py.

    Returns a Counter so callers can see how many rects use each colour, while
    still supporting set operations on its keys.
    """
    out = Counter()
    for r in page.rects:
        c = r.get("non_stroking_color")
        if r.get("fill") and c is not None:
            c = tuple(c) if isinstance(c, (list, tuple)) else (c,)
            if len(c) == 1:
                c = c * 3
            if len(c) == 3:
                hexc = "#%02x%02x%02x" % tuple(round(v * 255) for v in c)
                if hexc != "#ffffff":
                    out[hexc] += 1
    return out


def jobs_for(rd: Path):
    """(tag, original_pdf, generated_pdf) tuples for a report dir.

    Mirrors scripts/build_all.py jobs_for() report-dir resolution: tag is None
    for the standard single-source shape, otherwise it labels each per-source
    original/generated pair (data_<tag>.json -> original_<tag>.pdf /
    output/report_<tag>.pdf).
    """
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


def _counter_str(counter: Counter) -> str:
    if not counter:
        return "(none)"
    return " ".join(f"{hexc}×{n}" for hexc, n in sorted(counter.items()))


def measure(original: Path, generated: Path, label: str):
    print(f"\n=== {label} ===")
    print(f"original : {original.relative_to(ROOT) if original.is_relative_to(ROOT) else original}")
    print(f"generated: {generated.relative_to(ROOT) if generated.is_relative_to(ROOT) else generated}")
    if not original.exists():
        print("!!! original PDF missing")
        return
    if not generated.exists():
        print("!!! generated PDF missing (run scripts/build_all.py first)")
        return

    with pdfplumber.open(original) as orig, pdfplumber.open(generated) as gen:
        if len(orig.pages) != len(gen.pages):
            print(f"!!! page count differs: original {len(orig.pages)} vs generated {len(gen.pages)}")
        n = max(len(orig.pages), len(gen.pages))
        for i in range(n):
            of = fills(orig.pages[i]) if i < len(orig.pages) else Counter()
            gf = fills(gen.pages[i]) if i < len(gen.pages) else Counter()
            orig_only = sorted(set(of) - set(gf))
            gen_only = sorted(set(gf) - set(of))
            print(f"\n-- page {i + 1} --")
            print(f"  original fills : {_counter_str(of)}")
            print(f"  generated fills: {_counter_str(gf)}")
            print(f"  orig-only      : {' '.join(orig_only) or '-'}")
            print(f"  gen-only       : {' '.join(gen_only) or '-'}")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report_dir", type=Path,
                    help="report directory (e.g. reports/secondary/council/council-schools-rank-subjectwise)")
    a = ap.parse_args(argv)

    rd = a.report_dir if a.report_dir.is_absolute() else (ROOT / a.report_dir)
    rd = rd.resolve()
    if not rd.is_dir():
        print(f"not a directory: {a.report_dir}")
        return 1

    jobs = jobs_for(rd)
    if not jobs:
        print(f"no original/generated PDF pairs found under {a.report_dir}")
        return 1

    for tag, original, generated in jobs:
        label = rd.name + (f" [{tag}]" if tag else "")
        measure(original, generated, label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
