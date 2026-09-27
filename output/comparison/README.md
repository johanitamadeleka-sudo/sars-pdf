# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 9.70% | 4.81% | 0 | 0 | - | - | ❌ FAIL (pixels 4.81%>4%) |
| 2 | 10.95% | 6.66% | 0 | 0 | - | - | ❌ FAIL (pixels 6.66%>4%) |
| 3 | 9.91% | 5.33% | 0 | 0 | - | - | ❌ FAIL (pixels 5.33%>4%) |
| 4 | 10.76% | 6.65% | 0 | 0 | - | - | ❌ FAIL (pixels 6.65%>4%) |
| 5 | 10.83% | 6.78% | 0 | 0 | - | - | ❌ FAIL (pixels 6.78%>4%) |
| 6 | 10.53% | 6.05% | 0 | 0 | - | - | ❌ FAIL (pixels 6.05%>4%) |
| 7 | 10.62% | 6.06% | 0 | 0 | - | - | ❌ FAIL (pixels 6.06%>4%) |
| 8 | 10.66% | 6.08% | 0 | 0 | - | - | ❌ FAIL (pixels 6.08%>4%) |
| 9 | 10.57% | 6.07% | 0 | 0 | - | - | ❌ FAIL (pixels 6.07%>4%) |
| 10 | 9.86% | 5.23% | 0 | 0 | - | - | ❌ FAIL (pixels 5.23%>4%) |
| 11 | 28.22% | 23.18% | 0 | 0 | - | - | ❌ FAIL (pixels 23.18%>4%) |

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

