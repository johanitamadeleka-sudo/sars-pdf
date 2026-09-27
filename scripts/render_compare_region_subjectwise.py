"""Render + compare the region-schools-rank-subjectwise report.

This report's single self-contained template+CSS drives TWO source subjects (EDK 1pp
and English Language 6pp). Each source PDF keeps its OWN comparison, as required.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RD = ROOT / "reports" / "secondary" / "region" / "region-schools-rank-subjectwise"

JOBS = [
    ("edk", "data_edk.json", "original_edk.pdf"),
    ("english", "data_english.json", "original_english.pdf"),
]


def main():
    for tag, data, ref in JOBS:
        pdf = RD / "output" / f"report_{tag}.pdf"
        html = RD / "output" / f"report_{tag}.html"
        subprocess.run([sys.executable, "-m", "sars_pdf.render", str(RD / data),
                        "--template-dir", str(RD), "--pdf", str(pdf), "--html", str(html)],
                       cwd=ROOT, check=True)
        print(f"=== compare {tag} ===")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "compare.py"),
                        str(RD / "reference" / ref), str(pdf),
                        "--out", str(RD / "output" / f"comparison_{tag}"),
                        "--pages-out", str(RD / "output" / f"pages_{tag}")],
                       cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
