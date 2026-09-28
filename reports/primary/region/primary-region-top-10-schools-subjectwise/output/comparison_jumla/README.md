# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 18.70% | 15.65% | 8 | 22 | #c6e0b4 #d1f5f9 #d6dce4 #ddebf7 #e2efda #f2f2f2 #f4b084 #fce4d6 #fff2cc #ffffcc | - | ❌ FAIL (pixels 15.65%>4%, fills 10orig/0gen, words 8miss/22extra) |
| 2 | 19.20% | 16.74% | 11 | 24 | #c6e0b4 #d1f5f9 #d6dce4 #ddebf7 #e2efda #f2f2f2 #f4b084 #fce4d6 #fff2cc #ffffcc | - | ❌ FAIL (pixels 16.74%>4%, fills 10orig/0gen, words 11miss/24extra) |
| 3 | 19.86% | 17.46% | 14 | 27 | #c6e0b4 #d1f5f9 #d6dce4 #ddebf7 #e2efda #f2f2f2 #f4b084 #fce4d6 #fff2cc #ffffcc | - | ❌ FAIL (pixels 17.46%>4%, fills 10orig/0gen, words 14miss/27extra) |

**Verdict summary: 0/3 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'WASTANI': 2, 'SOMO': 2, 'ISAFAN': 2, 'SAJILIWA': 2}`
extra: `{'O': 4, 'WAS': 2, 'S': 2, 'T': 2, 'A': 2, 'M': 2, 'N': 2, 'I': 2, 'NAFASI': 2, 'WALIOSAJILIWA': 2}`

![page 1](page_01.png)

## Page 2
missing: `{'WASTANI': 2, 'SOMO': 2, 'ISAFAN': 2, 'SAJILIWA': 2, 'PRSEE': 1, 'ARNIKDA': 1, 'LI': 1}`
extra: `{'O': 4, 'WAS': 2, 'S': 2, 'T': 2, 'A': 2, 'M': 2, 'N': 2, 'I': 2, 'NAFASI': 2, 'WALIOSAJILIWA': 2}`

![page 2](page_02.png)

## Page 3
missing: `{'WASTANI': 2, 'SOMO': 2, 'ISAFAN': 2, 'SAJILIWA': 2, 'PRSEE': 1, 'ARNIKDA': 1, 'LI': 1, 'AND': 1, 'ANDB': 1, 'INAFSI': 1}`
extra: `{'O': 4, 'A': 3, 'WAS': 2, 'S': 2, 'T': 2, 'M': 2, 'N': 2, 'I': 2, 'NAFASI': 2, 'WALIOSAJILIWA': 2}`

![page 3](page_03.png)

