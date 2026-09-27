# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 18.24% | 11.00% | 2 | 1 | - | - |
| 2 | 12.24% | 7.70% | 2 | 1 | - | #ffff00 |

## Page 1
missing: `{'LEVEL': 1, 'KNAR/R': 1}`
extra: `{'LEVELKNAR/R': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'LEVEL': 1, 'KNAR/R': 1}`
extra: `{'LEVELKNAR/R': 1}`

![page 2](page_02.png)

