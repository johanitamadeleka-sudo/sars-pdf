"""Word extraction helpers for the Excel-exported source PDFs (used by scripts/extract_*.py).

Two traps in those PDFs:

* Text longer than its cell keeps drawing past the cell edge; the viewer hides the excess
  with a clip path. PyMuPDF's default word extraction honours that clip and DROPS the hidden
  glyphs, gluing whatever survives onto the next cell's text: "STAR REACHERS GIRLS A" +
  "PRIVATE" becomes one word "APRIVATE". ``page_words()`` keeps every glyph.
* With every glyph kept, the spilled words sit over the neighbouring cell. ``column_x()``
  gives the x to use for column assignment: a word's own x0, except when it overlaps text
  of another run (the signature of a spill) - then the x0 of the previous word of its own
  run, so it stays in the cell it was typed into.
"""

import pymupdf

WORD_FLAGS = pymupdf.TEXTFLAGS_WORDS & ~pymupdf.TEXT_MEDIABOX_CLIP


def page_words(page):
    """PyMuPDF word tuples (x0, y0, x1, y1, text, block, line, word) incl. clipped glyphs."""
    return page.get_text("words", flags=WORD_FLAGS)


def column_x(line, overlap=0.5):
    """Map id(word) -> x to use for column assignment, for the words of one text line."""
    run = lambda w: (w[5], w[6])
    out = {}
    ordered = sorted(line, key=lambda w: (w[5], w[6], w[7]))
    prev = {}
    for w in ordered:
        spilled = any(run(o) != run(w) and min(w[2], o[2]) - max(w[0], o[0]) > overlap
                      for o in line)
        if spilled and run(w) in prev:
            out[id(w)] = prev[run(w)]
        else:
            out[id(w)] = w[0]
        prev[run(w)] = out[id(w)]
    return out
