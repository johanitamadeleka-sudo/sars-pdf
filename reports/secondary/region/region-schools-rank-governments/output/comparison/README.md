# Original vs generated

Columns: **original | generated | diff** (pink = sub-pixel differences, red = real differences).

Pixel diff = share of pixels that differ at 110 dpi; tolerant = still different when a 1px shift is allowed (ignores sub-pixel anti-aliasing).

**Verdict** is the stricter >=96%-match bar (position-by-position across colours, borders, data and cell sizes): a page **PASS**es when tolerant diff <= 4% (>=96% pixel match) AND there are zero fills-only diffs both ways AND zero words missing/extra; otherwise **FAIL** with the failing dimension(s) named.

| page | pixel diff | tolerant diff | words missing | words extra | fills only in original | fills only in generated | verdict (>=96%) |
|---|---|---|---|---|---|---|---|
| 1 | 34.08% | 16.44% | 17 | 6 | - | - | ❌ FAIL (pixels 16.44%>4%, words 17miss/6extra) |
| 2 | 41.87% | 21.50% | 42 | 38 | - | - | ❌ FAIL (pixels 21.50%>4%, words 42miss/38extra) |
| 3 | 41.69% | 21.47% | 69 | 66 | - | - | ❌ FAIL (pixels 21.47%>4%, words 69miss/66extra) |
| 4 | 39.58% | 21.01% | 5 | 122 | #9eeaea #b5e6a2 #f2ceef #f7c7ac | - | ❌ FAIL (pixels 21.01%>4%, fills 4orig/0gen, words 5miss/122extra) |

**Verdict summary: 0/4 pages meet the >=96% bar** (tolerant diff <= 4% AND zero fill diffs AND zero word diffs).

## Page 1
missing: `{'97.70': 2, '54302': 1, '28414': 1, '22856': 1, '51270': 1, '93.73': 1, '2258': 1, '4060': 1, '8053210721470235774': 1, '643': 1}`
extra: `{'PERFORMANCE': 1, 'GPA': 1, '5430228414228565127093.73': 1, '22584060': 1, '8053210721470235774643': 1, '97.703.823': 1}`

![page 1](page_01.png)

## Page 2
missing: `{'0': 2, '1': 2, '2': 2, '146': 2, '211': 2, '150': 2, 'GOVERNMENT': 1, '6': 1, '14': 1, 'Grade': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, 'PERFORMANCE': 1, 'GPA': 1, 'S/NO.': 1, 'COUNCIL': 1, 'SCHOOL': 1, 'NAME': 1}`

![page 2](page_02.png)

## Page 3
missing: `{'3': 3, '4': 3, '5': 2, '9': 2, '2': 2, '226': 2, '17': 2, '10': 2, '227': 2, '0': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, '146': 2, '211': 2, '150': 2, 'PERFORMANCE': 1, 'GPA': 1, 'S/NO.': 1}`

![page 3](page_03.png)

## Page 4
missing: `{'3920': 1, '8053': 1, '21072': 1, '14702': 1, '35774': 1}`
extra: `{'F': 9, 'M': 9, 'T': 9, '%': 4, '2': 4, '0': 3, '4': 3, '1': 3, '3': 3, '226': 2}`

![page 4](page_04.png)

