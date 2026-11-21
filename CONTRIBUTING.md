# Contributing to Let's Practice

Thank you for wanting to help! Let's Practice is a free project: printable learning materials for every child, with
no sign-up, subscriptions, ads or hidden payments. Every contribution must keep it that way.

Issues and pull requests can be written in English, Ukrainian or Russian.

## 1. Project principles (a pull request that breaks one of them will not be merged)

1. **Free and private.** No accounts, payments, ads, trackers, analytics, cookies or collection of personal data.
   No calls to external services except the pinned Pyodide CDN the site already uses.
2. **Simple.** A parent must understand the site without instructions; a child must understand a task without reading
   (Reception and Year 1: action icon + worked example on grey). Simplicity beats features.
3. **Printable and calm.** Black and white, A4, Nunito font, 2.5 px outlines, simple outline pictures (no photos, no emoji
   on worksheets, no decorations without a purpose). Every page must fit A4 in every language.
4. **Correct and unambiguous.** Every generated task has exactly one correct answer, and the answer page shows it.
5. **Curriculum-based.** Tasks follow a published curriculum (first the National Curriculum for England) and are tagged
   with the year and term when the topic is taught.
6. **Own work only.** Do not copy tasks, pictures or texts from textbooks, White Rose Maths, TES, NRICH or other
   copyrighted sources. Using the official curriculum documents (gov.uk, Open Government Licence) as a reference is fine.
7. **No children's personal data.** Never attach photos of real children or worksheets with names.

Every task, page and card must also follow the numbered rules of [STANDARDS.md](STANDARDS.md)
(text sizes, icons, worked example, easy → harder, page limits …). Open items are listed in [ROADMAP.md](ROADMAP.md).

## 2. What is welcome

- Bug reports and fixes (wrong answers, ambiguous tasks, layout problems, broken site).
- New task types and topics (please open an issue first, see below).
- Translations and corrections by native speakers — very welcome, the current translations were not made by native speakers.
- Accessibility improvements (keyboard, screen readers, contrast) and simplifications.

Please **open an issue before** a big change (a new topic, a new stage, a change of the site layout or of the
architecture), so we can agree on it before you spend time on it. Small fixes can go straight to a pull request.

## 3. How to make a change

1. Fork the repository and create a branch from `main` (`fix-number-line`, `topic-money-y1`, ...).
2. Install: `pip install playwright pypdf && playwright install chromium`.
3. Make the change. Where things live:
   - `scripts/generate.py` — Year 1 review sheet (18 tasks), page layout, CSS;
   - `scripts/stages.py` — Reception and Year 1 Autumn sheets (icon-led tasks);
   - `scripts/cheats.py` — cheat-sheet cards;
   - `scripts/topics.py` — topics (year, term, strand) and sheets made of chosen topics;
   - `scripts/i18n.py` — **all** texts in all languages;
   - `site/index.html` — the website (one file, no build step, no frameworks).
4. Rules for code:
   - The generator uses only the Python standard library: it also runs in the browser (Pyodide). No new dependencies
     without discussing them in an issue first.
   - **Do not change the order of random calls in existing tasks** — worksheet numbers would then produce different
     sheets for everyone. Add new random calls only in new tasks.
   - Every text a child or a parent reads goes into `i18n.py`, never into the code. If you do not speak a language,
     put the English text there and write "needs translation" in the pull request; `python scripts/i18n.py` must pass.
   - Every new task gets its answer on the answer page and a curriculum tag.
   - Python: PEP 8, lines up to 120 characters, comments in English. Keep functions short and readable.
5. Check before opening the pull request:
   ```
   python scripts/i18n.py            # all languages have all texts
   python scripts/measure_topics.py  # after changing a task: re-measure topic heights (commit topic_heights.json)
   python scripts/build_site.py      # every level, language and cheat card builds
   python scripts/check_layout.py    # every page fits A4 in every language (must print "all ... pages fit")
   python scripts/generate.py --level R --seed 7    # look at the PNG previews in out/
   ```
6. Commit messages in English, imperative mood, explaining *why* (`Fix ambiguous answer in number walls`).
7. Open the pull request and fill in the template. Add screenshots of the pages you changed.

The same checks run automatically on every pull request. After the pull request is merged into `main`,
the website is updated automatically.

## 4. Review

The maintainer reviews every pull request and may ask for changes. A pull request is merged when it follows the
principles above, the checks pass, and the pages look right. Please keep pull requests small and about one thing;
they are much easier to review. AI tools may be used, but you are responsible for checking everything they produce.

## 5. License of contributions

Let's Practice is published under the [Let's Practice Community License](LICENSE.md): free for learning, not for resale.
By opening a pull request you confirm that:

- the contribution is your own work, or you have the right to submit it;
- it is licensed under the Let's Practice Community License, the same as the rest of the project;
- the maintainer may also distribute it under future versions of that license and include it when granting the
  additional permissions described in Section 9 of the license.

## 6. Be kind

This project is for children. Be patient and respectful in issues and reviews; criticise ideas, not people.
