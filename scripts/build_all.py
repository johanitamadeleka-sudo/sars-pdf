"""Regenerate and compare EVERY secondary report in one command.

Discovers each self-contained report directory under ``reports/secondary/**`` and,
for each, renders its own template + CSS with WeasyPrint and runs the fidelity
comparison against its reference original PDF. It writes artifacts into each
report's own ``output/`` folder (report.pdf/.html, page PNGs, comparison PNGs +
comparison/README.md) exactly as ``scripts/render_and_compare.py`` does for a
single report.

    python scripts/build_all.py                 # build+compare all secondary reports
    python scripts/build_all.py --level council  # only council reports
    python scripts/build_all.py --no-compare     # render only (skip compare.py)

A report directory is any directory that is fully self-contained, i.e. it holds
its OWN ``template.html.j2`` + ``style.css`` and either:

  * the standard shape - a single ``data.json`` and ``reference/original.pdf``; or
  * the multi-source shape - one or more ``data_<tag>.json`` files, each paired
    with ``reference/original_<tag>.pdf`` (used by region-schools-rank-subjectwise,
    whose one template drives two subject PDFs, each compared separately).

This entrypoint NEVER modifies report sources; it only regenerates ``output/``.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECONDARY = ROOT / "reports" / "secondary"


def is_report_dir(d: Path) -> bool:
    """A report dir owns its template + CSS and has at least one data.json."""
    if not (d / "template.html.j2").is_file() or not (d / "style.css").is_file():
        return False
    return bool(list(d.glob("data*.json")))


def discover(level: str | None):
    """Yield every report directory under reports/secondary/[level]."""
    roots = [SECONDARY / level] if level else sorted(p for p in SECONDARY.iterdir() if p.is_dir())
    for root in roots:
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            if d.is_dir() and is_report_dir(d):
                yield d


def jobs_for(rd: Path):
    """Return (tag, data_json, original_pdf) tuples for a report directory.

    tag is None for the standard single-source shape; otherwise it labels the
    per-source output/comparison so multiple sources in one dir stay separate.
    """
    ref = rd / "reference"
    if (rd / "data.json").is_file() and (ref / "original.pdf").is_file():
        return [(None, rd / "data.json", ref / "original.pdf")]
    out = []
    for data in sorted(rd.glob("data_*.json")):
        tag = data.stem[len("data_"):]
        original = ref / f"original_{tag}.pdf"
        if original.is_file():
            out.append((tag, data, original))
    return out


def render_and_compare(rd: Path, do_compare: bool) -> bool:
    ok = True
    for tag, data, original in jobs_for(rd):
        suffix = "" if tag is None else f"_{tag}"
        out = rd / "output"
        out.mkdir(parents=True, exist_ok=True)
        pdf = out / f"report{suffix}.pdf"
        html = out / f"report{suffix}.html"
        label = rd.relative_to(ROOT).as_posix() + (f" [{tag}]" if tag else "")
        print(f"::: render {label}")
        r = subprocess.run(
            [sys.executable, "-m", "sars_pdf.render", str(data),
             "--template-dir", str(rd), "--pdf", str(pdf), "--html", str(html)],
            cwd=ROOT,
        )
        if r.returncode != 0:
            print(f"!!! render FAILED: {label}")
            ok = False
            continue
        if do_compare:
            print(f"::: compare {label}")
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "compare.py"),
                 str(original), str(pdf),
                 "--out", str(out / f"comparison{suffix}"),
                 "--pages-out", str(out / f"pages{suffix}")],
                cwd=ROOT,
            )
            if r.returncode != 0:
                print(f"!!! compare FAILED: {label}")
                ok = False
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--level", choices=["council", "region"], default=None,
                    help="restrict to one level under reports/secondary/ (default: all)")
    ap.add_argument("--no-compare", action="store_true",
                    help="render only; skip the fidelity comparison")
    a = ap.parse_args(argv)

    report_dirs = list(discover(a.level))
    if not report_dirs:
        print("no report directories found under", SECONDARY)
        return 1

    print(f"found {len(report_dirs)} report directories")
    all_ok = True
    for rd in report_dirs:
        if not render_and_compare(rd, not a.no_compare):
            all_ok = False

    print("\n=== build-all", "OK" if all_ok else "FAILED", "===")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
