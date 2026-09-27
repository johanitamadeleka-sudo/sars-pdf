# Primary reports — fidelity summary (verdict at a glance)

This mirrors [`../secondary/INDEX.md`](../secondary/INDEX.md): for each primary
(Darasa la IV / STD4) report it lists the source PDF, scope/level, page count,
the latest pixel-diff / tolerant-diff / word-diff / fill-diff scores from
[`scripts/compare.py`](../../scripts/compare.py), and the **>=96% verdict**.

Regenerate everything (and refresh these numbers) with one command:

```bash
python scripts/build_all.py --level primary   # render + compare every report under reports/primary/**
```

## How to read the scores

Identical to the secondary INDEX (see
[How to read the scores](../secondary/INDEX.md#how-to-read-the-scores)). The two
key facts:

- **Page count** matches the original **exactly** for every report.
- The dominant reason a page does not clear the strict `tolerant-diff <= 4%` bar
  is the **proprietary-font substitution floor**: the primary originals embed
  genuine Monotype `ArialMT` / `Arial-BoldMT` / `ArialNarrow-Bold` (verified with
  `pymupdf get_fonts`), which cannot be redistributed in-sandbox, so each report
  renders with the metric-compatible OFL **Liberation** faces registered under
  the real family names. They match advance widths exactly but are not
  glyph-identical, so thousands of tiny digits differ along their edges. This is
  the same documented floor the Lakezone genuine-Arial example hits (0/11 pages
  pass the strict pixel bar with 0/0 words and 0 fill mismatches). The generated
  PDFs embed **only** Liberation-as-Arial (never Noto) — verified per report.
- **Palettes are measured PER REPORT** from that report's OWN
  `reference/original.pdf` with [`scripts/measure_fills.py`](../../scripts/measure_fills.py);
  only the **KUNDI LA UMAHIRI** (competency-level) cell colour is data-driven,
  via [`../../sars_pdf/grading.py`](../../sars_pdf/grading.py), which is now
  Daraja-aware. On the repeating main-grid pages the fill-diff is driven to
  **0 orig / 0 gen** (or a single decorative one-off cell, itemised below).

## Council reports (`reports/primary/council/`)

| Report | Source PDF | Scope / level | Pages | tolerant-diff | word-diff (miss/extra)* | fills (orig/gen)† | verdict >=96% (pass/total) |
|---|---|---|---|---|---|---|---|
| `primary-council-wards-rank` | MWANZA CC KATA RANK GRADING.pdf | council, per-ward (KATA) division/grade grid (WAV/WAS/JML); summary + JUMLA total | 1 | 11.82% | 129 / 34 | 0 / 0 | **0 / 1** |
| `primary-council-subjects-rank` | MWANZA CC UFAULU WA MASOMO.pdf | council, per-subject performance grid + summary + ASILIMIA row + KUNDI LA UMAHIRI box (data-driven competency colour) | 1 | 8.83% | 26 / 28 | 1 / 0 | **0 / 1** |
| `primary-council-schools-rank-overall` | MWANZA CC SCHOOL RANK IN GRADE.pdf | council, all-schools division/grade grid (WAV/WAS/JML) + UMILIKI; data-driven competency | 3 | 9.9–26.0% | 191–349 / 81–257 | 0 / 0 (gen) | **0 / 3** |
| `primary-council-schools-rank-ownership` (serikali) | MWANZA CC SCHOOL RANK SERIKALI.pdf | council, government-only division/grade grid (+KATA col) | 2 | 19.7–23.3% | 28–71 / 115–127 | 1–3 / 0 | **0 / 2** |
| `primary-council-schools-rank-ownership` (binafsi) | MWANZA CC SCHOOL RANK BINAFSI.pdf | council, private-only division/grade grid (no KATA col) | 2 | 19.6–24.4% | 50–187 / 121–208 | 1–3 / 0 | **0 / 2** |
| `primary-council-best-students-overall` | MWANZA CC 10 BEST STUDENTS.pdf | council, section-centric top-10 students, per-candidate 6-subject AL/DRJ grid | 4 | 5.6–12.1% | 109–206 / 32–70 | 0 / 0 | **0 / 4** |
| `primary-council-top-10-schools` | MWANZA CC 10 BEST SCHOOLS ALAMA.pdf | council, section-centric top-10 schools by marks (incl. SHULE KUMI DUNI) | 2 | 10.5–12.4% | 136–187 / 65–81 | 0 / 0 | **0 / 2** |

\* word-diff is the fuzzy-tokeniser total (see the secondary INDEX): it
over-counts visually identical **rotated headers** (the vertical `NAFASI KIKATA`
label tokenised char-by-char) and **compact wrapped group headers** whose
multi-line labels the tokeniser splits differently from the original. The
extracted `data.json` content is verified correct against the source by the
coordinate extractor; a page can therefore fail the verdict on `words` while the
data is identical.

† fills = distinct fill colours on only one side, aggregated across pages
(orig-only / gen-only). `0 / 0` means the measured per-report palette reproduces
the original's colours exactly.

- **`primary-council-wards-rank` — 0 / 0 fills.** The measured palette reproduces
  every band exactly on the main grid. In this report the `KUNDI LA UMAHIRI`
  column is **NOT** colour-filled in the original (the competency text is plain),
  so the template deliberately leaves it uncoloured — verified by `measure_fills.py`
  (0 orig / 0 gen). Residual `pixels`/`words` are the font-noise floor plus the
  rotated `NAFASI KIKATA` header tokeniser artifact.
- **`primary-council-subjects-rank` — 1 orig-only fill (`#fed4fc`).** A single
  one-off decorative cell in the top summary band; every other fill (including the
  data-driven `Daraja B`→`#92d050` / `Daraja C`→`#ffff00` competency cells) matches
  0 orig / 0 gen. Residual `pixels`/`words` are the font-noise floor plus the
  wrapped group-header tokeniser split.
- **`primary-council-schools-rank-overall` — 0 gen-only fills on every page.**
  The remaining orig-only fills (`#ff0000`, `#ffe699`, page-3 `#92d050`/`#f4b084`)
  are the one-off decorative SUMMARY/aggregate banner (E% column). Competency
  colours are data-driven and correct. Residual `pixels`/`words` are the
  font-noise floor on a dense wide grid.
- **`primary-council-schools-rank-ownership` (SERIKALI + BINAFSI) — 0 gen-only
  fills on every page.** The two ownership variants have DIFFERENT physical column
  layouts (SERIKALI carries a `KATA` column; BINAFSI omits it and shifts every
  numeric x-centre), so each is driven by its own `data_<tag>.json` with its own
  measured header x-centres; one shared self-contained template/CSS renders both.
  Orig-only residuals (`#ff0000` decorative empty-cell red, `#f4b084`/`#f2f2f2`
  one-off JUMLA/aggregate banner cells on page 2) are the documented decorative
  class. Tolerant sits ~20–24% (dense wide grid + the two divergent layouts share
  one measured CSS), the proprietary-font floor.
- **`primary-council-best-students-overall` — 0 / 0 fills on all 4 pages.**
  Section-centric per-candidate 6-subject `AL`/`DRJ` grid; the original does NOT
  colour the grade cells (all top candidates are Daraja A on white), so no
  data-driven colour is applied. Pagination is data-driven (each section's
  `page_top` mirrors the original's own page breaks: JUMLA+WAVULANA, then
  WASICHANA alone, then the two SERIKALI blocks, then SERIKALI WASICHANA alone).
  Residual `pixels`/`words` (tol 5.6–12.1%) are the font-noise floor plus the
  stacked subject/group headers the fuzzy tokeniser splits.
- **`primary-council-top-10-schools` — 0 / 0 fills on both pages.**
  Section-centric top-10 schools by marks (JUMLA / ZA SERIKALI / BINAFSI, plus
  the SHULE KUMI DUNI worst-10 block), per-school 6-subject `AL`/`DRJ` averages.
  No data-driven colour (original leaves the grade/competency cells white).
  Residual `pixels`/`words` are the font-noise floor plus the vertical/stacked
  `WASTANI WA UFAULU/30` and subject group headers.

`MWANZA CC` is the **test instance name of the sampled PDFs**, not a template
name — every directory above is named by **level + function** so the same
template renders any future council data of the same shape.

## Coverage status

The 13 `MWANZA CC …` STD4 council source PDFs under
`primary_council_pdf/primary_council_pdf/` consolidate by **structure** (the
SERIKALI / BINAFSI / JUMLA and ALAMA / GRADING variants are filtered views of a
shared shape). **Six** distinct structures are implemented so far, each a fully
self-contained, coordinate-extracted, per-report-measured report:

| structure group | report | source PDFs it represents |
|---|---|---|
| per-ward division/grade grid | `primary-council-wards-rank` | KATA RANK GRADING |
| per-subject performance grid | `primary-council-subjects-rank` | UFAULU WA MASOMO (SUBJECT SUMMARY is the same shape) |
| all-schools division/grade grid | `primary-council-schools-rank-overall` | SCHOOL RANK IN GRADE |
| schools division/grade grid by ownership | `primary-council-schools-rank-ownership` | SCHOOL RANK SERIKALI + BINAFSI (`data_serikali`/`data_binafsi`) |
| section-centric top-10 students | `primary-council-best-students-overall` | 10 BEST STUDENTS |
| section-centric top-10 schools by marks | `primary-council-top-10-schools` | 10 BEST SCHOOLS ALAMA |

Remaining council structures to add (same proven pipeline —
`scripts/extract_primary_council_<fn>.py` + own template/CSS + measured
palette/grid): `primary-council-schools-rank-marks` (SCHOOL RANK UFAULU ALAMA,
multi-section A/B/C/D/E/ABS grid), `primary-council-top-10-schools` GRADING
variant (10 BEST SCHOOLS GRADING is a division/grade top-10, a DIFFERENT shape
from the marks top-10 already built), `primary-council-top-10-schools-subjectwise`
(10 BEST SCHOOLS KIMASOMO OVERALL + SERIKALI), and the KATA RANK ALAMA per-ward
marks variant.
