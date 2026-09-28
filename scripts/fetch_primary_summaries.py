"""Discover + download the PRIMARY (STD4 / Darasa la IV) council and region
summary PDFs from the Mwanza SARS results index, mirroring how the secondary
council_pdf / region_pdf collections were sourced.

The results index page exposes a "summary-row" list of documents, each linking
to a PDF.js viewer at ``/view-results?file=summaries%2F<hash>.pdf&name=<title>``.
The raw file is served at ``/serve-pdf?file=summaries%2F<hash>.pdf``.

Documents split into two scopes by title:
  * council-level  -> titles beginning "MWANZA CC ..."
  * region-level   -> the "... STD4 2026" set (MKOA ..., SHULE ... STD4,
                      KATA STD4, HALMASHAURI ... STD4)

Usage:
    python scripts/fetch_primary_summaries.py --out <staging-dir>
"""
import argparse
import hashlib
import html as H
import os
import re
import urllib.parse
import urllib.request

INDEX_URL = (
    "https://sars.ac.tz/results/exam/matokeo-darasa-la-iv-mock-mkoa/"
    "2026/mwanza/mwanza-cc-1787231849"
)
UA = {"User-Agent": "Mozilla/5.0"}
LINK = re.compile(
    r"view-results\?file=summaries%2F([A-Za-z0-9]+)\.pdf&amp;name=([^\"']+)"
)


def discover():
    raw = urllib.request.urlopen(
        urllib.request.Request(INDEX_URL, headers=UA), timeout=60
    ).read().decode("utf-8", "ignore")
    seen = {}
    for m in LINK.finditer(raw):
        h = m.group(1)
        name = H.unescape(urllib.parse.unquote(m.group(2)))
        seen.setdefault(name, h)
    return seen


def scope_for(name: str) -> str:
    return "council" if name.upper().startswith("MWANZA CC") else "region"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    docs = discover()
    hashes = {}
    for name, h in sorted(docs.items()):
        scope = scope_for(name)
        d = os.path.join(a.out, scope)
        os.makedirs(d, exist_ok=True)
        serve = f"https://sars.ac.tz/serve-pdf?file=summaries%2F{h}.pdf"
        data = urllib.request.urlopen(
            urllib.request.Request(serve, headers=UA), timeout=180
        ).read()
        assert data[:5] == b"%PDF-", f"not a PDF: {name}"
        open(os.path.join(d, name + ".pdf"), "wb").write(data)
        md5 = hashlib.md5(data).hexdigest()
        hashes.setdefault(md5, []).append(name)
        print(f"{scope:8} {len(data):>8} {md5[:12]} {name}")
    print("--- duplicate md5 groups ---")
    for md5, names in hashes.items():
        if len(names) > 1:
            print(md5, names)
    print(f"total {len(docs)} documents")


if __name__ == "__main__":
    main()
