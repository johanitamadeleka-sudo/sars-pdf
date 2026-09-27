# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated |
|---|---|---|---|---|---|---|
| 1 | 33.02% | 14.49% | 34 | 22 | #65ffab #ccffff #e8e8e8 #f2ceef #ff0000 #ffffcc | - |
| 2 | 40.64% | 19.00% | 22 | 49 | - | - |
| 3 | 40.38% | 18.88% | 32 | 54 | - | - |
| 4 | 36.90% | 17.54% | 19 | 46 | #9eeaea #b5e6a2 #f2ceef #f7c7ac | - |

## Page 1
missing: `{'DC': 13, '3920': 1, '8053210721470235774': 1, '97.70': 1, 'KATUNGURU': 1, 'SAVANA': 1, 'NYITUNDU': 1, 'BITOTO': 1, 'SIGU': 1, "ISUNGANG'HOLO": 1}`
extra: `{'I': 2, 'PERFORMANCE': 1, 'GPA': 1, 'REGIS': 1, 'TERED': 1, 'II': 1, 'V': 1, '39208053210721470235774': 1, 'DCKATUNGURU': 1, 'DCSAVANA': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'DC': 11, 'ISOLE': 1, 'NYAMPULUKANO': 1, 'TUNYENYE': 1, 'IBISABAGENI': 1, 'BUSISI': 1, 'NYANCHENCHE': 1, 'IGAKA': 1, 'MWALIGA': 1, 'NYAMAZUGO': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, 'PERFORMANCE': 1, 'GPA': 1, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'DC': 16, 'BUYAGU': 1, 'NEW': 1, 'BUTONGA': 1, 'SIMA': 1, 'LUSIKWI': 1, 'KISHINDA': 1, 'NYAMAHONA': 1, 'KABUSURI': 1, 'NGOMA': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, 'PERFORMANCE': 1, 'GPA': 1, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'DC': 7, 'NYAMTELELA': 1, 'NYAMPANDE': 1, 'KAHUMULO': 1, 'CHAMABANDA': 1, 'KIJUKA': 1, 'TAMABU': 1, 'NYAMATONGO': 1, '3920': 1, '8053': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, 'PERFORMANCE': 1, 'GPA': 1, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1}`

![page 4](page_04.png)

