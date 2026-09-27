# reports/ — data-driven report generators (by school level)

This directory holds the reorganized, self-contained report generators. The
original top-level Lakezone example (`../templates/`, `../sars_pdf/`,
`../data/`, `../output/`) stays exactly where it is as the **proven success
reference** — see the [top-level README](../README.md) for the full philosophy,
data model, palette and fidelity check. New work starts here.

## Layout

```
reports/
  _shared/
    fonts.css                 # @font-face: real fonts, one family name each, NO fallback (see ../fonts/)
  secondary/                  # SECONDARY school level (the current work: council + region)
    council/                  # council-level reports (one subdir per report)
      <level-plus-function>/
        template.html.j2      # this report's own Jinja2 template
        style.css             # this report's own CSS (references 'Arial' etc. from _shared/fonts.css)
        data.json             # display-string data for this report
        reference/original.pdf# the source PDF to match
        output/               # generated report.pdf/.html + page images + comparison
    region/                   # region-level reports (one subdir per report)
      <level-plus-function>/  # same self-contained shape
  primary/
    README.md                 # documented PLACEHOLDER for future primary-level work
```

## Naming convention: LEVEL + WHAT-IT-DOES

Name each report directory (and its template) by **school level + the function
it performs**, never by location or a proper noun. The sample PDFs came from a
specific council/region, but those are **test instance names, not template
names**:

- `MWANZA CC` is the **council name** of the PDFs we sampled for testing — it is
  NOT a template name.
- `Mwanza` (region) is likewise just the sampled region instance.

So use, e.g.:

| Good (level + function) | Not this (location / proper noun) |
|---|---|
| `council-schools-rank-subjectwise` | `mwanza-cc-schools-rank` |
| `region-schools-rank-subjectwise`  | `mwanza-school-rank`     |
| `region-top-10-schools`            | `mwanza-top-10`          |
| `council-wards-rank`               | `mwanza-wards`           |

This keeps every generator **reusable for any future data** of the same shape:
feed a different council's or region's data through the same template and it
renders the same report.

## Self-contained per report

Each report is its **own unit**: its own `template.html.j2`, `style.css`,
`data.json`, `reference/original.pdf` and `output/`. Do **not** force sharing
between reports. The only shared asset is `_shared/fonts.css` (font
registration) because every report must use the same real fonts.

Where a council report and its region counterpart are genuinely the **same
structure** (e.g. `schools-rank-subjectwise`; the region variant only adds a
COUNCIL column plus C/RANK + R/RANK), the later feature may reuse the structure
deliberately — but that is a decision made per report, not a blanket rule.

## Fonts: real files, no fallbacks

`_shared/fonts.css` registers real font files (in `../fonts/`) under the exact
family names the source PDFs embed — `Arial`, `Arial Narrow`, `Times New
Roman` — with **one family name per `@font-face` and no comma-separated
fallback list**. A report's `style.css` writes `font-family: 'Arial';` (single
name). See [`../fonts/README.md`](../fonts/README.md) for the licensing
decision (metric-compatible Liberation substitutes for proprietary
Arial/Times).

> WeasyPrint note for generators: pass a shared `FontConfiguration` to BOTH the
> `CSS(...)` object and `write_pdf(...)`, otherwise the `@font-face` rules are
> ignored and text falls back to Noto Sans.

## Data as display strings

Store every value as a **display string**, preserving the original's exact
number formatting (`70.4` vs `65.00`, `43.937`, `100`). Fixed column fills live
in the report's CSS `:root`; only the data-driven cell (competency level, via
`../sars_pdf/grading.py`) changes colour based on GPA band. This mirrors the
Lakezone example so the output matches the source PDF character-for-character.

## Data-driven generation

Generation is **data-driven**: the template + CSS define the report; the JSON
supplies the rows. The goal is not only to reproduce the sample PDF, but to have
a template that renders **any future data of the same shape** into the same
report. Verify with the fidelity harness: render `data.json` to a PDF, then run
`../scripts/compare.py reference/original.pdf output/report.pdf` and drive the
pixel-diff and word-diff toward zero, exactly as the Lakezone example does.
