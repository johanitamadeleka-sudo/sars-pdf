# sars-pdf — School Rank by Subject report (HTML + CSS → PDF)

This project rebuilds the OHONGSS-T **"SCHOOL RANK IN <SUBJECT> LAKEZONEWISE"** report (Lakezone Form Two Mock, August 2026, 11 pages, 16 subject tables) as HTML + CSS and prints it to PDF. The layout, fonts, column fills and colours are the same for every report. Only the data changes.

**Acceptance criterion:** the generated PDF must match the original. `scripts/compare.py` measures this (see [Fidelity check](#fidelity-check)).

## Why HTML + CSS (WeasyPrint) and not ReportLab

| | HTML + CSS + WeasyPrint | ReportLab |
|---|---|---|
| Complex table (row/col spans, per-column fills, rotated `Z/RANK`) | CSS tables, handled natively | cell coordinates and spans managed by hand |
| Templating for N subjects / new data | Jinja2 loops, one template | Python layout code |
| Tuning to match the original | edit CSS variables / widths | edit drawing code |
| Output | vector PDF with real, selectable text | vector PDF with real, selectable text |

We use **WeasyPrint** for printing and **Jinja2** for templating (already in place). The PDF is deterministic, needs no browser, and uses the same fonts on every run.

## Layout

```
data/lakezone_f2_mock_aug2026.json   # the data from the original PDF (source of truth for the demo)
templates/report.html.j2             # Jinja2 page/table template
templates/report.css                 # geometry, fonts, palette (fixed colours in :root)
sars_pdf/render.py                   # JSON -> HTML -> PDF (CLI)
sars_pdf/grading.py                  # competency level <- GPA rules (the only conditional colour)
scripts/compare.py                   # fidelity check against the original PDF
reference/                           # put original.pdf here
output/report.pdf, output/report.html  # generated
```

## Usage

```bash
pip install -r requirements.txt          # WeasyPrint needs Pango (present on most Linux distros)
# Arial or a metric-compatible font is required, e.g. Liberation Sans:
#   dnf install liberation-sans-fonts   |   apt install fonts-liberation
python -m sars_pdf.render data/lakezone_f2_mock_aug2026.json --pdf output/report.pdf --html output/report.html
```

## Page heading semantics

Each table has a title block with the same meaning on every page:

| Line(s) | Field | Example |
|---|---|---|
| 1–2 | `document.ministry` (one entity shown on two lines) | THE PRIME MINISTER'S OFFICE / REGIONAL ADMINISTRATION AND LOCAL GOVERNMENT |
| 3 | `document.exam_board` | ORGANIZATION OF HEADS OF NON-GOVERNMENT SECONDARY SCHOOLS-TANZANIA (OHONGSS-T) |
| 4 | `document.exam_name` | LAKEZONE FORM TWO MOCK  ASSESSMENT AUGUST   2026 |
| (5) | `table.scope_area`, optional: the region/council/ward being ranked | CHATO |
| last | `SCHOOL RANK IN {table.subject} {table.scope}` | SCHOOL RANK IN HISTORIA YA TZ NA MAADILI LAKEZONEWISE |

`scope` sets the ranking level and the rank column label:

| scope | rank column |
|---|---|
| `LAKEZONEWISE` (zone) | `Z/RANK` |
| `REGIONWISE` | `R/RANK` |
| `COUNCILWISE` | `C/RANK` |
| `WARDWISE` | `W/RANK` |

`scope_label` overrides the printed scope text. It is used only to keep the original's typo "GEOGRAPHY LAKEZONEWISE**E**".

## Data model

```jsonc
{
  "document": { "page_size": "Letter", "ministry": [...], "exam_board": "...", "exam_name": "...",
                "overall_label": "ZONAL OVERALL  PERFORMANCE" },
  "pages": [
    { "page": 1, "density": "normal",          // "compact" = several tables stacked on one page (page 11)
      "tables": [
        { "subject": "HISTORIA YA TZ NA MAADILI", "scope": "LAKEZONEWISE",
          "style": { ... optional per-table quirks, see below ... },
          "rows": [ { "sn": "001", "region": "MWANZA", "council": "MWANZA CC", "centre_no": "S5344",
                      "school_name": "MUSABE GIRLS", "av": "72.82", "grd": "B",
                      "a": "84", "b": "73", "c": "31", "d": "1", "f": "0", "total": "189",
                      "a_c": "188", "pct_a_c": "99.47", "a_d": "189", "pct_a_d": "100",
                      "gpa": "1.7302", "competency": "Grade B (Very Good)", "rank": "1" },
                    { "sn": "008", "blank": true, "a_c": "0", "a_d": "0", "rank": "8" } ],   // empty placeholder row
          "overall": { "av": "48.10", "grd": "C", ..., "gpa": "3.3", "competency": "Grade C (Good)" } } ] } ]
}
```

Values are stored as **display strings** so the output keeps the original number formatting exactly (`70.4` vs `65.00`, `43.937`, `100`).

## Colours

**Fixed** (the same on every report, in `templates/report.css` `:root`):

| Column(s) | Fill |
|---|---|
| AV, GRD (header + cells) | `#ffffcc` |
| A B C D header | `#e2efda` |
| F (header + cells) | `#f8cbad` |
| TOTAL header | `#ddebf7` |
| A-C header / %A-C header | `#66ff99` / `#66ffcc` |
| A-C, %A-C cells | `#ccffff` |
| A-D, %A-D (header + cells) | `#b7dee8` |
| GPA header | `#daeef3` |
| Z/RANK header (and S/N header on page 1) | `#fce4d6` |

**Conditional:** only the **COMPETENCY LEVEL** cell (school rows and the overall row). The level comes from the `Grade X` label, or from the GPA if the label is missing (`sars_pdf/grading.py`):

| GPA | Level | Fill |
|---|---|---|
| < 1.6 | Grade A (Excellent) | `#00b050` |
| 1.6 – < 2.6 | Grade B (Very Good) | `#92d050` |
| 2.6 – < 3.6 | Grade C (Good) | `#ffff00` |
| 3.6 – < 4.6 | Grade D (Satisfactory) | `#ffc000` |
| ≥ 4.6 | Grade F (Fail) | `#ff0000` |

These GPA bands agree with every row in the original. AV/GRD letter grades are taken from the data, not recalculated, because the original is not consistent at the boundaries (e.g. 29.62 → D, 44.67 → C).

> The hex values were measured from the page images of the original. Once `reference/original.pdf` is committed, `compare.py` prints the exact fill colours used in the original, and the variables in `:root` can be corrected in one place.

## Per-table presentation quirks (`table.style`)

The original was exported from Excel sheets that differ slightly from each other. These flags reproduce the differences:

| key | default | used on |
|---|---|---|
| `title_size` | `normal` | `large`: page 1 subject line |
| `sn_header_fill` | `false` | `true`: page 1 (peach S/N header) |
| `centre_align` | `center` | `left`: pages 8–11 |
| `total_bold` | `true` | `false`: pages 8–11 |
| `competency_size` | `small` | `large`: pages 8–11 |
| `overall_competency_size` | `normal` | `small`: Chinese Language |

Geometry: US Letter, table x = 31.5–583.1 pt, data rows 9.07 pt (6.3 pt on the compact page), Arial/Liberation Sans.

## Fidelity check

```bash
cp /path/to/original.pdf reference/original.pdf
python scripts/compare.py reference/original.pdf output/report.pdf
```

For each page it reports page size, pixel-difference %, missing/extra words, and fill colours that appear in only one of the two PDFs. It also writes `output/diff/page_NN.png` (original | generated | diff).

## Next steps

- Build a data layer that computes rows from raw candidate results (A–F counts, totals, %, GPA, rank, competency via `grading.py`) and writes this JSON for any number of subjects and scopes (zone/region/council/ward).
- Calibrate the colours and fonts against `reference/original.pdf` with `compare.py`.
