# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 3.89% | 0.26% | 0 | 0 | - | - | ✅ PASS |
| 2 | 0.59% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 3 | 2.94% | 0.17% | 0 | 0 | - | - | ✅ PASS |
| 4 | 0.69% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 5 | 3.23% | 0.17% | 0 | 0 | - | - | ✅ PASS |
| 6 | 0.51% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 7 | 3.62% | 0.18% | 0 | 0 | - | - | ✅ PASS |
| 8 | 0.81% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 9 | 3.33% | 0.19% | 0 | 0 | - | - | ✅ PASS |
| 10 | 0.62% | 0.07% | 0 | 0 | - | - | ✅ PASS |
| 11 | 3.13% | 0.19% | 0 | 0 | - | - | ✅ PASS |
| 12 | 0.57% | 0.08% | 0 | 0 | - | - | ✅ PASS |
| 13 | 3.29% | 0.19% | 0 | 0 | - | - | ✅ PASS |
| 14 | 0.54% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 15 | 3.31% | 0.22% | 0 | 0 | - | - | ✅ PASS |
| 16 | 0.58% | 0.08% | 0 | 0 | - | - | ✅ PASS |
| 17 | 3.40% | 0.23% | 0 | 0 | - | - | ✅ PASS |
| 18 | 0.53% | 0.05% | 0 | 0 | - | - | ✅ PASS |
| 19 | 3.74% | 0.21% | 0 | 0 | - | - | ✅ PASS |
| 20 | 0.44% | 0.04% | 0 | 0 | - | - | ✅ PASS |
| 21 | 3.32% | 0.15% | 0 | 0 | - | - | ✅ PASS |
| 22 | 8.21% | 0.22% | 11 | 0 | - | - | ❌ FAIL (words 11miss/0extra) |
| 23 | 4.68% | 0.25% | 0 | 0 | - | - | ✅ PASS |
| 24 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 23/24 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

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

## Page 12

![page 12](page_12.png)

## Page 13

![page 13](page_13.png)

## Page 14

![page 14](page_14.png)

## Page 15

![page 15](page_15.png)

## Page 16

![page 16](page_16.png)

## Page 17

![page 17](page_17.png)

## Page 18

![page 18](page_18.png)

## Page 19

![page 19](page_19.png)

## Page 20

![page 20](page_20.png)

## Page 21

![page 21](page_21.png)

## Page 22
missing: `{'A': 1, 'SCHOOL': 1, 'K': 1, 'N': 1, 'R': 1, 'S/N': 1, 'NAME': 1, 'GPA': 1, 'COMPENTENCY': 1, 'LEVEL': 1}`

![page 22](page_22.png)

## Page 23

![page 23](page_23.png)

## Page 24

![page 24](page_24.png)

