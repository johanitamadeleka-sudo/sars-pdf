"""Compare the generated PDF against the original (the fidelity check for this project).

    python scripts/compare.py reference/original.pdf output/report.pdf [--out output/diff]

Reports, per page:
  * text   - words missing/extra vs. the original (pdfplumber)
  * pixels - % of pixels that differ after rasterising both at the same DPI
  * colours- fill colours used in the original that our CSS does not use (and vice versa)
Writes side-by-side/diff PNGs to --out for visual review.
"""

import argparse
from collections import Counter
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageChops

DPI = 110


def words(page):
    return Counter(w["text"] for w in page.extract_words())


def fills(page):
    out = set()
    for r in page.rects:
        c = r.get("non_stroking_color")
        if r.get("fill") and c is not None:
            c = tuple(c) if isinstance(c, (list, tuple)) else (c,)
            if len(c) == 1:
                c = c * 3
            if len(c) == 3:
                out.add("#%02x%02x%02x" % tuple(round(v * 255) for v in c))
    return out - {"#ffffff"}


def raster(pdf, i):
    return pdf[i].render(scale=DPI / 72).to_pil().convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original", type=Path)
    ap.add_argument("generated", type=Path)
    ap.add_argument("--out", type=Path, default=Path("output/diff"))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    ref_r, gen_r = pdfium.PdfDocument(a.original), pdfium.PdfDocument(a.generated)
    with pdfplumber.open(a.original) as ref, pdfplumber.open(a.generated) as gen:
        if len(ref.pages) != len(gen.pages):
            print(f"PAGE COUNT differs: original {len(ref.pages)} vs generated {len(gen.pages)}")
        for i in range(min(len(ref.pages), len(gen.pages))):
            rp, gp = ref.pages[i], gen.pages[i]
            rw, gw = words(rp), words(gp)
            missing, extra = rw - gw, gw - rw
            ri, gi = raster(ref_r, i), raster(gen_r, i)
            gi = gi.resize(ri.size)
            diff = ImageChops.difference(ri, gi).convert("L").point(lambda v: 255 if v > 40 else 0)
            pct = 100 * sum(1 for v in diff.getdata() if v) / (diff.width * diff.height)
            rf, gf = fills(rp), fills(gp)
            print(f"page {i + 1}: size {rp.width:.0f}x{rp.height:.0f} vs {gp.width:.0f}x{gp.height:.0f} | "
                  f"pixel diff {pct:.2f}% | words missing {sum(missing.values())} extra {sum(extra.values())}")
            if missing:
                print("   missing:", dict(missing.most_common(10)))
            if extra:
                print("   extra:  ", dict(extra.most_common(10)))
            if rf != gf:
                print("   fills only in original :", sorted(rf - gf))
                print("   fills only in generated:", sorted(gf - rf))
            side = Image.new("RGB", (ri.width * 3, ri.height), "white")
            side.paste(ri, (0, 0))
            side.paste(gi, (ri.width, 0))
            side.paste(Image.merge("RGB", (diff, Image.new("L", diff.size), Image.new("L", diff.size))), (ri.width * 2, 0))
            side.save(a.out / f"page_{i + 1:02d}.png")
    print(f"side-by-side images (original | generated | diff) in {a.out}/")


if __name__ == "__main__":
    main()
