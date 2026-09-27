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

## Build + compare everything

Regenerate and compare **all** secondary reports in one step (each report writes
into its own `output/`; sources are never modified):

```bash
python ../scripts/build_all.py                 # every report under reports/secondary/**
python ../scripts/build_all.py --level council # council only
python ../scripts/build_all.py --level region  # region only
```

`build_all.py` discovers every self-contained report directory (a dir that owns
`template.html.j2` + `style.css` and has a `data.json`, or the multi-source
`data_<tag>.json` + `reference/original_<tag>.pdf` shape used by
`region-schools-rank-subjectwise`). For a single report, use
[`../scripts/render_and_compare.py <report-dir>`](../scripts/render_and_compare.py).

The **verdict at a glance** — source PDF, scope, page count and latest
pixel/word diff for every report — lives in
[`secondary/INDEX.md`](secondary/INDEX.md).

## Decisions / blockers

For the PR body. These record deliberate choices and the reports that could not
reach near-zero pixel fidelity, and why.

### Fonts: real files, metric-compatible substitution (no fallback chains)

The source PDFs embed genuine **Monotype** faces — `ArialMT`, `Arial-BoldMT`,
`ArialNarrow-Bold`, `TimesNewRomanPS-BoldMT` (region PDFs use subsetted CIDFonts
of the same visual families). Those fonts are **proprietary** and no genuine
licensed Arial/Times file can be obtained or redistributed in-sandbox. The user
requires **real fonts with NO fallback chains**.

Decision: acquire **real, open font files** that are **metric-compatible** with
the originals and register them under the **exact family names** the CSS uses,
so each `@font-face` maps one family name to one real file with **no
comma-separated fallback**:

| Family name in CSS | Real file shipped in `../fonts/` | Stands in for |
|---|---|---|
| `Arial` (Regular / Bold) | `LiberationSans-Regular.ttf` / `LiberationSans-Bold.ttf` | ArialMT / Arial-BoldMT |
| `Arial Narrow` (Bold) | `LiberationSansNarrow-Bold.ttf` | ArialNarrow-Bold |
| `Times New Roman` (Bold) | `LiberationSerif-Bold.ttf` | TimesNewRomanPS-BoldMT |

Liberation is SIL OFL 1.1 licensed (see
[`../fonts/README.md`](../fonts/README.md) and
`../fonts/LICENSE-Liberation.txt`). Every generated PDF embeds these **real
Liberation glyphs** (verified with `pymupdf get_fonts()` — never Noto). If a
genuinely licensed Arial/Times file becomes available, drop it into `../fonts/`
under the same family name and re-render; nothing else changes.

> WeasyPrint gotcha: `@font-face` is ignored unless a **single shared**
> `FontConfiguration` is passed to BOTH the `CSS(...)` object and
> `write_pdf(...)`. `sars_pdf/render.py` wires this; without it text silently
> falls back to Noto Sans.

**Residual consequence:** because Liberation is metric-compatible but not
glyph-identical to Monotype Arial/Times, `compare.py` reports a residual
**pixel-diff** even though geometry and colours align exactly. The diff overlay
shows red only along glyph edges. This is expected and is the direct cost of the
no-genuine-Arial-in-sandbox constraint.

### Reports that could not reach near-zero pixel fidelity, and why

Page count matches the original exactly for every report, and the extracted
content is verified correct. The remaining diff is **not** a content error:

- **Dense wide F/M/T division grids** — `council-schools-rank-overall`,
  `region-schools-rank-overall`, `region-schools-rank-governments`,
  `region-mobility`, and the multi-page `region-schools-rank-subjectwise`
  (English) — sit at ~**35–45% pixel-diff**. These pages pack thousands of tiny
  digits; the per-glyph Liberation-vs-Arial edge noise accumulates across the
  grid even though rows/columns/colours align to within ~1pt.
- **`compare.py` tokeniser artifacts** inflate the reported **word-diff** on
  every report with rotated/vertical headers (`RANK`, `COMPETENCY LEVEL`,
  `S/NO.`, `SUMMARY PERFORMANCE`), compact continuation headers, and long
  COUNCIL/SCHOOL/DETAILED SUBJECTS strings that kern into the adjacent cell so
  pdfplumber merges the tokens. These are **visual-identical** metric artifacts,
  not missing data — see [`secondary/INDEX.md`](secondary/INDEX.md) for the
  per-report note.
- Sparse reports (`*-top-10-schools`, `*-best-students-*`,
  `region-district-performance`, `council-subjects-rank`) sit low (~**9–20%**).

### Primary level: future placeholder

`../reports/primary/` is an intentional **placeholder** for the future PRIMARY
school level. It mirrors this secondary structure and follows the same
conventions (level+function naming, self-contained per report, real fonts, no
fallback, display strings, data-driven). No primary implementation is scheduled
in the current task — see [`primary/README.md`](primary/README.md).
