# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 30.92% | 18.18% | 7 | 8 | - | - | ❌ FAIL (pixels 18.18%>4%, words 7miss/8extra) |
| 2 | 32.82% | 18.68% | 2 | 3 | - | - | ❌ FAIL (pixels 18.68%>4%, words 2miss/3extra) |
| 3 | 33.31% | 18.65% | 0 | 0 | - | - | ❌ FAIL (pixels 18.65%>4%) |
| 4 | 33.18% | 18.66% | 0 | 0 | - | - | ❌ FAIL (pixels 18.66%>4%) |
| 5 | 32.37% | 18.72% | 0 | 0 | - | - | ❌ FAIL (pixels 18.72%>4%) |
| 6 | 26.60% | 16.29% | 3 | 1 | #d9d9d9 | #f7c7ac | ❌ FAIL (pixels 16.29%>4%, fills 1orig/1gen, words 3miss/1extra) |

**Verdict summary: 0/6 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'BOYS': 1, 'NYANTAKU2B6WA': 1, 'G2IR8LS': 1, 'NYANTAKU2BWA': 1, 'BO13YS': 1, 'AND1': 1, 'SUBJECT': 1}`
extra: `{'NYANTA': 2, 'A': 1, '1': 1, '2': 1, '26': 1, '13': 1, '28': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'CHRISTIAN0': 1, 'SEMINA0RY': 1}`
extra: `{'0': 2, 'CHRIST': 1}`

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5

![page 5](page_05.png)

## Page 6
missing: `{'859': 1, '2645': 1, '(Satisfactory)': 1}`
extra: `{'(Satis8f5a9ctory2)645': 1}`

![page 6](page_06.png)

