# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 20.59% | 14.65% | 36 | 8 | - | - | ❌ FAIL (pixels 14.65%>4%, words 36miss/8extra) |
| 2 | 19.52% | 14.13% | 40 | 10 | - | - | ❌ FAIL (pixels 14.13%>4%, words 40miss/10extra) |
| 3 | 18.95% | 13.36% | 42 | 11 | - | - | ❌ FAIL (pixels 13.36%>4%, words 42miss/11extra) |
| 4 | 20.03% | 15.31% | 36 | 8 | - | - | ❌ FAIL (pixels 15.31%>4%, words 36miss/8extra) |
| 5 | 8.66% | 5.32% | 18 | 4 | - | - | ❌ FAIL (pixels 5.32%>4%, words 18miss/4extra) |

**Verdict summary: 0/5 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'O': 6, 'G': 4, 'N': 4, 'IS': 4, 'X': 2, 'E': 2, 'S': 2, 'T': 2, 'A': 2, 'IV': 2}`
extra: `{'XES': 2, 'TGGA': 2, 'NOISIVID': 2, 'NOITISOP': 2}`

![page 1](page_01.png)

## Page 2
missing: `{'O': 6, 'G': 4, 'N': 4, 'IS': 4, 'X': 2, 'E': 2, 'S': 2, 'T': 2, 'A': 2, 'IV': 2}`
extra: `{'XES': 2, 'TGGA': 2, 'NOISIVID': 2, 'NOITISOP': 2, 'MABULVAICENT': 1, 'MABULSAAMWEL': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'O': 6, 'G': 4, 'N': 4, 'IS': 4, 'MABULA': 3, 'X': 2, 'E': 2, 'S': 2, 'T': 2, 'A': 2}`
extra: `{'XES': 2, 'TGGA': 2, 'NOISIVID': 2, 'NOITISOP': 2, 'MABULCALEMENSIA': 1, 'MABULVAICENT': 1, 'MABULSAAMWEL': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'O': 6, 'G': 4, 'N': 4, 'IS': 4, 'X': 2, 'E': 2, 'S': 2, 'T': 2, 'A': 2, 'IV': 2}`
extra: `{'XES': 2, 'TGGA': 2, 'NOISIVID': 2, 'NOITISOP': 2}`

![page 4](page_04.png)

## Page 5
missing: `{'O': 3, 'G': 2, 'N': 2, 'IS': 2, 'X': 1, 'E': 1, 'S': 1, 'T': 1, 'A': 1, 'IV': 1}`
extra: `{'XES': 1, 'TGGA': 1, 'NOISIVID': 1, 'NOITISOP': 1}`

![page 5](page_05.png)

