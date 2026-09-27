# reports/primary/ — PLACEHOLDER for future primary-level reports

This directory is **intentionally empty** right now. It is a documented
placeholder for the future **PRIMARY** school level. There is deliberately **no
data and no templates** here yet.

When primary-level work begins, it will **mirror the secondary structure**:

```
reports/primary/
  <level-plus-function>/          # e.g. primary-schools-rank-subjectwise
    template.html.j2
    style.css
    data.json
    reference/original.pdf
    output/
```

It follows the same conventions as the secondary level (see
[`../README.md`](../README.md)):

- name reports by **level + what-it-does** (here the level is `primary-`), never
  by location or proper noun;
- each report is **self-contained** (its own template, CSS, data, reference,
  output);
- register the real fonts (in [`../../fonts/`](../../fonts/)) with an OWN inline
  `@font-face` in each report's `style.css`, one family name each and **no
  fallback chains** (no shared stylesheet, nothing `@import`ed);
- store data as **display strings**;
- generation is **data-driven** and verified with `../../scripts/compare.py`.

No implementation is scheduled for primary in the current task; this file exists
so the intended layout is clear and the tree is ready.
