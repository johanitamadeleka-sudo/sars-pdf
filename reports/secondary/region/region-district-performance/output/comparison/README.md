# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 1.01% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 2 | 0.84% | 0.04% | 0 | 0 | - | - | ✅ PASS |
| 3 | 1.24% | 0.27% | 0 | 0 | - | - | ✅ PASS |
| 4 | 1.29% | 0.27% | 0 | 0 | - | - | ✅ PASS |
| 5 | 1.26% | 0.27% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 5/5 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5

![page 5](page_05.png)

