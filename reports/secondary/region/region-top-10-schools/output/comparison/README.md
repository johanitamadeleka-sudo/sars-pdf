# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 10.84% | 9.11% | 1 | 4 | #8ed973 #ff0000 | - | ❌ FAIL (pixels 9.11%>4%, fills 2orig/0gen, words 1miss/4extra) |
| 2 | 9.99% | 8.41% | 1 | 4 | #8ed973 #caedfb #ff0000 | #29ff8a #c0e6f5 | ❌ FAIL (pixels 8.41%>4%, fills 3orig/2gen, words 1miss/4extra) |
| 3 | 10.91% | 9.88% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #29ff8a #c0e6f5 | ❌ FAIL (pixels 9.88%>4%, fills 3orig/2gen, words 1miss/4extra) |
| 4 | 10.66% | 9.61% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #65ffab #c0e6f5 | ❌ FAIL (pixels 9.61%>4%, fills 3orig/2gen, words 1miss/4extra) |
| 5 | 10.75% | 9.64% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #29ff8a #c0e6f5 | ❌ FAIL (pixels 9.64%>4%, fills 3orig/2gen, words 1miss/4extra) |
| 6 | 9.54% | 8.37% | 1 | 4 | #8ed973 #caedfb #ff0000 | #65ffab #c0e6f5 | ❌ FAIL (pixels 8.37%>4%, fills 3orig/2gen, words 1miss/4extra) |

**Verdict summary: 0/6 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 5](page_05.png)

## Page 6
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 6](page_06.png)

