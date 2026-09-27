# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 11.33% | 9.07% | 0 | 0 | - | - | ❌ FAIL (pixels 9.07%>4%) |
| 2 | 11.19% | 8.91% | 0 | 0 | - | - | ❌ FAIL (pixels 8.91%>4%) |
| 3 | 11.02% | 8.78% | 0 | 0 | - | - | ❌ FAIL (pixels 8.78%>4%) |
| 4 | 10.93% | 8.71% | 0 | 0 | - | - | ❌ FAIL (pixels 8.71%>4%) |
| 5 | 11.18% | 9.12% | 16 | 8 | - | - | ❌ FAIL (pixels 9.12%>4%, words 16miss/8extra) |
| 6 | 11.01% | 8.82% | 0 | 0 | - | - | ❌ FAIL (pixels 8.82%>4%) |
| 7 | 10.88% | 8.66% | 0 | 0 | - | - | ❌ FAIL (pixels 8.66%>4%) |
| 8 | 10.97% | 8.71% | 0 | 0 | - | - | ❌ FAIL (pixels 8.71%>4%) |
| 9 | 11.07% | 8.78% | 0 | 0 | - | - | ❌ FAIL (pixels 8.78%>4%) |
| 10 | 11.06% | 8.86% | 1 | 1 | - | - | ❌ FAIL (pixels 8.86%>4%, words 1miss/1extra) |
| 11 | 11.21% | 9.20% | 32 | 6 | #00b050 | - | ❌ FAIL (pixels 9.20%>4%, fills 1orig/0gen, words 32miss/6extra) |
| 12 | 11.28% | 8.91% | 0 | 0 | - | - | ❌ FAIL (pixels 8.91%>4%) |
| 13 | 11.25% | 9.02% | 0 | 0 | - | - | ❌ FAIL (pixels 9.02%>4%) |
| 14 | 11.24% | 9.11% | 20 | 10 | - | - | ❌ FAIL (pixels 9.11%>4%, words 20miss/10extra) |
| 15 | 11.24% | 9.08% | 20 | 10 | - | - | ❌ FAIL (pixels 9.08%>4%, words 20miss/10extra) |
| 16 | 11.06% | 8.80% | 0 | 0 | #ffff00 | #92d050 | ❌ FAIL (pixels 8.80%>4%, fills 1orig/1gen) |
| 17 | 11.24% | 8.90% | 0 | 0 | - | - | ❌ FAIL (pixels 8.90%>4%) |
| 18 | 11.26% | 8.88% | 0 | 0 | - | - | ❌ FAIL (pixels 8.88%>4%) |
| 19 | 11.27% | 8.97% | 0 | 0 | - | #92d050 | ❌ FAIL (pixels 8.97%>4%, fills 0orig/1gen) |
| 20 | 11.36% | 9.18% | 2 | 1 | - | - | ❌ FAIL (pixels 9.18%>4%, words 2miss/1extra) |
| 21 | 11.36% | 9.24% | 25 | 15 | #ffff00 | #92d050 | ❌ FAIL (pixels 9.24%>4%, fills 1orig/1gen, words 25miss/15extra) |
| 22 | 11.06% | 8.87% | 20 | 10 | - | #92d050 | ❌ FAIL (pixels 8.87%>4%, fills 0orig/1gen, words 20miss/10extra) |
| 23 | 11.20% | 9.09% | 20 | 10 | - | #92d050 | ❌ FAIL (pixels 9.09%>4%, fills 0orig/1gen, words 20miss/10extra) |

**Verdict summary: 0/23 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1

![page 1](page_01.png)

## Page 2

![page 2](page_02.png)

## Page 3

![page 3](page_03.png)

## Page 4

![page 4](page_04.png)

## Page 5
missing: `{'MUSABE': 4, 'GIRLS': 4, 'PRIVATE': 2, 'DIPLOMATI': 1, 'BUKUMBI': 1, 'CENTRAL': 1, 'VALLEY': 1, 'MORNING': 1, 'STAR': 1}`
extra: `{'MUSABGEIRLS': 4, 'DIPLPORMIVAATTIE': 1, 'BUKUPRMIVBAITE': 1, 'CENTRVAALLLEY': 1, 'MORNISNTGAR': 1}`

![page 5](page_05.png)

## Page 6

![page 6](page_06.png)

## Page 7

![page 7](page_07.png)

## Page 8

![page 8](page_08.png)

## Page 9

![page 9](page_09.png)

## Page 10
missing: `{'SEMINARPYRIVATE': 1}`
extra: `{'SEMINARPRIVATE': 1}`

![page 10](page_10.png)

## Page 11
missing: `{'A': 10, 'MWANZA': 6, 'CC': 6, '10': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1}`
extra: `{'MWANZACC': 6}`

![page 11](page_11.png)

## Page 12

![page 12](page_12.png)

## Page 13

![page 13](page_13.png)

## Page 14
missing: `{'ISLAMIC': 10, 'ILEMELA': 5, 'NYASAKA': 3, 'BUHONGWA': 2}`
extra: `{'ILEMELISALAMIC': 5, 'NYASAIKSLAAMIC': 3, 'BUHONISGLAWMAIC': 2}`

![page 14](page_14.png)

## Page 15
missing: `{'MUSABE': 10, 'GIRLS': 6, 'BOYS': 4}`
extra: `{'MUSABGEIRLS': 6, 'MUSABBEOYS': 4}`

![page 15](page_15.png)

## Page 16

![page 16](page_16.png)

## Page 17

![page 17](page_17.png)

## Page 18

![page 18](page_18.png)

## Page 19

![page 19](page_19.png)

## Page 20
missing: `{'GOVERNMENT': 1, 'MWANZA': 1}`
extra: `{'MWANGZOAVERNMENT': 1}`

![page 20](page_20.png)

## Page 21
missing: `{'GOVERNMENT': 5, 'MONTESSORI': 5, 'MARIA': 5, 'PRIVATE': 5, 'IBINZA': 4, 'JITIHADA': 1}`
extra: `{'MONTEMSASROIAR': 5, 'PIRIVATE': 5, 'IBINZAGOVERNMENT': 4, 'JITIHGAODVAERNMENT': 1}`

![page 21](page_21.png)

## Page 22
missing: `{'GOVERNMENT': 10, 'KAHANGARA': 10}`
extra: `{'KAHANGAGROAVERNMENT': 10}`

![page 22](page_22.png)

## Page 23
missing: `{'GOVERNMENT': 10, 'LUSHAMBA': 8, 'MWAKILYAMBITI': 1, 'NYASAKA': 1}`
extra: `{'LUSHAMGBAOVERNMENT': 8, 'MWAKIGLYOAVMEBRINTMIENT': 1, 'NYASAGKOAVERNMENT': 1}`

![page 23](page_23.png)

