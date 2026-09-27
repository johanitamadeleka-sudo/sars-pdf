# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 18.86% | 11.32% | 2 | 1 | #65ffab #83e28e #c1f0c8 #caedfb #d2fce6 #daf2d0 #f1a983 #f2ceef #f2f2f2 #fbe2d5 | #66ff99 #66ffcc #ccffcc #ddebf7 #e2efda #f8cbad #fce4d6 #ff0000 |
| 2 | 12.68% | 7.97% | 2 | 1 | #65ffab #83e28e #c1f0c8 #d2fce6 #daf2d0 #f1a983 #f2ceef #f2f2f2 #fbe2d5 | #66ff99 #66ffcc #ccffcc #ddebf7 #e2efda #f8cbad #fce4d6 #ffff00 |

## Page 1
missing: `{'LEVEL': 1, 'KNAR/R': 1}`
extra: `{'LEVELKNAR/R': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'LEVEL': 1, 'KNAR/R': 1}`
extra: `{'LEVELKNAR/R': 1}`

![page 2](page_02.png)

