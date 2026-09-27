# fonts/ — real font files (no fallback chains)

The reports render with **real font files** registered via `@font-face`, not with a
CSS fallback stack. Each family name maps to exactly one file. There is **no shared
font stylesheet**: every report's own `style.css` carries its own inline `@font-face`
blocks that point at the files in this directory (the report stays fully
self-contained — nothing is `@import`ed).

## What the source PDFs embed

The council/region source PDFs embed these exact families:

| Embedded font (in the PDF) | CSS family name reports use | Weight |
|---|---|---|
| `ArialMT`                 | `Arial`           | normal |
| `Arial-BoldMT`            | `Arial`           | bold   |
| `ArialNarrow-Bold`        | `Arial Narrow`    | bold   |
| `TimesNewRomanPS-BoldMT`  | `Times New Roman` | bold   |

## Licensing decision point (why substitutes)

`ArialMT`, `Arial-BoldMT`, `ArialNarrow-Bold` and `TimesNewRomanPS-BoldMT` are
**Monotype proprietary** fonts. They are **not freely/legally redistributable**,
and no genuine Arial/Times files are installed on this host or available from a
license-clean source in-sandbox. We therefore cannot commit the genuine files.

Instead we bundle **metric-compatible open substitutes** from the
**Liberation** family. Liberation fonts are designed to be metric-compatible
(same character widths and line metrics) with Arial, Arial Narrow and Times New
Roman, so text lays out at the same widths — which is exactly what the
pixel/word fidelity check (`scripts/compare.py`) needs. They are licensed under
the **SIL Open Font License 1.1** (with the GPLv2 + font exception heritage),
which permits redistribution and bundling.

If a genuinely licensed Arial/Times file becomes available, drop it in here and
repoint the matching `@font-face` `src` in each report's `style.css`; no other
change is needed because the CSS references the family name, not the vendor.

## Lakezone success example — genuine Arial

The lakezone reference report (`templates/report.css`, rendered to
`output/report.pdf`) registers the **genuine Microsoft Arial** files under the
family name `R Arial` (normal -> `arial.ttf`, bold -> `arialbd.ttf`), with **one
family name and no comma fallback**. These are the freely distributed "core fonts
for the web" files; install them with `python scripts/fetch_fonts.py` (needs
`cabextract`). They are not committed to git (licence), so the fetch script pulls
them on demand. WeasyPrint embeds them (verified: `pymupdf get_fonts` shows
`R-Arial` / `R-Arial-Bold`, never Noto) because `sars_pdf/render.py` passes one
shared `FontConfiguration()` to `write_pdf()`.

## Files in this directory

| File | Backs CSS family | Source |
|---|---|---|
| `arial.ttf`                      | `R Arial` (normal, lakezone) | Microsoft core fonts (arial32.exe; not committed) |
| `arialbd.ttf`                    | `R Arial` (bold, lakezone)   | Microsoft core fonts (arial32.exe; not committed) |
| `LiberationSans-Regular.ttf`     | `Arial` (normal)          | liberation-fonts 2.1.5 |
| `LiberationSans-Bold.ttf`        | `Arial` (bold)            | liberation-fonts 2.1.5 |
| `LiberationSansNarrow-Bold.ttf`  | `Arial Narrow` (bold)     | Debian `fonts-liberation` 1:1.07.4-11 (Narrow was dropped after the 1.07.x line) |
| `LiberationSerif-Bold.ttf`       | `Times New Roman` (bold)  | liberation-fonts 2.1.5 |
| `LICENSE-Liberation.txt`         | (license text)            | SIL OFL 1.1 |

### Provenance / verification

Downloaded and verified with fonttools; family/subfamily names confirmed:

| File | family / subfamily | sha256 (first 16) | bytes |
|---|---|---|---|
| `LiberationSans-Regular.ttf`    | `Liberation Sans` / `Regular`      | `76d04c18ea243f42` | 410712 |
| `LiberationSans-Bold.ttf`       | `Liberation Sans` / `Bold`         | `788abee4c806d660` | 414456 |
| `LiberationSansNarrow-Bold.ttf` | `Liberation Sans Narrow` / `Bold`  | `f77fe6ca01c8b043` | 110252 |
| `LiberationSerif-Bold.ttf`      | `Liberation Serif` / `Bold`        | `d754ba427cfe0bca` | 370096 |

- Liberation Sans / Serif came from the official
  `liberation-fonts-ttf-2.1.5.tar.gz` release.
- Liberation Sans **Narrow** is no longer shipped in the 2.x releases, so its
  Bold face was extracted from the archived Debian `fonts-liberation`
  `1:1.07.4-11` package (snapshot.debian.org, verified deb sha1
  `1d4311e811a29f52a5be2c179100f85001c74d20`).

The `@font-face` blocks register each file under the exact family name above
with **one name and no comma-separated fallback**.
