"""Regenerate and compare EVERY report in one command.

Discovers each self-contained report directory under ``reports/secondary/**`` and
``reports/primary/**`` and,
for each, renders its own template + CSS with WeasyPrint and runs the fidelity
comparison against its reference original PDF. It writes artifacts into each
report's own ``output/`` folder (report.pdf/.html, page PNGs, comparison PNGs +
comparison/README.md) exactly as ``scripts/render_and_compare.py`` does for a
single report.

    python scripts/build_all.py                  # build+compare ALL reports (secondary + primary)
    python scripts/build_all.py --level primary  # only primary-level reports
    python scripts/build_all.py --level council  # only the council scope of every level
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
REPORTS = ROOT / "reports"
# Each level is a self-contained report tree under reports/<level>/<scope>/<report>/.
# Discovery walks every level so a bare `build_all.py` builds all of them.
LEVELS = ["secondary", "primary"]
# Scope names used to restrict discovery within a level (reports/<level>/<scope>/).
SCOPES = ["council", "region"]


def is_report_dir(d: Path) -> bool:
    """A report dir owns its template + CSS and has at least one data.json."""
    if not (d / "template.html.j2").is_file() or not (d / "style.css").is_file():
        return False
    return bool(list(d.glob("data*.json")))


def discover(level: str | None = None, scope: str | None = None):
    """Yield every report directory under reports/<level>/<scope>/.

    ``level`` restricts to one of ``LEVELS`` (e.g. 'primary'); when None, every
    level is walked. ``scope`` restricts to one of ``SCOPES`` (e.g. 'council')
    within each walked level; when None, every scope under the level is walked.
    """
    levels = [level] if level else LEVELS
    for lvl in levels:
        level_root = REPORTS / lvl
        if not level_root.is_dir():
            continue
        scope_roots = ([level_root / scope] if scope
                       else sorted(p for p in level_root.iterdir() if p.is_dir()))
        for root in scope_roots:
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
    ap.add_argument("--level", choices=LEVELS + SCOPES, default=None,
                    help="restrict to one level (primary/secondary) or, for "
                         "backwards compatibility, one scope (council/region) "
                         "across all levels (default: all)")
    ap.add_argument("--scope", choices=SCOPES, default=None,
                    help="restrict to one scope (council/region) within the level(s)")
    ap.add_argument("--no-compare", action="store_true",
                    help="render only; skip the fidelity comparison")
    a = ap.parse_args(argv)

    # --level historically accepted a scope name (council/region); honour that by
    # treating a scope value there as a scope filter across all levels.
    level = a.level if a.level in LEVELS else None
    scope = a.scope or (a.level if a.level in SCOPES else None)

    report_dirs = list(discover(level, scope))
    if not report_dirs:
        where = REPORTS / level if level else REPORTS
        print("no report directories found under", where)
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
