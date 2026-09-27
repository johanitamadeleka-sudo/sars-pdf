"""Paint collapsed table rules as filled rectangles, like the originals (opt-in per template).

The Excel-exported originals draw every grid rule as a thin FILLED rectangle, which PDF
rasterisers snap to a crisp 1-device-pixel black line. WeasyPrint *strokes* collapsed
borders instead, and a 0.24pt stroke rasterises as a 2-pixel anti-aliased grey line. On a
dense grid that alone was ~98% of the remaining pixel difference against the original
even with every rule in exactly the right place.

A template opts in with this tag in its <head>:

    <meta name="sars-pdf:rules" content="filled">

and its solid collapsed borders are emitted as filled rectangles of the same geometry
(same centre line, thickness and colour). Templates without the tag are untouched.
"""

import contextlib

META = '<meta name="sars-pdf:rules" content="filled">'


def wants_filled_rules(html):
    return META in html


@contextlib.contextmanager
def filled_rules(enabled=True):
    """While active, WeasyPrint paints solid collapsed-border segments as filled rects."""
    import weasyprint.draw as wp_draw

    original = getattr(wp_draw, "draw_line", None)
    if not enabled or original is None:
        yield
        return

    def draw_line(stream, x1, y1, x2, y2, thickness, style, color, *args, **kwargs):
        if style != "solid" or not (x1 == x2 or y1 == y2):
            return original(stream, x1, y1, x2, y2, thickness, style, color, *args, **kwargs)
        with stream.stacked():
            stream.set_color(color)
            if x1 == x2:
                stream.rectangle(x1 - thickness / 2, y1, thickness, y2 - y1)
            else:
                stream.rectangle(x1, y1 - thickness / 2, x2 - x1, thickness)
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
    with filled_rules(wants_filled_rules(html)):
        HTML(string=html, base_url=str(base_url)).write_pdf(pdf_path, font_config=font_config)
