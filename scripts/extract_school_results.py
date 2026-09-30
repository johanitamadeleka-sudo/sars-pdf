"""Extract a secondary per-SCHOOL result PDF (Form Two mock, sars.ac.tz) into data_<tag>.json.

    python scripts/extract_school_results.py "school_pdf/S0762 KOME SECONDARY SCHOOL.pdf" [...]

Each source PDF is one Excel sheet, printed on US Letter landscape:

  page 1       titles + DIVISION PERFORMANCE SUMMARY (F/M/T x I..0), then the candidate list
  pages 2..n   more candidate rows (CNO | NAME | SEX | AGGT | DIV | POS | DETAILED SUBJECTS)
  last page(s) EXAMINATION CENTRE OVERALL PERFORMANCE, DIVISION PERFORMANCE,
               SUBJECT PERFORMANCE AND RANKING, SUBJECTS GRADING PERFORMANCE SUMMARY

Every table sits on the same sheet columns, so the whole grid is described by one list of
25 column boundaries (``layout.cols``: band edge, b1..b23, band edge) and each table cell
is a range of those columns (see the *_CELLS tables below, mirrored by template.html.j2).

Excel scales each school's sheet differently, so the extractor also measures that
school's row heights, font scale and page breaks into ``layout``. ``layout`` is optional:
data without it (e.g. produced straight from the results database) renders with the
template's defaults and automatic pagination. All values are display strings read from
the PDF by coordinates, never typed by hand.

Writes reports/secondary/school/school-results/data_<tag>.json and copies the source to
reference/original_<tag>.pdf, where <tag> is the centre number in lower case (s0762).
"""

import argparse
import json
import re
import shutil
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "reports" / "secondary" / "school" / "school-results"

CNO_RE = re.compile(r"^S\d{4}-\d{4}$")
CODE_RE = re.compile(r"^\d{3}$")
# Excel draws every rule as two 0.48pt rects ~1pt apart ("double"); the boundary is midway.
HALF = 0.24
NATIVE_BODY = 7.0  # body font size (pt) of the sheet at 100%

# merged-cell column ranges (indices into layout.cols) per table
CAND_CELLS = [(1, 2), (2, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 23)]
DIVSUM_CELLS = [(3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
OVR_CELLS = [(1, 8), (8, 23)]
GPA_CELLS = [(1, 8), (8, 10), (10, 14), (14, 23)]
DIVP_CELLS = [(1, 3), (3, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 16),
              (16, 18), (18, 20), (20, 22), (22, 23)]
SUBJ_CELLS = [(1, 2), (2, 4)] + [(i, i + 1) for i in range(4, 19)] + [(19, 21), (21, 23)]
GRAD_CELLS = [(1, 2), (2, 4)] + [(i, i + 1) for i in range(4, 22)]
DIVP_KEYS = ["regist", "absent", "sat", "inc", "clean", "div_i", "div_ii", "div_iii",
             "div_iv", "div_0", "div_i_iii", "div_i_iv"]


# ---------------------------------------------------------------- geometry helpers
def _cluster(values, tol=1.6):
    groups = []
    for v in sorted(values):
        if groups and v - groups[-1][-1] < tol:
            groups[-1].append(v)
        else:
            groups.append([v])
    return [round((g[0] + g[-1]) / 2 + HALF, 2) for g in groups]


def rules(page):
    """Thin black rects -> (horizontal rects, vertical rects)."""
    hs, vs = [], []
    for d in page.get_drawings():
        f = d.get("fill")
        if not f or max(f) > 0:
            continue
        r = d["rect"]
        if r.height < 2 and r.width > 2:
            hs.append(r)
        elif r.width < 2 and r.height > 2:
            vs.append(r)
    return hs, vs


def row_lines(page):
    hs, _ = rules(page)
    return _cluster([r.y0 for r in hs])


def col_lines(page, y0, y1):
    _, vs = rules(page)
    return _cluster([r.x0 for r in vs if r.y0 >= y0 - 2 and r.y1 <= y1 + 2])


def band(page):
    """Extent (x0, y0, x1, y1) of the sheet's blue background (#92cddc) on the page."""
    rs = [d["rect"] for d in page.get_drawings()
          if d.get("fill") and "%02x%02x%02x" % tuple(round(c * 255) for c in d["fill"]) == "92cddc"]
    return (min(r.x0 for r in rs), min(r.y0 for r in rs), max(r.x1 for r in rs), max(r.y1 for r in rs))


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                if s["text"].strip():
                    x0, y0, x1, y1 = s["bbox"]
                    out.append({"t": s["text"].strip(), "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                                "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2,
                                "font": s["font"], "size": s["size"], "origin": s["origin"]})
    return out


def interval(v, bounds):
    """Index i with bounds[i] <= v < bounds[i+1], else None."""
    for i in range(len(bounds) - 1):
        if bounds[i] <= v < bounds[i + 1]:
            return i
    return None


def find(sp, text):
    return next((s for s in sp if s["t"].startswith(text)), None)


def row_cells(sp, top, bottom, cols, cells):
    """Texts of one sheet row, one string per merged cell range."""
    out = [""] * len(cells)
    for s in sorted(sp, key=lambda s: s["x0"]):
        if not top <= s["cy"] < bottom:
            continue
        for k, (a, b) in enumerate(cells):
            if cols[a] <= s["cx"] < cols[b]:
                out[k] = (out[k] + " " + s["t"]).strip()
                break
    return out


class Page:
    def __init__(self, doc, pi):
        self.pi = pi
        self.page = doc[pi]
        self.sp = spans(self.page)
        self.ys = row_lines(self.page)
        self.band = band(self.page)

    def row(self, s, offset=0):
        """(top, bottom) of the sheet row containing span ``s`` (or ``offset`` rows below)."""
        i = interval(s["cy"], self.ys) + offset
        return self.ys[i], self.ys[i + 1]


def locate(pages, text):
    for p in reversed(pages):
        s = find(p.sp, text)
        if s:
            return p, s
    raise SystemExit(f"'{text}' not found")


def med(v):
    v = sorted(v)
    return round(v[len(v) // 2], 2)


# ---------------------------------------------------------------- extraction
def extract(pdf_path):
    doc = pymupdf.open(pdf_path)
    pages = [Page(doc, i) for i in range(len(doc))]
    p1 = pages[0]

    # --- titles (Tahoma, centred) and page footer (Courier, optional)
    titles = sorted([s for s in p1.sp if s["font"].startswith("Tahoma")], key=lambda s: s["y0"])
    title_text = [s["t"] for s in titles]
    footer = next((s["t"] for s in p1.sp if s["font"].startswith("Courier")), None)
    school_title = title_text[-1]
    m = re.match(r"^(S\d{4})\s*-\s*(.+)$", school_title)
    centre_no, school_name = (m.group(1), m.group(2)) if m else ("", school_title)
    font_scale = round(max(s["size"] for s in p1.sp if s["font"] == "ArialMT") / NATIVE_BODY, 4)

    # --- sheet columns: candidate grid -> b1..b8 + b23; division summary -> b3, b9;
    #     grading grid -> b1..b22 (except b3, merged into SUBJECT NAME)
    cno0 = next(s for s in p1.sp if CNO_RE.match(s["t"]))
    cand_cols = col_lines(p1.page, *p1.row(cno0))
    div_label = find(p1.sp, "DIVISION PERFORMANCE SUMMARY")
    sex_hdr = min((s for s in p1.sp if s["t"] == "SEX"), key=lambda s: s["y0"])
    t_row = next(s for s in p1.sp if s["t"] == "T" and s["y0"] > sex_hdr["y0"] and s["x0"] < cand_cols[3])
    div_top, _ = p1.row(sex_hdr)
    _, div_bottom = p1.row(t_row)
    divsum_cols = col_lines(p1.page, div_top, div_bottom)
    gp, g_title = locate(pages, "EXAMINATION CENTRE SUBJECTS GRADING")
    g_top, _ = gp.row(g_title)
    grad_cols = col_lines(gp.page, gp.row(g_title, 1)[0], gp.ys[-1])
    cols = ([round(p1.band[0], 2)] + grad_cols[:2] + [divsum_cols[0]] + grad_cols[2:]
            + [cand_cols[-1], round(p1.band[2], 2)])
    assert len(cols) == 25, (len(cols), cols)
    assert abs(cols[9] - divsum_cols[-1]) < 1.0 and abs(cols[8] - cand_cols[-2]) < 1.0, cols

    # --- page-1 division summary (header row + F/M/T)
    div_ys = [y for y in p1.ys if div_top - 0.1 <= y <= div_bottom + 0.1]
    division_summary = []
    for r in range(1, len(div_ys) - 1):
        c = row_cells(p1.sp, div_ys[r], div_ys[r + 1], cols, DIVSUM_CELLS)
        division_summary.append(dict(zip(["sex", "i", "ii", "iii", "iv", "zero"], c)))

    # --- candidates, page by page
    candidates, page_rows, row_h = [], [], []
    cand_first = cont_top = last_cand = None
    for p in pages:
        cnos = sorted((s for s in p.sp if CNO_RE.match(s["t"]) and s["x0"] < cols[2]),
                      key=lambda s: s["cy"])
        if not cnos:
            continue
        for n, s in enumerate(cnos):
            top, bottom = p.row(s)
            c = row_cells(p.sp, top, bottom, cols, CAND_CELLS)
            candidates.append(dict(zip(["cno", "name", "sex", "aggt", "div", "pos", "subjects"], c)))
            row_h.append(bottom - top)
            if n == 0 and p.pi == 0:
                cand_first = top
            elif n == 0 and cont_top is None:
                cont_top = top
        last_cand = (p, p.row(cnos[-1])[1])
        page_rows.append(len(cnos))
    # CNO / NAME are bottom-aligned on most sheets but vertically centred on some
    top, bottom = p1.row(cno0)
    cno_bottom_aligned = abs(cno0["y1"] - (bottom - 0.74)) < 0.4
    cand_head_top = p1.ys[p1.ys.index(cand_first) - 1]

    # --- overall performance: title + 7 label/value rows
    op, o_title = locate(pages, "EXAMINATION CENTRE OVERALL PERFORMANCE")
    o_i = op.ys.index(op.row(o_title)[0])
    o_ys = op.ys[o_i:o_i + 9]
    rows = [row_cells(op.sp, o_ys[r], o_ys[r + 1], cols, OVR_CELLS) for r in range(1, 8)]
    gpa = row_cells(op.sp, o_ys[5], o_ys[6], cols, GPA_CELLS)
    overall = {"region": rows[0][1], "council": rows[1][1], "passed": rows[2][1],
               "average": rows[3][1], "gpa": gpa[1], "competency": gpa[2],
               "council_rank": rows[5][1], "region_rank": rows[6][1]}

    # --- division performance: title, header, counts, percent
    dp, d_title = locate(pages, "EXAMINATION CENTRE DIVISION PERFORMANCE")
    d_i = dp.ys.index(dp.row(d_title)[0])
    d_ys = dp.ys[d_i:d_i + 5]
    counts = row_cells(dp.sp, d_ys[2], d_ys[3], cols, DIVP_CELLS)
    pct = row_cells(dp.sp, d_ys[3], d_ys[4], cols, DIVP_CELLS)
    division_performance = {"counts": dict(zip(DIVP_KEYS, counts)),
                            "percent": dict(zip(DIVP_KEYS, pct))}

    # --- subject performance and ranking
    sp_, s_title = locate(pages, "EXAMINATION CENTRE SUBJECT PERFORMANCE AND RANKING")
    s_i = sp_.ys.index(sp_.row(s_title)[0])
    subjects, subj_h = [], []
    r = s_i + 3
    while r < len(sp_.ys) - 1:
        c = row_cells(sp_.sp, sp_.ys[r], sp_.ys[r + 1], cols, SUBJ_CELLS)
        if not CODE_RE.match(c[0]):
            break
        subjects.append({"code": c[0], "name": c[1], "sat": c[2:5], "pass": c[5:9],
                         "fail": c[9:13], "s_rank": c[13], "c_rank": c[14], "r_rank": c[15],
                         "z_rank": c[16], "gpa": c[17], "competency": c[18]})
        subj_h.append(sp_.ys[r + 1] - sp_.ys[r])
        r += 1
    subj_bottom = sp_.ys[r]

    # --- subjects grading summary
    g_i = gp.ys.index(g_top)
    grading, grad_h = [], []
    r = g_i + 3
    while r < len(gp.ys) - 1:
        c = row_cells(gp.sp, gp.ys[r], gp.ys[r + 1], cols, GRAD_CELLS)
        if not CODE_RE.match(c[0]):
            break
        grading.append({"code": c[0], "name": c[1], "a": c[2:5], "b": c[5:8], "c": c[8:11],
                        "d": c[11:14], "f": c[14:17], "reg": c[17:20]})
        grad_h.append(gp.ys[r + 1] - gp.ys[r])
        r += 1
    grad_bottom = gp.ys[r]

    # ---------------------------------------------------------------- layout
    def h(ys, i):
        return round(ys[i + 1] - ys[i], 2)

    # Each summary block either follows the previous one on the same page (gap = blank
    # sheet rows between them) or starts a new page (tail = blank band left under the
    # previous block, lead = blank band above the new block).
    gaps, breaks = {}, {}

    def link(name, prev_page, prev_bottom, page, top):
        if page.pi == prev_page.pi:
            gaps[name] = round(top - prev_bottom, 2)
        else:
            breaks[name] = {"tail": round(prev_page.band[3] - prev_bottom, 2),
                            "lead": round(top - page.band[1], 2)}

    link("overall", last_cand[0], last_cand[1], op, o_ys[0])
    link("division", op, o_ys[8], dp, d_ys[0])
    link("subjects", dp, d_ys[4], sp_, sp_.ys[s_i])
    link("grading", sp_, subj_bottom, gp, g_top)

    layout = {
        "cols": cols,
        "font_scale": font_scale,
        "top": round(p1.band[1], 2),
        "title_baselines": [round(s["origin"][1], 2) for s in titles],
        "div_label_baseline": round(div_label["origin"][1], 2),
        "div_top": div_top,
        "div_row": med([div_ys[i + 1] - div_ys[i] for i in range(len(div_ys) - 1)]),
        "cand_head_top": cand_head_top,
        "cand_head": round(cand_first - cand_head_top, 2),
        "cand_row": med(row_h),
        "cand_middle": (["sex", "aggt", "div", "pos", "subjects"] if cno_bottom_aligned
                        else ["cno", "name", "sex", "aggt", "div", "pos", "subjects"]),
        "cont_top": cont_top if cont_top is not None else round(p1.band[1], 2),
        "first_page_rows": page_rows[0],
        "rows_per_page": max(page_rows[1:-1] or page_rows[1:] or page_rows),
        "overall_rows": {"title": h(o_ys, 0), "row": med([h(o_ys, i) for i in range(1, 8)])},
        "division_rows": {"title": h(d_ys, 0), "head": h(d_ys, 1), "row": med([h(d_ys, 2), h(d_ys, 3)])},
        "subject_rows": {"title": h(sp_.ys, s_i), "head1": h(sp_.ys, s_i + 1),
                         "head2": h(sp_.ys, s_i + 2), "row": med(subj_h)},
        "grading_rows": {"title": h(gp.ys, g_i), "head1": h(gp.ys, g_i + 1),
                         "head2": h(gp.ys, g_i + 2), "row": med(grad_h)},
        "gaps": gaps,
        "breaks": breaks,
        "tail_last": round(gp.band[3] - grad_bottom, 2),
    }

    return {
        "document": {
            "ministry": title_text[:2],
            "region_title": title_text[2],
            "exam_name": title_text[3],
            "centre_no": centre_no,
            "school_name": school_name,
            "school_title": school_title,
            "footer": footer,
        },
        "division_summary": division_summary,
        "candidates": candidates,
        "overall": overall,
        "division_performance": division_performance,
        "subjects": subjects,
        "grading": grading,
        "layout": layout,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path, default=REPORT)
    a = ap.parse_args(argv)
    (a.out_dir / "reference").mkdir(parents=True, exist_ok=True)
    for pdf in a.pdfs:
        data = extract(pdf)
        tag = (data["document"]["centre_no"] or pdf.stem.split()[0]).lower()
        out = a.out_dir / f"data_{tag}.json"
        out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        shutil.copyfile(pdf, a.out_dir / "reference" / f"original_{tag}.pdf")
        lay = data["layout"]
        print(f"wrote {out.relative_to(ROOT)}: {len(data['candidates'])} candidates, "
              f"{len(data['subjects'])} subjects, rows {lay['first_page_rows']}+"
              f"{lay['rows_per_page']}/page, page breaks before {sorted(lay['breaks'])}")


if __name__ == "__main__":
    main()
