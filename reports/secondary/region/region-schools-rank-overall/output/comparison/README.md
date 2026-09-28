# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 2.63% | 0.22% | 10 | 9 | - | - | ❌ FAIL (words 10miss/9extra) |
| 2 | 2.39% | 0.27% | 2 | 2 | - | - | ❌ FAIL (words 2miss/2extra) |
| 3 | 2.93% | 0.27% | 0 | 0 | - | - | ✅ PASS |
| 4 | 2.96% | 0.28% | 0 | 0 | - | - | ✅ PASS |
| 5 | 2.96% | 0.26% | 0 | 0 | - | - | ✅ PASS |
| 6 | 1.26% | 0.17% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 4/6 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'NYANTAKUPBRWIVAA': 2, '3.53535': 1, 'Grade': 1, 'TBEOYS': 1, 'TGEIRLS': 1, 'ANDP': 1, 'BROIVYASTE': 1, 'KNAR/C': 1, 'KNAR/R': 1}`
extra: `{'NYANTAKUBWA': 2, 'BOYSPRIVATE': 2, 'AND': 1, '3.53535Grade': 1, 'GIRLSPRIVATE': 1, 'KKNNAARR//CC': 1, 'KKNNAARR//RR': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'CHRISTIANP': 1, 'RSIEVMATINEARY': 1}`
extra: `{'CHRISTIAN': 1, 'SEMINARYPRIVATE': 1}`

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5

![page 5](page_05.png)

## Page 6

![page 6](page_06.png)

