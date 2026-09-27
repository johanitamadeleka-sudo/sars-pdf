# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 33.89% | 23.26% | 18 | 0 | #65ffab #c00000 | - |
| 2 | 36.54% | 25.01% | 39 | 23 | #c00000 | - |
| 3 | 36.74% | 24.86% | 51 | 32 | #c00000 | - |
| 4 | 36.91% | 25.03% | 60 | 41 | #c00000 | - |
| 5 | 36.81% | 24.75% | 70 | 51 | #c00000 | - |
| 6 | 34.22% | 24.11% | 10 | 75 | #c00000 | - |

## Page 1
missing: `{'AND': 1, 'MWANZA': 1, 'PRIVATE': 1, 'IMEPANDA': 1, 'GIRLS': 1, 'CC': 1, 'BOYS': 1, '12': 1, '14': 1, 'STAR': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'UMESHUKA': 2, '57': 1, 'NYANZA': 1, 'ADVENTIST': 1, 'PRIVATE': 1, '73': 1, '93.59': 1, '2.2969': 1, '122': 1, '87.77': 1}`
extra: `{'TOTAL': 2, '%': 2, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1, 'OWNERSHIP': 1, '56': 1, 'STAR': 1, 'REACHERS': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'GOVERNMENT': 3, 'DC': 2, '38.94': 2, '125': 1, 'SENGEREMA': 1, 'KILABELA': 1, '176': 1, '3.6645': 1, '129': 1, '42.3': 1}`
extra: `{'TOTAL': 2, '%': 2, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1, 'OWNERSHIP': 1, '123': 1, 'ILEMELA': 1, 'MC': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'DC': 3, 'UMESHUKA': 3, 'SENGEREMA': 2, 'GOVERNMENT': 2, '30': 2, '190': 1, 'BUSISI': 1, '51': 1, '45.13': 1, '3.5856': 1}`
extra: `{'TOTAL': 2, '%': 2, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1, 'OWNERSHIP': 1, '187': 1, 'KANDAWE': 1, '81': 1}`

![page 4](page_04.png)

## Page 5
missing: `{'MWANZA': 2, 'CC': 2, 'GOVERNMENT': 2, 'IMEPANDA': 2, '16': 2, '52': 2, '258': 1, 'IGOMA': 1, '173': 1, '24.2': 1}`
extra: `{'TOTAL': 2, '%': 2, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1, 'OWNERSHIP': 1, '254': 1, 'SENGEREMA': 1, 'SIMA': 1}`

![page 5](page_05.png)

## Page 6
missing: `{'331': 1, 'BULALE': 1, '111': 1, '30.75': 1, '3.8043': 1, '71': 1, '15.14': 1, '4.0884': 1, '-15.61': 1, '-0.2841': 1}`
extra: `{'DC': 4, 'GOVERNMENT': 4, 'UMESHUKA': 3, 'TOTAL': 2, '%': 2, '52': 2, '16': 2, 'KWIMBA': 2, 'S/NO.': 1, 'COUNCIL': 1}`

![page 6](page_06.png)

