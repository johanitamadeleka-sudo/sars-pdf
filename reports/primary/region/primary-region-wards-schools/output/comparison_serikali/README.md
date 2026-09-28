# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 38.54% | 26.24% | 55 | 27 | #a4e9f0 #a9d08e #c65911 #c6e0b4 #d6dce4 #d9e1f2 #dbf3f9 #ddebf7 #e2efda #ededed #f4b084 #f8cbad #fce4d6 #ffe699 #fff2cc #ffffcc | - | ❌ FAIL (pixels 26.24%>4%, fills 16orig/0gen, words 55miss/27extra) |
| 2 | 41.61% | 28.42% | 69 | 68 | #a4e9f0 #a9d08e #c65911 #c6e0b4 #d6dce4 #d9e1f2 #ddebf7 #e2efda #ededed #f4b084 #f8cbad #fce4d6 #ffe699 #fff2cc #ffffcc | - | ❌ FAIL (pixels 28.42%>4%, fills 15orig/0gen, words 69miss/68extra) |
| 3 | 41.21% | 27.84% | 171 | 119 | #92d050 #a4e9f0 #a9d08e #c65911 #c6e0b4 #d6dce4 #d9e1f2 #ddebf7 #e2efda #ededed #f4b084 #f8cbad #fce4d6 #ffe699 #fff2cc #ffffcc | - | ❌ FAIL (pixels 27.84%>4%, fills 16orig/0gen, words 171miss/119extra) |
| 4 | 6.92% | 5.82% | 61 | 68 | #92d050 #a4e9f0 #a9d08e #c65911 #c6e0b4 #ccffff #d6dce4 #d9e1f2 #ddebf7 #e2efda #ededed #f2f2f2 #f4b084 #f8cbad #fce4d6 #ffe699 #fff2cc #ffffcc | - | ❌ FAIL (pixels 5.82%>4%, fills 18orig/0gen, words 61miss/68extra) |

**Verdict summary: 0/4 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'0': 5, 'WAV': 3, 'WAS': 3, 'JML': 2, '5': 2, '1': 2, '2': 2, '109': 2, '159': 2, '58': 2}`
extra: `{'A': 6, 'S': 2, 'I': 2, 'W': 2, 'ID': 1, 'H': 1, 'D': 1, 'U': 1, 'L': 1, 'Y': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'WAV': 3, 'WAS': 3, 'BUCHOSA': 3, 'MISUNGWI': 3, 'JML': 2, 'KWIMBA': 2, '29': 2, 'SENGEREMA': 2, '122': 2, 'IDADI': 1}`
extra: `{'A': 6, '0': 5, 'S': 2, 'I': 2, 'W': 2, '159': 2, '268': 2, 'ID': 1, 'H': 1, 'D': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'UKEREWE': 19, 'MWANZA': 12, 'ILEMELA': 10, 'MAGU': 6, 'SENGEREMA': 5, 'BUCHOSA': 5, 'MISUNGWI': 4, 'WAV': 3, 'WAS': 3, '0': 3}`
extra: `{'A': 6, '1': 3, 'S': 2, 'I': 2, 'W': 2, '29': 2, 'ID': 1, 'H': 1, 'D': 1, 'U': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'UKEREWE': 5, 'WAV': 3, 'WAS': 3, 'JML': 2, 'IDADI': 1, 'YA': 1, 'SHULE': 1, 'ISAFAN': 1, 'AOKM': 1, 'UFAULU': 1}`
extra: `{'A': 6, '0': 3, 'S': 2, 'I': 2, 'W': 2, '6': 2, '13': 2, 'ID': 1, 'H': 1, 'D': 1}`

![page 4](page_04.png)

