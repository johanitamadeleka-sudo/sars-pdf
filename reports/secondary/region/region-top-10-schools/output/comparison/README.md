# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 11.27% | 9.56% | 1 | 4 | #65ffab #8ed973 #c0e6f5 #c1f0c8 #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #8fd968 #d2fbe6 #fce9d9 |
| 2 | 10.36% | 8.78% | 5 | 6 | #65ffab #8ed973 #c1f0c8 #caedfb #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #29ff8a #8fd968 #d2fbe6 #fce9d9 |
| 3 | 11.44% | 10.42% | 1 | 4 | #65ffab #b5e6a2 #c1f0c8 #caedfb #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #29ff8a #8fd968 #d2fbe6 #fce9d9 |
| 4 | 11.20% | 10.16% | 1 | 4 | #b5e6a2 #c1f0c8 #caedfb #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #8fd968 #d2fbe6 #fce9d9 |
| 5 | 11.30% | 10.19% | 1 | 4 | #65ffab #b5e6a2 #c1f0c8 #caedfb #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #29ff8a #8fd968 #d2fbe6 #fce9d9 |
| 6 | 9.98% | 8.80% | 5 | 6 | #8ed973 #c1f0c8 #caedfb #ccffff #d2fce6 #daf2d0 #f2ceef #f2f2f2 #fbe2d5 #ff0000 | #8fd968 #d2fbe6 #fce9d9 |

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

