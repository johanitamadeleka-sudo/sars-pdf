# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 30.87% | 8.75% | 209 | 64 | - | - | ❌ FAIL (pixels 8.75%>4%, words 209miss/64extra) |

**Verdict summary: 0/1 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'E': 8, '5': 8, 'O': 7, 'C': 7, '6': 7, '1': 7, 'I': 6, 'N': 6, 'A': 6, '2': 5}`
extra: `{'PERFORMANCE': 4, 'GPA': 3, 'NUMBER': 2, 'OF': 2, 'CANDIDATES': 2, 'REGISTERED': 2, 'SAT': 2, 'SCHOOLS': 1, 'DIVISION': 1, 'III': 1}`

![page 1](page_01.png)

