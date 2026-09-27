# sars-pdf — School Rank by Subject report (HTML + CSS → PDF)

This project rebuilds the OHONGSS-T **"SCHOOL RANK IN <SUBJECT> LAKEZONEWISE"** report (Lakezone Form Two Mock, August 2026, 11 pages, 16 subject tables) in HTML + CSS and prints it to PDF with WeasyPrint. The layout, fonts, borders and column fills are fixed. The only thing that changes colour with the data is the competency level.

**Acceptance criterion:** the generated PDF matches `reference/original.pdf`. See [`output/comparison/README.md`](output/comparison/README.md) for the page-by-page results (original | generated | diff).

## Current match

| Check | Result |
|---|---|
| Page count / size | 11 pages, US Letter: same |
| Text | every word identical on all 11 pages (0 missing, 0 extra) |
| Fill colours | every fill colour identical on all pages |
| Fonts | the same real fonts: Arial, Arial Bold, Arial Narrow Bold |
| Grid lines | same x/y positions and widths (0.48 pt thin, 0.84 pt thick) |
| Text position | median offset < 0.1 pt; most text within ±0.3 pt |
| Pixels differing (110 dpi) | ~3.5 % raw, ~1.6 % after allowing a 1 px shift (anti-aliasing) |

The remaining pixel difference comes from Excel's GDI text layout, which rounds some glyph advances (e.g. the `W` in `MWANZA` is 0.5 pt wider in the original).

## Usage

```bash
pip install -r requirements.txt           # WeasyPrint needs Pango (present on most Linux distros)
python scripts/fetch_fonts.py             # real fonts -> fonts/ (needs cabextract)
python -m sars_pdf.render data/lakezone_f2_mock_aug2026.json --pdf output/report.pdf --html output/report.html
python scripts/compare.py                 # -> output/pages/, output/comparison/
```

A GitHub Action (`.github/workflows/compare.yml`) does all of this on every push that touches data, templates, code, fonts or `reference/original.pdf`. It then commits `output/` back to the branch.

## Fonts (real, not substitutes)

| Used for | Font | Source |
|---|---|---|
| body text | **Arial** | Microsoft core fonts package (`arial32.exe`), extracted by `fetch_fonts.py` |
| bold numbers, headings | **Arial Bold** | same |
| TOTAL, COMPENTENCY LEVEL, competency labels, page-1 headers | **Arial Narrow Bold** | copied from the system if installed, otherwise the real glyphs embedded in `reference/original.pdf` |

Arial Narrow Bold is not freely downloadable, and the copy embedded in the original only contains the characters that report uses. That covers every string the report prints in that font. If some other character is ever needed, only that character falls back to **Liberation Sans Narrow Bold** (`fonts/fallback/`, SIL OFL, metric-compatible). That is the only substitute.

The Microsoft `.ttf` files are licensed and are **not committed**. `fetch_fonts.py` installs them locally and in CI.

## Layout

```
data/lakezone_f2_mock_aug2026.json   # data + measured per-table layout
templates/report.html.j2             # Jinja2 template (absolute page layout, one <table> per subject)
templates/report.css                 # fonts and Excel-style text offsets
sars_pdf/layout.py                   # fixed geometry: column grid X[], default thick borders, default layout
sars_pdf/render.py                   # builds every cell (text, font, size, alignment, fill, border widths)
sars_pdf/grading.py                  # competency level from GPA (the only conditional colour)
scripts/fetch_fonts.py               # installs the real fonts
scripts/calibrate.py                 # measures the original -> layout/borders/titles in the JSON
scripts/compare.py                   # original vs generated: text, fills, pixels, side-by-side images
reference/original.pdf               # the original report
output/                              # generated PDF/HTML, page images, comparison (committed)
```

## Page heading

| Line(s) | Field | Example |
|---|---|---|
| 1–2 | `document.ministry` (one entity on two lines) | THE PRIME MINISTER'S OFFICE / REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT |
| 3 | `document.exam_board` | ORGANIZATION OF HEADS OF NON-GOVERNMENT SECONDARY SCHOOLS-TANZANIA (OHONGSS-T) |
| 4 | `document.exam_name` | LAKEZONE FORM TWO MOCK  ASSESSMENT AUGUST   2026 |
| (5) | `table.scope_area` (optional) | CHATO |
| last | `table.title`, default `SCHOOL RANK IN {subject}  {scope}` | SCHOOL RANK IN PHYSICS  LAKEZONEWISE |

Strings keep the original's exact spacing, including double spaces and the leading and trailing spaces used for centring. `scope` sets the rank column label: `LAKEZONEWISE`/`ZONEWISE` → `Z/RANK`, `REGIONWISE` → `R/RANK`, `COUNCILWISE` → `C/RANK`, `WARDWISE` → `W/RANK`.

## Data model (per table)

```jsonc
{
  "subject": "PHYSICS", "scope": "LAKEZONEWISE",
  "rows": [ { "sn": "001", "region": "MWANZA", "council": "MWANZA CC", "centre_no": "S5343",
              "school_name": "MUSABE BOYS", "av": "53.28", "grd": "C",
              "a": "10", "b": "34", "c": "75", "d": "36", "f": "9", "total": "164",
              "a_c": "119", "pct_a_c": "72.56", "a_d": "155", "pct_a_d": "94.51",
              "gpa": "3.0000", "competency": "Grade C (Good)", "rank": "1" },
            { "sn": "008", "blank": true, "a_c": "0", "a_d": "0", "rank": "8" } ],
  "overall": { "av": "34.63", "grd": "D", ..., "gpa": "4.0916", "competency": "Grade D (Satisfactory)" },
  // optional; defaults in sars_pdf/layout.py and render.py DEFAULT_STYLE
  "layout":  { "title_top": 71.3, "subject_top": 108.0, "subject_size": 6.11, "table_top": 117.66,
               "rows": [11.04, 11.04, 8.88, 11.1] },       // header row 1, header row 2, school row, overall row
  "borders": { "add": ["V20:ov"], "remove": ["V15:h2"] }, // exceptions to the default thick borders
  "style":   { "centre_align": "left", "total_bold": false, "competency_font": "bold",
               "overall_competency": { "size": 6.11, "align": "left" } }
}
```

Values are **display strings**, so the number formatting of the original is kept exactly (`70.4`, `65.00`, `43.937`). For new data, omit `layout`, `borders` and `style` to get the standard layout.

## Colours

**Fixed** (exact values from the original):

| Where | Header | Cells | Overall row |
|---|---|---|---|
| AV, GRD | `#ffffcc` | `#ebf1de` | `#ebf1de` |
| A B C D | `#d8e4bc` | – | – (page 1: `#daeef3`) |
| F | `#fabf8f` | `#fcd5b4` | – (page 1: `#fcd5b4`) |
| TOTAL | `#b7dee8` | – | – (page 1: `#f2dcdb`) |
| A-C, %A-C | `#65ffab` | `#ccffff` | – (page 1: `#ccffff`) |
| A-D, %A-D | `#ccffff` | `#b7dee8` | – (page 1: `#b7dee8`) |
| GPA | `#daeef3` (page 1: `#d2fce6`) | – | – (page 1: `#d2fce6`) |
| Z/RANK (and S/N on page 1) | `#fde9d9` | – | – |

**Conditional:** only the COMPETENCY LEVEL cell. The letter comes from the label, or from the GPA if the label is missing (`sars_pdf/grading.py`). The text is black on every level.

| GPA | Level | Fill |
|---|---|---|
| < 1.6 | Grade A (Excellent) | `#00b050` |
| 1.6 – < 2.6 | Grade B (Very Good) | `#92d050` |
| 2.6 – < 3.6 | Grade C (Good) | `#ffff00` |
| 3.6 – < 4.6 | Grade D (Satisfactory) | `#ffc000` |
| ≥ 4.6 | Grade F (Fail) | `#ff0000` |

## Borders

Thin lines are 0.48 pt and thick lines 0.84 pt, positioned on the column grid in `sars_pdf/layout.py`. The standard thick segments (`DEFAULT_THICK`) outline the column groups: AV/GRD | A–TOTAL | A-C/%A-C | A-D/%A-D | GPA, the header and the overall row. Where one of the original's Excel sheets differs (pages 1, 7, 8 and 11), the table's `borders.add/remove` records it. `calibrate.py` writes these values.

## Recalibrating against a new original

```bash
python scripts/calibrate.py reference/original.pdf data/<file>.json   # layout, borders, exact titles
python scripts/compare.py
```
