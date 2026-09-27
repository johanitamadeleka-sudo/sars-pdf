# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 3.70% | 0.17% | 202 | 64 | - | - | ❌ FAIL (words 202miss/64extra) |

**Verdict summary: 0/1 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'5': 8, 'E': 7, 'N': 7, 'O': 7, '6': 7, '1': 7, 'I': 6, 'C': 6, 'A': 6, 'S': 5}`
extra: `{'PERFORMANCE': 3, 'NUMBER': 2, 'OF': 2, 'CANDIDATES': 2, 'GPA': 2, 'REGISTERED': 2, 'SAT': 2, 'AND': 1, 'SCHOOLS': 1, 'DIVISION': 1}`

![page 1](page_01.png)

