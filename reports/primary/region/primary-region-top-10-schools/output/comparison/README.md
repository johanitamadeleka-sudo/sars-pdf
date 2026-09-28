# Original vs generated

**Page count differs: original 5 vs generated 6**

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 16.62% | 14.35% | 429 | 69 | #c6e0b4 #d6dce4 #d9e1f2 #ddebf7 #e2efda #f2f2f2 #fce4d6 #ff0000 #ffe699 #fff2cc | #00b050 | ❌ FAIL (pixels 14.35%>4%, fills 10orig/1gen, words 429miss/69extra) |
| 2 | 16.15% | 14.30% | 492 | 147 | #c6e0b4 #d6dce4 #d9e1f2 #ddebf7 #e2efda #f2f2f2 #fce4d6 #ff0000 #ffe699 #fff2cc | #00b050 | ❌ FAIL (pixels 14.30%>4%, fills 10orig/1gen, words 492miss/147extra) |
| 3 | 15.99% | 14.15% | 524 | 187 | #c6e0b4 #d6dce4 #d9e1f2 #ddebf7 #e2efda #f2f2f2 #fce4d6 #ff0000 #ffe699 #fff2cc | #00b050 | ❌ FAIL (pixels 14.15%>4%, fills 10orig/1gen, words 524miss/187extra) |
| 4 | 16.64% | 14.92% | 559 | 372 | #f2f2f2 #fce4d6 #fff2cc | #ffc000 | ❌ FAIL (pixels 14.92%>4%, fills 3orig/1gen, words 559miss/372extra) |
| 5 | 15.54% | 13.50% | 457 | 320 | #f2f2f2 #fce4d6 #fff2cc | #ffc000 | ❌ FAIL (pixels 13.50%>4%, fills 3orig/1gen, words 457miss/320extra) |

**Verdict summary: 0/5 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'0': 105, 'WAS': 15, 'JML': 11, 'WAV': 10, 'DC': 10, '100': 10, 'Daraja': 10, '(Bora': 10, 'Sana)': 10, 'SERIKALI': 10}`
extra: `{'W': 13, 'L': 6, 'S': 5, 'AS': 4, 'U': 4, 'I': 4, 'J': 3, 'M': 3, 'N': 3, 'A': 2}`

![page 1](page_01.png)

## Page 2
missing: `{'0': 60, 'WAS': 15, '9': 13, 'JML': 11, 'BINAFSI': 11, 'WAV': 10, 'Daraja': 10, '7': 10, '8': 10, 'D': 10}`
extra: `{'W': 13, 'A': 12, 'DC': 7, 'L': 6, 'S': 5, 'AS': 4, 'U': 4, 'I': 4, 'KWIMBA': 4, '46': 4}`

![page 2](page_02.png)

## Page 3
missing: `{'1': 22, '3': 21, '2': 18, '8': 16, 'WAS': 15, '5': 12, 'JML': 11, 'SERIKALI': 11, '13': 11, 'C': 11}`
extra: `{'A': 22, '0': 18, 'W': 13, '(Bora': 10, 'Sana)': 10, '22': 7, 'L': 6, 'S': 5, 'AS': 4, 'U': 4}`

![page 3](page_03.png)

## Page 4
missing: `{'A': 107, 'B': 32, '(Bora': 20, 'Sana)': 20, 'DRJ': 12, 'AL': 11, 'DC': 11, 'SERIKALI': 11, 'BINAFSI': 10, 'Daraja': 10}`
extra: `{'0': 41, 'W': 13, 'D': 12, '(Wastani)': 10, 'UKEREWE': 9, '1': 7, '13': 7, 'L': 6, 'WAV': 6, '24': 6}`

![page 4](page_04.png)

## Page 5
missing: `{'A': 48, 'D': 45, 'C': 13, 'E': 13, 'DRJ': 12, 'AL': 11, 'BINAFSI': 11, 'B': 11, 'Daraja': 10, '(Bora': 10}`
extra: `{'0': 41, 'W': 13, '1': 7, 'L': 6, 'WAV': 6, '13': 6, '24': 6, 'S': 5, 'JML': 5, '38': 5}`

![page 5](page_05.png)

