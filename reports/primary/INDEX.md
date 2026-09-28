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

## Region reports (`reports/primary/region/`)

Region reports carry the extra **COUNCIL / HALMASHAURI** text column where the
original has it (exactly as the secondary region variants do), plus `KATA` (ward)
and `JINA LA SHULE` (school) columns as present. Multi-source dirs consolidate
same-structure filtered variants into one template driven by `data_<tag>.json` +
`reference/original_<tag>.pdf` (the tags are listed per row).

| Report | Source PDF | Scope / level | Pages | pixel-diff | tolerant-diff | word-diff (miss/extra)* | fills (orig/gen)† | verdict >=96% (pass/total) |
|---|---|---|---|---|---|---|---|---|
| `primary-region-schools-rank-overall` | SHULE NAFASI STD4 JUMLA 2026.pdf | region, all-schools (open) division-grid rank + COUNCIL & KATA cols; WAV/WAS/JML grade groups + WASTANI + KUNDI + NAFASI WILAYA/MKOA | 16 | 19.1–42.6% | 17.6–30.6% | 7908 / 7108 | 2–4 / 0–2 | **0 / 16** |
| `primary-region-schools-rank-governments` (serikali) | SHULE SERIKALI STD4 2026.pdf | region, government-only division-grid rank + COUNCIL col | 15 | 20.1–37.2% | 14.3–25.1% | 853 / 989 | 9–12 / 1–2 | **0 / 15** |
| `primary-region-schools-rank-governments` (binafsi) | SHULE BINAFSI STD4 2026.pdf | region, private-only division-grid rank (same template, 2nd source) | 4 | 30.1–38.7% | 21.8–28.0% | 433 / 475 | 10–12 / 1–2 | **0 / 4** |
| `primary-region-district-performance` | HALMASHAURI MASOMO STD4 2026.pdf | region, per-council (HALMASHAURI) subject-performance grid, one subject block per page + JUMLA + ASILIMIA rows | 6 | 10.8–11.9% | 8.0–8.9% | 372 / 229 | 13 / 2 | **0 / 6** |
| `primary-region-best-students-overall` | MKOA WANAFUNZI BORA STD4 2026.pdf | region, section-centric top-10 students + COUNCIL col + per-candidate 6-subject AL/DRJ | 6 | 9.6–10.8% | 7.7–8.7% | 108 / 194 | 4 / 1 | **0 / 6** |
| `primary-region-top-10-schools` | MKOA SHULE BORA STD4 JUMLA 2026.pdf | region, section-centric top schools (two blocks/page; WAV/WAS/JML division blocks + per-subject AL/DRJ marks blocks) + COUNCIL col | 5 | 18.9–21.0% | 14.8–17.1% | 261 / 738 | 3–10 / 1–2 | **0 / 5** |
| `primary-region-top-10-schools-subjectwise` (jumla) | MKOA SHULE BORA MASOMO STD4 JUMLA 2026.pdf | region, per-subject top-10 schools overall (+UMILIKI col) | 3 | 18.7–19.9% | 15.7–17.5% | 33 / 73 | 10 / 0 | **0 / 3** |
| `primary-region-top-10-schools-subjectwise` (serikali) | MKOA SHULE BORA MASOMO SERIKALI STD4 2026.pdf | region, per-subject top-10 government schools (same template, 2nd source, no UMILIKI col) | 3 | 19.7–20.0% | 16.9–17.7% | 40 / 98 | 11 / 0 | **0 / 3** |
| `primary-region-subjects-rank` | MKOA UFAULU MASOMO STD4 JUMLA 2026.pdf | region, per-subject performance grid (WAV/WAS/JML + WASTANI + NAFASI, KIMKOA overall) | 1 | 8.7% | 7.0% | 11 / 25 | 12 / 2 | **0 / 1** |
| `primary-region-wards-schools` (serikali) | MKOA KATA SHULE ZA SERIKALI STD4 2026.pdf | region, per-ward (KATA) government-schools grid (idadi/wastani/nafasi + Daraja) | 4 | 6.9–41.6% | 5.8–28.4% | 356 / 282 | 15–18 / 0 | **0 / 4** |
| `primary-region-wards-schools` (binafsi) | MKOA KATA SHULE BINAFSI STD4 2026.pdf | region, per-ward (KATA) private-schools grid (same template, 2nd source) | 2 | 6.1–39.4% | 5.3–28.3% | 102 / 88 | 16–17 / 0 | **0 / 2** |

\* word-diff is the fuzzy-tokeniser total (see the secondary INDEX): the large
counts on the dense multi-page schools-rank grids grow down-page because the
original's per-page row count is **non-uniform** (e.g. `SHULE NAFASI` p1=48,
p2–14=60, p15=78, p16=7) while the template paginates at a near-uniform rows/page,
so a small row-packing offset re-tokenises every subsequent row. The extracted
per-cell `data.json` content is verified correct by the coordinate extractor; a
page can fail on `words` while being visually faithful.

† fills = distinct fill colours on only one side, aggregated across the report's
pages (orig-only / gen-only). **Region grids follow a documented convention that
differs from the council grids:** the region originals do **NOT** tint the data
body or the main grid header - they tint only a decorative top legend/key banner
(top &lt; 80pt) plus a few full-column highlight stripes. The report therefore
renders the data rows + grid header **white** and does not attempt to reproduce
the one-off decorative top banner/stripes (documented residual, same class as the
secondary decorative banners), which is where the orig-only fills come from. And
because `pdfplumber` does not record the original's per-row competency fills as
rects, the data-driven `KUNDI LA UMAHIRI` (competency) greens show up as
**gen-only** on the main-grid pages - this is an **EXPECTED** residual, not a
defect: the colour is present and correct, it is simply the only fill the
harness sees on our side that it cannot match against a rect on the original.

- **`primary-region-schools-rank-overall` (SHULE NAFASI, 16pp) - page count
  16/16 EXACT.** Columns `S/N | HALMASHAURI | KATA | JINA LA SHULE | UMILIKI` +
  9 WAV/WAS/JML grade groups + WASTANI + KUNDI + NAFASI WILAYA/MKOA, all verified
  correct. Residual is the font-noise floor + untinted header/decorative legend +
  the non-uniform row-packing pagination drift described above.
- **`primary-region-schools-rank-governments` (SERIKALI 15pp main + BINAFSI 4pp
  tag) - page counts 15/15 and 4/4 EXACT.** One self-contained template renders
  both tags, but each tag carries its **own** measured numeric x-centres (SERIKALI
  numerics start ~150, BINAFSI ~179; both `S/N | HALMASHAURI | JINA LA SHULE`, no
  KATA/UMILIKI, single NAFASI KIMKOA). Residual = font floor + untinted header +
  decorative top legend.
- **`primary-region-district-performance` (HALMASHAURI MASOMO, 6pp) - 6/6 EXACT.**
  Per-council subject-performance grid, one subject block per page, all 8 councils
  + JUMLA total + ASILIMIA (%) rows. The extractor derives per-page column
  geometry from the header (the source shifts the grid ~24pt right on pages 2–6)
  and assembles the staggered council rows (`IDADI YA SHULE`, `WASTANI`, and the
  `Daraja X (...)` label on a 2nd physical line) by y-band + x-centre. Cleanest of
  the dense region reports (tol 8.0–8.9%).
- **`primary-region-best-students-overall` (MKOA WANAFUNZI BORA, 6pp) - 6/6
  EXACT.** Section-centric: 6 `WANAFUNZI KUMI BORA` top-10 blocks, one per page,
  per-candidate 6-subject `AL`/`DRJ`. Candidate registration numbers are detected
  by a PS-number pattern so they never glue into the school/name text. The
  cleanest report of the region set (tol 7.7–8.7%, 4 orig / 1 gen).
- **`primary-region-top-10-schools` (MKOA SHULE BORA JUMLA, 5pp) - 5/5 EXACT.**
  The source packs **two** `SHULE KUMI BORA/DUNI` blocks per page (10 blocks over
  5 pages) and MIXES two physical layouts - a WAV/WAS/JML division grid (source
  pages 1–3) and a per-subject `AL`/`DRJ` marks grid with a `KATA` column (pages
  4–5). Pagination is fully data-driven: each section is tagged `layout=grid|subj`
  and carries `page_top` (True only for the first block on its source page), so
  the template reproduces the irregular two-blocks-per-page grouping exactly.
- **`primary-region-top-10-schools-subjectwise` (MASOMO JUMLA 3pp + SERIKALI 3pp
  tags) - page counts 3/3 and 3/3 EXACT.** 6 per-subject `SHULE 10 BORA` blocks
  two-per-page, data-driven `page_top`. One template, but each tag carries its own
  measured geometry (jumla has an UMILIKI column, serikali does not; numerics start
  ~229 vs ~192). 0 gen-only fills; orig-only residuals are the decorative top
  legend.
- **`primary-region-subjects-rank` (MKOA UFAULU MASOMO JUMLA, 1pp) - 1/1 EXACT.**
  Subject-performance WAV/WAS/JML grid (6 subjects + JUMLA total). The staggered
  2-physical-lines-per-subject rows are grouped into one logical row per subject
  by y-band + x-centre binning so each `Daraja X (...)` label is associated
  EXACTLY ONCE. Only the 1pp JUMLA (KIMKOA) grid is consolidated here; the 3pp
  `MKOA UFAULU MASOMO STD4 2026` variant is a DIFFERENT physical structure (pages
  2–3 are a school-count-by-subject grid) so it was not folded in as a tag.
- **`primary-region-wards-schools` (MKOA KATA SHULE SERIKALI 4pp + BINAFSI 2pp
  tags) - page counts 4/4 and 2/2 EXACT.** Flat per-ward (KATA) grid auto-paginated
  by a repeating `thead`; the `tr.row` height is tuned (8.4pt) so WeasyPrint's row
  overflow reproduces the originals' ward-per-page breaks. The higher pixel % on
  the dense early pages is cumulative per-row vertical drift plus the original
  tinting the whole header band (region grids tint only the header; the data body
  is white per the documented convention); the last, sparser page of each tag sits
  low (tol ~5.3–5.8%).

Region reports use the **STD4 Swahili grade labels** (`Daraja A (Bora Sana)`,
`Daraja B (...)`, … `Daraja F (...)`) for the competency column and the
**WAV / WAS / JML** (girls / boys / total) column triplets, exactly as the council
reports do; the COUNCIL / HALMASHAURI column is carried wherever the original has
it. `Mwanza` is the **test instance name of the sampled region PDFs**, not a
template name - every directory above is named by **level + function**.

## Coverage status

Both scopes are now implemented: **6 distinct council structures** under
`reports/primary/council/` **and 8 distinct region structures** under
`reports/primary/region/`, each a fully self-contained, coordinate-extracted,
per-report-measured report. The source PDFs consolidate by **structure** (the
SERIKALI / BINAFSI / JUMLA and ALAMA / GRADING variants are filtered views of a
shared shape, folded into one report dir via `data_<tag>.json` +
`reference/original_<tag>.pdf`).

### Council coverage (6 structures)

The 13 `MWANZA CC …` STD4 council source PDFs under
`primary_council_pdf/primary_council_pdf/`:

| structure group | report | source PDFs it represents |
|---|---|---|
| per-ward division/grade grid | `primary-council-wards-rank` | KATA RANK GRADING |
| per-subject performance grid | `primary-council-subjects-rank` | UFAULU WA MASOMO (SUBJECT SUMMARY is the same shape) |
| all-schools division/grade grid | `primary-council-schools-rank-overall` | SCHOOL RANK IN GRADE |
| schools division/grade grid by ownership | `primary-council-schools-rank-ownership` | SCHOOL RANK SERIKALI + BINAFSI (`data_serikali`/`data_binafsi`) |
| section-centric top-10 students | `primary-council-best-students-overall` | 10 BEST STUDENTS |
| section-centric top-10 schools by marks | `primary-council-top-10-schools` | 10 BEST SCHOOLS ALAMA |

**Council source PDFs still deferred** (genuinely distinct structures, each needs
its own bespoke extractor + palette/grid measurement - NOT yet built):
`SCHOOL RANK UFAULU ALAMA` (a multi-section A/B/C/D/E/ABS marks grid),
`10 BEST SCHOOLS GRADING` (a division/grade top-10, a DIFFERENT shape from the
`ALAMA` marks top-10 already built), `10 BEST SCHOOLS KIMASOMO OVERALL` +
`10 BEST SCHOOLS KIMASOMO SERIKALI` (per-subject top-10), and `KATA RANK ALAMA`
(the per-ward marks variant of `KATA RANK GRADING`).

### Region coverage (8 structures)

The 14 `MKOA … / SHULE … / KATA … / HALMASHAURI … STD4 2026` region source PDFs
under `primary_region_pdf/primary_region_pdf/`:

| structure group | report | source PDFs it represents |
|---|---|---|
| all-schools (open) division-grid rank + COUNCIL col | `primary-region-schools-rank-overall` | SHULE NAFASI STD4 JUMLA 2026 |
| schools division-grid rank by ownership + COUNCIL col | `primary-region-schools-rank-governments` | SHULE SERIKALI STD4 2026 + SHULE BINAFSI STD4 2026 (`original`/`original_binafsi`) |
| per-council (HALMASHAURI) subject-performance grid | `primary-region-district-performance` | HALMASHAURI MASOMO STD4 2026 |
| section-centric top-10 students + COUNCIL col | `primary-region-best-students-overall` | MKOA WANAFUNZI BORA STD4 2026 |
| section-centric top schools (division + marks blocks) + COUNCIL col | `primary-region-top-10-schools` | MKOA SHULE BORA STD4 JUMLA 2026 |
| per-subject top-10 schools | `primary-region-top-10-schools-subjectwise` | MKOA SHULE BORA MASOMO STD4 JUMLA 2026 + MKOA SHULE BORA MASOMO SERIKALI STD4 2026 (`_jumla`/`_serikali`) |
| per-subject performance grid (KIMKOA overall) | `primary-region-subjects-rank` | MKOA UFAULU MASOMO STD4 JUMLA 2026 |
| per-ward (KATA) schools grid by ownership | `primary-region-wards-schools` | MKOA KATA SHULE ZA SERIKALI STD4 2026 + MKOA KATA SHULE BINAFSI STD4 2026 (`_serikali`/`_binafsi`) |

That maps **12 of the 14** region source PDFs. **Region source PDFs still
deferred** (distinct structures folded in a follow-up; NOT yet built):
`MKOA UFAULU MASOMO STD4 2026` (the 3pp variant - page 1 is the same KIMKOA grid
already covered by `primary-region-subjects-rank`, but pages 2–3 are a separate
school-count-by-subject grid), `HALMASHAURI STD4 JUMLA 2026` (per-council overall
division grid - a different shape from the per-subject `HALMASHAURI MASOMO`), and
`KATA STD4 JUMLA 2026` (per-ward overall division grid). Each would be its own
report dir or an added tag with its own measured geometry.

## Residuals summary (PR-body ready)

Every implemented primary report matches its source PDF **page-for-page exactly**
(council 6 dirs / 7 render jobs, region 8 dirs / 11 render jobs), embeds **only**
the metric-compatible OFL Liberation faces registered as `Arial` / `Arial Bold`
(verified per report with `pymupdf get_fonts` - **never Noto**), stores every
value as a display string, colours only the `KUNDI LA UMAHIRI` competency cell
from data (Daraja-aware `grading.py`), and takes its palette from its **own**
measured original. **No page clears the strict >=96% verdict** (tolerant-diff
&lt;= 4% AND 0 fill diffs AND 0 word diffs), for the honest reasons below - the
same floor the Lakezone genuine-Arial example hits (0/11):

- **Proprietary-font substitution floor (the dominant reason).** The primary
  originals embed genuine Monotype `ArialMT` / `Arial-BoldMT` / `ArialNarrow-Bold`,
  which cannot be redistributed in-sandbox; Liberation matches advance widths
  exactly but is not glyph-identical, so thousands of tiny digits differ along
  their edges on the dense wide WAV/WAS/JML grids. Colours, borders, cell sizes
  and data are correct underneath.
- **Region decorative-legend + untinted-body residual (region reports).** The
  region originals tint only a decorative top legend/key banner (and a few
  highlight stripes), not the data body or grid header; those one-off decorative
  fills are not reproduced (documented residual), which is where the region
  orig-only fills come from. The data-driven competency greens correctly show as
  **gen-only** because `pdfplumber` records the original's per-row competency
  colour as a glyph path, not a rect the harness can match - EXPECTED, not a
  defect.
- **Council one-off decorative banner residual (council reports).** The remaining
  council orig-only fills (`#ff0000`, `#ffe699`, `#f4b084`, `#f2f2f2`, `#fed4fc`,
  page-3 `#92d050`) are the one-off decorative SUMMARY/aggregate banner cells; the
  repeating main-grid pages are **0 gen-only** everywhere.
- **Row-packing / pagination drift.** On the multi-page schools-rank and per-ward
  grids the original's per-page row count is non-uniform, so a near-uniform
  rows/page break introduces a growing vertical offset that inflates pixel-diff and
  the fuzzy word-diff on later pages; the per-cell data is verified correct.
- **Fuzzy-tokeniser word-diff.** Rotated/stacked headers (e.g. the vertical
  `NAFASI KIKATA` label) tokenise char-by-char and dense numeric runs concatenate
  in the PDF text layer, so `words` over-counts on visually identical content.
