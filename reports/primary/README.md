# reports/primary/ — primary (Darasa la IV / STD4) level reports

This directory holds the **PRIMARY** school level reports. They mirror the proven
**secondary** structure exactly (see [`../README.md`](../README.md)): each report
is a self-contained unit driven by JSON data → its own Jinja2 template → its own
CSS → WeasyPrint PDF, verified with [`../../scripts/compare.py`](../../scripts/compare.py).

```
reports/primary/
  council/
    <primary-level-plus-function>/    # e.g. primary-council-wards-rank
      template.html.j2
      style.css
      data.json                        # (or data_<tag>.json for multi-source dirs)
      reference/original.pdf           # (or reference/original_<tag>.pdf)
      output/                          # committed report.pdf/.html, pages/, comparison/
  region/                              # region-scope primary reports (implemented)
    <primary-level-plus-function>/    # e.g. primary-region-schools-rank-overall
      template.html.j2
      style.css
      data.json                        # (or data_<tag>.json for multi-source dirs)
      reference/original.pdf           # (or reference/original_<tag>.pdf)
      output/                          # committed report.pdf/.html, pages/, comparison/
```

Both scopes are now implemented (6 council report dirs + 8 region report dirs).
See [`INDEX.md`](INDEX.md) for the per-report fidelity verdict summary.

## Source of the primary PDFs

The 27 primary source PDFs were downloaded from the sars.ac.tz **Darasa la IV
Mock MKOA** results index (the `/serve-pdf?file=summaries%2F<hash>.pdf` endpoint)
by [`../../scripts/fetch_primary_summaries.py`](../../scripts/fetch_primary_summaries.py),
which reproduces the download. They are committed two ways:

- extracted, arranged by scope, under
  [`../../primary_council_pdf/`](../../primary_council_pdf/) (13 `MWANZA CC …`
  council docs) and [`../../primary_region_pdf/`](../../primary_region_pdf/) (14
  `… STD4 2026` region docs); and
- as the `primary_council_pdf.zip` / `primary_region_pdf.zip` bundles at the repo
  root.

Each report keeps its own copy as `reference/original.pdf` (or
`reference/original_<tag>.pdf`).

Conventions (identical to secondary — see [`../README.md`](../README.md)):

- name reports by **level + what-it-does** (`primary-` prefix), never by the
  sampled MWANZA/MKOA instance name (those live only inside `data.json` values);
- each report is **self-contained** (its own template, CSS, data, reference,
  output);
- register the real fonts (in [`../../fonts/`](../../fonts/)) with an OWN inline
  `@font-face` in each report's `style.css` — one family name per face
  (`'Arial'` / `'Arial Narrow'` / `'Times New Roman'`), **no fallback chains**,
  **no `@import`**, `src` pointing four levels up at `../../../../fonts/`;
- store every value as a **display string** (`'49.50'`, `'289.800'`, `'100'`),
  and store the full Swahili competency label (`'Daraja A (Bora Sana)'`);
- extraction is **coordinate-based** via `pymupdf` words
  (`scripts/extract_primary_council_*.py` and
  `scripts/extract_primary_region_*.py`), never hand-typed;
- palette is **measured per report** from its OWN original
  ([`../../scripts/measure_fills.py`](../../scripts/measure_fills.py)) and grid
  topology from [`../../scripts/measure_grid.py`](../../scripts/measure_grid.py);
- only the **competency-level (KUNDI LA UMAHIRI)** cell colour is data-driven,
  via [`../../sars_pdf/grading.py`](../../sars_pdf/grading.py) — which now
  recognises the Swahili `Daraja X (...)` labels in addition to `Grade X`.

## Primary column vocabulary (Swahili / abbreviations)

Primary STD4 originals use Swahili and abbreviated headers. The mapping to the
F/M/T-equivalent triplets used by the secondary reports:

| Primary header | Meaning |
|---|---|
| `WAV` | girls (wasichana) — the **F** equivalent |
| `WAS` | boys (wavulana) — the **M** equivalent |
| `JML` | total (jumla) — the **T** equivalent |
| `AL` | marks (alama) |
| `DRJ` | grade (daraja) |
| `KATA` | ward |
| `HALMASHAURI` | council |
| `UMILIKI` / `SERIKALI` / `BINAFSI` | ownership / government / private |
| `Daraja X (...)` | competency level label (A–F, e.g. `Daraja B (Vizuri Sana)`) |

## Build + verify

```bash
pyenv global 3.11.15
python scripts/build_all.py --level primary   # render + compare every primary report
python scripts/measure_fills.py reports/primary/region/<report>   # palette check
python scripts/measure_grid.py  reports/primary/region/<report>   # grid topology
```

`build_all.py` discovers every self-contained report dir under `reports/primary/**`
and never touches `reports/secondary/**`. Restrict to one scope with
`python scripts/build_all.py --level primary --scope council` or
`--scope region`.

See [`INDEX.md`](INDEX.md) for the per-report fidelity verdict summary.

## Implemented council reports (`reports/primary/council/`)

Built from the `MWANZA CC ... STD4` sources in
[`../../primary_council_pdf/`](../../primary_council_pdf/), each consolidated by
STRUCTURE (not by instance/filter name) and driven by its own coordinate
extractor `scripts/extract_primary_council_<function>.py`:

| Report | Source PDF | Pages | Nearest secondary starting point |
|---|---|---|---|
| `primary-council-subjects-rank` | MWANZA CC SUBJECT SUMMARY.pdf | 1 | `council-subjects-rank` (one row per subject) |
| `primary-council-wards-rank` | MWANZA CC KATA RANK GRADING.pdf | 1 | `council-wards-rank` (per-ward WAV/WAS/JML grid) |
| `primary-council-schools-rank-overall` | MWANZA CC SCHOOL RANK IN GRADE.pdf | 3 | `council-schools-rank-overall` (all-schools division/grade grid) |
| `primary-council-schools-rank-ownership` | MWANZA CC SCHOOL RANK SERIKALI.pdf + BINAFSI.pdf (`data_serikali`/`data_binafsi`) | 2 + 2 | `council-schools-rank-overall` (division/grade grid, filtered by ownership) |
| `primary-council-best-students-overall` | MWANZA CC 10 BEST STUDENTS.pdf | 4 | `council-best-students-overall` (section-centric per-candidate 6-subject AL/DRJ grid) |
| `primary-council-top-10-schools` | MWANZA CC 10 BEST SCHOOLS ALAMA.pdf | 2 | `council-top-10-schools` (section-centric top-10 schools by marks) |

Each reproduces the primary STD4 layout: `WAV`/`WAS`/`JML` triplets, the
`Daraja X (...)` competency label (the only data-driven cell colour, via
`grading.py`), and the per-report measured palette (0 gen-only fills on the
repeating main-grid pages; the remaining orig-only residuals are the one-off
decorative SUMMARY/aggregate banner cells, documented in `INDEX.md`). Fonts are
the metric-compatible Liberation faces registered as `Arial`/`Arial Bold`
(never Noto). Generated page counts match each source exactly.

The government-only (`SCHOOL RANK SERIKALI`) and private-only (`SCHOOL RANK
BINAFSI`) variants share the report TYPE but have DIFFERENT physical column
layouts from each other (the SERIKALI grid carries a `KATA` column; the BINAFSI
grid omits it, and every numeric x-centre is shifted) and from `IN GRADE` (no
shared `UMILIKI` column). They are therefore consolidated into their OWN report
dir `primary-council-schools-rank-ownership`, driven by
`data_serikali.json`/`data_binafsi.json`, each with its OWN measured header
x-centres in `scripts/extract_primary_council_schools_rank_ownership.py` — not as
tag reuse of the `IN GRADE` mapping.

**Not yet built (remaining council structures for a follow-up pass):**
`10 BEST SCHOOLS GRADING` (division/grade top-10, a different structure from the
`ALAMA` marks top-10 already built), the `10 BEST SCHOOLS KIMASOMO
OVERALL/SERIKALI` per-subject top-10, `SCHOOL RANK UFAULU ALAMA` (multi-section
A/B/C/D/E/ABS marks grid), and the `KATA RANK ALAMA` per-ward marks variant. Each
needs its own bespoke coordinate extractor + per-report palette/grid measurement.

## Implemented region reports (`reports/primary/region/`)

Built from the `MKOA … / SHULE … / KATA … / HALMASHAURI … STD4 2026` sources in
[`../../primary_region_pdf/`](../../primary_region_pdf/), each consolidated by
STRUCTURE and driven by its own coordinate extractor
`scripts/extract_primary_region_<function>.py`. Region reports carry the extra
**COUNCIL / HALMASHAURI** column where the original has it (as the secondary
region variants do):

| Report | Source PDF(s) | Pages |
|---|---|---|
| `primary-region-schools-rank-overall` | SHULE NAFASI STD4 JUMLA 2026.pdf | 16 |
| `primary-region-schools-rank-governments` | SHULE SERIKALI STD4 2026.pdf + SHULE BINAFSI STD4 2026.pdf (`original`/`original_binafsi`) | 15 + 4 |
| `primary-region-district-performance` | HALMASHAURI MASOMO STD4 2026.pdf | 6 |
| `primary-region-best-students-overall` | MKOA WANAFUNZI BORA STD4 2026.pdf | 6 |
| `primary-region-top-10-schools` | MKOA SHULE BORA STD4 JUMLA 2026.pdf | 5 |
| `primary-region-top-10-schools-subjectwise` | MKOA SHULE BORA MASOMO STD4 JUMLA + MASOMO SERIKALI STD4 2026.pdf (`_jumla`/`_serikali`) | 3 + 3 |
| `primary-region-subjects-rank` | MKOA UFAULU MASOMO STD4 JUMLA 2026.pdf | 1 |
| `primary-region-wards-schools` | MKOA KATA SHULE ZA SERIKALI + KATA SHULE BINAFSI STD4 2026.pdf (`_serikali`/`_binafsi`) | 4 + 2 |

Each reproduces the STD4 layout (`WAV`/`WAS`/`JML` triplets, `AL`/`DRJ`,
`Daraja X (...)` competency labels, and the COUNCIL/KATA/school text columns as
present), matches its source page-for-page exactly, and embeds Liberation as
`Arial` (never Noto). Region grids follow a documented palette convention that
differs from the council grids: the region originals tint **only** a decorative
top legend/key banner (not the data body or grid header), so the data rows are
rendered white and the one-off decorative banner is not reproduced (a documented
residual); the data-driven competency greens show as gen-only in `measure_fills`
because `pdfplumber` records the original's per-row competency colour as a glyph
path, not a matchable rect (EXPECTED, not a defect). The full honest per-report
residuals and verdict numbers are in [`INDEX.md`](INDEX.md).

**Not yet built (remaining region structures for a follow-up pass):**
`MKOA UFAULU MASOMO STD4 2026` (3pp variant - its pages 2-3 are a separate
school-count-by-subject grid), `HALMASHAURI STD4 JUMLA 2026` (per-council overall
division grid), and `KATA STD4 JUMLA 2026` (per-ward overall division grid).
