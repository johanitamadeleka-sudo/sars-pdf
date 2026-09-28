"""Extract MKOA WANAFUNZI KUMI BORA STD4 (region best students overall) -> data.json.

Section-centric: 6 "WANAFUNZI KUMI BORA ..." top-10 blocks, ONE block per page over 6 pages.
Each candidate row is STAGGERED across up to 3 physical lines (the S/N, JUMLA/WASTANI/NAFASI
and the Swahili "Daraja X (...)" competency label frequently wrap onto their own y-lines),
so each candidate is assembled by Y-BAND (nearest candidate anchor) then X-CENTRE binning.

Columns: S/N | HALMASHAURI | JINA LA SHULE | UMILIKI | NAMBA YA MTAHINIWA
  | JINA LA MWANAFUNZI | JINSI | 6 subjects (AL avg + DRJ)
  | JUMLA | WASTANI | NAFASI | KUNDI LA UMAHIRI

Pagination is DATA-DRIVEN (one section per page; page_top True for all but the first).
Extraction is coordinate based (pymupdf words), never hand-typed.
"""

import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sars_pdf.grading import competency_letter

ROOT = Path(__file__).resolve().parent.parent
SRCDIR = ROOT / "primary_region_pdf" / "primary_region_pdf"
OUTDIR = ROOT / "reports" / "primary" / "region" / "primary-region-best-students-overall"

SOURCES = [
    (None, "MKOA WANAFUNZI BORA STD4 2026.pdf"),
]

SUBJECTS = ["hisabati", "kiswahili", "sayansi", "english", "jiografia", "historia"]
SN_MAX_X = 55.0


import re

_CANDNO_RE = re.compile(r"^PS\s*\d", re.IGNORECASE)


def _is_candno(txt):
    return bool(_CANDNO_RE.match(txt.replace(" ", "")))


def group_lines(words, y_tol=2.4):
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


def page_geometry(page):
    """Derive per-page column positions (the source shifts columns and drops the NAMBA YA
    MTAHINIWA / JINSI columns on the single-sex blocks)."""
    lines = group_lines(page.get_text("words"))
    al_c, drj_c = [], []
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        if [w[4] for w in line].count("AL") >= 3:
            for w in line:
                cx = (w[0] + w[2]) / 2
                if w[4] == "AL":
                    al_c.append(cx)
                elif w[4] == "DRJ":
                    drj_c.append(cx)
            break
    if len(al_c) < 6 or len(drj_c) < 6:
        return None
    al_c, drj_c = al_c[:6], drj_c[:6]
    # text-column label header
    lbl = None
    for cy, line in lines:
        txts = [w[4] for w in line]
        if "HALMASHAURI" in txts and ("SHULE" in txts):
            lbl = sorted(line, key=lambda w: w[0])
            break
    def cx_of(name, default=None):
        if lbl:
            for w in lbl:
                if w[4] == name:
                    return (w[0] + w[2]) / 2
        return default
    umiliki_c = cx_of("UMILIKI", 179.0)
    has_jinsi = any(w[4] == "JINSI" for cy, line in lines for w in line)
    name_c = cx_of("JINALA", 291.0)
    first_al = al_c[0]
    return {
        "al_c": al_c, "drj_c": drj_c,
        "council_max": 104.0,
        "school_max": umiliki_c - 14,
        "own_max": umiliki_c + 30,
        "name_max": first_al - 24 if has_jinsi else first_al - 8,
        "jinsi_max": first_al - 8 if has_jinsi else None,
        "has_jinsi": has_jinsi,
        "jumla_c": drj_c[-1] + 20,
        "wastani_c": drj_c[-1] + 43,
        "nafasi_c": drj_c[-1] + 64,
        "comp_min": drj_c[-1] + 74,
    }


def subj_cell(cx, geo):
    al_c, drj_c = geo["al_c"], geo["drj_c"]
    ai = min(range(6), key=lambda i: abs(cx - al_c[i]))
    di = min(range(6), key=lambda i: abs(cx - drj_c[i]))
    if abs(cx - al_c[ai]) <= abs(cx - drj_c[di]):
        return SUBJECTS[ai] + "_al"
    return SUBJECTS[di] + "_g"


def parse_block(page):
    geo = page_geometry(page)
    if geo is None:
        return []
    lines = group_lines(page.get_text("words"))
    anchors = []
    for cy, line in lines:
        line = sorted(line, key=lambda w: w[0])
        f = line[0]
        fcx = (f[0] + f[2]) / 2
        if fcx < SN_MAX_X and f[4].isdigit() and len(f[4]) <= 2 and len(line) > 12:
            anchors.append(cy)
    anchors.sort()
    if not anchors:
        return []
    lo = anchors[0] - 6
    hi = anchors[-1] + 7.0
    keys = ["sn", "council", "school", "ownership", "candno", "candidate", "jinsi"]
    for s in SUBJECTS:
        keys += [s + "_al", s + "_g"]
    keys += ["jumla", "wastani", "nafasi", "competency"]
    rows = [{k: "" for k in keys} for _ in anchors]
    council_p = [[] for _ in anchors]
    school_p = [[] for _ in anchors]
    name_p = [[] for _ in anchors]
    comp_p = [[] for _ in anchors]
    for w in page.get_text("words"):
        y = (w[1] + w[3]) / 2
        if y < lo or y > hi:
            continue
        cx = (w[0] + w[2]) / 2
        txt = w[4]
        bi = min(range(len(anchors)), key=lambda i: abs(y - anchors[i]))
        r = rows[bi]
        if cx < SN_MAX_X:
            if txt.isdigit() and len(txt) <= 2:
                r["sn"] = txt
        elif cx < geo["council_max"]:
            council_p[bi].append((w[0], txt))
        elif cx < geo["school_max"]:
            school_p[bi].append((w[0], txt))
        elif cx < geo["own_max"]:
            r["ownership"] = txt
        elif cx < geo["name_max"] and _is_candno(txt):
            r["candno"] = txt
        elif cx < geo["name_max"]:
            name_p[bi].append((w[0], txt))
        elif geo["has_jinsi"] and cx < geo["jinsi_max"]:
            r["jinsi"] = txt
        elif cx < geo["jumla_c"] - 10:
            r[subj_cell(cx, geo)] = txt
        elif cx < geo["wastani_c"] - 9:
            r["jumla"] = txt
        elif cx < geo["nafasi_c"] - 9:
            r["wastani"] = txt
        elif cx < geo["comp_min"]:
            r["nafasi"] = txt
        else:
            comp_p[bi].append((w[0], txt))
    for i, r in enumerate(rows):
        r["council"] = " ".join(t for _, t in sorted(council_p[i]))
        r["school"] = " ".join(t for _, t in sorted(school_p[i]))
        r["candidate"] = " ".join(t for _, t in sorted(name_p[i]))
        comp = " ".join(t for _, t in sorted(comp_p[i]))
        r["competency"] = comp
        r["level"] = (competency_letter(comp) or "").upper() or None
    return rows


def block_title(page):
    for cy, line in group_lines(page.get_text("words")):
        txt = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
        if txt.startswith("WANAFUNZI KUMI"):
            return txt
    return ""


def extract(src):
    doc = pymupdf.open(src)
    sections = []
    for pi in range(doc.page_count):
        rows = parse_block(doc[pi])
        if rows:
            sections.append({"title": block_title(doc[pi]), "page": pi,
                             "page_top": pi > 0, "rows": rows})
    return sections


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ref = OUTDIR / "reference"
    ref.mkdir(parents=True, exist_ok=True)
    for tag, name in SOURCES:
        src = SRCDIR / name
        sections = extract(src)
        document = {
            "page_size": "Letter-landscape",
            "ministry": [
                "OFISI YA WAZIRI MKUU",
                "TAWALA ZA MIKOA NA SERIKALI ZA MITAA",
                "MKOA WA MWANZA",
            ],
            "exam_name": "MATOKEO YA MTIHANI WA MOCK MKOA DARASA LA NNE MWEZI AGOSTI, 2026",
            "report_title": "WANAFUNZI KUMI BORA MKOA",
            "subjects": ["HISABATI", "KISWAHILI", "SAYANSI", "ENGLISH",
                         "JIOGRAFIA & MAZINGIRA", "HISTORIA YA TZ & MAADILI"],
        }
        data = {"document": document, "sections": sections}
        suffix = "" if tag is None else f"_{tag}"
        out = OUTDIR / f"data{suffix}.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ref / f"original{suffix}.pdf").write_bytes(src.read_bytes())
        print(f"[{tag or 'main'}] sections={len(sections)} -> {out.name}")
        for s in sections:
            r = s["rows"][0]
            print(f"   p{s['page']+1} top={s['page_top']} {s['title'][:44]:<44} "
                  f"{len(s['rows'])} rows; first sn={r['sn']} sch={r['school']} "
                  f"cand={r['candidate']} jumla={r['jumla']} wastani={r['wastani']} "
                  f"nm={r['nafasi']} comp={r['competency']}")


if __name__ == "__main__":
    main()
