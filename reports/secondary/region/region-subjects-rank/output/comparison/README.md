# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 27.95% | 19.73% | 4 | 2 | #65ffab #83e28e #c1f0c8 #caedfb #d2fce6 #daf2d0 #f1a983 #f2ceef #f2f2f2 #fbe2d5 | #66ff99 #66ffcc #ccffcc #ddebf7 #e2efda #f8cbad #fce4d6 #ff0000 |
| 2 | 17.79% | 12.69% | 0 | 0 | #65ffab #83e28e #c1f0c8 #d2fce6 #daf2d0 #f1a983 #f2ceef #f2f2f2 #fbe2d5 | #66ff99 #66ffcc #ccffcc #ddebf7 #e2efda #f8cbad #fce4d6 #ffff00 |

## Page 1
missing: `{'1': 1, '0': 1, 'TECHNOLOGY': 1, 'WORKS': 1}`
extra: `{'TECHNOL1OGY': 1, 'WOR0KS': 1}`

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

