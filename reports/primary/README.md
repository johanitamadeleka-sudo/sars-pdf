# reports/primary/ — primary (Darasa la IV / STD4) level reports

This directory holds the **PRIMARY** school level reports. They mirror the proven
**secondary** structure exactly (see [`../README.md`](../README.md)): each report
is a self-contained unit driven by JSON data → its own Jinja2 template → its own
CSS → WeasyPrint PDF, verified with [`../../scripts/compare.py`](../../scripts/compare.py).

```
reports/primary/
  council/
    <primary-level-plus-function>/    # e.g. primary-council-wards-rank
      template.html.j2
      style.css
      data.json                        # (or data_<tag>.json for multi-source dirs)
      reference/original.pdf           # (or reference/original_<tag>.pdf)
      output/                          # committed report.pdf/.html, pages/, comparison/
  region/                              # region-scope primary reports (separate task)
```

Conventions (identical to secondary — see [`../README.md`](../README.md)):

- name reports by **level + what-it-does** (`primary-` prefix), never by the
  sampled MWANZA/MKOA instance name (those live only inside `data.json` values);
- each report is **self-contained** (its own template, CSS, data, reference,
  output);
- register the real fonts (in [`../../fonts/`](../../fonts/)) with an OWN inline
  `@font-face` in each report's `style.css` — one family name per face
  (`'Arial'` / `'Arial Narrow'` / `'Times New Roman'`), **no fallback chains**,
  **no `@import`**, `src` pointing four levels up at `../../../../fonts/`;
- store every value as a **display string** (`'49.50'`, `'289.800'`, `'100'`),
  and store the full Swahili competency label (`'Daraja A (Bora Sana)'`);
- extraction is **coordinate-based** via `pymupdf` words
  (`scripts/extract_primary_council_*.py`), never hand-typed;
- palette is **measured per report** from its OWN original
  ([`../../scripts/measure_fills.py`](../../scripts/measure_fills.py)) and grid
  topology from [`../../scripts/measure_grid.py`](../../scripts/measure_grid.py);
- only the **competency-level (KUNDI LA UMAHIRI)** cell colour is data-driven,
  via [`../../sars_pdf/grading.py`](../../sars_pdf/grading.py) — which now
  recognises the Swahili `Daraja X (...)` labels in addition to `Grade X`.

## Primary column vocabulary (Swahili / abbreviations)

Primary STD4 originals use Swahili and abbreviated headers. The mapping to the
F/M/T-equivalent triplets used by the secondary reports:

| Primary header | Meaning |
|---|---|
| `WAV` | girls (wasichana) — the **F** equivalent |
| `WAS` | boys (wavulana) — the **M** equivalent |
| `JML` | total (jumla) — the **T** equivalent |
| `AL` | marks (alama) |
| `DRJ` | grade (daraja) |
| `KATA` | ward |
| `HALMASHAURI` | council |
| `UMILIKI` / `SERIKALI` / `BINAFSI` | ownership / government / private |
| `Daraja X (...)` | competency level label (A–F, e.g. `Daraja B (Vizuri Sana)`) |

## Build + verify

```bash
pyenv global 3.11.15
python scripts/build_all.py --level primary   # render + compare every primary report
python scripts/measure_fills.py reports/primary/council/<report>   # palette check
python scripts/measure_grid.py  reports/primary/council/<report>   # grid topology
```

`build_all.py` discovers every self-contained report dir under `reports/primary/**`
and never touches `reports/secondary/**`.

See [`INDEX.md`](INDEX.md) for the per-report fidelity verdict summary.
