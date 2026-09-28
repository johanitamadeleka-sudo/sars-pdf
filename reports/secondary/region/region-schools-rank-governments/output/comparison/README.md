# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 2.81% | 0.26% | 2 | 2 | - | - | ❌ FAIL (words 2miss/2extra) |
| 2 | 3.23% | 0.39% | 0 | 0 | - | - | ✅ PASS |
| 3 | 3.17% | 0.39% | 0 | 0 | - | - | ✅ PASS |
| 4 | 2.98% | 0.38% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 3/4 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'KNAR/R': 1, 'KNAR/C': 1}`
extra: `{'KKNNAARR//CC': 1, 'KKNNAARR//RR': 1}`

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

