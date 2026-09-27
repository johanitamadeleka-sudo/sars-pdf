# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 9.96% | 4.81% | 0 | 0 | - | - | ❌ FAIL (pixels 4.81%>4%) |
| 2 | 11.25% | 6.69% | 0 | 0 | - | - | ❌ FAIL (pixels 6.69%>4%) |
| 3 | 10.17% | 5.26% | 0 | 0 | - | - | ❌ FAIL (pixels 5.26%>4%) |
| 4 | 10.98% | 6.62% | 0 | 0 | - | - | ❌ FAIL (pixels 6.62%>4%) |
| 5 | 11.05% | 6.74% | 2 | 1 | - | - | ❌ FAIL (pixels 6.74%>4%, words 2miss/1extra) |
| 6 | 10.72% | 5.94% | 0 | 0 | - | - | ❌ FAIL (pixels 5.94%>4%) |
| 7 | 10.81% | 5.93% | 0 | 0 | - | - | ❌ FAIL (pixels 5.93%>4%) |
| 8 | 10.83% | 5.94% | 0 | 0 | - | - | ❌ FAIL (pixels 5.94%>4%) |
| 9 | 10.79% | 5.98% | 0 | 0 | - | - | ❌ FAIL (pixels 5.98%>4%) |
| 10 | 10.07% | 5.10% | 0 | 0 | - | - | ❌ FAIL (pixels 5.10%>4%) |
| 11 | 28.95% | 23.61% | 0 | 0 | - | - | ❌ FAIL (pixels 23.61%>4%) |

**Verdict summary: 0/11 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5
missing: `{'1425': 1, '82.597': 1}`
extra: `{'142582.597': 1}`

![page 5](page_05.png)

## Page 6

![page 6](page_06.png)

## Page 7

![page 7](page_07.png)

## Page 8

![page 8](page_08.png)

## Page 9

![page 9](page_09.png)

## Page 10

![page 10](page_10.png)

## Page 11

![page 11](page_11.png)

