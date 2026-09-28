# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 12.71% | 3.13% | 5 | 10 | - | - | ❌ FAIL (words 5miss/10extra) |
| 2 | 18.28% | 2.52% | 2 | 4 | - | - | ❌ FAIL (words 2miss/4extra) |
| 3 | 18.62% | 2.53% | 0 | 0 | - | - | ✅ PASS |
| 4 | 18.47% | 2.49% | 0 | 0 | - | - | ✅ PASS |
| 5 | 18.21% | 3.00% | 0 | 0 | - | - | ✅ PASS |
| 6 | 15.63% | 4.03% | 0 | 0 | - | #f7c7ac | ❌ FAIL (pixels 4.03%>4%, fills 0orig/1gen) |

**Verdict summary: 3/6 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'NYANTAKU2B6WA': 1, 'G2IR8LS': 1, 'NYANTAKU2BWA': 1, 'BO13YS': 1, 'AND1': 1}`
extra: `{'NYANTAKUBWA': 2, 'AND': 1, '1': 1, '2': 1, 'GIRLS': 1, '26': 1, 'BOYS': 1, '13': 1, '28': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'CHRISTIAN0': 1, 'SEMINA0RY': 1}`
extra: `{'0': 2, 'CHRISTIAN': 1, 'SEMINARY': 1}`

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5

![page 5](page_05.png)

## Page 6

![page 6](page_06.png)

