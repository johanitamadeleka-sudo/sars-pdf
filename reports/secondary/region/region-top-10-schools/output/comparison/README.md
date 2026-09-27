# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 10.86% | 9.11% | 1 | 4 | #8ed973 #ff0000 | - |
| 2 | 10.00% | 8.41% | 5 | 6 | #8ed973 #caedfb #ff0000 | #29ff8a #c0e6f5 |
| 3 | 10.92% | 9.89% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #29ff8a #c0e6f5 |
| 4 | 10.67% | 9.63% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #65ffab #c0e6f5 |
| 5 | 10.78% | 9.65% | 1 | 4 | #b5e6a2 #caedfb #ff0000 | #29ff8a #c0e6f5 |
| 6 | 9.55% | 8.38% | 5 | 6 | #8ed973 #caedfb #ff0000 | #65ffab #c0e6f5 |

## Page 1
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'DC': 2, '%': 1, 'KATUNGURU': 1, 'SAVANA': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1, 'DCKATUNGURU': 1, 'DCSAVANA': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'%': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1}`

![page 5](page_05.png)

## Page 6
missing: `{'DC': 2, '%': 1, 'JUVENARY': 1, 'NTUNDURU': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, 'REGISTERED': 1, 'T': 1, 'DCJUVENARY': 1, 'DCNTUNDURU': 1}`

![page 6](page_06.png)

