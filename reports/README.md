# reports/ — data-driven report generators (by school level)

This directory holds the reorganized, self-contained report generators. The
original top-level Lakezone example (`../templates/`, `../sars_pdf/`,
`../data/`, `../output/`) stays exactly where it is as the **proven success
reference** — see the [top-level README](../README.md) for the full philosophy,
data model, palette and fidelity check. New work starts here.

## Layout

```
reports/
  secondary/                  # SECONDARY school level (the current work: council + region)
    council/                  # council-level reports (one subdir per report)
      <level-plus-function>/
        template.html.j2      # this report's own Jinja2 template
        style.css             # this report's own CSS, with its OWN inline @font-face (no shared stylesheet)
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
between reports. There is **no shared stylesheet** — every report's `style.css`
carries its OWN inline `@font-face` blocks (pointing at the real font files in
`../fonts/`). Reports use the same real font *files*, but each registers them
itself; nothing is `@import`ed.

Where a council report and its region counterpart are genuinely the **same
structure** (e.g. `schools-rank-subjectwise`; the region variant only adds a
COUNCIL column plus C/RANK + R/RANK), the later feature may reuse the structure
deliberately — but that is a decision made per report, not a blanket rule.

## Fonts: real files, no fallbacks

Each report's `style.css` registers its own real font files (in `../fonts/`)
inline via `@font-face`, under the exact family names the source PDFs embed —
`Arial`, `Arial Narrow`, `Times New Roman` — with **one family name per
`@font-face` and no comma-separated fallback list**. A report's `style.css`
writes `font-family: 'Arial';` (single name). See
[`../fonts/README.md`](../fonts/README.md) for the licensing decision
(metric-compatible Liberation substitutes for proprietary Arial/Times).

> WeasyPrint note for generators: pass a shared `FontConfiguration` to BOTH the
> `CSS(...)` object and `write_pdf(...)`, otherwise the `@font-face` rules are
> ignored and text falls back to Noto Sans.

## Data as display strings

Store every value as a **display string**, preserving the original's exact
number formatting (`70.4` vs `65.00`, `43.937`, `100`). Fixed column fills live
in the report's CSS `:root` and are **measured PER REPORT from that report's own
`reference/original.pdf`** — the non-competency fills are a fixed but
per-report palette, **not** identical across different reports, because the
originals genuinely use different hex values. Only the data-driven cell
(competency level, via `../sars_pdf/grading.py`) changes colour based on GPA
band. This mirrors the Lakezone example so the output matches each report's own
source PDF character-for-character.

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

**Header overflow was CSS sizing, not font width.** Because Liberation matches
Arial's advance widths, a header that spilled its cell was always a CSS bug, not
a font-width bug. `council-top-10-schools` printed "COMPETENCY LEVEL" on one
`white-space:nowrap` line running ~33pt past the page edge while the original
wraps it to two lines inside the cell; the fix was a single CSS rule
(`thead th.comp-h { white-space: normal }`) and every page's pixel-diff improved
with the palette unchanged. Genuine Arial for the Lakezone example is fetched at
build time and **gitignored** (proprietary). See
[`secondary/fixtures/README.md`](secondary/fixtures/README.md) for the full
measurement.

### The >=96% verdict, and which pages meet it

`scripts/compare.py` now emits a **machine-checkable per-page verdict** against
the user's stricter bar — *"at least 96% everywhere in colours, borders, data
and cell sizes"*. A page **PASS**es only when **all three** dimensions clear it
at once: tolerant pixel diff **<= 4%** (>=96% pixel match, position-by-position)
**AND** zero fills-only diffs both ways (colours) **AND** zero words
missing/extra (data). Otherwise it **FAIL**s and the failing dimension(s) are
named. The verdict is **added on top of** the existing tolerant-diff ruler and
never weakens it. It prints to stdout and is written into every
`output/comparison*/README.md` (a `verdict` column plus a per-report **verdict
summary** line). See [`secondary/INDEX.md`](secondary/INDEX.md) for the
per-report pass counts and the full PR-body breakdown.

### Reports that could not reach the >=96% bar, and why

Page count matches the original exactly for every report; the extracted content
is verified correct; palettes are now measured **per report** from each report's
own original (no shared palette); and the F/M/T grids' **cell-merge topology**
(colspan/rowspan) now matches each original to ~0.5pt with straight
`border-collapse` gridlines and independent summary vs. detail tables (Thread C).
The remaining diff is **not** a content, colour, border or cell-size error:

- **The dominant blocker is the proprietary-font substitution.** The originals
  embed genuine Monotype Arial/Times, which cannot be redistributed in-sandbox,
  so we embed **metric-compatible Liberation** faces under the real family names.
  They match advance widths and geometry exactly but are **not glyph-identical**,
  so thousands of tiny digits differ along their edges and push the tolerant-diff
  above 4% even when everything else is correct. This is a **rendering-noise
  floor, not a defect** — the Lakezone success example, which embeds **genuine
  Arial**, still reports tolerant-diff 4.8–6.8% (23% on its dense compact page
  11) and therefore also shows **0/11 pages** passing the strict pixel bar while
  having **0/0 words and 0 fill mismatches** on every page. Dense wide F/M/T
  grids sit highest (most digits); sparse reports sit lowest.
- **Colours now match on the repeating main-grid pages** of every report
  (fill-diff driven to 0 there). The residual fills-only diffs are limited to:
  the **one-off decorative SUMMARY / aggregate banner** (a multi-colour legend
  rendered once, e.g. `council-wards-rank`, `region-schools-rank-governments`
  last page), the `region-mobility` `#c00000` negative-delta ink (rendered as
  coloured **text**; pdfplumber counts the original's as a filled glyph path),
  the `region-top-10` single-`0`-column topology choice, and single **data-driven
  competency** colours on paginated sections — all documented, none the
  shared-palette bug that the per-report measurement removed.
- **`compare.py` tokeniser artifacts** inflate the reported **word-diff** on
  every report with rotated/vertical headers (`RANK`, `COMPETENCY LEVEL`,
  `S/NO.`, `SUMMARY PERFORMANCE`), compact continuation headers, and long
  COUNCIL/SCHOOL/DETAILED SUBJECTS strings that kern into the adjacent cell so
  pdfplumber merges the tokens. These are **visual-identical** metric artifacts,
  not missing data — see [`secondary/INDEX.md`](secondary/INDEX.md).
- **Pages that DO pass the >=96% bar** are the near-blank / sparse continuation
  pages where the font-noise floor drops below 4%: `council-best-students-subjectwise`
  10/30, `council-schools-rank-subjectwise` 8/24, `council-subjects-rank` 1/2 —
  19 report-pages total. Every other page fails on `pixels` (font noise) and/or
  `words` (tokeniser), with the honest per-page reason listed in the INDEX.

### Primary level: future placeholder

`../reports/primary/` is an intentional **placeholder** for the future PRIMARY
school level. It mirrors this secondary structure and follows the same
conventions (level+function naming, self-contained per report, real fonts, no
fallback, display strings, data-driven). No primary implementation is scheduled
in the current task — see [`primary/README.md`](primary/README.md).
