"""Extract 'Mwanza f2 Mock Mobility 2026' (6pp, portrait) into region-mobility/data.json.

Region-only report. 2025-vs-2026 GPA movement, flowing across 6 pages. Columns:
  S/NO. | COUNCIL | SCHOOL NAME | OWNERSHIP
  FTNA 2025(TOTAL, %(I-III), GPA) | MOCK 2026(TOTAL, %(I-III), GPA)
  CHANYA | MJONGEO WA GPA | HALI YA MJONGEO
Swahili labels (IMEPANDA / UMESHUKA / MJONGEO / CHANYA) preserved exactly. Header
'POSITIVE MOBILITY'. Coordinate based (pymupdf words), never hand-typed.
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "region_pdf" / "region_pdf" / "Mwanza f2 Mock Mobility 2026.pdf"
OUT = ROOT / "reports" / "secondary" / "region" / "region-mobility" / "data.json"

SNO_MAX = 37.7
COUNCIL_MAX = 97.7
SCHOOL_MAX = 242.8
OWN_MAX = 296.3
# numeric column centres (midpoints of measured boundaries)
BOUNDS = [296.3, 325.8, 350.5, 381.8, 411.4, 436.9, 470.2, 502.4, 539.6, 589.9]
NUM_KEYS = ["ftna_total", "ftna_pct", "ftna_gpa", "mock_total", "mock_pct", "mock_gpa",
            "chanya", "mjongeo", "hali"]
NUM_CENTERS = [(BOUNDS[i] + BOUNDS[i + 1]) / 2 for i in range(len(BOUNDS) - 1)]


def group_lines(words, y_tol=3.2):
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w)
            cy = y if cy is None else (cy * (len(cur) - 1) + y) / len(cur)
        else:
            lines.append((cy, cur))
            cur, cy = [w], y
    if cur:
        lines.append((cy, cur))
    return lines


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_KEYS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def parse_band(band):
    row = {k: "" for k in ["sno", "council", "school", "ownership", *NUM_KEYS]}
    council_p, school_p, own_p = [], [], []
    for w in band:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SNO_MAX:
            row["sno"] = txt
        elif x0 < COUNCIL_MAX:
            council_p.append((x0, txt))
        elif x0 < SCHOOL_MAX:
            school_p.append((x0, txt))
        elif x0 < OWN_MAX:
            own_p.append((x0, txt))
        else:
            key = col_for(cx)
            row[key] = (row[key] + " " + txt).strip() if row[key] else txt
    row["council"] = " ".join(t for _, t in sorted(council_p))
    row["school"] = " ".join(t for _, t in sorted(school_p))
    row["ownership"] = " ".join(t for _, t in sorted(own_p))
    return row


def main():
    doc = pymupdf.open(SRC)
    rows = []
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        # merge the two text-lines of each row: cluster with a tolerance that joins the
        # ~0.2pt-separated pair but not adjacent rows (~11.6pt apart).
        hdr_limit = 145 if pi == 0 else 62
        for cy, band in group_lines(words, y_tol=3.2):
            if cy <= hdr_limit:
                continue
            first = min(band, key=lambda w: w[0])
            numeric = sum(1 for w in band if w[4].replace(".", "").replace("-", "").isdigit())
            if first[0] < SNO_MAX and first[4].isdigit() and len(first[4]) <= 3 and numeric >= 5:
                rows.append(parse_band(band))

    document = {
        "page_size": "Letter-portrait",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "POSITIVE MOBILITY",
    }
    data = {"document": document, "rows": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    empt = sum(1 for r in rows for k in NUM_KEYS if not r[k])
    print(f"rows={len(rows)} empty={empt} -> {OUT}")
    for r in rows[:3] + rows[-2:]:
        print(f"  {r['sno']} {r['council']:<12} {r['school']:<22} {r['ownership']:<10} "
              f"FTNA {r['ftna_total']}/{r['ftna_pct']}/{r['ftna_gpa']} "
              f"MOCK {r['mock_total']}/{r['mock_pct']}/{r['mock_gpa']} "
              f"CH {r['chanya']} MJ {r['mjongeo']} {r['hali']}")


if __name__ == "__main__":
    main()
