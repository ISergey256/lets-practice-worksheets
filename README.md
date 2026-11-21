# LET'S PRACTICE! — maths worksheets

Free printable maths worksheets for Year 1 (ages 5–7): 18 tasks on 4 pages plus an answer page for parents.

**Website: https://isergey256.github.io/lets-practice-worksheets/**

Choose a level and a worksheet number, then press “Print worksheet”. To get a PDF, choose “Save as PDF” in the print dialog.
Everything runs in your browser: nothing to install, nothing is sent anywhere.

## Languages

English by default. The site language, the language of the tasks and the language of the answers are chosen separately:
English, Українська, Русский, Ελληνικά, Deutsch, Français, Español.

## What is on a worksheet

- counting and estimating;
- odd and even numbers, number line, comparing numbers, numbers in words;
- 3D and 2D shapes, polygons, fractions (halves, quarters, thirds);
- longer / shorter, taller / lower;
- number bonds, counting in 2s, 5s and 10s, sums;
- number walls, positional words (in, on, behind…), ordinal numbers.

| Level | What is inside |
|---|---|
| 1 · Easy | numbers to 10, adding within 10, halves |
| 2 · Medium | numbers to 20, quarters |
| 3 · Hard | to 100, crossing ten, thirds and ¾, 4-row number walls |

A worksheet number always gives the same worksheet: level 2, No. 123 is the same in every language.
Links like `…/#L2-123` or `…/#L2-123-uk-ru` (tasks in Ukrainian, answers in Russian) can be shared.

## Running it on your computer (real PDF files)

```
pip install playwright pypdf
playwright install chromium
python scripts/server.py                          # the same website at http://127.0.0.1:8000, plus PDF download
python scripts/generate.py --level 2 --seed 123 --lang en --answers-lang en   # command line, PDFs go to out/
```

On Windows you can also double-click `start_site.bat`.

## How it works

- `scripts/generate.py`: the 18 tasks (one `task_*` function each) and the A4 layout (HTML + inline SVG).
- `scripts/i18n.py`: all texts in every language, plus number words and ordinals. To add a language, copy the `en` entries, translate them and run the checks below.
- `site/index.html`: the website. On GitHub Pages it runs the same `generate.py` in the browser with [Pyodide](https://pyodide.org) (Python compiled to WebAssembly), so worksheet numbers match the local version. With `scripts/server.py` the same page asks the local server instead and can download PDF files.
- `scripts/build_site.py`: checks the generator in every language and builds `_site/`. GitHub Actions (`.github/workflows/pages.yml`) publishes it on every push to `main`. Use `python scripts/build_site.py --serve` to preview it.
- `scripts/check_layout.py`: renders worksheets in every language and checks that every page fits A4.
- `fonts/`: Nunito, plus M PLUS Rounded 1c for Greek letters (both under the SIL Open Font License, see `fonts/OFL-*.txt`). `scripts/fetch_fonts.py` downloads them again.

License: MIT.
