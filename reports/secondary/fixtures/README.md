# Synthetic volume-robustness fixtures (FEAT-003, Thread B)

These are **synthetic, oversized** data variants used to prove that the report
templates are data-driven for *volume* (no hard-coded 10-row, single-page, or
fixed-rows-per-page assumptions). They are **never** fed into the fidelity
comparison against the real originals: the real `data.json` render + compare in
`scripts/build_all.py` remains the only fidelity verdict, and those scores are
unchanged by this work.

Generate + render + self-verify all fixtures with:

```
python scripts/render_fixtures.py      # prints "=== render-fixtures OK ==="
```

Each fixture is derived from a report's real `data.json` (so it exercises that
report's OWN `template.html.j2` + `style.css`, inline `@font-face`, no shared
stylesheet) and renders to that report's own `output/fixtures/<name>.pdf` plus a
`<name>-pages/` folder of page PNGs, committed as proof artifacts.

| fixture JSON | report exercised | proves |
|---|---|---|
| `council-best-students-overall__ties-26-rows.json` | council-best-students-overall | a "Top 10" block that actually holds **26 ranked rows including tied POSITION values** renders ALL 26 rows (verified by counting the unique `FULLNAME` token per row) - not truncated at 10, layout intact. |
| `council-best-students-overall__long-text.json` | council-best-students-overall | very long SCHOOL / CANDIDATE / DETAILED-SUBJECTS strings **WRAP inside their fixed cell** (opt-in `wrap_text` policy) and never fall outside the page (verified: every char stays within the media box; the detail text spans ~30 wrapped baselines). |
| `council-schools-rank-overall__3-page.json` | council-schools-rank-overall | a report whose real instance fits on **ONE** page paginates to **exactly 3 pages** when given 195 rows, with the column-header band repeated on **every** page (`<thead>` + `thead { display: table-header-group; }`) and **continuous S/N numbering 1..195** across the page breaks. |

## Header overflow: it was CSS sizing, not font width (documented per FEAT-003)

The secondary reports embed **OFF Liberation** faces, which are **metric-compatible**
with the originals' Monotype Arial / Arial Bold (same advance widths). So when a
header spilled past its cell it was a **CSS-sizing** bug, not a font-width bug.

Concretely, `council-top-10-schools` printed the two-word header **"COMPETENCY
LEVEL"** on a single `white-space: nowrap` line, which ran ~33 pt past the right
page edge (measured with pdfplumber: header chars reaching `x1 ≈ 825` on a 792 pt
page; the **original PDF has 0 off-page chars** and wraps that label to two lines
inside the cell). The fix was purely CSS - a `thead th.comp-h { white-space: normal }`
rule so the label wraps within its existing column width exactly like the original.
Result: header off-page chars dropped and every page's pixel diff **improved**
(p1 19.99%->19.72%, p2 19.06%->18.12%, p3 18.39%->18.25%) with the fill palette
**unchanged**. No font substitution or width hacking was involved.
