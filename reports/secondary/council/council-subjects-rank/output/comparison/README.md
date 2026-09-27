# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 18.87% | 9.61% | 4 | 1 | #65ffab #d2fce6 #d8e4bc #daeef3 #ebf1de #f2f2f2 #fcd5b4 #fde9d9 | #66ff99 #66ffcc #ccffcc #ddebf7 #e2efda #f8cbad #fce4d6 |
| 2 | 4.08% | 2.58% | 0 | 0 | #65ffab #d2fce6 #f2f2f2 #fcd5b4 | #ccffcc #ddebf7 #f8cbad |

## Page 1
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1}`
extra: `{'KNAR': 1}`

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

