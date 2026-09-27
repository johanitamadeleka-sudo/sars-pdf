# council-schools-rank-subjectwise

Secondary level, **council** scope, **schools rank subjectwise** function. Per-subject
school ranking: one table per subject, ordered by GPA, with a `C/RANK` (councilwise rank)
column. Named by LEVEL + FUNCTION only, never by a council/region proper noun, so any
council's data of this shape renders through the same template. (The bundled data is the
`MWANZA CC` test instance; `MWANZA CC` / `MWANZA` are data values, not template names.)

## Self-contained

Everything this report needs lives in this folder; nothing is shared except the physical
font files under repo `fonts/`:

| file | purpose |
|---|---|
| `template.html.j2` | this report's own Jinja2 template |
| `style.css` | this report's own stylesheet, incl. inline `@font-face` (one family name each, **no fallback list**) |
| `data.json` | display-string data model (numbers kept as exact strings) |
| `reference/original.pdf` | the source PDF to match |
| `output/` | generated `report.pdf`, `report.html`, `pages/`, `comparison/` |

Only the **competency-level** cell background is data-driven (via `sars_pdf/grading.py`,
GPA -> A-F band -> colour). Every other fill is a fixed `:root` colour **measured from THIS
report's own original** — the non-competency fills are a per-report palette, not one shared
across the report family (different originals use different hex values).

## Columns

`S/N | SCHOOL NAME | A B C D F | TOTAL | A-C %A-C A-D %A-D | GPA | COMPETENCY LEVEL | C/RANK`
(no REGION / COUNCIL / CENTRE / AV / GRD columns).

## Data model

```
document: { ministry[], exam_name, report_title, scope, rows_per_page, trailing_blank_page }
tables:   [ { subject, scope, rows[ {sn,school_name,a,b,c,d,f,total,a_c,pct_a_c,a_d,pct_a_d,gpa,competency,rank} ],
              overall{...}, overall_label } ]
```

`data.json` is produced by `scripts/extract_council_subjectwise.py` straight from the source
PDF (pdfplumber/pymupdf) — values are never hand-typed. One table per subject; rows flow
across page breaks. `rows_per_page` marks big subjects (their own 2-page span); small
subjects stack several per page, matching the original pagination.

## Render + verify

```
python scripts/render_and_compare.py reports/secondary/council/council-schools-rank-subjectwise
```

Verdict: 24 pages (same as original), per-page word-diff at/near zero, competency colours
and geometry matching. Residual pixel-diff on data-heavy pages is font-substitution noise
(Liberation Sans standing in for Arial; see `fonts/README.md`).
