# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 36.62% | 20.93% | 7 | 8 | #65ffab #caedfb #d2fce6 #daf2d0 #f2ceef #f2f2f2 #f7c7ac #fbe2d5 #ffffcc | #00b050 #66ff99 #66ffcc #92d050 #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ffff00 |
| 2 | 38.70% | 21.00% | 2 | 3 | #65ffab #d2fce6 #daf2d0 #f2ceef #f2f2f2 #f7c7ac #fbe2d5 #ffffcc | #66ff99 #66ffcc #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ffc000 #ffff00 |
| 3 | 41.03% | 23.26% | 0 | 0 | #65ffab #d2fce6 #daf2d0 #f2ceef #f2f2f2 #f7c7ac #fbe2d5 #ffffcc | #66ff99 #66ffcc #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ffc000 |
| 4 | 40.96% | 23.24% | 0 | 0 | #65ffab #d2fce6 #daf2d0 #f2ceef #f2f2f2 #f7c7ac #fbe2d5 #ffffcc | #66ff99 #66ffcc #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ffc000 |
| 5 | 41.22% | 24.17% | 0 | 0 | #65ffab #d2fce6 #daf2d0 #f2ceef #f2f2f2 #f7c7ac #fbe2d5 #ffffcc | #66ff99 #66ffcc #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ff0000 #ffc000 |
| 6 | 34.39% | 21.11% | 3 | 1 | #65ffab #d2fce6 #d9d9d9 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ffffcc | #66ff99 #66ffcc #b7dee8 #daeef3 #ddebf7 #e2efda #f8cbad #fce4d6 #ff0000 #ffc000 |

## Page 1
missing: `{'BOYS': 1, 'NYANTAKU2B6WA': 1, 'G2IR8LS': 1, 'NYANTAKU2BWA': 1, 'BO13YS': 1, 'AND1': 1, 'SUBJECT': 1}`
extra: `{'NYANTA': 2, 'A': 1, '1': 1, '2': 1, '26': 1, '13': 1, '28': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'CHRISTIAN0': 1, 'SEMINA0RY': 1}`
extra: `{'0': 2, 'CHRIST': 1}`

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5

![page 5](page_05.png)

## Page 6
missing: `{'859': 1, '2645': 1, '(Satisfactory)': 1}`
extra: `{'(Satis8f5a9ctory2)645': 1}`

![page 6](page_06.png)

