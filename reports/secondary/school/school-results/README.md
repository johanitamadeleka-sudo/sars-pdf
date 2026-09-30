# school-results — per-school Form Two mock result sheet

This report rebuilds the per-school PDF that sars.ac.tz publishes for each secondary
school, for example on the
[Buchosa council page](https://sars.ac.tz/results/exam/form-two-mock-result/2026/mwanza/buchosa-1787231755).
The directory is named by level and function. School names appear only in the data.

| Page(s) | Content |
|---|---|
| 1 | Titles, DIVISION PERFORMANCE SUMMARY (F/M/T × I–0), then the first candidate rows |
| 2 … n | Candidate list: CNO, name, sex, AGGT, DIV, POS, detailed subjects |
| last 1–2 | Centre overall performance, division performance, subject performance & ranking, subjects grading summary |

## Rendering a school from your own data

```bash
python -m sars_pdf.render my_school.json \
    --template-dir reports/secondary/school/school-results --pdf out/my_school.pdf
```

[`input.example.json`](input.example.json) shows the input shape. All values are
display strings, printed exactly as given.

| Key | Shape |
|---|---|
| `document` | `ministry` [2 lines], `region_title`, `exam_name`, `centre_no`, `school_name`, optional `school_title` (defaults to `"<centre_no> - <school_name>"`), optional `footer` (e.g. `"LAKE ZONE MOCK IV"`) |
| `division_summary[]` | `{sex, i, ii, iii, iv, zero}` for rows F, M, T |
| `candidates[]` | `{cno, name, sex, aggt, div, pos, subjects}` (absent candidates use `"ABS"`, with `pos` left empty) |
| `overall` | `{region, council, passed, average, gpa, competency, council_rank, region_rank}` |
| `division_performance` | `{counts: {...}, percent: {...}}` with keys `regist absent sat inc clean div_i div_ii div_iii div_iv div_0 div_i_iii div_i_iv` |
| `subjects[]` | `{code, name, sat:[F,M,T], pass:[F,M,T,%], fail:[F,M,T,%], s_rank, c_rank, r_rank, z_rank, gpa, competency}` |
| `grading[]` | `{code, name, a:[F,M,T], b, c, d, f, reg:[F,M,T]}` |
| `layout` | optional, see below |

The competency label (`"Grade D (Satisfactory)"`) sets the only data-driven colour
(`sars_pdf/grading.py`). The subject table and the centre GPA cell use different
palettes: D is `#e26b0a` in the subject table and `#ffc000` in the GPA cell, as in the
originals.

## `layout`: sheet geometry

Excel scales every school's sheet to fit the page. Column widths, row heights, font
scale and page breaks therefore differ from school to school.
`scripts/extract_school_results.py` measures these values from a source PDF and stores
them in `layout`:

- `cols`: 25 boundaries (band edge, b1…b23, band edge). Every cell spans a range of these.
- `font_scale`: the size the sheet's 7pt body font prints at, divided by 7 (e.g. 6.72 / 7 = 0.96).
- Row heights (`cand_row`, `overall_rows`, `subject_rows`, …).
- `first_page_rows` and `rows_per_page`.
- `gaps` (blank rows between summary blocks) and `breaks` (which summary blocks start a new page).

If `layout` is missing, the template uses the S0762 sheet's geometry. Candidate rows then
fill each page down to Excel's bottom margin, and any summary block that does not fit
moves to the next page.

## Reproducing the sample sources

```bash
python scripts/fetch_school_results.py \
    https://sars.ac.tz/results/exam/form-two-mock-result/2026/mwanza/buchosa-1787231755 \
    --only S0762 S1419 S1941                       # -> school_pdf/
python scripts/extract_school_results.py school_pdf/*.pdf   # -> data_<cno>.json + reference/
python scripts/build_all.py --scope school                  # render + compare
```

| Source | Candidates | Pages | Page breaks before | Tolerant diff | Verdict ≥96% |
|---|---|---|---|---|---|
| S0762 KOME | 210 | 8 | overall, subjects | 0.15–0.65% | 7 / 8 |
| S1419 BANGWE | 195 | 6 | overall | 0.41–1.26% | 5 / 6 |
| S1941 KAKOBE | 234 | 8 | subjects | 0.19–0.39% | 7 / 8 |

Page count, page breaks and fills match the original on every page, and all words
match on every candidate page. The only failing page per school is the one holding the
subject table, and it fails on words only. That is the repo-wide tokeniser artefact for
rotated headers: pdfplumber splits the original's rotated `S/RANK` into `K N A R /S`.
The pixels are identical within tolerance.

## Rendering notes

- **Grid.** Excel prints every rule as a "double" line: two 0.48pt rules with a 0.52pt
  gap. This is reproduced with separate borders (`border-spacing: 0.52pt`, 0.48pt cell
  borders). `<meta name="sars-pdf:rules" content="filled-boxes">` (see
  `sars_pdf/rules.py`) paints each side as its own filled rectangle, the way Excel does.
  That change took tolerant diff from about 17% to about 0.6%.
- **Overflowing text.** Excel lets text overflow its row, e.g. the 8pt block titles in
  9.7pt rows and the two-line SUBJECT/CODE header. In the template that text is anchored
  to the cell's inner bottom edge (`.ab`), so it does not stretch the row.
- **Fonts.** Titles use Tahoma Bold (Wine's metric-compatible `WineTahoma-Bold.ttf`,
  LGPL) and the footer uses Courier New Bold Italic (Liberation Mono). See `fonts/README.md`.
