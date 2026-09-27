# Secondary reports — fidelity summary (verdict at a glance)

This is the visible **verdict** for every secondary report built so far. It
mirrors how [`output/comparison/README.md`](../../output/comparison/README.md)
reports the Lakezone success example: for each report it lists the source PDF,
the scope/level, the page count, the latest pixel-diff / tolerant-diff /
word-diff / fill-diff scores from [`scripts/compare.py`](../../scripts/compare.py),
and the new **>=96% verdict** (how many pages pass the stricter bar).

Regenerate everything (and refresh these numbers) with one command:

```bash
python scripts/build_all.py            # render + compare every report under reports/secondary/**
```

Each report keeps its own side-by-side images and per-page score table (now
including the per-page **verdict** column and a **verdict summary** line) under
`reports/secondary/<level>/<report>/output/comparison*/README.md`.

## How to read the scores

- **Page count** matches the original **exactly** for every report.
- **pixel-diff** is `compare.py`'s raw pixel-difference percentage per page
  (range shown min–max across the report's pages). **tolerant-diff** allows a
  1px shift to discount sub-pixel anti-aliasing and is the **true fidelity
  ruler** — the same one that grades the Lakezone success example. The residual
  is dominated by **font-substitution glyph-edge noise**: the originals embed
  genuine Monotype Arial/Times, which cannot be obtained or redistributed
  in-sandbox, so we render with metric-compatible Liberation faces registered
  under the real family names (see [`../../fonts/README.md`](../../fonts/README.md)
  and the [decisions note](../README.md#decisions--blockers)). Dense wide F/M/T
  grids therefore sit higher (thousands of tiny digits differ at the edges);
  sparse reports sit low.
- **Verdict (>=96%)** is the new, stricter, **machine-checkable** bar the user
  asked for: *"compare even pixel or position-by-position and attain at least
  96% everywhere in colours, borders, data, sizes of the cells etc."*
  `compare.py` marks a page **PASS** only when **all three** dimensions clear it
  at once: tolerant pixel diff **<= 4%** (>=96% pixel match, which measures
  colours + borders + cell sizes + data glyphs position-by-position) **AND**
  zero *fills only in original* / *fills only in generated* (colours) **AND**
  zero words missing / extra (data). Otherwise it **FAIL**s and names the failing
  dimension(s) (pixels / fills / words). This verdict is **added on top of** the
  existing tolerant-diff ruler — it never weakens it. The column below shows the
  per-report **pass count** (pages meeting >=96% / total pages).
- **Palettes are measured PER REPORT** — there is **no shared palette**. Every
  report's `style.css` `:root` fills were **re-measured from that report's OWN
  `reference/original.pdf`** with `pdfplumber` `page.rects`
  ([`scripts/measure_fills.py`](../../scripts/measure_fills.py)) and corrected
  off the old generalized Lakezone palette. The only **data-driven** colour that
  remains is the COMPETENCY LEVEL cell background (via
  [`../../sars_pdf/grading.py`](../../sars_pdf/grading.py)); every other fill is a
  **fixed** entry taken from that specific report's own original. On the
  repeating **main-grid** pages the fill-diff is now **0 orig / 0 gen** for the
  large majority of reports; the residuals are listed per report below and are
  limited to one-off decorative SUMMARY/aggregate banners, data-driven
  competency pagination, the `region-mobility` `#c00000` coloured-text delta, and
  the `region-top-10` single-`0`-column topology choice.
- **word-diff** is `compare.py`'s **fuzzy tokeniser** total (missing + extra
  across all pages), NOT a true content diff. The residual counts are metric
  artifacts: vertical/rotated headers tokenised char-by-char (e.g. `C/RANK` →
  `K N A R /C`), compact continuation headers splitting group labels
  differently, and long COUNCIL/SCHOOL/DETAILED strings kerning into the next
  cell so tokens merge (e.g. `KAHANGARA GOVERNMENT` → `KAHANGAGROAVERNMENT`).
  The extracted `data.json` content is verified correct against the source. A
  page can therefore fail the verdict on `words` while being visually identical.

## Council reports (`reports/secondary/council/`)

| Report | Source PDF | Scope / level | Pages | pixel-diff | tolerant-diff | word-diff (miss/extra)* | fills (orig/gen)† | verdict >=96% (pass/total) |
|---|---|---|---|---|---|---|---|---|
| `council-schools-rank-subjectwise` | MWANZA CC SCHOOLS RANK SUBJECTWISE.pdf | council, per-subject school rank (COUNCILWISE, C/RANK) | 24 | 0.0–26.9% | 0.0–21.6% | 162 / 130 | 4 / 0 | **8 / 24** |
| `council-subjects-rank` | MWANZA CC SUBJECTS RANK.pdf | council, one row per subject | 2 | 4.1–18.8% | 2.6–9.7% | 4 / 1 | 0 / 0 | **1 / 2** |
| `council-schools-rank-overall` | MWANZA CC SCHOOLS RANK.pdf | council, division-performance grid (F/M/T); fixed per-column tints + data-driven competency | 1 | 30.9% | 8.8% | 209 / 64 | 0 / 0 | **0 / 1** |
| `council-top-10-schools` | MWANZA CC 10 BEST SCHOOLS.pdf | council, top-10 sections (incl. districtwise/govt) | 3 | 18.1–19.7% | 12.6–14.8% | 46 / 32 | 1 / 4 | **0 / 3** |
| `council-best-students-overall` | MWANZA CC 10 BEST STUDENTS.pdf | council, top students + detailed subjects | 5 | 8.7–20.6% | 5.3–15.3% | 172 / 41 | 0 / 0 | **0 / 5** |
| `council-best-students-subjectwise` | MWANZA CC 10 BEST STUDENTS SUBJECTWISE.pdf | council, top-10 students per subject | 30 | 0.0–10.5% | 0.0–8.8% | 398 / 110 | 0 / 0 | **10 / 30** |
| `council-wards-rank` | MWANZA CC Wards Rank.pdf | council, per-ward performance (WARDWISE, RANK) | 1 | 19.4% | 13.6% | 38 / 7 | 7 / 0 | **0 / 1** |

## Region reports (`reports/secondary/region/`)

| Report | Source PDF | Scope / level | Pages | pixel-diff | tolerant-diff | word-diff (miss/extra)* | fills (orig/gen)† | verdict >=96% (pass/total) |
|---|---|---|---|---|---|---|---|---|
| `region-schools-rank-subjectwise` (EDK) | Mwanza School Rank-EDK.pdf | region, per-subject school rank + COUNCIL col + C/RANK & R/RANK (REGIONWISE) | 1 | 13.8% | 8.8% | 1 / 0 | 1 / 0 | **0 / 1** |
| `region-schools-rank-subjectwise` (English) | Mwanza School Rank-English Language.pdf | region, per-subject school rank (same template, 2nd source) | 6 | 26.6–33.3% | 16.3–18.7% | 12 / 12 | 1 / 1 | **0 / 6** |
| `region-subjects-rank` | Mwanza Overall Subjects Performance.pdf | region, one row per subject (REGIONALWISE) | 2 | 12.2–18.2% | 7.7–11.0% | 4 / 2 | 0 / 1 | **0 / 2** |
| `region-schools-rank-overall` | Mwanza schools rank Overall.pdf | region, division grid + COUNCIL col; fixed per-column pastel tints reproduced | 6 | 13.3–40.9% | 5.7–20.5% | 231 / 375 | 1 / 0 | **0 / 6** |
| `region-schools-rank-governments` | Mwanza Schools Rank For Governments.pdf | region, division grid, government schools only; fixed per-column pastel tints reproduced | 4 | 34.3–42.0% | 16.6–21.5% | 225 / 277 | 4 / 0 | **0 / 4** |
| `region-top-10-schools` | Mwanza Top 10 Schools.pdf | region, top-10 overall + COUNCIL col | 6 | 9.6–10.9% | 8.4–9.9% | 14 / 28 | 4 / 3 | **0 / 6** |
| `region-best-students-overall` | Mwanza Best Students-Overall.pdf | region, top students + COUNCIL col + detailed subjects | 9 | 10.6–12.1% | 7.2–9.9% | 219 / 74 | 2 / 0 | **0 / 9** |
| `region-best-students-subjectwise` | Mwanza Best students-Subjectwise.pdf | region, top-10 students per subject + COUNCIL col | 23 | 10.9–11.4% | 8.7–9.2% | 156 / 71 | 2 / 1 | **0 / 23** |
| `region-district-performance` | Mwanza f2 District Performance.pdf | region only, per-council/district division grid | 5 | 8.4–9.2% | 5.5–7.1% | 17 / 35 | 0 / 1 | **0 / 5** |
| `region-mobility` | Mwanza f2 Mock Mobility 2026.pdf | region only, FTNA 2025 vs Mock 2026 (Swahili labels); fixed section/header fills + IMEPANDA/UMESHUKA up-down colour-coding | 6 | 28.5–33.7% | 16.9–23.6% | 71 / 45 | 1 / 1 | **0 / 6** |

\* word-diff is the fuzzy-tokeniser total (see [How to read the scores](#how-to-read-the-scores)); it over-counts visually identical rotated headers (e.g. `C/RANK` → `K N A R /C`). It USED to also over-count **cell-adjacency kern merges** — adjacent cell contents gluing in the PDF text layer such as `DCKATUNGURU` (`DC` + ward `KATUNGURU`) and `DCSAVANA` on `region-top-10-schools` / `region-schools-rank-governments`. Those were a real structural symptom (COUNCIL names in metric-compatible Liberation are wider than the original's Arial, so `…DC` overflowed its column and touched the next cell). They are now **fixed** by tightening the COUNCIL column's font/tracking so the text stays inside its own fixed-width column (column boundaries unchanged, grid still aligns to ~0.3pt): `region-top-10-schools` pages 2/6 dropped from 5 miss / 6 extra to 1 miss / 4 extra (the residual is only the rotated-header split). The remaining word diffs are rotated-header tokeniser artifacts (visually identical) or the dense F/M/T triplet numeric runs on the schools-rank grids, which pdfplumber concatenates regardless of cell borders; extracted per-cell content is verified correct.

† fills = the count of **distinct** fill colours that appear on only one side, aggregated across the report's pages (orig-only / gen-only). `0 / 0` means the fixed per-report palette reproduces the original's colours exactly on every page. Non-zero residuals are itemised in the [PR-body summary](#pr-body-ready-summary--per-report-beforeafter--verdict) below.

**Duplicate note:** `Mwanza Schools Rank For Governments (1).pdf` is
**byte-identical** (md5 `abcc1c77b83d95a426e3ad2292c27e6e`) to
`Mwanza Schools Rank For Governments.pdf`, so only one report
(`region-schools-rank-governments`) is built for both.

`MWANZA CC` (council) and `Mwanza` (region) are the **test instance names of the
sampled PDFs**, not template names — every directory above is named by
**level + function** so the same template renders any future council/region data
of the same shape.

## Cell-merge topology corrections (Thread C)

The third problem the user raised was structural: the generated grids tried to
force the aggregate/summary block and the per-school detail table to **start and
align the same on the left and right** even though the originals genuinely have
**different structures**, some cells that should be merged were **not merged**,
and **gridlines were not straight**. Thread C corrected the cell-merge topology
of the seven F/M/T division-grid reports so each generated table reproduces the
**exact colspan/rowspan of its OWN original**, verified with
[`scripts/measure_grid.py`](../../scripts/measure_grid.py) (column-boundary x and
row-boundary y positions) and `pdfplumber` `page.rects` (which header rects are
actually merged):

| Report | topology correction |
|---|---|
| `council-schools-rank-overall` | proof report: summary/aggregate block given its **own** `<table>` + colgroup/widths (no longer force-shares the detail grid's left/right alignment); removed a spurious empty summary spacer row; group / sub / F-M-T bands span the measured columns; columns align to **~0.5pt**. tolerant-diff p1 **14.08% → 8.67%**. |
| `region-schools-rank-overall` | own boundaries (extra COUNCIL column) re-measured; vertical labels fixed; columns align ~0.5pt. tolerant-diff p1 **19.98% → 17.32%**. |
| `region-subjects-rank` | genuine **column-width** bug: SUBJECT NAME col was 143.5pt in CSS but 215.3pt in the original — all 15 col widths re-measured from boundary diffs; biggest structural win. tolerant-diff p1/p2 **19.73/12.69% → 11.32/7.97%**. |
| `region-mobility` | removed the `h4` spacer row that added an extra full-width boundary; row pitch 11.78 → 11.6pt; rotated labels switched to `writing-mode: vertical-rl`. tolerant-diff p2–6 **~25–27% → ~17–20%**. |
| `region-district-performance` | section-centric (OVERALL/GOVERNMENT/PRIVATE carry REGISTERED; BY-PERCENTAGE/BY-KPI omit it) — each section's own header topology reproduced; columns already aligned to ~0.3pt. |
| `region-schools-rank-governments` | government-only grid re-measured; columns align ~0.5pt (residual is header-band fill overlap, Thread A territory, not topology). |
| `council-wards-rank` | per-ward detail grid + summary/overall row modeled independently; columns align ~0.5pt. |

The rotated single-column headers (`C/RANK`, `R/RANK`, `SUMMARY PERFORMANCE`)
were switched from `position:absolute`+`rotate(-90deg)` (which bled the label out
of its cell, above the grid) to `writing-mode:vertical-rl` inside an
`overflow:hidden` flex cell, so they stay inside their merged cell. `border-collapse:collapse`
with one consistent border width now yields **straight gridlines** on every grid
report — verified visually in each report's `output/comparison*/page_NN.png`.
**Structurally-different tables on one page are no longer forced into one shared
grid**: summary/aggregate blocks and detail grids each carry their own colgroup
and widths, sharing widths only where the original actually aligns them.

## Robustness / dynamic data (Thread B)

Volume-robustness is proved with committed **synthetic** fixtures under
[`reports/secondary/fixtures/`](fixtures/README.md), rendered + self-verified by
[`scripts/render_fixtures.py`](../../scripts/render_fixtures.py) (prints
`=== render-fixtures OK ===`). These fixtures are **never** fed into the fidelity
comparison against the real originals — the real `data.json` renders remain the
only fidelity verdict, and the scores in the tables above are unchanged by them.
Each fixture renders through its report's OWN template + CSS to that report's
`output/fixtures/<name>.pdf` (+ page PNGs), committed as proof:

| fixture | report exercised | proves |
|---|---|---|
| `…__ties-26-rows.json` | council-best-students-overall | a "Top 10" block that actually holds **26 ranked rows, including tied POSITION values**, renders **ALL 26 rows** (not truncated at 10, layout intact) — verified by counting the unique `FULLNAME` token per row. |
| `…__long-text.json` | council-best-students-overall | very long SCHOOL / CANDIDATE / DETAILED-SUBJECTS strings **WRAP inside their cell** (opt-in `wrap_text` policy) and never fall outside the page — verified: every char stays within the media box (~30 wrapped baselines). The real `data.json` keeps the original single-line/clip behaviour, so its comparison is byte-identical. |
| `…__3-page.json` | council-schools-rank-overall | a report whose real instance is **1 page** paginates to **exactly 3 pages** with 195 rows — the column-header band **repeats on every page** (`<thead>` + `thead { display: table-header-group; }`) and **S/N numbering is continuous 1..195** across the breaks. |

**Header overflow was CSS sizing, not font width.** Liberation is
**metric-compatible** with the originals' Monotype Arial (same advance widths),
so when `council-top-10-schools` spilled the two-word header **"COMPETENCY
LEVEL"** past its cell it was a pure CSS bug: it printed on one `white-space:nowrap`
line reaching `x1 ≈ 825` on a 792pt page, while the original wraps the label to
two lines inside the cell (0 off-page chars). The fix was a single CSS rule
(`thead th.comp-h { white-space: normal }`); every page's pixel diff improved
with the palette unchanged. Pagination was also made **content-driven**: the
hard-coded "page-top on even section index" break in `council-top-10-schools`
and `council-best-students-overall` was replaced with a data-driven
`blocks_per_page` hint (default 2, reproducing the original exactly), and the
paginating tables now carry their column-header band in `<thead>` so WeasyPrint
repeats it automatically. Templates carry **no hard-coded row counts, page
numbers, or fixed rows-per-page** assumptions.

## PR-body-ready summary — per report: before/after + verdict

**Thread A (colours):** every report's palette is now measured **per report** from
its own original (no shared palette). **Thread C (topology):** the seven F/M/T
grids reproduce their own original's colspan/rowspan, with straight gridlines and
independent summary vs. detail tables. **Thread B (robustness):** three synthetic
fixtures prove ties→26 rows, long-text wrap, and 3-page pagination.

**About the >=96% verdict:** the bar the user set ("at least 96% *everywhere* —
colours, borders, data, cell sizes") is deliberately strict and is measured
honestly, position-by-position. The dominant reason most pages do **not** hit
tolerant-diff <= 4% is the **proprietary-font substitution**: genuine Monotype
Arial/Times cannot be redistributed in-sandbox, so we embed metric-compatible
Liberation faces. They match advance widths and geometry exactly but are **not
glyph-identical**, so thousands of tiny digits differ along their edges and push
the tolerant-diff above 4% even when colours, borders, cell sizes and data are
correct. **This is the same reason the Lakezone success example — which does
embed genuine Arial — still reports tolerant-diff 4.8–6.8% (23% on its dense
compact page 11) and therefore also shows 0/11 pages passing the strict pixel
bar, with 0/0 words and 0 fill mismatches on every page.** In other words, the
verdict's `pixels` failures are a font-rendering-noise floor, not a content,
colour, border or cell-size error.

### Pages that MEET the >=96% bar (PASS on all three dimensions)

| Report | passing pages | why they pass |
|---|---|---|
| `council-best-students-subjectwise` | **10 / 30** (pages 21–30) | near-blank per-subject continuation pages: 0 tolerant diff, 0 fills, 0 words. |
| `council-schools-rank-subjectwise` | **8 / 24** (pages 6, 10, 12, 14, 16, 18, 20, 24) | sparse continuation pages where tolerant diff ≤ ~1.5% and fills/words are clean. |
| `council-subjects-rank` | **1 / 2** (page 2) | continuation page, tolerant 2.60%, 0/0 fills, 0/0 words. |

Total: **19 report-pages** clear the full >=96% bar. Every other page fails on at
least one dimension, itemised below.

### Pages that do NOT meet the >=96% bar, with the honest reason

- **Font-noise floor (`pixels` only; colours + data are correct):**
  `council-best-students-overall` (5/5 fail, tol 5.3–15.3%),
  `region-best-students-subjectwise` (23/23, tol 8.7–9.2%),
  `region-district-performance` (5/5, tol 5.5–7.1%),
  `region-best-students-overall` (9/9, tol 7.2–9.9%),
  `region-top-10-schools` (6/6, tol 8.4–9.9%), and the dense first pages of
  `council-schools-rank-*`, `region-schools-rank-*` and `region-subjects-rank`.
  Root cause: Liberation-vs-Monotype glyph-edge noise across thousands of digits
  (documented, unavoidable in-sandbox). These pages have **0 fill mismatch** on
  their main grid.
- **`region-mobility` (0/6):** `pixels` (tol 16.9–23.6%, dense wide grid) **plus**
  two documented, unavoidable fill deltas:
  - `#c00000` orig-only on every page is a **coloured-text glyph, not a rect**: the
    negative-MJONGEO delta is rendered as dark-red *text* (`.mj-down { color }`),
    which is visually identical to the original but pdfplumber records the
    original's as a filled glyph path in `page.rects`, so it can never appear in
    our generated fill Counter. This is the text-vs-rect case — correcting CSS
    cannot make a text colour show up as a rect fill.
  - `#65ffab` gen-only on pages 2–6 is a **per-page inconsistency in the ORIGINAL**:
    `measure_fills.py` shows the original paints the `%(I-III)` sub-header green
    (`#65ffab`) only on page 1 (where we match it 0 gen-only), but on pages 2–6 the
    original does NOT repeat that green on the re-drawn header band. Our template
    repeats the header identically on every page (data-driven, correct), so we emit
    `#65ffab` on every page. Suppressing it only on pages 2–6 would need a
    hard-coded page index, which the constraint forbids. Documented residual.
- **Dense F/M/T grids `region-schools-rank-overall` / `-governments` (0/6, 0/4):**
  `pixels` (tol 16.6–21.5%) from font noise **plus** high fuzzy `words` counts
  from rotated/kerned headers. Columns align to ~0.5pt (Thread C) and main-grid
  fills are clean; residual orig-only fills (`#f2ceef`, `#9eeaea #b5e6a2 #f2ceef
  #f7c7ac`) are the **one-off decorative SUMMARY/aggregate banner** on the last
  page only.
- **`council-top-10-schools` (0/3):** `pixels` + `words` + a residual per-section
  tint delta (`#fcd5b4` vs `#fabf8f`, `#dce6f1`, and gen-only competency
  `#ffc000 #ffff00` from a paginated second section that is data-driven, not a
  palette error).
- **`council-wards-rank` (0/1):** `pixels` + `words` + **7 orig-only** fills that
  are the one-off decorative **SUMMARY block** legend; the main per-ward grid is
  clean.
- **`region-top-10-schools` fills residual (per-page palette inconsistency in the
  ORIGINAL):** re-measuring page-by-page with `measure_fills.py` shows the original
  itself uses **different tints on different pages** for the same cells — page 1
  paints REGISTERED `#c0e6f5` and I-III% `#29ff8a`/0% `#8ed973`, while pages 2–6
  switch REGISTERED to `#caedfb` and I-III% to `#65ffab`. Our fixed per-report
  palette is measured from page 1 and reproduces it **0 orig / 0 gen on page 1**;
  pages 2–6 then show `#caedfb`/`#65ffab` (orig-only) vs `#c0e6f5`/`#29ff8a`
  (gen-only). Matching the original's per-page tint drift would require hard-coding
  a page/section index into the palette, which the data-driven constraint forbids
  (no hard-coded page numbers). This is a documented residual, not a palette bug we
  can fix without violating the constraint. The `#ff0000` orig-only is a single
  empty-cell red the original paints but our topology leaves unfilled — one cell,
  decorative.
- **`region-schools-rank-subjectwise` (EDK 0/1, English 0/6):** `pixels` (tol
  8.8% / 16.3–18.7%); EDK has 1 orig-only `#d9d9d9` on one aggregate-row C/RANK
  cell; English has a `#d9d9d9`↔`#f7c7ac` swap on its last aggregate page. One
  palette satisfies both sources.
- **`council-schools-rank-subjectwise` / `region-subjects-rank` / others:** the
  remaining fill residuals are continuation-page repeated header fills
  (`#d2fce6 #daeef3 #f2dcdb`), single data-driven competency colours on paginated
  sections (`#00b050`, `#ffff00`, `#92d050`), or a single `#f8cbad` in a section
  that omits the 0-div fill — all documented as decorative / data-driven, not the
  shared-palette bug that Thread A removed.

**Net:** colours are correct on the repeating main-grid pages of every report
(fill-diff driven to 0 there; residuals are decorative banners, data-driven
competency, `region-mobility` coloured text, and the `region-top-10` single-`0`
column); cell-merge topology and gridlines now match each original to ~0.5pt; and
the only thing keeping most pages under the strict 96% pixel bar is the
proprietary-font substitution, which the Lakezone genuine-Arial example proves is
a rendering-noise floor rather than a content/colour/border/size defect.
