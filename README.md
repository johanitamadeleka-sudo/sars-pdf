# sars-pdf — School Rank by Subject report (HTML + CSS → PDF)

This project rebuilds the OHONGSS-T **"SCHOOL RANK IN <SUBJECT> LAKEZONEWISE"** report (Lakezone Form Two Mock, August 2026, 11 pages, 16 subject tables) as HTML + CSS and prints it to PDF. Within **this** Lakezone example the layout, fonts, column fills and colours are the same on every page; only the data changes. (The wider secondary reports under [`reports/`](reports/README.md) each carry their **own** fixed palette measured from their **own** original — the fills are **not** identical across different reports. See [Colours](#colours) below.)

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
sars_pdf/fit.py                      # opt-in shrink-to-fit for fixed-pitch grid cells (template global fit())
sars_pdf/rules.py                    # opt-in: paint table rules as filled rects, like the Excel originals
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

> **Scope of this table.** The palette below is the **fixed** palette for **this
> Lakezone example** (`templates/report.css` `:root`) — it is the same on every
> *page* of this report. It is **not** a palette shared across the other
> reports. Each secondary report under [`reports/`](reports/README.md) carries
> its **own** fixed palette, **measured per report** from that report's own
> `reference/original.pdf` (with `pdfplumber` `page.rects`), because the
> originals genuinely use different hex values. The **only data-driven** colour
> anywhere is the COMPETENCY LEVEL cell background (via `sars_pdf/grading.py`);
> every other fill is a fixed, per-report-measured entry. See
> [`reports/secondary/INDEX.md`](reports/secondary/INDEX.md) for the per-report
> fill-diff scores.

**Fixed** (for this Lakezone example, in `templates/report.css` `:root`):

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

For each page it reports pixel-difference %, missing/extra words, and fill colours that appear in only one of the two PDFs. Everything is committed to git so it can be viewed on GitHub:

| Path | Content |
|---|---|
| `output/report.pdf`, `output/report.html` | generated report |
| `output/pages/page_NN.png` | generated pages as images |
| `output/comparison/page_NN.png` | original \| generated \| diff (red = differing pixels) |
| `output/comparison/README.md` | score table + all side-by-side images |

**Automatic:** `.github/workflows/compare.yml` runs on every push that touches `reference/original.pdf`, data, templates or code. It rebuilds the PDF, runs the comparison and commits `output/` back to the branch. So uploading `reference/original.pdf` through the GitHub web UI is enough to get the side-by-side results.

## Beyond the success example: the `reports/` tree

The Lakezone report above is the **documented success example** and stays exactly
where it is (`data/`, `templates/`, `sars_pdf/`, `scripts/compare.py`,
`output/`). The wider work — reproducing the council- and region-level SARS mock
reports the same way — lives under [`reports/`](reports/README.md), organised by
**school level**:

```
reports/
  _shared/fonts.css            # @font-face for the real fonts (see below)
  secondary/                   # SECONDARY level — built now (council + region)
    INDEX.md                   # fidelity verdict for every secondary report
    council/<level-plus-function>/   # one self-contained report per subdir
    region/<level-plus-function>/
  primary/README.md            # PRIMARY level — documented placeholder for the future
```

**Secondary is done now; primary is future.** `reports/primary/` is an
intentional placeholder that mirrors the secondary structure.

### Naming: LEVEL + FUNCTION, never the instance

Each report directory (and its template) is named by **school level + what it
does** — e.g. `council-schools-rank-subjectwise`, `region-top-10-schools`,
`region-district-performance`. It is **never** named after the sampled location.
The sample PDFs came from one council and one region:

- **`MWANZA CC`** is the **council name** of the PDFs sampled for testing — it is
  **not** a template name.
- **`Mwanza`** is likewise just the sampled **region instance** name.

Those strings appear only inside each report's `data.json` values. Keeping the
directory/template names level+function means the same template renders **any
future data of the same shape** (a different council's or region's numbers)
without edits — the real goal is a reusable template, not a one-off copy of one
PDF.

### Fully self-contained per report

Every report is its **own unit**: its own `template.html.j2`, its own `style.css`
with **inline `@font-face`**, its own `data.json` and `reference/original.pdf`,
and its own generated `output/`. There is **no shared report stylesheet** —
reports that share a structure (e.g. a council report and its region counterpart)
were built by **copying** the layout as a starting point, not by linking a common
file. The **only data-driven colour is the COMPETENCY LEVEL cell background**
(via [`sars_pdf/grading.py`](sars_pdf/grading.py)); every other fill is a
**fixed palette, but one measured PER REPORT from that report's own original** —
the non-competency fills are **not** identical across different reports, because
the originals genuinely use different hex values. Geometry and font are likewise
each expressed in that report's own HTML + CSS + Jinja2.

### Real fonts, no fallbacks

The source PDFs embed genuine Monotype Arial/Times, which cannot be legally
redistributed in-sandbox. Each report's CSS therefore writes a **single family
name with no fallback list** (`font-family: 'Arial';`) and
[`reports/_shared/fonts.css`](reports/_shared/fonts.css) / the inline
`@font-face` maps that name to a **real, metric-compatible open font file**
(Liberation Sans → Arial, Liberation Sans Narrow → Arial Narrow, Liberation Serif
→ Times New Roman) shipped in [`fonts/`](fonts/README.md). This is a deliberate
licensing decision, documented as a blocker for the PR in
[`reports/README.md` › Decisions / blockers](reports/README.md#decisions--blockers).
If a genuinely licensed Arial/Times file becomes available it drops in under the
same family name with no other change.

### Render + compare workflow

Same fidelity discipline as the Lakezone example — render `data.json` to a PDF,
then diff it against the report's `reference/original.pdf`:

```bash
python scripts/render_and_compare.py reports/secondary/council/council-subjects-rank  # one report
python scripts/build_all.py                                                           # ALL secondary reports
```

The verdict for every report (source PDF, scope, page count, latest pixel/word
diff) is in [`reports/secondary/INDEX.md`](reports/secondary/INDEX.md).

## Next steps

- Build a data layer that computes rows from raw candidate results (A–F counts, totals, %, GPA, rank, competency via `grading.py`) and writes this JSON for any number of subjects and scopes (zone/region/council/ward).
- Calibrate the colours and fonts against `reference/original.pdf` with `compare.py`.
- Fill in `reports/primary/` when the primary school level is scheduled, mirroring the secondary layout.
