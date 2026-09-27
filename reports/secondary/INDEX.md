# Secondary reports — fidelity summary (verdict at a glance)

This is the visible **verdict** for every secondary report built so far. It
mirrors how [`output/comparison/README.md`](../../output/comparison/README.md)
reports the Lakezone success example: for each report it lists the source PDF,
the scope/level, the page count, and the latest pixel-diff / word-diff scores
from [`scripts/compare.py`](../../scripts/compare.py).

Regenerate everything (and refresh these numbers) with one command:

```bash
python scripts/build_all.py            # render + compare every report under reports/secondary/**
```

Each report keeps its own side-by-side images and per-page score table under
`reports/secondary/<level>/<report>/output/comparison*/README.md`.

## How to read the scores

- **Page count** matches the original **exactly** for every report.
- **pixel-diff** is `compare.py`'s pixel-difference percentage per page (range
  shown min–max across the report's pages). It is dominated by
  **font-substitution glyph-edge noise**: the originals embed genuine Monotype
  Arial/Times, which cannot be obtained or redistributed in-sandbox, so we
  render with metric-compatible Liberation faces registered under the real
  family names (see [`../../fonts/README.md`](../../fonts/README.md) and the
  [decisions note](../README.md#decisions--blockers)). Geometry and colours
  align — the diff overlay shows red only along glyph edges. Dense wide F/M/T
  grids therefore sit higher (thousands of tiny digits differ at the edges);
  sparse reports sit low.
- **word-diff** is `compare.py`'s **fuzzy tokeniser** total (missing + extra
  across all pages), NOT a true content diff. The residual counts are metric
  artifacts: vertical/rotated headers tokenised char-by-char (e.g. `C/RANK` →
  `K N A R /C`), compact continuation headers splitting group labels
  differently, and long COUNCIL/SCHOOL/DETAILED strings kerning into the next
  cell so tokens merge (e.g. `KAHANGARA GOVERNMENT` → `KAHANGAGROAVERNMENT`).
  The extracted `data.json` content is verified correct against the source.

## Council reports (`reports/secondary/council/`)

| Report | Source PDF | Scope / level | Pages | pixel-diff | word-diff (miss/extra)* |
|---|---|---|---|---|---|
| `council-schools-rank-subjectwise` | MWANZA CC SCHOOLS RANK SUBJECTWISE.pdf | council, per-subject school rank (COUNCILWISE, C/RANK) | 24 | 0.0–27.3% | 162 / 130 |
| `council-subjects-rank` | MWANZA CC SUBJECTS RANK.pdf | council, one row per subject | 2 | 4.1–18.9% | 4 / 1 |
| `council-schools-rank-overall` | MWANZA CC SCHOOLS RANK.pdf | council, division-performance grid (F/M/T) | 1 | 36.8% | 208 / 71 |
| `council-top-10-schools` | MWANZA CC 10 BEST SCHOOLS.pdf | council, top-10 sections (incl. districtwise/govt) | 3 | 19.3–21.8% | 46 / 26 |
| `council-best-students-overall` | MWANZA CC 10 BEST STUDENTS.pdf | council, top students + detailed subjects | 5 | 8.7–20.6% | 172 / 41 |
| `council-best-students-subjectwise` | MWANZA CC 10 BEST STUDENTS SUBJECTWISE.pdf | council, top-10 students per subject | 30 | 0.0–10.5% | 398 / 110 |
| `council-wards-rank` | MWANZA CC Wards Rank.pdf | council, per-ward performance (WARDWISE, RANK) | 1 | 18.2% | 31 / 7 |

## Region reports (`reports/secondary/region/`)

| Report | Source PDF | Scope / level | Pages | pixel-diff | word-diff (miss/extra)* |
|---|---|---|---|---|---|
| `region-schools-rank-subjectwise` (EDK) | Mwanza School Rank-EDK.pdf | region, per-subject school rank + COUNCIL col + C/RANK & R/RANK (REGIONWISE) | 1 | 16.8% | 1 / 0 |
| `region-schools-rank-subjectwise` (English) | Mwanza School Rank-English Language.pdf | region, per-subject school rank (same template, 2nd source) | 6 | 34.4–41.2% | 12 / 12 |
| `region-subjects-rank` | Mwanza Overall Subjects Performance.pdf | region, one row per subject (REGIONALWISE) | 2 | 17.8–27.9% | 4 / 2 |
| `region-schools-rank-overall` | Mwanza schools rank Overall.pdf | region, division grid + COUNCIL col | 6 | 15.9–44.8% | 61 / 205 |
| `region-schools-rank-governments` | Mwanza Schools Rank For Governments.pdf | region, division grid, government schools only | 4 | 35.9–45.0% | 107 / 171 |
| `region-top-10-schools` | Mwanza Top 10 Schools.pdf | region, top-10 overall + COUNCIL col | 6 | 10.0–11.4% | 14 / 28 |
| `region-best-students-overall` | Mwanza Best Students-Overall.pdf | region, top students + COUNCIL col + detailed subjects | 9 | 9.8–11.7% | 219 / 74 |
| `region-best-students-subjectwise` | Mwanza Best students-Subjectwise.pdf | region, top-10 students per subject + COUNCIL col | 23 | 10.8–11.3% | 156 / 71 |
| `region-district-performance` | Mwanza f2 District Performance.pdf | region only, per-council/district division grid | 5 | 9.1–9.6% | 1 / 27 |
| `region-mobility` | Mwanza f2 Mock Mobility 2026.pdf | region only, FTNA 2025 vs Mock 2026 (Swahili labels) | 6 | 35.1–39.3% | 152 / 102 |

\* word-diff is the fuzzy-tokeniser total (see [How to read the scores](#how-to-read-the-scores)); it over-counts visually identical rotated headers and cell-adjacency kern merges. Extracted content is verified correct.

**Duplicate note:** `Mwanza Schools Rank For Governments (1).pdf` is
**byte-identical** (md5 `abcc1c77b83d95a426e3ad2292c27e6e`) to
`Mwanza Schools Rank For Governments.pdf`, so only one report
(`region-schools-rank-governments`) is built for both.

`MWANZA CC` (council) and `Mwanza` (region) are the **test instance names of the
sampled PDFs**, not template names — every directory above is named by
**level + function** so the same template renders any future council/region data
of the same shape.
