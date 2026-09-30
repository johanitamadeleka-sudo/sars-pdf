"""Download per-SCHOOL result PDFs from a sars.ac.tz council results page.

    python scripts/fetch_school_results.py \
        https://sars.ac.tz/results/exam/form-two-mock-result/2026/mwanza/buchosa-1787231755 \
        --only S0762 S1419 S1941            # centre numbers (default: every school)

The council page lists every school as
``view-results?file=results%2Fpdfs%2F<hash>.pdf&name=<CNO>-<SCHOOL NAME>`` (the region /
council summaries are ``file=summaries%2F...`` links and are skipped). Each PDF is fetched
from ``serve-pdf?file=results%2Fpdfs%2F<hash>.pdf`` and saved as
``school_pdf/<CNO> <SCHOOL NAME>.pdf``, ready for scripts/extract_school_results.py.
Same approach as scripts/fetch_primary_summaries.py.
"""

import argparse
import html
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "school_pdf"
LINK = re.compile(r'view-results\?file=(results%2Fpdfs%2F[A-Za-z0-9]+\.pdf)&(?:amp;)?name=([^"&]+)')


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sars-pdf)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="council results page (…/form-two-mock-result/<year>/<region>/<council>)")
    ap.add_argument("--only", nargs="*", help="centre numbers to fetch, e.g. S0762")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)

    page = get(a.url.split("?")[0] + "?letter=ALL").decode("utf-8", "replace")
    schools = {}
    for file_q, name_q in LINK.findall(page):
        name = re.sub(r"\s+", " ", html.unescape(urllib.parse.unquote(name_q))).strip()
        cno, _, school = name.partition("-")
        schools[cno.strip()] = (file_q, school.strip())
    wanted = [c.upper() for c in a.only] if a.only else sorted(schools)
    print(f"{len(schools)} schools listed; fetching {len(wanted)}")

    base = "https://sars.ac.tz/serve-pdf?file="
    a.out.mkdir(parents=True, exist_ok=True)
    for cno in wanted:
        if cno not in schools:
            print(f"!! {cno} not on the page")
            continue
        file_q, school = schools[cno]
        data = get(base + file_q)
        if not data.startswith(b"%PDF"):
            print(f"!! {cno}: not a PDF")
            continue
        dest = a.out / f"{cno} {school}.pdf"
        dest.write_bytes(data)
        print(f"wrote {dest.relative_to(ROOT)} ({len(data) // 1024} KB)")


if __name__ == "__main__":
    main()
