"""One-off extraction of MWANZA CC SCHOOLS RANK SUBJECTWISE into data.json (display strings).

The report is subject-centric: each subject has a header block + one table whose rows
flow across page breaks (continuation pages do NOT repeat the header). Small subjects
stack several-per-page at the end. We therefore model ONE table per subject (in document
order) and let the HTML/CSS paginate to reproduce the 24-page layout.

Column layout (NO region/council/centre/av/grd):
  S/N | SCHOOL NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA | COMPETENCY LEVEL | C/RANK
"""

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "council_pdf" / "council_pdf" / "MWANZA CC SCHOOLS RANK SUBJECTWISE.pdf"
OUT = ROOT / "reports" / "secondary" / "council" / "council-schools-rank-subjectwise" / "data.json"

NUM_COLS = ["a", "b", "c", "d", "f", "total", "a_c", "pct_a_c", "a_d", "pct_a_d", "gpa"]
NUM_CENTERS = [197, 220, 244, 268, 295, 324, 352, 379, 406, 434, 466]
SCHOOL_MAX_X = 175.0
COMP_MIN_X = 478.0
RANK_MIN_X = 570.0
SN_MAX_X = 55.0


def col_for(cx):
    best, bd = None, 1e9
    for name, c in zip(NUM_COLS, NUM_CENTERS):
        if abs(cx - c) < bd:
            best, bd = name, abs(cx - c)
    return best


def _is_num(t):
    return t.replace(".", "").replace(",", "").isdigit()


def group_lines(words, y_tol=3.0):
    """Group words into visual lines by y-centre."""
    words = sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0]))
    lines, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w)
            cy = y if cy is None else cy
        else:
            lines.append((cy, cur))
            cur, cy = [w], y
    if cur:
        lines.append((cy, cur))
    return lines


def parse_data_row(line):
    row = {k: "" for k in ["sn", "school_name", *NUM_COLS, "competency", "rank"]}
    school_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx < SN_MAX_X:
            row["sn"] = txt
        elif x0 < SCHOOL_MAX_X:
            school_parts.append((x0, txt))
        elif cx >= RANK_MIN_X:
            row["rank"] = txt
        elif cx >= COMP_MIN_X:
            comp_parts.append((x0, txt))
        else:
            row[col_for(cx)] = txt
    row["school_name"] = " ".join(t for _, t in sorted(school_parts))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return row


def parse_overall_row(line):
    row = {k: "" for k in [*NUM_COLS, "competency"]}
    label_parts, comp_parts = [], []
    for w in line:
        x0, x1, txt = w[0], w[2], w[4]
        cx = (x0 + x1) / 2
        if cx >= COMP_MIN_X and not _is_num(txt):
            comp_parts.append((x0, txt))
        elif _is_num(txt) and cx > SN_MAX_X:
            row[col_for(cx)] = txt
        else:
            label_parts.append((x0, txt))
    row["competency"] = " ".join(t for _, t in sorted(comp_parts))
    return " ".join(t for _, t in sorted(label_parts)), row


def hrules(plumber_page):
    """y centres of the horizontal grid rules on a page (thin + thick filled rects)."""
    ys = sorted((r["top"] + r["bottom"]) / 2 for r in plumber_page.rects
                if r.get("fill") and r["bottom"] - r["top"] < 1.2 and r["x1"] - r["x0"] > 10
                and r.get("non_stroking_color") in (0, 0.0, (0,), (0, 0, 0), [0], [0, 0, 0]))
    out = []
    for y in ys:
        if out and y - out[-1][-1] < 0.3:
            out[-1].append(y)
        else:
            out.append([y])
    return [round(sum(c) / len(c), 2) for c in out]


def spans(page):
    """(baseline, text, size, fontname) of every text span, top to bottom."""
    res = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                chars = span["chars"]
                text = "".join(c["c"] for c in chars)
                if text.strip():
                    res.append((round(chars[0]["origin"][1], 2), text.strip(), round(span["size"], 2),
                                span["font"]))
    return sorted(res)


def measure(doc, pdf, subjects):
    """Per-table geometry measured from the original, so each table keeps its own sheet's
    title block, header band heights, row pitch and overall-row height, and the tables that
    Excel printed as one continuous sheet keep their spacing (``gap``)."""
    prev_end = None  # (page index, y of the previous table's bottom rule)
    for s in subjects:
        pi = s["start_page"] - 1
        sp = spans(doc[pi])
        subj = next(x for x in sp if "SCHOOL RANK IN" in x[1] and s["subject"] in x[1])
        above = [x for x in sp if subj[0] - 66 < x[0] < subj[0]]
        lines = above[-5:] + [subj]
        ys = hrules(pdf.pages[pi])
        after = [y for y in ys if y > subj[0]]
        if len(after) >= 3:
            top, y1, y2 = after[:3]
            h1 = y2 - y1
        else:  # header split by the page break (band 2 at the top of the next page)
            top, y1 = after[0], (after[1] if len(after) > 1 else after[0] + 13.95)
            nxt = hrules(pdf.pages[pi + 1])
            h1 = nxt[1] - nxt[0]
        n_first = len([r for r in s["rows"] if r["_page"] == pi])
        body = [y for y in ys if y > top + 1][2:]
        if n_first and len(body) >= n_first:
            pitch = (body[n_first - 1] - (y1 + h1)) / n_first
        else:
            pitch = 11.28
        op, obase = s["overall_pos"]
        oys = hrules(pdf.pages[op])
        o_top = max(y for y in oys if y < obase)
        o_bot = min(y for y in oys if y > obase)
        new_page = prev_end is None or prev_end[0] != pi
        geom = {
            "new_page": new_page,
            "first": lines[0][0] if new_page else round(lines[0][0] - prev_end[1], 2),
            "title": [[round(x[0] - lines[0][0], 2), x[2]] for x in lines],
            "top": round(top - subj[0], 2),
            "hdr": [round(y1 - top, 2), round(h1, 2)],
            "row": round(pitch, 4),
            "ov": round(o_bot - o_top, 2),
            "ov_comp": s["overall_comp_size"],
        }
        band = [r for r in pdf.pages[pi].rects if r.get("fill") and r["x1"] - r["x0"] > 300
                and 3 < r["bottom"] - r["top"] < 20 and lines[0][0] - 12 < r["top"] < subj[0]
                and r.get("non_stroking_color") not in (1, (1, 1, 1), [1, 1, 1], (1,), [1])]
        if band:
            b = band[0]
            geom["band"] = [round(b["x0"], 2), round(b["top"] - lines[0][0], 2), round(b["x1"], 2),
                            round(b["bottom"] - lines[0][0], 2)]
        s["geom"] = geom
        s["subtitle"] = lines[4][1]
        # the header's S/N label is Arial Narrow on the first sheet's design only
        sn = next((x for x in spans(doc[pi]) if x[1] == "S/N" and x[0] > subj[0]), None)
        s["design"] = "a" if sn and "Narrow" in sn[3] else "b"
        # the school rows' competency label: Arial Narrow Bold on some sheets, Arial Bold on others
        comp = next((x for x in spans(doc[pi]) if x[1].startswith("Grade") and x[0] > top), None)
        geom["comp_font"] = "N" if comp and "Narrow" in comp[3] else "A"
        prev_end = (op, o_bot)


def main():
    doc = pymupdf.open(SRC)
    import pdfplumber
    pdf = pdfplumber.open(SRC)
    subjects = []  # each: {subject, start_page, rows, overall, overall_label}
    cur = None
    for pi in range(doc.page_count):
        page = doc[pi]
        lines = group_lines(page.get_text("words"))
        for cy, line in lines:
            line = sorted(line, key=lambda w: w[0])
            text = " ".join(w[4] for w in line)
            if "SCHOOL RANK IN" in text and "COUNCILWISE" in text:
                subj = text.split("SCHOOL RANK IN", 1)[1].rsplit("COUNCILWISE", 1)[0].strip()
                cur = {"subject": subj, "start_page": pi + 1, "rows": [],
                       "overall": None, "overall_label": None}
                subjects.append(cur)
                continue
            if cur is None:
                continue
            if "OVERALL" in text and "PERFORMANCE" in text:
                lbl, orow = parse_overall_row(line)
                # keep the label's literal spacing ('COUNCIL OVERALL  PERFORMANCE')
                sp = next((x for x in spans(page) if "OVERALL" in x[1] and abs(x[0] - line[0][3]) < 4), None)
                cur["overall_label"] = sp[1] if sp else lbl
                cur["overall"] = orow
                comp = next((x for x in spans(page) if x[1].startswith("Grade") and abs(x[0] - line[0][3]) < 4), None)
                cur["overall_comp_size"] = comp[2] if comp else 7.32
                cur["overall_pos"] = (pi, sp[0] if sp else line[0][3])
                continue
            first = line[0]
            if first[0] < SN_MAX_X and first[4].isdigit():
                row = parse_data_row(line)
                row["_page"] = pi
                cur["rows"].append(row)

    document = {
        "page_size": "Letter",
        "ministry": [
            "THE PRIME MINISTER'S OFFICE",
            "REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT",
            "MWANZA REGION",
        ],
        "exam_name": "REGIONAL FORM TWO MOCK ASSESSMENT RESULTS, JULY 2026",
        "report_title": "MWANZA CC SCHOOLS RANK SUBJECTWISE",
        "scope": "COUNCILWISE",
        # the source PDF ends with one empty page
        "trailing_blank_page": not doc[doc.page_count - 1].get_text("words"),
    }
    measure(doc, pdf, subjects)
    tables = []
    for s in subjects:
        for r in s["rows"]:
            r.pop("_page", None)
        tab = {"subject": s["subject"], "scope": "COUNCILWISE", "subtitle": s["subtitle"],
               "design": s["design"], "geom": s["geom"], "rows": s["rows"]}
        if s["overall"]:
            tab["overall"] = s["overall"]
            tab["overall_label"] = s["overall_label"]
        tables.append(tab)

    data = {"document": document, "tables": tables}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(len(t["rows"]) for t in tables)
    print(f"subjects={len(tables)} rows={total} -> {OUT}")
    for t in tables:
        print(f"  {t['subject']:<28} rows={len(t['rows']):>3} "
              f"overall={t.get('overall_label') or '-'}")


if __name__ == "__main__":
    main()
