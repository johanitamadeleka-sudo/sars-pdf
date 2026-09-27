"""Render the generated PDF to images and compare it side by side with the original.

    python scripts/compare.py                       # uses reference/original.pdf + output/report.pdf
    python scripts/compare.py ORIGINAL GENERATED --out output/comparison

Writes (all committed to git so they can be viewed on GitHub):
  output/pages/page_NN.png              generated pages
  output/comparison/page_NN.png         original | generated | diff (red = different pixels)
  output/comparison/README.md           per-page scores + embedded images

Per page it reports pixel-difference %, words missing/extra (pdfplumber) and fill colours
that appear in only one of the two PDFs. If the original PDF is not present, only the
generated pages are rendered and the report says so.
"""

import argparse
from collections import Counter
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
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


def tolerant_diff(a, b, tol=40):
    """Pixels that differ even when allowed to shift by 1px (ignores sub-pixel anti-aliasing)."""
    a, b = a.convert("L"), b.convert("L")
    out = None
    for x, y in ((a, b), (b, a)):
        lo, hi = y.filter(ImageFilter.MinFilter(3)), y.filter(ImageFilter.MaxFilter(3))
        below = ImageChops.subtract(lo, x)   # x darker than any neighbour in y
        above = ImageChops.subtract(x, hi)   # x lighter than any neighbour in y
        m = ImageChops.lighter(below, above).point(lambda v: 255 if v > tol else 0)
        out = m if out is None else ImageChops.lighter(out, m)
    return out


def label(img, text):
    ImageDraw.Draw(img).text((8, 6), text, fill=(200, 0, 0))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original", type=Path, nargs="?", default=ROOT / "reference" / "original.pdf")
    ap.add_argument("generated", type=Path, nargs="?", default=ROOT / "output" / "report.pdf")
    ap.add_argument("--out", type=Path, default=ROOT / "output" / "comparison")
    ap.add_argument("--pages-out", type=Path, default=ROOT / "output" / "pages")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    a.pages_out.mkdir(parents=True, exist_ok=True)

    gen_r = pdfium.PdfDocument(a.generated)
    for i in range(len(gen_r)):
        raster(gen_r, i).save(a.pages_out / f"page_{i + 1:02d}.png")
    print(f"rendered {len(gen_r)} generated pages -> {a.pages_out}/")

    md = ["# Original vs generated", ""]
    if not a.original.exists():
        md += [f"**`{a.original.relative_to(ROOT)}` is missing - no comparison possible yet.**", "",
               "Upload the original PDF to `reference/original.pdf`, then run `python scripts/compare.py`.", "",
               "Generated pages:", ""]
        md += [f"![page {i + 1}](../pages/page_{i + 1:02d}.png)" for i in range(len(gen_r))]
        (a.out / "README.md").write_text("\n".join(md) + "\n")
        print(f"original not found at {a.original}; wrote generated pages only")
        return

    ref_r = pdfium.PdfDocument(a.original)
    md += ["Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).", "",
           "Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed "
           "(ignores sub-pixel anti-aliasing).", "",
           "| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |",
           "|---|---|---|---|---|---|---|"]
    imgs = []
    with pdfplumber.open(a.original) as ref, pdfplumber.open(a.generated) as gen:
        if len(ref.pages) != len(gen.pages):
            md.insert(2, f"**Page count differs: original {len(ref.pages)} vs generated {len(gen.pages)}**\n")
        for i in range(min(len(ref.pages), len(gen.pages))):
            rp, gp = ref.pages[i], gen.pages[i]
            rw, gw = words(rp), words(gp)
            missing, extra = rw - gw, gw - rw
            ri, gi = raster(ref_r, i), raster(gen_r, i).resize(raster(ref_r, i).size)
            diff = ImageChops.difference(ri, gi).convert("L").point(lambda v: 255 if v > 40 else 0)
            pct = 100 * diff.histogram()[255] / (diff.width * diff.height)
            tdiff = tolerant_diff(ri, gi)
            tpct = 100 * tdiff.histogram()[255] / (tdiff.width * tdiff.height)
            rf, gf = fills(rp), fills(gp)
            print(f"page {i + 1}: pixel diff {pct:.2f}% (±1px tolerant {tpct:.2f}%) | words missing {sum(missing.values())} "
                  f"extra {sum(extra.values())}")
            md.append(f"| {i + 1} | {pct:.2f}% | {tpct:.2f}% | {sum(missing.values())} | {sum(extra.values())} | "
                      f"{' '.join(sorted(rf - gf)) or '-'} | {' '.join(sorted(gf - rf)) or '-'} |")
            overlay = ri.copy()
            overlay.paste((255, 170, 170), mask=diff)
            overlay.paste((255, 0, 0), mask=tdiff)
            side = Image.new("RGB", (ri.width * 3, ri.height), "white")
            side.paste(label(ri, "ORIGINAL"), (0, 0))
            side.paste(label(gi, "GENERATED"), (ri.width, 0))
            side.paste(label(overlay, "DIFF"), (ri.width * 2, 0))
            side.save(a.out / f"page_{i + 1:02d}.png")
            detail = []
            if missing:
                detail.append(f"missing: `{dict(missing.most_common(10))}`")
            if extra:
                detail.append(f"extra: `{dict(extra.most_common(10))}`")
            imgs += [f"## Page {i + 1}", *detail, "", f"![page {i + 1}](page_{i + 1:02d}.png)", ""]
    (a.out / "README.md").write_text("\n".join(md + [""] + imgs) + "\n")
    print(f"side-by-side images + README.md in {a.out}/")


if __name__ == "__main__":
    main()
