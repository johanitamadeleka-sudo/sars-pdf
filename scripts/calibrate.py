"""Measure the original PDF and store each table's layout in the data JSON.

    python scripts/calibrate.py reference/original.pdf data/lakezone_f2_mock_aug2026.json

Per table (in page order) it records:
  layout.title_top    top of the first heading line (pt, pdfplumber "top")
  layout.subject_top  top of the "SCHOOL RANK IN ..." line
  layout.subject_size font size of that line
  layout.table_top    y of the table's top grid line
  layout.rows         [h1, h2, body row, overall]  grid-line distances
  borders             thick (0.84pt) border segments, only if they differ from the default
  title / exam strings exactly as printed (spacing included)

Everything else (fonts, colours, column widths) is fixed and lives in the CSS / renderer.
"""

import json
import sys
from pathlib import Path

import pdfplumber

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.layout import DEFAULT_THICK, X  # noqa: E402


def black(c):
    c = tuple(c) if isinstance(c, (list, tuple)) else (c,)
    return all(v == 0 for v in c)


def text_line(chars):
    chars = sorted(chars, key=lambda c: c["x0"])
    out = chars[0]["text"]
    for a, b in zip(chars, chars[1:]):
        gap, sp = b["x0"] - a["x1"], 0.2778 * a["size"]
        out += " " * (round(gap / sp) if gap > sp * 0.5 else 0) + b["text"]
    return out


def measure(path):
    tables = []
    for p in pdfplumber.open(path).pages:
        blk = [r for r in p.rects if r["non_stroking_color"] is not None and black(r["non_stroking_color"])]
        hs = sorted({round((r["top"] + r["bottom"]) / 2, 2) for r in blk if r["x1"] - r["x0"] > 100})
        hs = [y for i, y in enumerate(hs) if i == 0 or y - hs[i - 1] > 1]
        groups = [[hs[0]]]
        for y in hs[1:]:
            (groups[-1].append(y) if y - groups[-1][-1] < 30 else groups.append([y]))
        prev = 0
        for t in groups:
            # heading lines: bold upright chars between previous table and this one, centred on the page
            lines = {}
            for c in p.chars:
                if c["upright"] and prev < c["top"] < t[0] and 100 < c["x0"] < 520:
                    lines.setdefault(round(c["top"], 1), []).append(c)
            heads = [(top, cs[0]["size"], text_line(cs)) for top, cs in sorted(lines.items())
                     if min(c["x0"] for c in cs) > 100 and max(c["x1"] for c in cs) < 520]
            bands = [("h1", t[0], t[1]), ("h2", t[1], t[2]), ("body", t[2], t[-2] if len(t) > 4 else t[-1]),
                     ("ov", t[-2], t[-1])] if len(t) > 4 else [("h1", t[0], t[1]), ("h2", t[1], t[2]), ("body", t[2], t[-1])]
            thick = set()
            for r in blk:
                w, h = r["x1"] - r["x0"], r["bottom"] - r["top"]
                if not (t[0] - 1 < r["top"] < t[-1] + 1):
                    continue
                if h > w and w > 0.65:
                    k = min(range(len(X)), key=lambda i: abs(X[i] - (r["x0"] + r["x1"]) / 2))
                    for n, a, b in bands:
                        if b - a > 1 and r["top"] < b - 1 and r["bottom"] > a + 1:
                            thick.add(f"V{k}:{n}")
                if w > h and h > 0.65:
                    yc = (r["top"] + r["bottom"]) / 2
                    k = min(range(len(t)), key=lambda i: abs(t[i] - yc))
                    if k == 0:
                        name = "top"
                    elif k == 1:
                        name = "h1b"
                    elif k == 2:
                        name = "hb"
                    elif k == len(t) - 1:
                        name = "bot"
                    elif k == len(t) - 2 and len(t) > 4:
                        name = "ovt"
                    else:
                        continue
                    c0 = min(range(len(X)), key=lambda i: abs(X[i] - r["x0"]))
                    c1 = min(range(len(X)), key=lambda i: abs(X[i] - r["x1"]))
                    thick.add(f"H{name}:{c0}-{c1}")
            rows = [round(t[1] - t[0], 2), round(t[2] - t[1], 2)]
            if len(t) > 4:
                body = [b - a for a, b in zip(t[2:-2], t[3:-1])]
                body = sorted(body)
                rows += [round(body[len(body) // 2], 2), round(t[-1] - t[-2], 2)]
            else:
                rows += [round(t[-1] - t[2], 2), None]
            tables.append({"heads": heads, "table_top": t[0], "rows": rows, "thick": sorted(thick)})
            prev = t[-1]
    return tables


def main(orig, data_path):
    m = measure(orig)
    doc = json.loads(Path(data_path).read_text())
    tables = [t for p in doc["pages"] for t in p["tables"]]
    assert len(m) == len(tables), (len(m), len(tables))
    first = m[0]["heads"]
    doc["document"]["ministry"] = [first[0][2], first[1][2]]
    doc["document"]["exam_board"] = first[2][2]
    doc["document"]["exam_name"] = first[3][2]
    for t, mm in zip(tables, m):
        heads = mm["heads"]
        t["title"] = heads[-1][2]
        t["layout"] = {
            "title_top": heads[0][0],
            "subject_top": heads[-1][0],
            "subject_size": round(heads[-1][1], 2),
            "table_top": mm["table_top"],
            "rows": mm["rows"],
        }
        if set(mm["thick"]) != set(DEFAULT_THICK):
            t["borders"] = {"add": sorted(set(mm["thick"]) - set(DEFAULT_THICK)),
                            "remove": sorted(set(DEFAULT_THICK) - set(mm["thick"]))}
        else:
            t.pop("borders", None)
    Path(data_path).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"calibrated {len(tables)} tables")


if __name__ == "__main__":
    main(*sys.argv[1:3])
