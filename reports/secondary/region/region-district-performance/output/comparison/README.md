# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 9.11% | 5.62% | 5 | 9 | #e0f8e3 #e2efda #ebeef1 #ededed #eeb500 #f4b084 #f8cbad #fce4d6 #fff2cc #ffffcc | #64ffab #d2fbe6 #dce6f0 #fce9d9 #ffc000 |
| 2 | 9.20% | 5.74% | 4 | 7 | #e0f8e3 #e2efda #ebeef1 #ededed #eeb500 #f4b084 #f8cbad #fce4d6 #fff2cc #ffffcc | #64ffab #d2fbe6 #dce6f0 #fce9d9 #ffc000 |
| 3 | 9.63% | 7.30% | 4 | 7 | #e0f8e3 #e2efda #ebeef1 #ededed #f4b084 #fce4d6 #fff2cc #ffffcc | #64ffab #d2fbe6 #dce6f0 #fce9d9 |
| 4 | 9.62% | 6.38% | 2 | 6 | #e0f8e3 #e2efda #ebeef1 #ededed #eeb500 #f4b084 #f8cbad #fce4d6 #fff2cc #ffffcc | #64ffab #d2fbe6 #dce6f0 #fce9d9 #ffc000 |
| 5 | 9.63% | 6.43% | 2 | 6 | #e0f8e3 #e2efda #ebeef1 #ededed #eeb500 #f4b084 #f8cbad #fce4d6 #fff2cc #ffffcc | #64ffab #d2fbe6 #dce6f0 #fce9d9 #ffc000 |

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

