# Let's Practice — learning should be accessible to everyone ❤️

**Website: https://isergey256.github.io/lets-practice-worksheets/** · [Читать по-русски](README.ru.md)

Let's Practice is a free educational platform built on a simple idea: good learning materials should be available to every
child, whatever their family can afford. The source code is open and available here on GitHub.

Today even simple practice sheets often sit behind subscriptions and paywalls. Why should parents pay to print a few
maths exercises for their child?

**No sign-up, no subscriptions, no ads, no hidden payments.**
The goal: open the site → choose a year → a subject → a topic → get the tasks → print. That's all.
(Today: maths for Reception, Year 1 and the first Year 2 topics; more subjects will follow.)

**What is planned**
- Ages: from preschool (Reception) up to Year 11.
- Subjects: maths, languages and other school subjects.
- Fresh variations of every exercise for regular practice, at different levels of difficulty.
- Printable worksheets for home and the classroom.
- An interface any parent understands without instructions.
- First the curriculum of England, other countries later.

Today there is the first version: maths for Reception and Year 1. This is only the beginning.

**Free for everyone:** children and parents, teachers and tutors, state and private schools — everyone who learns or helps
others learn. The license allows free educational use and forbids reselling the product or its materials without permission.
Use it, learn with it, share it — just don't turn free education into another paid product.

**How it started.** I needed maths exercises for my child that I could make and print quickly. Instead of searching
through different sites, I built my own generator. The first version took about an hour with Claude AI — one more example
of how today's tools let one person quickly build something useful.

**The main principle.** Education is not a luxury. Not every family can pay for dozens of learning subscriptions, but every
child should be able to learn, practise and grow. Let Let's Practice be a small contribution to making learning simpler
and more accessible.

*Free for learning. Not for resale.* The project is at an early stage; new subjects, tasks and features will be added step by step.

## How to use

Choose the **year** (Reception, Year 1, Year 2), the **subject** (maths for now) and **what to practise**: a ready-made sheet or **your own topics** (up to 12, grouped like the curriculum, each tagged with the term it is taught in). Then pick a worksheet number and press “Print worksheet”. To get a PDF, choose “Save as PDF” in the print dialog.
Everything runs in your browser: nothing to install, nothing is sent anywhere.

## Languages

English by default. The site language, the language of the tasks and the language of the answers are chosen separately:
English, Українська, Русский, Ελληνικά, Deutsch, Français, Español.

## Stages

| Stage | For whom | What is inside |
|---|---|---|
| **Reception** | ages 4–5, no reading needed | ladybird spots (subitising), count and circle, more / fewer, ten frames, part + part, tracing dotted numbers, patterns, colouring shapes |
| **Year 1 · Autumn** | ages 5–6, first term | count and write, ten frames, 1 more / 1 less, &lt; &gt; =, number lines, part–whole, adding and taking away within 10, make 10, naming shapes |
| **Year 1 review** (levels 1–3) | Year 1 | the full 18-task sheet below, easy / medium / hard |

On the Reception and Year 1 Autumn sheets every task has an **action icon** (count, circle, match, colour, trace, write, tick,
cross out, draw) and its **first item is already done on a grey background**: grey means “do it like this”.
Children answer by circling, matching, ticking, drawing or tracing; the short text is for the adult.

## Cheat sheets

For Reception and Year 1 Autumn a parent or teacher can tick the tasks the child needs help with and print **cheat sheets**:
one card per task, two cards per A4 page. Every card has the same order — **Look** (a worked example), **Do** (3 short steps),
**Check**, **Try** (one mini task) and an “I can do it!” box — so the child always knows where to look.
The numbers on the cards differ from the worksheet, so they never give its answers away.

## What is on a Year 1 review worksheet

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
- `scripts/stages.py`: the Reception and Year 1 Autumn sheets (action icons, worked examples, dotted digits for tracing).
- `scripts/cheats.py`: the cheat-sheet cards (texts in `i18n.CHEAT`).
- `scripts/topics.py`: every task as a topic (year, curriculum term, strand) and sheets built from chosen topics; `scripts/measure_topics.py` measures every topic in every language into `scripts/topic_heights.json`, so any choice of topics is packed onto A4 safely.
- `scripts/i18n.py`: all texts in every language, plus number words and ordinals. To add a language, copy the `en` entries, translate them and run the checks below.
- `site/index.html`: the website. On GitHub Pages it runs the same `generate.py` in the browser with [Pyodide](https://pyodide.org) (Python compiled to WebAssembly), so worksheet numbers match the local version. With `scripts/server.py` the same page asks the local server instead and can download PDF files.
- `scripts/build_site.py`: checks the generator in every language and builds `_site/`. GitHub Actions (`.github/workflows/pages.yml`) publishes it on every push to `main`. Use `python scripts/build_site.py --serve` to preview it.
- `scripts/check_layout.py`: renders worksheets in every language and checks that every page fits A4.
- `fonts/`: Nunito, plus M PLUS Rounded 1c for Greek letters (both under the SIL Open Font License, see `fonts/OFL-*.txt`). `scripts/fetch_fonts.py` downloads them again.

## Why it looks like this

Black and white, a worked example on grey, one icon per action, little on a page: every choice has a reason, with research where there is research — including for children with ADHD, autism and dyslexia. See [DESIGN.md](DESIGN.md).

## Contributing

Help is welcome: bug reports, new tasks and topics, translations by native speakers, accessibility.
Please read [CONTRIBUTING.md](CONTRIBUTING.md) first — it lists the project principles (free, no tracking, simple,
printable, own work), how to make a change and the checks every pull request must pass.
Issues and pull requests can be written in English, Ukrainian or Russian.

## License: free for learning, not for resale

Let's Practice is free for children, families, teachers, tutors, nurseries, and schools — public and private.

You can generate, print, and share worksheets for free, including in paid lessons, and run the project on your own computer or
school network. You can also study the source code and share non-commercial modifications with attribution.

**You may not sell the project or a copy of it, offer it as a paid or ad-funded service, or sell its worksheets without written permission.**

See [LICENSE.md](LICENSE.md) for the full terms. This is a source-available license, not an OSI open-source license.
The fonts keep their own SIL Open Font License.

Our principle: **education should be accessible, not locked behind a paywall.**
