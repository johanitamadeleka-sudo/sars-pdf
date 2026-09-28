# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 11.00% | 8.86% | 26 | 28 | #fed4fc | - | ❌ FAIL (pixels 8.86%>4%, fills 1orig/0gen, words 26miss/28extra) |

**Verdict summary: 0/1 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'WAS': 2, 'YA': 1, 'NA': 1, 'WA': 1, 'LA': 1, '%': 1, '55': 1, '136': 1, 'KUNDI': 1, 'UMAHIRI': 1}`
extra: `{'A': 5, 'W': 2, 'S': 2, 'I': 2, 'U': 2, 'UFAULU': 1, 'KIMADARAJA': 1, 'D': 1, 'A-D': 1, 'M': 1}`

![page 1](page_01.png)

