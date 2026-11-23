# Architecture: years, subjects and topics

How Let's Practice is organised, and how to add a new subject. Rules for how sheets look are in
[STANDARDS.md](STANDARDS.md); how to send changes is in [CONTRIBUTING.md](CONTRIBUTING.md).

## The idea in one line

**Year → subject → topics → worksheet.** One registry says which years and subjects exist; each subject that has
worksheets is a Python module with the same small interface. The website reads everything from the registry,
so adding a subject never needs changes in `site/index.html`.

```
site/index.html ──► topics.catalog(lang) ──► registry.py (years, subjects, what is ready)
      │                                   └► each ready subject: rows (topics), presets (ready-made sheets)
      └► generate.build(level, seed, lang, answers_lang)
             ├─ "R" | "Y1A"            → stages.build      (maths: Reception, Year 1 autumn)
             └─ "T:<topic ids>"        → registry: subject of the ids → that subject's module .build()
```

The same Python runs locally (`scripts/server.py`) and in the browser (Pyodide on GitHub Pages), so both always
give the same worksheet for the same number.

## Registry — `scripts/registry.py`

- `YEARS`: Reception, Year 1 … Year 11 (National Curriculum for England), each with the ages and the nearest
  Ukrainian class (UK Year 2, ages 6–7 ≈ Ukrainian class 1).
- `SUBJECTS`: subjects change with age, like a real school. Years R–Y6: Maths (geometry is a section inside),
  Languages, Nature, People and society. From Year 7: Physics, Chemistry, Biology, Geography, History; from Year 8
  maths splits into Algebra and Geometry. For every subject: `years` (taught), `ready` (have worksheets),
  `module` (Python module with the topics), `prefix` (topic ids start with it).
- Names in 7 languages: `i18n.REG`. `python scripts/registry.py` prints the whole table; `registry.check()` and
  `i18n.check()` verify it.

## A subject module

A module that provides worksheets for a subject has the same interface as `scripts/topics.py` (maths):

| Name | What it returns |
|---|---|
| `META` | every topic id → `{year, period, strand, card, …}` |
| `catalog(lang)` | rows for the topic picker: `{row, year, subject, strand, title, variants:[{id, period, label}]}`, plus `presets()` |
| `presets()` | ready-made sheets per year: `[{id, key, part, subject}]` |
| `build(spec, seed, L)` | `(pages, answer_page)` as HTML for a sheet `"T:id_id…"` |
| `cards(spec)` | help cards available for the sheet: `[(task number, card key)]` |

Rules: one subject per worksheet; at most 12 topics; numbers depend only on the topics and the sheet number;
every task has an action icon, a worked example in grey and one clear answer (STANDARDS.md).

## Topic ids and links

- Ids are lowercase letters and digits. Maths keeps its ids (`r1…r8`, `y1…y10`, `v<task><a|b|c>`), so all old
  links still work: `#R-7`, `#Y1A-12`, `#L2-7`, `#T-r1_v4a-7`.
- Every other subject uses its 2-letter prefix from the registry (`la`, `nt`, `ph`, `ch`, `bi`, `so`, `ge`, `hi`,
  `al`, `gm`), e.g. `nt3`, `ph12`. Prefixes never start with `r`, `y` or `v`.

## How to add a subject (5 steps)

1. Open an issue first and collect the official sources for the subject and years (`reference/`, with licences).
2. Write `scripts/<subject>.py` with the interface above (copy the structure of `topics.py`; tasks follow STANDARDS.md).
3. In `scripts/registry.py` set `module` and the `ready` years of the subject; add texts to `scripts/i18n.py`
   (task texts in all 7 languages; `i18n.check()` must pass).
4. Add the module to the files copied for the website: the file list in `build()` of `scripts/build_site.py` and the Pyodide list in
   `site/index.html` (`for (const f of [...])`).
5. Run `python scripts/build_site.py`, `python scripts/measure_topics.py`, `python scripts/check_layout.py`,
   and open the site: the subject appears in its years by itself.

## Answers for solving online

Besides printing, a child can solve a sheet on the site ("Solve on screen", `site/online.js`), one task at a time with a
big keypad. For that every task marks its answers with data attributes. They change nothing on paper (the sheets are
pixel-identical) and are added with `generate.ans_attr()`:

| Attribute | Meaning |
|---|---|
| `data-a="7"` | a box to fill; `data-k="sign"` (<, >, =), `"word"` (typed), `"bank"` (a word from the `.pill` bank of the task), `"shape"` (one of the `data-shape` pictures); `data-a="*"` = any answer (an estimate) |
| `data-p="1"` / `"0"` | something to pick (circle, tick, colour): right / wrong; `data-look="tick"` or `"fill"` changes how a pick looks |
| `data-n="4"` + `data-cell` | tap this many cells (draw dots in a ten frame, cross out objects) |
| `data-ml` / `data-mr` | the two ends of a "join with a line" pair have the same key |
| `data-sum="10"` | a row of two boxes (`data-a="?"`) that make 10; every pair once |
| `data-self` | the child checks it (tracing digits, shading) |

Worked examples (grey) are never marked. `scripts/build_site.py` (`check_online`) checks every topic in three languages.
The child's results go to the progress on the device (`site/practice.js`, `localStorage` key `lp-progress`):
first try = easy, at least half right = so-so, else hard. Nothing is sent anywhere.

