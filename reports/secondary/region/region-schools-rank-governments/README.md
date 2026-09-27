# region-schools-rank-governments

Region-level overall division grid for **government schools only** (`SCHOOL PERFORMANCE
FOR GOVERNMENT SCHOOLS ONLY`), rebuilt from `region_pdf/region_pdf/Mwanza Schools Rank
For Governments.pdf` (4 pages, landscape).

## Duplicate source note

The region source set ships two files for this report:

- `Mwanza Schools Rank For Governments.pdf`
- `Mwanza Schools Rank For Governments (1).pdf`

They are **byte-identical** (same MD5 `abcc1c77b83d95a426e3ad2292c27e6e`), so only one
report is built here. The `(1)` copy is an upload duplicate and is intentionally **not**
rebuilt separately.

```
$ md5sum "Mwanza Schools Rank For Governments.pdf" "Mwanza Schools Rank For Governments (1).pdf"
abcc1c77b83d95a426e3ad2292c27e6e  Mwanza Schools Rank For Governments.pdf
abcc1c77b83d95a426e3ad2292c27e6e  Mwanza Schools Rank For Governments (1).pdf
```

## Rebuild

```
python scripts/extract_region_schools_rank_governments.py
python scripts/render_and_compare.py reports/secondary/region/region-schools-rank-governments
```
