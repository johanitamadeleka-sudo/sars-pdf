# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 22.68% | 8.26% | 5 | 1 | - | - | ❌ FAIL (pixels 8.26%>4%, words 5miss/1extra) |
| 2 | 3.76% | 1.33% | 0 | 0 | #d2fce6 #daeef3 #f2dcdb | - | ❌ FAIL (fills 3orig/0gen) |
| 3 | 24.71% | 16.62% | 5 | 21 | - | - | ❌ FAIL (pixels 16.62%>4%, words 5miss/21extra) |
| 4 | 4.35% | 2.32% | 17 | 0 | - | - | ❌ FAIL (words 17miss/0extra) |
| 5 | 20.90% | 9.17% | 5 | 4 | - | - | ❌ FAIL (pixels 9.17%>4%, words 5miss/4extra) |
| 6 | 3.63% | 1.43% | 0 | 0 | - | - | ✅ PASS |
| 7 | 25.34% | 16.38% | 5 | 21 | - | - | ❌ FAIL (pixels 16.38%>4%, words 5miss/21extra) |
| 8 | 4.31% | 1.85% | 17 | 0 | - | - | ❌ FAIL (words 17miss/0extra) |
| 9 | 24.45% | 14.82% | 5 | 4 | - | - | ❌ FAIL (pixels 14.82%>4%, words 5miss/4extra) |
| 10 | 3.85% | 1.38% | 0 | 0 | - | - | ✅ PASS |
| 11 | 23.66% | 14.85% | 5 | 4 | - | - | ❌ FAIL (pixels 14.85%>4%, words 5miss/4extra) |
| 12 | 3.49% | 1.38% | 0 | 0 | - | - | ✅ PASS |
| 13 | 24.30% | 14.69% | 5 | 4 | - | - | ❌ FAIL (pixels 14.69%>4%, words 5miss/4extra) |
| 14 | 3.59% | 1.37% | 0 | 0 | - | - | ✅ PASS |
| 15 | 23.83% | 15.22% | 5 | 4 | - | - | ❌ FAIL (pixels 15.22%>4%, words 5miss/4extra) |
| 16 | 3.58% | 1.45% | 0 | 0 | - | - | ✅ PASS |
| 17 | 23.91% | 15.26% | 5 | 4 | - | - | ❌ FAIL (pixels 15.26%>4%, words 5miss/4extra) |
| 18 | 3.70% | 1.51% | 0 | 0 | - | - | ✅ PASS |
| 19 | 23.42% | 15.60% | 5 | 4 | - | - | ❌ FAIL (pixels 15.60%>4%, words 5miss/4extra) |
| 20 | 3.45% | 1.41% | 0 | 0 | - | - | ✅ PASS |
| 21 | 23.99% | 18.32% | 42 | 12 | #00b050 | - | ❌ FAIL (pixels 18.32%>4%, fills 1orig/0gen, words 42miss/12extra) |
| 22 | 26.95% | 21.56% | 21 | 36 | - | - | ❌ FAIL (pixels 21.56%>4%, words 21miss/36extra) |
| 23 | 21.51% | 17.80% | 15 | 11 | - | - | ❌ FAIL (pixels 17.80%>4%, words 15miss/11extra) |
| 24 | 0.00% | 0.00% | 0 | 0 | - | - | ✅ PASS |

**Verdict summary: 8/24 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'C/RANK': 1}`

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

## Page 3
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1, 'F': 1, '15': 1, '1': 1, '0': 1, 'Grade': 1, '14': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'053': 1, 'SHAMALIWA': 1, '0': 1, '1': 1, '14': 1, '89': 1, '482': 1, '586': 1, '15': 1, '2.56': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 5](page_05.png)

## Page 6

![page 6](page_06.png)

## Page 7
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1, 'C': 1, '2': 1, 'Grade': 1, '43': 1, '(Good)': 1, '23': 1}`

![page 7](page_07.png)

## Page 8
missing: `{'053': 1, 'SHAMALIWA': 1, '2': 1, '23': 1, '328': 1, '192': 1, '43': 1, '588': 1, '353': 1, '60.03': 1}`

![page 8](page_08.png)

## Page 9
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 9](page_09.png)

## Page 10

![page 10](page_10.png)

## Page 11
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 11](page_11.png)

## Page 12

![page 12](page_12.png)

## Page 13
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 13](page_13.png)

## Page 14

![page 14](page_14.png)

## Page 15
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 15](page_15.png)

## Page 16

![page 16](page_16.png)

## Page 17
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 17](page_17.png)

## Page 18

![page 18](page_18.png)

## Page 19
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1, '/C': 1}`
extra: `{'SCHOOLS': 1, 'RANK': 1, 'SUBJECTWISE': 1, 'C/RANK': 1}`

![page 19](page_19.png)

## Page 20

![page 20](page_20.png)

## Page 21
missing: `{'A': 5, '1': 5, '0': 4, 'K': 3, 'N': 3, 'R': 3, '/C': 3, '100': 2, 'B': 1, 'C': 1}`
extra: `{'SCHOOLS': 3, 'RANK': 3, 'SUBJECTWISE': 3, 'C/RANK': 3}`

![page 21](page_21.png)

## Page 22
missing: `{'K': 3, 'N': 3, 'R': 3, '/C': 3, 'A': 1, 'PERFORMANCE': 1, 'SCHOOL': 1, 'GRADING': 1, 'S/N': 1, 'NAME': 1}`
extra: `{'1': 5, '0': 4, 'SCHOOLS': 3, 'RANK': 3, 'SUBJECTWISE': 3, '100': 2, 'C/RANK': 2, 'B': 1, 'C': 1, 'D': 1}`

![page 22](page_22.png)

## Page 23
missing: `{'K': 3, 'N': 3, 'A': 3, 'R': 3, '/C': 3}`
extra: `{'C/RANK': 3, 'SCHOOLS': 2, 'RANK': 2, 'SUBJECTWISE': 2, 'GRADING': 1, 'PERFORMANCE': 1}`

![page 23](page_23.png)

## Page 24

![page 24](page_24.png)

