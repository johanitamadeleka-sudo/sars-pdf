# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 4.83% | 0.27% | 0 | 0 | - | - | ✅ PASS |
| 2 | 8.24% | 0.40% | 0 | 0 | - | - | ✅ PASS |
| 3 | 7.85% | 0.37% | 0 | 0 | - | - | ✅ PASS |
| 4 | 8.14% | 0.36% | 0 | 0 | - | - | ✅ PASS |
| 5 | 7.44% | 0.35% | 0 | 0 | - | - | ✅ PASS |
| 6 | 7.85% | 0.35% | 0 | 0 | - | - | ✅ PASS |
| 7 | 1.81% | 0.19% | 0 | 0 | - | - | ✅ PASS |
| 8 | 4.29% | 0.36% | 20 | 4 | - | - | ❌ FAIL (words 20miss/4extra) |

**Verdict summary: 7/8 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

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
missing: `{'K': 4, 'N': 4, 'A': 4, 'R': 4, '/S': 1, '/C': 1, '/R': 1, '/Z': 1}`
extra: `{'KNAR/S': 1, 'KNAR/C': 1, 'KNAR/R': 1, 'KNAR/Z': 1}`

![page 8](page_08.png)

