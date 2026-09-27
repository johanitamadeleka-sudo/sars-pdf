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

| Report | Source PDF | Scope / level | Pages | pixel-diff | tolerant-diff | word-diff (miss/extra)* | fills (orig/gen)† | verdict >=96% (pass/total) |
|---|---|---|---|---|---|---|---|---|
| `primary-council-wards-rank` | MWANZA CC KATA RANK GRADING.pdf | council, per-ward (KATA) division/grade grid (WAV/WAS/JML); summary + JUMLA total | 1 | 18.42% | 11.82% | 129 / 34 | 0 / 0 | **0 / 1** |
| `primary-council-subjects-rank` | MWANZA CC UFAULU WA MASOMO.pdf | council, per-subject performance grid + summary block + ASILIMIA row + KUNDI LA UMAHIRI overall box (data-driven competency colour) | 1 | 10.97% | 8.83% | 26 / 28 | 1 / 0 | **0 / 1** |

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

`MWANZA CC` is the **test instance name of the sampled PDFs**, not a template
name — every directory above is named by **level + function** so the same
template renders any future council data of the same shape.

## Coverage status

The 13 `MWANZA CC …` STD4 council source PDFs under
`primary_council_pdf/primary_council_pdf/` consolidate by **structure** (the
SERIKALI / BINAFSI / JUMLA and ALAMA / GRADING variants are filtered views of a
shared shape). Two distinct structures are implemented so far, each as a fully
self-contained, coordinate-extracted, per-report-measured report:

| structure group | report | source PDFs it represents |
|---|---|---|
| per-ward division/grade grid | `primary-council-wards-rank` | KATA RANK GRADING |
| per-subject performance grid | `primary-council-subjects-rank` | UFAULU WA MASOMO (SUBJECT SUMMARY is the same one-row-per-subject shape) |

Remaining council structures to add (same proven pipeline —
`scripts/extract_primary_council_<fn>.py` + own template/CSS + measured
palette/grid): `primary-council-schools-rank-overall` (SCHOOL RANK IN GRADE +
SERIKALI + BINAFSI as `data_<tag>` variants), `primary-council-schools-rank-marks`
(SCHOOL RANK UFAULU ALAMA), `primary-council-wards-rank-marks` (KATA RANK ALAMA),
`primary-council-top-10-schools` (10 BEST SCHOOLS ALAMA + GRADING),
`primary-council-top-10-schools-subjectwise` (10 BEST SCHOOLS KIMASOMO OVERALL +
SERIKALI), and `primary-council-best-students-overall` (10 BEST STUDENTS).
