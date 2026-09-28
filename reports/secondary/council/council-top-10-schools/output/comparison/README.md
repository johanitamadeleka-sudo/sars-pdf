# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 19.95% | 14.83% | 14 | 6 | - | #ffc000 #ffff00 | ❌ FAIL (pixels 14.83%>4%, fills 0orig/2gen, words 14miss/6extra) |
| 2 | 17.97% | 12.35% | 14 | 6 | #fcd5b4 | #dce6f1 #fabf8f | ❌ FAIL (pixels 12.35%>4%, fills 1orig/2gen, words 14miss/6extra) |
| 3 | 18.05% | 13.57% | 14 | 6 | #fcd5b4 | #dce6f1 | ❌ FAIL (pixels 13.57%>4%, fills 1orig/1gen, words 14miss/6extra) |

**Verdict summary: 0/3 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'S/NO.': 2, 'SCHOOL': 2, 'K': 2, 'N': 2, 'A': 2, 'R': 2, '/C': 2}`
extra: `{'S/NO.SCHOOL': 2, 'KNAR/C': 2, '%': 2}`

![page 1](page_01.png)

## Page 2
missing: `{'S/NO.': 2, 'SCHOOL': 2, 'K': 2, 'N': 2, 'A': 2, 'R': 2, '/C': 2}`
extra: `{'S/NO.SCHOOL': 2, 'KNAR/C': 2, '%': 2}`

![page 2](page_02.png)

## Page 3
missing: `{'S/NO.': 2, 'SCHOOL': 2, 'K': 2, 'N': 2, 'A': 2, 'R': 2, '/C': 2}`
extra: `{'S/NO.SCHOOL': 2, 'KNAR/C': 2, '%': 2}`

![page 3](page_03.png)

