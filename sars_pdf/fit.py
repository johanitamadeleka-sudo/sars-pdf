"""Shrink-to-fit for fixed-pitch grid cells (Excel's "Shrink to fit").

Dense report grids (e.g. the F/M/T division grid) print every row at one fixed
pitch, so a value wider than its column can neither wrap (the grid would break)
nor be clipped / spill into the next cell (the data would be wrong or unreadable).
`fit_style()` measures the text with the SAME font files WeasyPrint embeds
(``fonts/``) and, only when the text is too wide, returns an inline
``font-size`` that makes it fit the cell's text box. Text that already fits is
left untouched, so normal rows keep the design size measured from the original.

Widths come from the fonts' advance widths without kerning, which is an upper
bound of what Pango lays out (kerning only tightens these uppercase strings), so
a fitted value can never overflow.
"""

import math
from functools import lru_cache
from pathlib import Path

from markupsafe import Markup

FONTS = Path(__file__).resolve().parent.parent / "fonts"

# CSS family name (as written in the reports' @font-face rules) -> real font file.
FACES = {
    ("Arial", False): "LiberationSans-Regular.ttf",
    ("Arial", True): "LiberationSans-Bold.ttf",
    ("Arial Narrow", True): "LiberationSansNarrow-Bold.ttf",
    ("Times New Roman", True): "LiberationSerif-Bold.ttf",
    ("Calibri", False): "Carlito-Regular.ttf",
    ("Calibri", True): "Carlito-Bold.ttf",
}


@lru_cache(maxsize=None)
def _advances(family, bold):
    from fontTools.ttLib import TTFont

    font = TTFont(FONTS / FACES[(family, bold)])
    cmap = font.getBestCmap()
    hmtx = font["hmtx"].metrics
    upem = font["head"].unitsPerEm
    notdef = hmtx[".notdef"][0]
    return {cp: hmtx[g][0] / upem for cp, g in cmap.items()}, notdef / upem


def text_width(text, size, family="Arial", bold=False, letter_spacing=0.0):
    """Advance width of ``text`` in pt at ``size`` pt (no kerning)."""
    adv, notdef = _advances(family, bool(bold))
    em = sum(adv.get(ord(ch), notdef) for ch in text)
    return em * size + letter_spacing * len(text)


def fit_size(text, width, size, family="Arial", bold=False, letter_spacing=0.0, min_size=2.0):
    """Largest font size <= ``size`` (pt, 0.01pt steps) at which ``text`` fits ``width`` pt."""
    text = (text or "").strip()
    if not text:
        return size
    w = text_width(text, size, family, bold, letter_spacing)
    if w <= width:
        return size
    # letter-spacing does not scale with the font size, so solve for the glyphs only
    glyphs = w - letter_spacing * len(text)
    room = width - letter_spacing * len(text)
    return max(min_size, math.floor(size * room / glyphs * 100) / 100)


def fit_style(text, width, size, family="Arial", bold=False, letter_spacing=0.0):
    """`` style="font-size:..pt"`` when ``text`` must shrink to fit ``width`` pt, else ''."""
    fitted = fit_size(text, width, size, family, bold, letter_spacing)
    if fitted >= size:
        return Markup("")
    return Markup(f' style="font-size:{fitted:.2f}pt"')
