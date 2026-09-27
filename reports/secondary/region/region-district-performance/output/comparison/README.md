# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 8.39% | 5.49% | 5 | 9 | - | - |
| 2 | 8.58% | 5.62% | 4 | 7 | - | - |
| 3 | 9.23% | 7.07% | 4 | 7 | - | #f8cbad |
| 4 | 8.99% | 6.34% | 2 | 6 | - | - |
| 5 | 9.08% | 6.47% | 2 | 6 | - | - |

## Page 1
missing: `{'LEVEL': 1, '3.53535Grade': 1, 'KNAR': 1, 'REGISTERED': 1, 'SCHOOLS': 1}`
extra: `{'PERFORMANCE': 1, 'OF': 1, 'CANDIDATES': 1, 'DIVISION': 1, 'NO.': 1, 'SCHOORLESGISTERED': 1, 'KLENAVREL': 1, 'Grade': 1, '3.53535': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'LEVEL': 1, 'KNAR': 1, 'SCHOOLS': 1, 'REGISTERED': 1}`
extra: `{'PERFORMANCE': 1, 'OF': 1, 'CANDIDATES': 1, 'DIVISION': 1, 'NO.': 1, 'SCHOORLESGISTERED': 1, 'KLENAVREL': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'LEVEL': 1, 'KNAR': 1, 'SCHOOLS': 1, 'REGISTERED': 1}`
extra: `{'PERFORMANCE': 1, 'OF': 1, 'CANDIDATES': 1, 'DIVISION': 1, 'NO.': 1, 'SCHOORLESGISTERED': 1, 'KLENAVREL': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'LEVEL': 1, 'KNAR': 1}`
extra: `{'PERFORMANCE': 1, 'OF': 1, 'CANDIDATES': 1, 'DIVISION': 1, 'NO.': 1, 'LKENVAERL': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'LEVEL': 1, 'KNAR': 1}`
extra: `{'PERFORMANCE': 1, 'OF': 1, 'CANDIDATES': 1, 'DIVISION': 1, 'NO.': 1, 'LKENVAERL': 1}`

![page 5](page_05.png)

