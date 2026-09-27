# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 18.75% | 9.65% | 4 | 1 | - | - |
| 2 | 4.08% | 2.60% | 0 | 0 | - | - |

## Page 1
missing: `{'K': 1, 'N': 1, 'A': 1, 'R': 1}`
extra: `{'KNAR': 1}`

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

