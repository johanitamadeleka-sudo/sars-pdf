"""Paint collapsed table rules the way the original PDF paints them (opt-in per template).

WeasyPrint *strokes* collapsed borders; a 0.24-0.36pt stroke rasterises as a 2-pixel
anti-aliased grey line. The source PDFs never stroke their grid, and they come from two
exporters that fill it differently - which a rasteriser such as pdfium renders differently:

* Excel's own PDF export paints every rule as a separate thin RECTANGLE (``re f``), which
  pdfium snaps to a crisp 1-device-pixel black line.
* "Microsoft: Print To PDF" paints the whole grid as ONE filled path of many sub-paths, which
  is not a plain rectangle, so it is anti-aliased by coverage (light grey at 110 dpi).

On dense grids the difference between these and a stroke was ~98% of the remaining pixel
difference against the original, with every rule already in exactly the right place.

A template opts in with one of these tags in its <head>:

    <meta name="sars-pdf:rules" content="filled">      (Excel export: crisp rects)
    <meta name="sars-pdf:rules" content="filled-aa">   (Print To PDF: anti-aliased fill)

and its solid collapsed borders are emitted as filled shapes of the same geometry (same
centre line, thickness and colour). Templates without the tag are untouched.
"""

import contextlib
import re

META = re.compile(r'<meta name="sars-pdf:rules" content="(filled|filled-aa)">')


def rules_mode(html):
    m = META.search(html)
    return m.group(1) if m else None


@contextlib.contextmanager
def filled_rules(mode="filled"):
    """While active, WeasyPrint paints solid collapsed-border segments as filled shapes."""
    import weasyprint.draw as wp_draw

    original = getattr(wp_draw, "draw_line", None)
    if not mode or original is None:
        yield
        return

    def draw_line(stream, x1, y1, x2, y2, thickness, style, color, *args, **kwargs):
        if style != "solid" or not (x1 == x2 or y1 == y2):
            return original(stream, x1, y1, x2, y2, thickness, style, color, *args, **kwargs)
        if x1 == x2:
            left, top, right, bottom = x1 - thickness / 2, y1, x1 + thickness / 2, y2
        else:
            left, top, right, bottom = x1, y1 - thickness / 2, x2, y1 + thickness / 2
        with stream.stacked():
            stream.set_color(color)
            if mode == "filled":
                stream.rectangle(left, top, right - left, bottom - top)
            else:
                stream.move_to(left, top)
                stream.line_to(right, top)
                stream.line_to(right, bottom)
                stream.line_to(left, bottom)
                stream.close()
                # a zero-area second sub-path: the fill is no longer a lone rectangle, so it
                # is anti-aliased like the original's multi-sub-path grid fill
                stream.move_to(left, top)
                stream.line_to(left, top)
                stream.close()
            stream.fill()

    # draw_collapsed_borders() looks draw_line up in weasyprint.draw's namespace; text
    # decorations import their own reference and are not affected.
    wp_draw.draw_line = draw_line
    try:
        yield
    finally:
        wp_draw.draw_line = original


def write_pdf(html, pdf_path, base_url):
    """Render ``html`` to ``pdf_path`` the way every report is rendered."""
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration

    # CRITICAL (see fonts/README.md + FEAT-001 findings): @font-face is only honoured
    # when ONE shared FontConfiguration is passed to write_pdf. Otherwise WeasyPrint
    # silently falls back to Noto Sans instead of the registered real fonts.
    font_config = FontConfiguration()
    with filled_rules(rules_mode(html)):
        HTML(string=html, base_url=str(base_url)).write_pdf(pdf_path, font_config=font_config)
