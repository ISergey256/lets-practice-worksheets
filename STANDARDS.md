# Let's Practice — worksheet standard

[Читать по-русски](STANDARDS.ru.md) · Reasons and research: [DESIGN.md](DESIGN.md)

**Goal: every child can succeed, and success makes them want to do more and harder.**
Every task, page and card must follow this standard. Pull requests refer to rules by their number (e.g. "fixes D2").

Sizes are given in px of the A4 page (794 × 1123 px, printed at 96 dpi): **1 pt = 1.33 px**.

## Where the numbers come from

| Source | What it sets | |
|---|---|---|
| **Ukraine** — MON letters 2022 and 2018 for grade 1 | primer 20 pt; other subjects incl. maths 17 pt sans-serif; extra text 15 pt; line spacing +2 pt; ≤ 3 colours for highlights; minimal decoration; clear, distinct icons; realistic contour drawings | [2022][ua22], [2018][ua18] |
| **Russia** — SanPiN for school editions | grades 1–4: 12–18 pt; text over 200 characters on a grey/colour background 2 pt larger; no narrow fonts; ≤ 4 font variants | [secondary summary only][ru] — primary text not yet verified |
| **Europe** — Inclusion Europe "Information for all" | sans-serif ≥ 14 pt; no italics; no words in capitals; no background pictures/patterns; little text per page; left-aligned; page numbers; pictures next to the text, one style; numbers as digits; short positive sentences | [standard][ie] |
| **UK** — British Dyslexia Association (via Dyslexia Scotland) | sans-serif 12–14 pt+; light, not white background; no italics | [guide][bda] |
| **Accessibility** — WCAG 2.1 | colour is never the only cue; contrast | [1.4.1][wcag] |
| **Research** | decorations distract (stronger in autism); worked examples; visual supports; ~80 % success rate; praise effort; self-monitoring | see [DESIGN.md](DESIGN.md) |

Where the sources differ we take **the strictest**: e.g. 17 pt (Ukraine) for child-facing text, not 12–14 pt.

## T — Text

| # | Rule | Source |
|---|---|---|
| T1 | Font: Nunito (rounded sans-serif); Greek: M PLUS Rounded 1c. No serif, no narrow fonts, **no italics**. | UA, RU, IE, BDA |
| T2 | Text the **child reads** (task words, sentences, labels in a task): **≥ 23 px (17 pt)** for Reception and Year 1, ≥ 20 px (15 pt) from Year 2. | UA 2022 |
| T3 | Numbers the child reads or writes: ≥ 24 px; answer boxes ≥ 44 px, so a child's handwriting fits. | UA 2022, practice |
| T4 | Text for the **adult** (instruction next to the icon, answer page, hints): ≥ 16 px (12 pt), dark grey or black. | BDA |
| T5 | Line height ≥ 1.35 (≈ +2 pt). | UA 2022 |
| T6 | Left-aligned; no hyphenation; a word is never split between lines. | IE |
| T7 | No words in CAPITALS (except digits and symbols). | IE |
| T8 | No running text longer than 200 characters on a grey background. | RU (secondary) |
| T9 | Numbers as digits (except the task "numbers in words"). | IE |

## L — Page layout

| # | Rule | Source |
|---|---|---|
| L1 | A4 portrait, 40 px margins, black and white. Fits A4 in **every** language (`check_layout.py`). | practice |
| L2 | One task = one framed section: number in a black circle → action icon → short instruction. | UA 2018 (consistent signs) |
| L3 | At most **2 tasks per page** in Reception, **3** in Year 1, **4** from Year 2. | IE, CHADD, practice |
| L4 | Items per task: 3–6 in Reception, 3–8 in Year 1. | practice |
| L5 | Page number on every page: "1 / 4", bottom right. | IE |
| L6 | The last task on a page may stretch, but keeps together under its title (spare space above and below). | practice |
| L7 | A worksheet takes about 15–20 minutes and is at most 4 pages (+ answers). | practice |

## G — Graphics and colour

| # | Rule | Source |
|---|---|---|
| G1 | Black on white. Grey only for: the worked example, dots to trace, the coloured example in a colouring task. Colour never carries meaning. | UA (≤ 3 colours), WCAG, research |
| G2 | **No decoration.** A picture appears only if the task needs it (to count, compare, match …). No background pictures or patterns. | IE, UA 2018, Fisher, Hanley |
| G3 | Simple contour drawings in one style; real, recognisable objects with their key details; the same thing always has the same picture. | UA 2018, IE |
| G4 | Pictures are big enough to count without effort: ≥ 22 px per object, never touching each other. | practice |
| G5 | Print tip for dyslexia: cream or pastel paper (the page itself stays white to save ink). | BDA |

## I — Icons

| # | Rule | Source |
|---|---|---|
| I1 | Every task in every stage has exactly one **action icon** from the fixed set: count, circle, match, colour, trace, write, tick, cross out, draw. | NCAEP (visual supports), UA 2018 |
| I2 | One icon = one action, everywhere. A new action needs a new icon, agreed in an issue first. | UA 2018 |
| I3 | The adult instruction next to the icon names the same action. | IE |

## D — Difficulty, success and motivation

| # | Rule | Source |
|---|---|---|
| D1 | The **first item of every task is solved**, on grey ("do it like this"). Exactly one example. | worked examples, Rosenshine |
| D2 | Items go from **easy to harder** inside a task (after the example: the easiest first). | Rosenshine (small steps) |
| D3 | Aim for about **80 % success**: all items stay inside the stage's range; nothing from a later term without a label. | Rosenshine |
| D4 | Optional **challenge item ★** at the end of a task, clearly marked; leaving it out is never a "mistake". | SDT (optimal challenge) |
| D5 | Every task has **exactly one correct answer**, shown on the answer page with the curriculum tag. | practice |
| D6 | **"Done" box** next to every task title for the child to tick; cheat cards end with "I can do it!". | self-monitoring (Gaastra 2016) |
| D7 | Words praise **effort and strategy**, never ability: "I practised", "I checked", never "clever". | Mueller & Dweck 1998 |
| D8 | The way forward is visible: the answer page and the site offer "**next: a bit harder**" (next level or term). | SDT (competence) |
| D9 | The child or parent **chooses** (topics, order of tasks); a sheet never punishes skipping. | SDT (autonomy) |

## W — Wording

| # | Rule | Source |
|---|---|---|
| W1 | Instructions: imperative, ≤ 8 words per sentence, at most 2 sentences, positive ("Circle …", not "Don't …"). | IE |
| W2 | Same action → same words in every task and language. | IE |
| W3 | All texts live in `scripts/i18n.py`; every language has every text; native speakers check them. | project |

## A — Website and accessibility

| # | Rule | Source |
|---|---|---|
| A1 | WCAG 2.1 AA: contrast ≥ 4.5 : 1, keyboard use, visible focus, page language, no colour-only cues. | WCAG |
| A2 | Touch targets ≥ 44 × 44 px. | WCAG 2.5.5 (AAA, practice) |
| A3 | Off-white background option for the on-screen preview. | BDA |
| A4 | No accounts, payments, ads, trackers or data collection. | project principles |

## C — Cheat-sheet cards

| # | Rule |
|---|---|
| C1 | One card per task type, half an A4 page, always: Look → Do (≤ 3 steps) → Check → Try → "I can do it!". |
| C2 | Numbers differ from the worksheet's, so a card never gives away its answers. |
| C3 | The worked example in "Look" reads left to right on one line. |

## Checklist for a new task

- [ ] action icon (I1) and solved first item on grey (D1)
- [ ] items from easy to harder (D2), inside the stage range (D3)
- [ ] child-facing text ≥ 23 px (T2), adult text ≥ 16 px (T4), no capitals or italics (T1, T7)
- [ ] pictures only if needed, one style, ≥ 22 px (G2–G4)
- [ ] one correct answer on the answer page with a curriculum tag (D5)
- [ ] all texts in `i18n.py` (W3); instruction ≤ 8 words per sentence (W1)
- [ ] `python scripts/measure_topics.py` and `python scripts/check_layout.py` pass (L1)

[ua22]: https://osvita.ua/legislation/Ser_osv/87720/
[ua18]: https://osvita.ua/legislation/Ser_osv/59221/
[ru]: https://mel.fm/vospitaniye/eksperty/8415920-v-shkolnom-uchebnike-ochen-melky-shrift-kakovy-normy-i-kuda-mozhno-pozhalovatsya
[ie]: https://www.inclusion-europe.eu/easy-to-read-standards-guidelines/
[bda]: https://dyslexiascotland.org.uk/dyslexia-friendly-typed-formats
[wcag]: https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html
