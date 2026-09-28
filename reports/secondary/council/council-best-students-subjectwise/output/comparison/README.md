# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 10.49% | 6.39% | 19 | 4 | - | - | ❌ FAIL (pixels 6.39%>4%, words 19miss/4extra) |
| 2 | 9.16% | 7.11% | 19 | 4 | - | - | ❌ FAIL (pixels 7.11%>4%, words 19miss/4extra) |
| 3 | 9.14% | 7.07% | 19 | 4 | - | - | ❌ FAIL (pixels 7.07%>4%, words 19miss/4extra) |
| 4 | 9.06% | 7.04% | 19 | 4 | - | - | ❌ FAIL (pixels 7.04%>4%, words 19miss/4extra) |
| 5 | 10.30% | 8.76% | 19 | 4 | - | - | ❌ FAIL (pixels 8.76%>4%, words 19miss/4extra) |
| 6 | 9.27% | 7.11% | 22 | 7 | - | - | ❌ FAIL (pixels 7.11%>4%, words 22miss/7extra) |
| 7 | 10.02% | 8.30% | 21 | 8 | - | - | ❌ FAIL (pixels 8.30%>4%, words 21miss/8extra) |
| 8 | 9.69% | 7.51% | 19 | 4 | - | - | ❌ FAIL (pixels 7.51%>4%, words 19miss/4extra) |
| 9 | 10.12% | 8.43% | 19 | 4 | - | - | ❌ FAIL (pixels 8.43%>4%, words 19miss/4extra) |
| 10 | 9.69% | 7.97% | 20 | 6 | - | - | ❌ FAIL (pixels 7.97%>4%, words 20miss/6extra) |
| 11 | 9.53% | 7.41% | 21 | 5 | - | - | ❌ FAIL (pixels 7.41%>4%, words 21miss/5extra) |
| 12 | 9.40% | 7.27% | 19 | 4 | - | - | ❌ FAIL (pixels 7.27%>4%, words 19miss/4extra) |
| 13 | 9.27% | 7.14% | 19 | 4 | - | - | ❌ FAIL (pixels 7.14%>4%, words 19miss/4extra) |
| 14 | 10.03% | 7.86% | 29 | 24 | - | - | ❌ FAIL (pixels 7.86%>4%, words 29miss/24extra) |
| 15 | 9.19% | 7.09% | 19 | 4 | - | - | ❌ FAIL (pixels 7.09%>4%, words 19miss/4extra) |
| 16 | 9.19% | 7.19% | 19 | 4 | - | - | ❌ FAIL (pixels 7.19%>4%, words 19miss/4extra) |
| 17 | 10.22% | 8.37% | 19 | 4 | - | - | ❌ FAIL (pixels 8.37%>4%, words 19miss/4extra) |
| 18 | 8.75% | 6.78% | 19 | 4 | - | - | ❌ FAIL (pixels 6.78%>4%, words 19miss/4extra) |
| 19 | 8.97% | 6.89% | 19 | 4 | - | - | ❌ FAIL (pixels 6.89%>4%, words 19miss/4extra) |
| 20 | 8.87% | 6.87% | 19 | 4 | - | - | ❌ FAIL (pixels 6.87%>4%, words 19miss/4extra) |
| 21 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 22 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 23 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 24 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 25 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 26 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 27 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 28 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 29 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |
| 30 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 10/30 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 5](page_05.png)

## Page 6
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1, 'PRIVATE': 1, 'ARMYPRIVATE': 1, 'ISLAMIC': 1}`

![page 6](page_06.png)

## Page 7
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'ISLAMICPRIVATE': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1}`
extra: `{'PRIVATE': 2, 'ISLAMIC': 2, 'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 7](page_07.png)

## Page 8
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 8](page_08.png)

## Page 9
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 9](page_09.png)

## Page 10
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1, 'MABULA': 1, 'GOVERNMENT': 1}`

![page 10](page_10.png)

## Page 11
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1, 'ARMYPRIVATE': 1}`

![page 11](page_11.png)

## Page 12
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 12](page_12.png)

## Page 13
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 13](page_13.png)

## Page 14
missing: `{'ISLAMICPRIVATE': 10, 'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1}`
extra: `{'ISLAMIC': 10, 'PRIVATE': 10, 'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 14](page_14.png)

## Page 15
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 15](page_15.png)

## Page 16
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 16](page_16.png)

## Page 17
missing: `{'O': 2, 'S': 2, 'E': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 17](page_17.png)

## Page 18
missing: `{'S': 2, 'E': 2, 'O': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 18](page_18.png)

## Page 19
missing: `{'S': 2, 'E': 2, 'O': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 19](page_19.png)

## Page 20
missing: `{'S': 2, 'E': 2, 'O': 2, 'R': 2, 'A': 2, 'N': 1, 'K': 1, 'D': 1, 'IT': 1, 'X': 1}`
extra: `{'XES': 1, 'SKRAM': 1, 'EDARG': 1, 'NOITISOP': 1}`

![page 20](page_20.png)

## Page 21

![page 21](page_21.png)

## Page 22

![page 22](page_22.png)

## Page 23

![page 23](page_23.png)

## Page 24

![page 24](page_24.png)

## Page 25

![page 25](page_25.png)

## Page 26

![page 26](page_26.png)

## Page 27

![page 27](page_27.png)

## Page 28

![page 28](page_28.png)

## Page 29

![page 29](page_29.png)

## Page 30

![page 30](page_30.png)

