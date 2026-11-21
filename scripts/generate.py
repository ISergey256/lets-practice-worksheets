"""Generator of "LET'S PRACTICE!" maths worksheets: 18 tasks, 3 levels, several languages.

Usage:
    pip install playwright pypdf && playwright install chromium
    python scripts/generate.py --level 2              # random worksheet, level 2
    python scripts/generate.py --level 3 --seed 42    # reproducible worksheet
    python scripts/generate.py --level 1 --count 3    # three different worksheets
    python scripts/generate.py --lang uk --answers-lang ru   # tasks in Ukrainian, answers in Russian
    python scripts/server.py                          # the same in a local website (UI)

Languages (both default to English): see i18n.LANGS. The numbers and pictures of a worksheet
depend only on level and seed, so the same number gives the same sheet in every language.

Fonts: python scripts/fetch_fonts.py once -> fonts/ (works offline afterwards).

Levels:
    1 - easy:   numbers to 10, addition/subtraction within 10, halves
    2 - medium: numbers to 20, quarters
    3 - hard:   numbers to 100, adding/subtracting across ten, thirds and
                three quarters, bigger number walls, more objects to count

Output (in out/):  Worksheet_L<level>_<seed>_<lang>.pdf, ..._answers_<answers-lang>.pdf
plus PNG previews of every page. Check the PNGs: nothing must be cut off at the bottom.
"""
import argparse
import asyncio
import math
import os
import random
from pathlib import Path

import i18n
from i18n import SHY, text

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
FONTS = ROOT / "fonts"

LEVEL_NAMES = {1: "Easy", 2: "Medium", 3: "Hard", "R": "Reception", "Y1A": "Year 1 autumn"}


class Lang:
    """Worksheet language (w, what the child reads) and answer language (a, for parents)."""

    def __init__(self, lang=i18n.DEFAULT, answers_lang=i18n.DEFAULT):
        if lang not in i18n.LANGS or answers_lang not in i18n.LANGS:
            raise ValueError(f"language must be one of {', '.join(i18n.LANGS)}")
        self.wl, self.al = lang, answers_lang
        self.w, self.a = i18n.W[lang], i18n.A[answers_lang]

FONT_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Nunito:wght@600;700;800;900&display=swap">')

CSS = """
@page{size:794px 1123px;margin:0}
body{margin:0;font-family:'Nunito','M PLUS Rounded 1c',system-ui,sans-serif;line-height:1.36;color:#111;background:#fff}
.page{position:relative;width:794px;height:1123px;box-sizing:border-box;padding:40px;display:flex;flex-direction:column;gap:9px;background:#fff;overflow:hidden}
.sec{border:2.5px solid #111;border-radius:18px;padding:8px 16px 10px;box-sizing:border-box}
.q{display:flex;align-items:center;gap:10px;font-size:23px;font-weight:800;line-height:1.3;margin:0 0 6px}
.qt{flex:1}
.done{margin-left:auto;width:26px;height:26px;border:2.5px solid #111;border-radius:7px;box-sizing:border-box;flex:none}
.pgno{position:absolute;right:40px;bottom:12px;font-size:14px;font-weight:800}
.sub{margin:-4px 0 10px 40px;font-size:16px;font-weight:700}
.n{width:30px;height:30px;border-radius:50%;background:#111;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:17px;font-weight:900;flex:none}
.box{display:inline-block;width:46px;height:46px;border:2.5px solid #111;border-radius:10px;box-sizing:border-box;background:#fff;flex:none}
.num{display:inline-flex;align-items:center;justify-content:center;min-width:48px;height:48px;border:2.5px solid #111;border-radius:10px;font-size:24px;font-weight:800;padding:0 6px;box-sizing:border-box;flex:none}
.line{border-bottom:2.5px solid #111;flex:1;height:30px}
.th{font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center;height:38px;border-right:2px solid #111}
.td{display:flex;align-items:center;justify-content:center;border-top:2px solid #111;border-right:2px solid #111;font-size:23px;font-weight:800}
.pill{border:2.5px solid #111;border-radius:20px;padding:4px 12px;font-size:22px;font-weight:800;text-align:center}
.bond{display:flex;align-items:center;gap:5px;font-size:24px;font-weight:800;white-space:nowrap}
.bond .box{width:40px;height:40px}
.eq{display:flex;align-items:center;justify-content:center;gap:8px;font-size:28px;font-weight:800;height:62px;border-top:2px solid #111;border-right:2px solid #111;white-space:nowrap}
.eq .box{width:44px;height:44px}
.brick{height:48px;border:2.5px solid #111;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800;box-sizing:border-box;background:#fff}
.row{display:flex;justify-content:center;gap:2px}
.sent{font-size:23px;font-weight:700;line-height:1.4;margin:0}
.blank{display:inline-block;width:120px;border-bottom:2.5px solid #111}
.a{display:flex;gap:12px;align-items:baseline;font-size:16px;font-weight:600;line-height:1.4;padding:5px 0;border-bottom:1.5px solid #bbb}
.a .n{width:28px;height:28px;font-size:15px;transform:translateY(6px)}
.a b{font-weight:900}
.ih{display:flex;align-items:center;gap:12px;margin:0 0 8px}
.ih .n{width:34px;height:34px;font-size:18px}
.ih .it{flex:1;font-size:16px;font-weight:700;color:#333;line-height:1.3}
.opt{position:relative;display:inline-flex;width:56px;height:56px;align-items:center;justify-content:center;font-size:32px;font-weight:900}
.trace{font-size:62px;font-weight:900;line-height:1;color:#c2c2c2;width:52px;text-align:center}
.stretch>.q+:not(.sub),.stretch>.sub+*,.stretch>.ih+*{margin-top:auto}
.stretch>:last-child{margin-bottom:auto}
.card{border:3px solid #111;border-radius:22px;padding:14px 20px;display:flex;flex-direction:column;gap:10px;flex:1;min-height:0}
.ch{display:flex;align-items:center;gap:12px}
.ch .n{width:38px;height:38px;font-size:20px}
.ct{font-size:27px;font-weight:900}
.lab{display:inline-block;background:#111;color:#fff;border-radius:14px;padding:2px 12px;font-size:15px;font-weight:900;align-self:flex-start;flex:none}
.cm{display:flex;gap:18px;align-items:stretch;flex:1;min-height:0}
.cl{flex:1.15;display:flex;flex-direction:column;gap:8px}
.cpic{flex:1;display:flex;align-items:center;justify-content:center;background:#efefef;border-radius:14px;padding:10px}
.cd{flex:1;display:flex;flex-direction:column;gap:12px}
.cs{display:flex;align-items:center;gap:10px;font-size:19px;font-weight:800;line-height:1.25}
.csn{width:32px;height:32px;border-radius:50%;border:2.5px solid #111;display:inline-flex;align-items:center;justify-content:center;font-weight:900;flex:none}
.cc{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:800;border-top:2px dashed #999;padding-top:10px}
.ctr{display:flex;align-items:center;gap:12px;border-top:2px dashed #999;padding-top:10px}
.ican{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:900;flex:none}
.a .tag{flex:none;align-self:center;font-size:11.5px;font-weight:800;border:1.5px solid #111;border-radius:10px;padding:0 7px;white-space:nowrap}
"""

S = 'fill="#fff" stroke="#111" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"'
SN = 'fill="none" stroke="#111" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"'


EX_BG = "#e9e9e9"  # background of the worked example: grey = "do it like this" (STANDARDS D1)
SHADE = "#bdbdbd"  # grey used where an example is coloured in
DONE = '<span class="done"></span>'  # the child ticks it when the task is done (STANDARDS D6)
# action icon of each Year 1 review task (STANDARDS I1); icons are drawn in stages.py
TASK_ACTION = {1: "write", 2: "count", 3: "circle", 4: "write", 5: "write", 6: "write", 7: "write", 8: "count",
               9: "circle", 10: "colour", 11: "tick", 12: "circle", 13: "write", 14: "write", 15: "write",
               16: "write", 17: "write", 18: "write"}


def ring(html, pad=3):
    """A worked example answer: circled, on grey."""
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;border:3px solid #111;'
            f'border-radius:999px;padding:{pad}px;background:{EX_BG}">{html}</span>')


def number_pages(pages):
    """'1 / 4' at the bottom right of every page (STANDARDS L5)."""
    n = len(pages)
    return [p[:-6] + f'<div class="pgno">{i} / {n}</div></div>' for i, p in enumerate(pages, 1)]


def sec(num, title, body, sub="", grow=False):
    import stages  # the action icons live there
    icon = stages.action(TASK_ACTION[num], 40) if num in TASK_ACTION else ""
    s = f'<p class="sub">{sub}</p>' if sub else ""
    if grow:  # the last section fills the rest of the page; centre its content in the spare height
        st = ' style="flex:1;display:flex;flex-direction:column"'
        body = f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">{body}</div>'
    else:
        st = ""
    return (f'<section class="sec"{st}><p class="q"><span class="n">{num}</span>{icon}<span class="qt">{title}</span>{DONE}</p>'
            f'{s}{body}</section>')


def box(w=46, h=None, r=10):
    h = h or w
    return f'<span class="box" style="width:{w}px;height:{h}px;border-radius:{r}px"></span>'


def filled(v, w=46, ex=False):
    """An answer box with the answer already written in (a worked example; ex=True puts it on grey)."""
    bg = f";background:{EX_BG}" if ex else ""
    return (f'<span class="box" style="width:{w}px;height:{w}px;display:inline-flex;align-items:center;'
            f'justify-content:center;font-size:22px;font-weight:800{bg}">{v}</span>')


def num(v):
    return f'<span class="num">{v}</span>'


def join_list(xs):
    return ", ".join(str(x) for x in xs)


# ---------------------------------------------------------------- icons
# Each icon: (svg body drawn from 0,0, width, height); names are in i18n W["what"] / A["what"]
ICONS = {
    "fish": ('<path d="M56 25 L76 10 L72 25 L76 40 Z"/><path d="M30 11 Q38 1 46 12" fill="none"/>'
             '<ellipse cx="34" cy="25" rx="25" ry="16"/><circle cx="21" cy="21" r="2.8" fill="#111" stroke="none"/>'
             '<path d="M13 29 Q17 33 22 30" fill="none"/><path d="M38 17 Q45 25 38 33" fill="none"/>',
             80, 44),
    "apple": ('<path d="M25 4 L25 14" fill="none"/><path d="M27 8 Q36 1 42 7 Q34 13 27 8 Z"/>'
              '<path d="M25 14 C14 6 2 14 4 28 C6 42 16 50 25 46 C34 50 44 42 46 28 C48 14 36 6 25 14 Z"/>'
              '<path d="M12 24 Q12 18 17 16" fill="none"/>', 50, 50),
    "star": ('<path d="M25 3 L31 18 L47 19 L35 29 L39 45 L25 36 L11 45 L15 29 L3 19 L19 18 Z"/>'
             '<circle cx="21" cy="25" r="1.8" fill="#111" stroke="none"/><circle cx="29" cy="25" r="1.8" fill="#111" stroke="none"/>',
             50, 48),
    "flower": ('<path d="M25 30 L25 49 M25 42 Q33 36 38 40 Q32 46 25 42" fill="none"/>'
               '<circle cx="25" cy="7" r="7"/><circle cx="36" cy="15" r="7"/><circle cx="32" cy="28" r="7"/>'
               '<circle cx="18" cy="28" r="7"/><circle cx="14" cy="15" r="7"/><circle cx="25" cy="18" r="6.5"/>',
               50, 50),
    # beach ball: segments meet at the poles, reads as a ball even when drawn small
    "ball": ('<circle cx="25" cy="25" r="22"/><path d="M25 3 Q11 25 25 47 M25 3 Q39 25 25 47 M25 3 L25 47" fill="none"/>'
             '<path d="M10 17 Q12 11 17 8" fill="none"/>',
             50, 50),
    "heart": ('<path d="M25 44 C8 32 2 22 6 13 C10 4 21 4 25 13 C29 4 40 4 44 13 C48 22 42 32 25 44 Z"/>'
              '<path d="M12 16 Q13 11 18 10" fill="none"/>', 50, 48),
}


def icon_defs(key, pid):
    body, w, h, *_ = ICONS[key]
    return f'<defs><g id="{pid}" {S}>{body}</g></defs>'


# ---------------------------------------------------------------- task 1: count
def task_count(rng, lvl, L, key):
    n = {1: rng.randint(4, 9), 2: rng.randint(6, 12), 3: rng.randint(12, 20)}[lvl]
    _, w, h = ICONS[key]
    W = 380
    rows = 2 if n <= 10 else 3
    per = [n // rows + (1 if i < n % rows else 0) for i in range(rows)]
    cols = max(per)
    cw = W / cols
    sc = min(1.0, (cw - 10) / w, (46 if rows == 2 else 35) / h)
    gap, jit = (6, 4) if rows == 2 else (3, 2)  # 3 rows: tighter rows so page 1 still fits
    rh = h * sc + gap
    H = rows * rh + 4
    uses = []
    for r, cnt in enumerate(per):
        off = (cols - cnt) * cw / 2 + (cw / 4 if r % 2 and cnt == cols and cols > 1 else 0)
        off = min(off, W - cnt * cw)
        for c in range(cnt):
            x = off + c * cw + (cw - w * sc) / 2 + rng.uniform(-4, 4)
            y = 2 + r * rh + rng.uniform(0, jit)
            uses.append(f'<use href="#c1" transform="translate({x:.1f},{y:.1f}) scale({sc:.2f})"/>')
    svg = (f'<svg width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">{icon_defs(key, "c1")}'
           + "".join(uses) + "</svg>")
    import stages
    example = (f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;background:{EX_BG};'
               f'border-radius:12px;padding:8px 10px">{stages.objects(key, 3, 24)}{filled(3, 40)}</div>')
    body = (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 6px">'
            f'{example}{svg}{box(76, r=14)}</div>')
    return sec(1, text(L.w["t1"], what=L.w["what"][key]), body), f'{L.a["what"][key]}: <b>{n}</b>'


# ---------------------------------------------------------------- task 2: estimate
def task_estimate(rng, lvl, L, key):
    n = {1: rng.randint(6, 10), 2: rng.randint(10, 16), 3: rng.randint(16, 24)}[lvl]
    _, w, h = ICONS[key]
    shelves = 2 if n <= 16 else 3
    base = [n // shelves] * shelves
    for i in range(n % shelves):
        base[i] += 1
    if shelves == 2 and n > 6 and base[0] < 8:  # make shelves uneven like the original
        d = rng.randint(0, min(2, 8 - base[0], base[1] - 2))
        base = [base[0] + d, base[1] - d]
    step = 56
    W, rowh = 460, 66
    parts = []
    for r, cnt in enumerate(base):
        x0 = 8 + rng.randint(0, max(0, int((W - 10 - cnt * step) // 2)))
        y = 8 + r * rowh
        for c in range(cnt):
            parts.append(f'<use href="#c2" transform="translate({x0 + c * step},{y}) scale({50 / max(w, h):.2f})"/>')
        parts.append(f'<line x1="0" y1="{y + 53}" x2="{W - 10}" y2="{y + 53}" stroke="#111" stroke-width="3"/>')
    H = shelves * rowh + 2
    sc = 0.9 if shelves == 2 else 0.62
    svg = (f'<svg width="{W * sc:.0f}" height="{H * sc:.0f}" viewBox="0 0 {W} {H}">{icon_defs(key, "c2")}'
           + "".join(parts) + "</svg>")
    import stages
    lab = 'display:flex;flex-direction:column;align-items:center;gap:8px;font-size:23px;font-weight:800'
    lab_s = 'display:flex;flex-direction:column;align-items:center;gap:4px;font-size:15px;font-weight:800'
    example = (f'<div style="display:flex;align-items:center;gap:14px;background:{EX_BG};border-radius:12px;padding:6px 12px;'
               f'margin-bottom:8px;width:max-content">{stages.objects(key, 6, 22, 6, 4)}'
               f'<div style="{lab_s}">{L.w["estimate"]}{filled(5, 36)}</div><div style="{lab_s}">{L.w["counted"]}{filled(6, 36)}</div></div>')
    body = (f'{example}<div style="display:flex;align-items:center;justify-content:space-between">{svg}'
            f'<div style="display:flex;gap:22px;border-left:2.5px solid #111;padding-left:20px">'
            f'<div style="{lab}">{L.w["estimate"]}{box(70, r=14)}</div><div style="{lab}">{L.w["counted"]}{box(70, r=14)}</div>'
            f'</div></div>')
    return sec(2, text(L.w["t2"], what=L.w["what"][key]), body), f'{L.a["what"][key]}: <b>{n}</b>'


# ---------------------------------------------------------------- task 3: odd / even
def task_odd_even(rng, lvl, L):
    lo, hi = {1: (1, 10), 2: (1, 20), 3: (11, 60)}[lvl]
    want_odd = rng.random() < 0.5
    while True:
        xs = sorted(rng.sample(range(lo, hi + 1), 10))
        hits = [x for x in xs if (x % 2 == 1) == want_odd]
        if 3 <= len(hits) <= 7:
            break
    body = ('<div style="display:flex;justify-content:space-between;align-items:center;padding:0 4px">'
            + "".join(ring(num(x)) if x == hits[0] else num(x) for x in xs) + "</div>")
    title = L.w["t3_odd"] if want_odd else L.w["t3_even"]
    return sec(3, title, body), f'{L.a["odd" if want_odd else "even"]}: <b>{join_list(hits[1:])}</b>'


# ---------------------------------------------------------------- task 4: number line
def task_number_line(rng, lvl, L):
    if lvl == 1:
        start, step = rng.choice([0, 0, 1, 2]), 1
    elif lvl == 2:
        start, step = rng.randint(1, 10), 1
    else:
        step = rng.choice([1, 2, 5, 10])
        start = {1: rng.randint(20, 85), 2: rng.choice(range(0, 81, 2)),
                 5: rng.choice(range(0, 51, 5)), 10: rng.choice(range(0, 11))}[step]
        if step == 10:  # 11 marks in 10s fit into 0..100 only from 0 (rng call kept: same sheets elsewhere)
            start = 0
    vals = [start + i * step for i in range(11)]
    k = 5 if lvl == 3 else 4
    candidates = list(range(2, 11)) if step > 1 else list(range(1, 11))
    while True:
        miss = sorted(rng.sample(candidates, k))
        gaps = [b - a for a, b in zip(miss, miss[1:])]
        if all(g > 1 for g in gaps) or (lvl == 3 and not any(g1 == g2 == 1 for g1, g2 in zip(gaps, gaps[1:]))):
            break
    xs = [40 + 62 * i for i in range(11)]
    dots = "".join(f'<circle cx="{x}" cy="22" r="6"/>' for x in xs)
    ex = miss[0]  # worked example
    rects = "".join(f'<rect x="{xs[i] - 24}" y="42" width="48" height="40" rx="9"{" fill=" + chr(34) + EX_BG + chr(34) if i == ex else ""}/>'
                    for i in miss)
    texts = "".join(f'<text x="{xs[i]}" y="70">{vals[i]}</text>' for i in range(11) if i not in miss or i == ex)
    svg = ('<svg width="672" height="88" viewBox="0 0 704 92" style="font-weight:800">'
           '<line x1="12" y1="22" x2="692" y2="22" stroke="#111" stroke-width="3"/>'
           '<path d="M4 22 L18 14 L18 30 Z" fill="#111"/><path d="M700 22 L686 14 L686 30 Z" fill="#111"/>'
           f'<g fill="#111">{dots}</g><g fill="#fff" stroke="#111" stroke-width="2.5">{rects}</g>'
           f'<g font-size="24" text-anchor="middle" fill="#111">{texts}</g></svg>')
    return (sec(4, L.w["t4"], svg),
            f"<b>{join_list(vals[i] for i in miss[1:])}</b>" + (f' ({text(L.a["step"], s=step)})' if step > 1 else ""))


# ---------------------------------------------------------------- task 5: compare
def task_compare(rng, lvl, L):
    lo, hi = {1: (0, 10), 2: (0, 20), 3: (10, 99)}[lvl]
    pairs = []
    eq_pos = rng.randrange(4) if rng.random() < 0.7 else -1
    for i in range(4):
        a = rng.randint(lo, hi)
        if i == eq_pos:
            b = a
        elif lvl == 3 and rng.random() < 0.5 and a % 10 != a // 10:
            b = int(str(a)[::-1]) if a >= 10 and a % 10 else a + rng.choice([-1, 1, 2])  # 47 vs 74
        else:
            b = rng.randint(lo, hi)
            while b == a:
                b = rng.randint(lo, hi)
        pairs.append((a, b))
    pairs.sort(key=lambda ab: (ab[0] == ab[1], -abs(ab[0] - ab[1])))  # big differences first, equal last (STANDARDS D2)
    sep = '<span style="width:2.5px;height:48px;background:#111"></span>'
    sym = lambda a, b: "&lt;" if a < b else ("&gt;" if a > b else "=")
    items = [f'<div style="display:flex;gap:6px">{num(a)}{filled(sym(a, b), 48, ex=True) if i == 0 else box(48)}{num(b)}</div>'
             for i, (a, b) in enumerate(pairs)]
    body = ('<div style="display:flex;justify-content:space-between;align-items:center;padding:0 4px">'
            + sep.join(items) + "</div>")
    return (sec(5, L.w["t5"], body),
            "<b>" + ", ".join(f"{a} {sym(a, b)} {b}" for a, b in pairs[1:]) + "</b>")


# ---------------------------------------------------------------- task 6: words
def task_words(rng, lvl, L):
    lo, hi = {1: (0, 10), 2: (3, 20), 3: (13, 99)}[lvl]
    xs = sorted(rng.sample(range(lo, hi + 1), 4))  # easy to harder (STANDARDS D2)
    cell = '<div style="display:flex;align-items:flex-end;gap:12px">{}{}</div>'
    written = (f'<span style="flex:1;border-bottom:2.5px solid #111;background:{EX_BG};border-radius:8px 8px 0 0;'
               f'padding:0 8px;font-size:23px;font-weight:800">{i18n.numwords(L.wl, xs[0])}</span>')
    body = ('<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px;row-gap:10px">'
            + "".join(cell.format(num(x), written if i == 0 else '<span class="line"></span>') for i, x in enumerate(xs)) + "</div>")
    return (sec(6, L.w["t6"], body, grow=True),  # the child writes the words in the worksheet language
            "<b>" + ", ".join(i18n.numwords(L.wl, x) for x in xs[1:]) + "</b>")


# ---------------------------------------------------------------- task 7: 3D shapes
SHAPES3D = {
    "cube": ('<g ' + S + '><path d="M14 26 L28 14 L68 14 L54 26 Z"/><path d="M54 26 L68 14 L68 54 L54 66 Z"/>'
             '<rect x="14" y="26" width="40" height="40"/></g>', 6, 12),
    "cuboid": ('<g ' + S + '><path d="M8 26 L24 12 L74 12 L58 26 Z"/><path d="M58 26 L74 12 L74 46 L58 60 Z"/>'
               '<rect x="8" y="26" width="50" height="34"/></g>', 6, 12),
    "cone": ('<g ' + S + '><path d="M14 56 L40 6 L66 56"/><ellipse cx="40" cy="56" rx="26" ry="8"/></g>',
             2, 1),
    "cylinder": ('<g ' + S + '><path d="M18 14 L18 56 A22 7 0 0 0 62 56 L62 14"/>'
                 '<path d="M18 56 A22 7 0 0 1 62 56" fill="none" stroke-dasharray="4 4"/>'
                 '<ellipse cx="40" cy="14" rx="22" ry="7"/></g>', 3, 2),
    "sphere": ('<g ' + S + '><circle cx="40" cy="35" r="28"/>'
               '<path d="M12 35 A28 8 0 0 0 68 35" fill="none"/><path d="M12 35 A28 8 0 0 1 68 35" fill="none" stroke-dasharray="4 4"/></g>',
               1, 0),
    "pyramid": ('<g ' + SN + '><path d="M30 48 L72 48 L40 6 Z" stroke-dasharray="4 4"/>'
                '<path d="M8 60 L50 60 L72 48 L40 6 Z M40 6 L8 60 M40 6 L50 60"/>'
                '<path d="M8 60 L30 48" stroke-dasharray="4 4"/></g>', 5, 8),
    "prism": ('<g ' + SN + '><path d="M8 62 L30 26 L52 62 Z M30 26 L52 12 L74 48 L52 62"/>'
              '<path d="M8 62 L30 48 L74 48 M30 48 L52 12" stroke-dasharray="4 4"/></g>',
              5, 9),
}


def task_3d(rng, lvl, L):
    pool = ["cube", "sphere", "cylinder", "cone"] if lvl == 1 else list(SHAPES3D)
    picks = rng.sample(pool, 3)
    rows = []
    for i, k in enumerate(picks):
        svg = f'<svg width="64" height="56" viewBox="0 0 80 70">{SHAPES3D[k][0]}</svg>'
        if i == 0:  # worked example
            bg = f"background:{EX_BG};"
            rows.append(f'<div class="td" style="height:58px;{bg}">{svg}</div>'
                        f'<div class="td" style="{bg}font-size:22px">{L.w["shapes3d"][k]}</div>'
                        f'<div class="td" style="{bg}">{filled(SHAPES3D[k][1], 40)}</div>'
                        f'<div class="td" style="{bg}border-right:none">{filled(SHAPES3D[k][2], 40)}</div>')
            continue
        rows.append(f'<div class="td" style="height:58px">{svg}</div>'
                    '<div class="td" style="padding:0 16px 16px;align-items:flex-end"><span style="border-bottom:2.5px solid #111;width:100%"></span></div>'
                    f'<div class="td">{box(40)}</div><div class="td" style="border-right:none">{box(40)}</div>')
    bank = picks[:]
    if lvl >= 2:
        bank.append(rng.choice([k for k in SHAPES3D if k not in picks]))
    rng.shuffle(bank)
    names = L.w["shapes3d"]
    h_shape, h_name, h_faces, h_edges = L.w["th3"]

    def pill(word):  # long names get a smaller font; very long ones break at a soft hyphen (&shy;) in i18n
        n = len(word.replace(SHY, ""))
        fs = 19 if n <= 9 else 16 if n <= 12 else 14
        return f'<div class="pill" style="padding:2px 6px;font-size:{fs}px;line-height:1.15;hyphens:manual">{word}</div>'
    body = ('<div style="display:flex;gap:14px;align-items:stretch">'
            '<div style="flex:1;border:2.5px solid #111;border-radius:12px;overflow:hidden;display:grid;grid-template-columns:110px 1fr 86px 86px">'
            f'<div class="th">{h_shape}</div><div class="th">{h_name}</div><div class="th">{h_faces}</div>'
            f'<div class="th" style="border-right:none">{h_edges}</div>'
            + "".join(rows) + "</div>"
            '<div style="width:130px;border:2.5px solid #111;border-radius:12px;padding:6px 8px;box-sizing:border-box;display:flex;flex-direction:column;gap:6px;justify-content:center">'
            f'<div style="background:#111;color:#fff;border-radius:20px;padding:4px 8px;font-size:15px;font-weight:900;text-align:center">{L.w["bank"]}</div>'
            + "".join(pill(names[b]) for b in bank) + "</div></div>")
    ans = "; ".join(f'<b>{names[k]}</b> — {L.a["faces"][k]}' for k in picks[1:])
    if lvl >= 2:
        ans += " (" + text(L.a["extra"], w=names[[b for b in bank if b not in picks][0]]) + ")"
    return sec(7, L.w["t7"], body), ans


# ---------------------------------------------------------------- task 8: 2D shapes in a picture
def task_2d_picture(rng, lvl, L):
    c = {"circle": [], "triangle": [], "square": [], "rect": []}
    el = []

    def add(kind, svg, what):
        c[kind].append(what)
        el.append(svg)

    if lvl >= 2 or rng.random() < 0.7:
        el.append('<g stroke-linecap="round">' + "".join(
            f'<line x1="{42 + 24 * math.cos(a):.1f}" y1="{40 + 24 * math.sin(a):.1f}" x2="{42 + 31 * math.cos(a):.1f}" y2="{40 + 31 * math.sin(a):.1f}"/>'
            for a in [i * math.pi / 4 for i in range(8)]) + "</g>")
        add("circle", '<circle cx="42" cy="40" r="17"/>', "sun")
    square_body = rng.random() < 0.5
    if square_body:
        bx, bw, bh = 90, 110, 110
        add("square", f'<rect x="{bx}" y="120" width="{bw}" height="{bh}"/>', "house")
    else:
        bx, bw, bh = 80, 136, 96
        add("rect", f'<rect x="{bx}" y="134" width="{bw}" height="{bh}"/>', "house")
    top = 230 - bh
    cx = bx + bw / 2
    if rng.random() < 0.6 or lvl == 3:
        add("rect", f'<rect x="{bx + bw - 36}" y="{top - 46}" width="16" height="36"/>', "chimney")
    add("triangle", f'<path d="M{bx - 10} {top} L{cx} {top - 60} L{bx + bw + 10} {top} Z"/>', "roof")
    if rng.random() < 0.5:
        add("circle", f'<circle cx="{cx}" cy="{top - 22}" r="10"/>', "round_window")
    nwin = rng.randint(1, 2) if square_body else rng.randint(2, 3)
    if lvl == 1:
        nwin = min(nwin, 2)
    slots = ([bx + 12, bx + bw - 40] if nwin == 2 else [bx + 12]) if square_body else \
        ([bx + 12, bx + bw - 40] if nwin == 2 else [bx + 12, bx + 54, bx + bw - 40])
    if nwin == 1 and square_body:
        slots = [rng.choice([bx + 12, bx + bw - 40])]
    for x in slots:
        kind = rng.choice(["square", "square", "circle", "rect"] if lvl >= 2 else ["square", "circle"])
        y = top + 12
        if kind == "square":
            add("square", f'<rect x="{x}" y="{y}" width="28" height="28"/>', "window")
        elif kind == "circle":
            add("circle", f'<circle cx="{x + 14}" cy="{y + 14}" r="14"/>', "window")
        else:
            add("rect", f'<rect x="{x + 3}" y="{y}" width="22" height="38"/>', "window")
    dx = cx - 15 if nwin != 3 else bx + bw - 44
    if nwin == 3:
        dx = cx - 15
    add("rect", f'<rect x="{dx}" y="180" width="30" height="50"/>', "door")
    trees = {1: rng.randint(0, 1), 2: rng.randint(1, 2), 3: 2}[lvl]
    spots = [260, 38] if not c["circle"] or "sun" not in c["circle"] else [260]
    for tx in spots[:trees]:
        add("rect", f'<rect x="{tx - 8}" y="182" width="16" height="48"/>', "trunk")
        if rng.random() < 0.5:
            add("triangle", f'<path d="M{tx - 34} 186 L{tx} 138 L{tx + 34} 186 Z"/>', "fir")
            add("triangle", f'<path d="M{tx - 28} 150 L{tx} 108 L{tx + 28} 150 Z"/>', "fir")
        else:
            add("circle", f'<circle cx="{tx}" cy="160" r="28"/>', "crown")
    svg = (f'<svg width="252" height="170" viewBox="0 0 320 240"><g {S}>' + "".join(el) +
           '</g><line x1="4" y1="231" x2="316" y2="231" stroke="#111" stroke-width="3"/></svg>')
    kinds = ("circle", "triangle", "square", "rect")
    h_shape, h_many = L.w["th2"]
    table = ('<div style="flex:1;border:2.5px solid #111;border-radius:12px;overflow:hidden;display:grid;grid-template-columns:1fr 140px">'
             f'<div class="th">{h_shape}</div><div class="th" style="border-right:none">{h_many}</div>'
             + "".join(f'<div class="td" style="height:36px{";background:" + EX_BG if i == 0 else ""}">{n}</div>'
                       f'<div class="td" style="border-right:none{";background:" + EX_BG if i == 0 else ""}">'
                       f'{filled(len(c[kinds[0]]), 32) if i == 0 else box(32, 30)}</div>'
                       for i, n in enumerate(L.w["shapes2d"])) + "</div>")
    body = f'<div style="display:flex;align-items:center;gap:24px">{svg}{table}</div>'

    def expl(k):
        from collections import Counter
        cnt = Counter(L.a["parts"][p] for p in c[k])
        return ", ".join(w if v == 1 else f"{w} ×{v}" for w, v in cnt.items()) or L.a["none"]
    names = list(zip(L.a["shapes2d"], kinds))
    ans = ", ".join(f"{n} <b>{len(c[k])}</b>" for n, k in names)
    ans += " (" + "; ".join(f"{n.lower()}: {expl(k)}" for n, k in names) + ")"
    return sec(8, L.w["t8"], body), ans


# ---------------------------------------------------------------- task 9: polygon with N sides
def polygon(n, r=38, cx=45, cy=45):
    a0 = math.pi / 2 + (math.pi / n if n % 2 == 0 else 0)
    pts = [(cx + r * math.cos(a0 + 2 * math.pi * i / n), cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]
    ys = [p[1] for p in pts]
    shift = (cy - (max(ys) + min(ys)) / 2)
    return "M" + " L".join(f"{x:.1f} {y + shift:.1f}" for x, y in pts) + " Z"


def task_sides(rng, lvl, L):
    pool = {1: [3, 4, 5, 6], 2: [3, 4, 5, 6], 3: [4, 5, 6, 7, 8]}[lvl]
    target = rng.choice(pool[1:] if lvl < 3 else pool)
    others = rng.sample([p for p in pool if p != target], 3)
    order = others + [target]
    rng.shuffle(order)
    svgs = "".join(f'<svg width="74" height="74" viewBox="0 0 90 90"><path d="{polygon(n)}" {SN}/></svg>' for n in order)
    tri = f'<svg width="46" height="46" viewBox="0 0 90 90"><path d="{polygon(3)}" {SN}/></svg>'
    example = (f'<div style="display:flex;align-items:center;gap:8px;background:{EX_BG};border-radius:12px;padding:6px 12px">'
               f'<span style="font-size:24px;font-weight:900">3</span>{ring(tri, 2)}</div>')
    body = (f'<div style="display:flex;justify-content:space-around;align-items:center">{example}'
            f'<span style="width:2.5px;align-self:stretch;background:#111"></span>{svgs}</div>')
    ans = text(L.a["poly_ans"], name=L.a["poly"][target], nth=L.a["nth"][order.index(target)])
    return sec(9, text(L.w["t9"], n=target), body), ans[0].upper() + ans[1:]


# ---------------------------------------------------------------- fraction shapes
def frac_shape(kind, d, equal=True, rng=None, shade=0):
    """Return svg for a shape cut into d parts (equal or not); the first `shade` parts of an equal shape are shaded."""
    lines, regions = [], []
    if kind == "circle":
        if equal:
            angs = [-90 + 360 * i / d for i in range(d)]
        else:
            base = [-90 + 360 * i / d for i in range(d)]
            angs = [base[0]] + [a + rng.choice([-1, 1]) * rng.uniform(25, 40) for a in base[1:]]
        if d == 2 and not equal:
            lines.append('<line x1="6" y1="30" x2="94" y2="30"/>')
        else:
            for a in angs:
                t = math.radians(a)
                lines.append(f'<line x1="50" y1="50" x2="{50 + 44 * math.cos(t):.1f}" y2="{50 + 44 * math.sin(t):.1f}"/>')
            pt = lambda a: f"{50 + 44 * math.cos(math.radians(a)):.1f} {50 + 44 * math.sin(math.radians(a)):.1f}"
            for i in range(shade):
                a0, a1 = angs[i], angs[i] + 360 / d
                regions.append(f'<path d="M50 50 L{pt(a0)} A44 44 0 0 1 {pt(a1)} Z"/>')
        return (f'<svg width="86" height="86" viewBox="0 0 100 100"><g fill="{SHADE}" stroke="none">{"".join(regions)}</g>'
                f'<g {SN}><circle cx="50" cy="50" r="44"/>{"".join(lines)}</g></svg>')
    if kind == "square":
        if d == 4 and equal:
            lines = ['<line x1="50" y1="6" x2="50" y2="94"/>', '<line x1="6" y1="50" x2="94" y2="50"/>']
            quads = [(6, 6), (50, 6), (50, 50), (6, 50)]
            regions = [f'<rect x="{x}" y="{y}" width="44" height="44"/>' for x, y in quads[:shade]]
        elif d == 4:
            a, b = rng.choice([(30, 62), (64, 36), (34, 34)])
            lines = [f'<line x1="{a}" y1="6" x2="{a}" y2="94"/>', f'<line x1="6" y1="{b}" x2="94" y2="{b}"/>']
        elif d == 2 and equal:
            diagonal = rng.random() < 0.5
            lines = ['<line x1="6" y1="6" x2="94" y2="94"/>' if diagonal else '<line x1="50" y1="6" x2="50" y2="94"/>']
            if shade:
                regions = ['<path d="M6 6 L94 94 L6 94 Z"/>' if diagonal else '<rect x="6" y="6" width="44" height="88"/>']
        elif d == 2:
            lines = ['<line x1="30" y1="6" x2="30" y2="94"/>']
        else:
            # unequal: part widths clearly differ (e.g. 16/26/46), so the child can see it at a glance
            xs = [6 + 88 * i / d for i in range(1, d)] if equal else list(rng.choice([(22, 48), (52, 78), (28, 72)]))[:d - 1]
            lines = [f'<line x1="{x:.1f}" y1="6" x2="{x:.1f}" y2="94"/>' for x in xs]
            if equal:
                regions = [f'<rect x="{6 + 88 * i / d:.1f}" y="6" width="{88 / d:.1f}" height="88"/>' for i in range(shade)]
        return (f'<svg width="86" height="86" viewBox="0 0 100 100"><g fill="{SHADE}" stroke="none">{"".join(regions)}</g>'
                f'<g {SN}><rect x="6" y="6" width="88" height="88"/>{"".join(lines)}</g></svg>')
    # rectangle strips
    if equal:
        xs = [6 + 176 * i / d for i in range(1, d)]
    else:
        while True:
            xs = sorted(rng.uniform(20, 170) for _ in range(d - 1))
            widths = [b - a for a, b in zip([6] + xs, xs + [182])]
            if min(widths) > 16 and max(widths) - min(widths) > 30:
                break
    lines = [f'<line x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="86"/>' for x in xs]
    if equal:
        regions = [f'<rect x="{6 + 176 * i / d:.1f}" y="14" width="{176 / d:.1f}" height="72"/>' for i in range(shade)]
    return (f'<svg width="150" height="80" viewBox="0 0 190 100"><g fill="{SHADE}" stroke="none">{"".join(regions)}</g>'
            f'<g {SN}><rect x="6" y="14" width="176" height="72"/>{"".join(lines)}</g></svg>')


def task_shade(rng, lvl, L):
    f = {1: (1, 2), 2: (1, 4), 3: rng.choice([(1, 3), (3, 4)])}[lvl]
    d = f[1]
    kinds = ["square", "circle", "rect"]
    svgs = "".join(f'<span style="background:{EX_BG};border-radius:12px;padding:6px;display:inline-flex">{frac_shape(k, d, True, rng, f[0])}</span>'
                   if i == 0 else frac_shape(k, d, True, rng) for i, k in enumerate(kinds))  # the first shape is the worked example
    body = f'<div style="display:flex;justify-content:space-around;align-items:center">{svgs}</div>'
    key = f"{f[0]}/{f[1]}"
    return sec(10, text(L.w["t10"], frac=L.w["frac"][key]), body), text(L.a["shade"], part=L.a["shade_part"][key])


def task_equal_parts(rng, lvl, L):
    d = {1: 2, 2: 4, 3: rng.choice([3, 4])}[lvl]
    kinds = ["square", "circle", "rect", "rect"]
    while True:  # the first shape is the worked example: always equal, already ticked
        eq = [True] + [rng.random() < 0.5 for _ in kinds[1:]]
        if sum(eq) <= 3:
            break
    cells = []
    for i, (k, e) in enumerate(zip(kinds, eq)):
        tick = filled("✓", 42) if i == 0 else box(42)
        bg = f"background:{EX_BG};border-radius:12px;padding:6px;" if i == 0 else ""
        cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;{bg}">'
                     f'{frac_shape(k, d, e, rng)}{tick}</div>')
    body = f'<div style="display:flex;justify-content:space-around;align-items:flex-end">{"".join(cells)}</div>'
    yes = [n for n, e in zip(L.a["eq_names"], eq) if e]
    no = [n for n, e in zip(L.a["eq_names"], eq) if not e]
    ans = "✓ " + ", ✓ ".join(yes) + "; " + ", ".join(no) + " — " + L.a["not_equal"]
    return sec(11, text(L.w["t11"], n=d), body, grow=True), ans


# ---------------------------------------------------------------- task 12: compare lengths / heights
def task_lengths(rng, lvl, L):
    k = 4 if lvl == 3 else 3
    while True:
        lens = rng.sample(range(70, 251, 10), k)
        s = sorted(lens)
        if all(b - a >= (20 if lvl == 3 else 40) for a, b in zip(s, s[1:])):
            break
    short_q = rng.random() < 0.5
    rowh = 140 / k if k == 4 else 52
    pencils = []
    for i, ln in enumerate(lens):
        y = 6 + i * (36 if k == 4 else 52)
        pencils.append(f'<rect x="0" y="{y}" width="18" height="24" rx="5"/><rect x="18" y="{y}" width="10" height="24"/>'
                       f'<rect x="28" y="{y}" width="{ln}" height="24"/><path d="M{28 + ln} {y} L{58 + ln} {y + 12} L{28 + ln} {y + 24} Z"/>'
                       f'<path d="M{48 + ln} {y + 8} L{58 + ln} {y + 12} L{48 + ln} {y + 16} Z" fill="#111"/>')
    ph = 6 + k * (36 if k == 4 else 52)
    tw = rng.sample(range(2, 8 if lvl > 1 else 7), k)
    tall_q = rng.random() < 0.5
    towers = []
    gap = 300 / k
    for i, t in enumerate(tw):
        x = gap * i + (gap - 36) / 2
        for j in range(t):
            towers.append(f'<rect x="{x:.0f}" y="{194 - 32 * j}" width="32" height="32"/>')
    tw_svg = (f'<svg width="270" height="212" viewBox="0 0 300 236"><g {S}>{"".join(towers)}</g>'
              '<line x1="4" y1="227" x2="296" y2="227" stroke="#111" stroke-width="3"/></svg>')
    pen_svg = f'<svg width="340" height="{ph}" viewBox="0 0 340 {ph}"><g transform="translate(10,0)" {S}>{"".join(pencils)}</g></svg>'
    q1 = L.w["pencil_short"] if short_q else L.w["pencil_long"]
    q2 = L.w["tower_tall"] if tall_q else L.w["tower_low"]
    col = 'flex:1;display:flex;flex-direction:column;gap:10px'
    p = 'margin:0;font-size:23px;font-weight:800;line-height:1.25'
    # worked examples (not the answers): two short bars and two small towers, the right one circled
    bar = lambda ln: f'<svg width="{ln + 6}" height="16"><rect x="3" y="3" width="{ln}" height="10" rx="3" fill="#fff" stroke="#111" stroke-width="2.5"/></svg>'
    bars = [bar(34), bar(78)]
    bars[0 if short_q else 1] = ring(bars[0 if short_q else 1], 2)
    tower = lambda t: ('<svg width="18" height="' + str(14 * t + 4) + '">' + "".join(
        f'<rect x="2" y="{2 + 14 * j}" width="14" height="14" fill="#fff" stroke="#111" stroke-width="2"/>' for j in range(t)) + '</svg>')
    tws = [tower(2), tower(4)]
    tws[1 if tall_q else 0] = ring(tws[1 if tall_q else 0], 2)
    ex = lambda parts: (f'<div style="display:flex;align-items:flex-end;gap:16px;background:{EX_BG};border-radius:10px;'
                        f'padding:6px 12px;width:max-content">{"".join(parts)}</div>')
    body = (f'<div style="display:flex;gap:18px"><div style="{col}"><p style="{p}">{q1}</p>{ex(bars)}{pen_svg}</div>'
            f'<div style="width:2.5px;background:#111"></div><div style="{col}"><p style="{p}">{q2}</p>{ex(tws)}{tw_svg}</div></div>')
    pi = lens.index(min(lens) if short_q else max(lens))
    ti = tw.index(max(tw) if tall_q else min(tw))
    a = L.a
    ans = (f'{a["pencil_short"] if short_q else a["pencil_long"]} — {a["pencil_pos"][pi]}; '
           f'{a["tower_tall"] if tall_q else a["tower_low"]} — {a["tower_pos"][ti]} ({text(a["cubes"], n=tw[ti])})')
    return sec(12, L.w["t12"], body), ans


# ---------------------------------------------------------------- task 13: number bonds
def task_bonds(rng, lvl, L):
    n = {1: rng.choice([5, 6, 7]), 2: rng.choice([8, 9, 10]), 3: rng.choice([10, 11, 12])}[lvl]
    # the first bond (0 + n) is filled in as a model, so the child sees where to start and why there are n + 1 rows
    cells = (f'<div class="bond">{filled(0, 40)}+{filled(n, 40)}= {n}</div>'
             + "".join(f'<div class="bond">{box(40)}+{box(40)}= {n}</div>' for _ in range(n)))
    body = f'<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));row-gap:12px;column-gap:8px">{cells}</div>'
    return (sec(13, text(L.w["t13"], n=n), body, sub=L.w["t13_sub"]),
            "<b>" + ", ".join(f"{i}+{n - i}" for i in range(n + 1)) + "</b>")


# ---------------------------------------------------------------- task 14: counting in steps
def task_steps(rng, lvl, L):
    if lvl == 1:
        step = rng.choice([1, 2])
        start = rng.randint(0, 10) if step == 1 else 2
    elif lvl == 2:
        step = rng.choice([2, 5])
        start = rng.choice([0, 2, 4]) if step == 2 else rng.choice([0, 5])
    else:
        step = rng.choice([2, 3, 5, 10])
        start = {2: rng.randint(1, 30), 3: rng.choice([0, 3]), 5: rng.choice(range(0, 51, 5)), 10: rng.randint(1, 9)}[step]
    vals = [start + i * step for i in range(10)]
    k = 5 if lvl == 3 else 4
    miss = sorted(rng.sample(range(2, 10), k))
    cells = "".join((filled(v, 48, ex=True) if i == miss[0] else box(48)) if i in miss else num(v) for i, v in enumerate(vals))
    body = f'<div style="display:flex;justify-content:space-between;padding:0 4px">{cells}</div>'
    # curriculum depends on the step: 1s within 20 = Y1 spring, 2s / 5s / 10s = Y1 summer, 3s = Year 2
    period = {1: "Y1Sp", 2: "Y1Su", 5: "Y1Su", 10: "Y1Su", 3: "Y2"}[step]
    return sec(14, text(L.w["t14"], s=step), body), f"<b>{join_list(vals[i] for i in miss[1:])}</b>", period


# ---------------------------------------------------------------- task 15: equations
def gen_add(rng, lvl):
    while True:
        if lvl == 1:
            a, b = rng.randint(0, 9), rng.randint(0, 9)
            ok = a + b <= 10
        elif lvl == 2:
            a, b = rng.randint(1, 15), rng.randint(1, 9)
            ok = a + b <= 20 and (a + b <= 10 or a % 10 + b < 10)  # no crossing ten
        else:
            a, b = rng.randint(3, 18), rng.randint(3, 9)
            ok = a + b <= 30 and a % 10 + b >= 10  # crossing ten
        if ok:
            return a, b


def task_equations(rng, lvl, L):
    cells, ans_cols = [[], [], []], [[], [], []]
    for _ in range(4):
        a, b = gen_add(rng, lvl)
        cells[0].append(f"{a} + {b} ={box(44)}")
        ans_cols[0].append(a + b)
        a, b = gen_add(rng, lvl)
        s = a + b
        cells[1].append(f"{s} − {b} ={box(44)}")
        ans_cols[1].append(a)
        a, b = gen_add(rng, lvl)
        s = a + b
        form = rng.randrange(4)
        if form == 0:
            cells[2].append(f"{a} +{box(44)}= {s}"); ans_cols[2].append(b)
        elif form == 1:
            cells[2].append(f"{box(44)}+ {b} = {s}"); ans_cols[2].append(a)
        elif form == 2:
            cells[2].append(f"{s} −{box(44)}= {a}"); ans_cols[2].append(b)
        else:
            cells[2].append(f"{box(44)}− {b} = {a}"); ans_cols[2].append(s)
    for c in range(3):  # easy to harder: smaller answers first in every column (STANDARDS D2)
        order = sorted(range(4), key=lambda r: ans_cols[c][r])
        cells[c] = [cells[c][r] for r in order]
        ans_cols[c] = [ans_cols[c][r] for r in order]
    cells[0][0] = cells[0][0].replace(box(44), filled(ans_cols[0][0], 44, ex=True), 1)  # worked example
    ans_cols[0] = ans_cols[0][1:]
    out = []
    for r in range(4):
        for c in range(3):
            st = []
            if r == 0:
                st.append("border-top:none")
            if c == 2:
                st.append("border-right:none")
            out.append(f'<div class="eq" style="{";".join(st)}">{cells[c][r]}</div>')
    body = ('<div style="border:2.5px solid #111;border-radius:12px;overflow:hidden;display:grid;grid-template-columns:repeat(3,minmax(0,1fr))">'
            + "".join(out) + "</div>")
    ans = " · ".join(f'{text(L.a["column"], i=i + 1)}: <b>{join_list(col)}</b>' for i, col in enumerate(ans_cols))
    return sec(15, L.w["t15"], body, grow=True), ans


# ---------------------------------------------------------------- task 16: number walls
def wall_solvable(rows, known):
    """rows: list of lists bottom-up. known: set of (r,i). Return order-solvable."""
    known = set(known)
    changed = True
    while changed:
        changed = False
        for r in range(1, len(rows)):
            for i in range(len(rows[r])):
                t, l, rr = (r, i), (r - 1, i), (r - 1, i + 1)
                kn = [t in known, l in known, rr in known]
                if sum(kn) == 2:
                    known |= {t, l, rr}
                    changed = True
    return len(known) == sum(len(x) for x in rows)


def make_wall(rng, lvl):
    h = 4 if lvl == 3 else 3
    lo, hi = {1: (0, 3), 2: (1, 5), 3: (1, 5)}[lvl]
    base = [rng.randint(lo, hi) for _ in range(h)]
    rows = [base]
    while len(rows[-1]) > 1:
        p = rows[-1]
        rows.append([p[i] + p[i + 1] for i in range(len(p) - 1)])
    allc = [(r, i) for r in range(h) for i in range(len(rows[r]))]
    while True:
        if lvl == 1:
            known = {(0, i) for i in range(h)}  # whole bottom row given, only add
            hidden = [c for c in allc if c not in known]
            known |= set(rng.sample(hidden, 1))
        else:
            known = set(rng.sample(allc, h))
            if all(r == 0 for r, _ in known):
                continue
        if wall_solvable(rows, known):
            break
    return rows, known


def task_walls(rng, lvl, L):
    bw = 54 if lvl == 3 else 66
    walls, ans = [], []
    made = sorted((make_wall(rng, lvl) for _ in range(3)), key=lambda rk: rk[0][-1][0])  # smaller top first (D2)
    for w, (rows, known) in enumerate(made):
        html = []
        for r in range(len(rows) - 1, -1, -1):
            bricks = "".join(f'<span class="brick" style="width:{bw}px{"" if (r, i) in known or w else ";background:" + EX_BG}">'
                             f'{rows[r][i] if (r, i) in known or w == 0 else ""}</span>' for i in range(len(rows[r])))
            html.append(f'<div class="row">{bricks}</div>')
        walls.append(f'<div style="display:flex;flex-direction:column;gap:2px">{"".join(html)}</div>')
        if w == 0:  # the first wall is the worked example
            continue
        miss = []
        for r in range(len(rows) - 1, -1, -1):
            vs = [str(rows[r][i]) for i in range(len(rows[r])) if (r, i) not in known]
            if vs:
                miss.append(", ".join(vs))
        ans.append(f'{text(L.a["wall"], i=w + 1)}: <b>{" / ".join(miss)}</b>')
    hh = 4 * 50 if lvl == 3 else 150
    sep = f'<div style="width:0;height:{hh}px;border-left:2.5px dashed #111"></div>'
    body = f'<div style="display:flex;justify-content:space-around;align-items:flex-end">{sep.join(walls)}</div>'
    return (sec(16, L.w["t16"], body, sub=L.w["t16_sub"]),
            " · ".join(ans) + " " + L.a["top_down"])


# ---------------------------------------------------------------- task 17: positional words
# Items drawn with origin at bottom-centre.
ITEMS = {
    "ball": '<circle cx="0" cy="-17" r="17"/><path d="M-16 -21 Q0 -11 16 -21" fill="none"/>',
    "bird": ('<path d="M-10 -12 L-24 -22 L-20 -8 Z"/><ellipse cx="0" cy="-10" rx="20" ry="12"/>'
             '<path d="M-10 -12 Q2 -24 12 -10" fill="none"/><circle cx="22" cy="-20" r="9"/>'
             '<path d="M30 -23 L39 -20 L30 -17 Z"/><circle cx="25" cy="-22" r="1.8" fill="#111" stroke="none"/>'),
    "cat": ('<path d="M18 -4 Q36 -6 30 -30" fill="none"/><ellipse cx="0" cy="-18" rx="20" ry="18"/>'
            '<path d="M-17 -50 L-14 -70 L-2 -56 Z"/><path d="M17 -50 L14 -70 L2 -56 Z"/>'
            '<circle cx="0" cy="-46" r="20"/><circle cx="-8" cy="-49" r="2.2" fill="#111" stroke="none"/>'
            '<circle cx="8" cy="-49" r="2.2" fill="#111" stroke="none"/><path d="M-2 -42 L2 -42 L0 -39 Z" fill="#111"/>'
            '<path d="M-19 -42 L-31 -44 M-19 -38 L-31 -36 M19 -42 L31 -44 M19 -38 L31 -36" fill="none"/>'),
    "dog": ('<ellipse cx="0" cy="-18" rx="26" ry="18"/><ellipse cx="-21" cy="-56" rx="8" ry="15"/>'
            '<ellipse cx="21" cy="-56" rx="8" ry="15"/><circle cx="0" cy="-50" r="21"/>'
            '<circle cx="-8" cy="-54" r="2.2" fill="#111" stroke="none"/><circle cx="8" cy="-54" r="2.2" fill="#111" stroke="none"/>'
            '<ellipse cx="0" cy="-44" rx="4" ry="3" fill="#111" stroke="none"/><path d="M-6 -38 Q0 -33 6 -38" fill="none"/>'),
    "teddy": ('<circle cx="-15" cy="-62" r="8"/><circle cx="15" cy="-62" r="8"/><ellipse cx="0" cy="-20" rx="20" ry="20"/>'
              '<circle cx="0" cy="-50" r="18"/><ellipse cx="0" cy="-44" rx="7" ry="5"/>'
              '<circle cx="-7" cy="-54" r="2.2" fill="#111" stroke="none"/><circle cx="7" cy="-54" r="2.2" fill="#111" stroke="none"/>'
              '<circle cx="0" cy="-45" r="2" fill="#111" stroke="none"/>'),
}


ITEM_H = {"ball": 34, "bird": 32, "cat": 70, "dog": 71, "teddy": 70}


def task_positions(rng, lvl, L):
    # Box: front rect x=110..230, y=165..250 (ground); top face goes back by (+28,-22).
    words_pool = ["in", "on", "above", "behind", "in front of", "next to"] if lvl >= 2 else ["in", "on", "above", "next to", "in front of"]
    while True:
        pos = rng.sample(words_pool, 4)
        if not ("in" in pos and "on" in pos):  # both would sit in the same spot
            break
    items = rng.sample(list(ITEMS), 4)
    if "above" in pos:  # only something that can fly or be thrown is above the box
        if "bird" not in items:
            items[pos.index("above")] = "bird"
        ai, fi = pos.index("above"), items.index("bird")
        items[ai], items[fi] = items[fi], items[ai]
    layer_back, layer_mid, layer_front = [], [], []
    for it, p in zip(items, pos):
        h = ITEM_H[it]
        s = 0.85 if h > 40 else 1.0
        if p == "in":
            x, y = 184, 165 + 0.4 * h * s
        elif p == "on":
            x, y = 184, 156
        elif p == "above":
            x, y = 180, 70
        elif p == "behind":  # peeks out from behind the left edge, half hidden by the box
            x, y = 104, 232
        elif p == "in front of":  # overlaps the lower right part of the front face
            x, y = 196, 264
        else:  # next to
            x, y = 298, 250
        g = f'<g transform="translate({x},{y:.0f}) scale({s})">{ITEMS[it]}</g>'
        (layer_back if p == "behind" else layer_mid if p in ("in", "on") else layer_front).append(g)
    box_top = '<path d="M110 165 L138 143 L258 143 L230 165 Z"/>'
    box_front = '<path d="M230 165 L258 143 L258 228 L230 250 Z"/><rect x="110" y="165" width="120" height="85"/>'
    # "on": the item stands on a closed lid, so draw the lid then the item; "in": the box is open
    # (flaps folded out) and the front face hides the lower part of the item
    if "on" in pos:
        scene = "".join(layer_back) + box_top + box_front + "".join(layer_mid) + "".join(layer_front)
    else:
        flaps = ('<path d="M110 165 L138 143 L122 118 L94 140 Z"/><path d="M230 165 L258 143 L262 112 L234 134 Z"/>'
                 if "in" in pos else "")
        scene = "".join(layer_back) + flaps + box_top + "".join(layer_mid) + box_front + "".join(layer_front)
    svg = (f'<svg width="250" height="206" viewBox="0 0 340 280">'
           '<line x1="4" y1="250" x2="336" y2="250" stroke="#111" stroke-width="3"/>'
           f'<g {S}>{scene}</g></svg>')
    # with "on" the item stands on the top face; with "in" the item is drawn inside
    bank = pos[:]
    if lvl == 3:
        bank.append(rng.choice([w for w in ["under", "next to", "behind", "in front of", "on"] if w not in pos]))
    rng.shuffle(bank)
    w = L.w
    letters, blank = w["letters"], f'<span class="blank" style="width:{w["blank"]}px"></span>'
    done_blank = (f'<span class="blank" style="width:auto;min-width:{w["blank"]}px;background:{EX_BG};text-align:center;'
                  f'font-weight:800;padding:0 6px">{w["pos"][pos[0]]}</span>')
    sents = "".join(f'<p class="sent">{letters[i]}) {text(w["sent"], item=w["items"][it], blank=done_blank if i == 0 else blank)}</p>'
                    for i, it in enumerate(items))
    pills = "".join(f'<span class="pill">{w["pos"][p]}</span>' for p in bank)
    body = (f'<div style="display:flex;flex-wrap:wrap;justify-content:space-around;gap:8px 10px;margin-bottom:10px">{pills}</div>'
            f'<div style="display:flex;gap:12px;align-items:center">{svg}'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:14px;border-left:2.5px solid #111;padding-left:14px">{sents}</div></div>')
    ans = " · ".join(f'{letters[i]}) <b>{w["pos"][p]}</b>' for i, p in enumerate(pos) if i)
    return sec(17, w["t17"], body), ans


# ---------------------------------------------------------------- task 18: ordinal numbers


DUCK = ('<path d="M24 54 L24 64 L18 66 M34 54 L34 64 L28 66" fill="none"/><path d="M8 34 L0 24 L14 30 Z"/>'
        '<ellipse cx="28" cy="42" rx="22" ry="14"/><path d="M18 40 Q30 30 38 42" fill="none"/>'
        '<path d="M53 17 L64 21 L53 26 Z"/><circle cx="44" cy="21" r="11"/><circle cx="47" cy="18" r="2" fill="#111" stroke="none"/>')


def task_ordinals(rng, lvl, L):
    n = {1: 5, 2: 8, 3: 10}[lvl]
    pond_right = rng.random() < 0.5 if lvl >= 2 else True
    if lvl == 1:
        given = [1]
    elif lvl == 2:
        given = [1, rng.randint(3, n - 1)]
    else:
        given = [rng.randint(2, 4), rng.randint(6, n - 1)]
    sp = min(76, 590 / n)
    sc = min(1.0, (sp - 6) / 64)
    x0 = 10 if pond_right else 130
    parts, circ, txt = [], [], []
    for i in range(n):
        x = x0 + i * sp
        rank = n - i if pond_right else i + 1
        if pond_right:
            parts.append(f'<use href="#dk" transform="translate({x:.1f},{40 + (1 - sc) * 66:.1f}) scale({sc:.2f})"/>')
        else:
            parts.append(f'<use href="#dk" transform="translate({x + 64 * sc:.1f},{40 + (1 - sc) * 66:.1f}) scale({-sc:.2f},{sc:.2f})"/>')
        cx = x + 32 * sc
        circ.append(f'<circle cx="{cx:.1f}" cy="152" r="{min(26, sp / 2 - 3):.1f}"{" fill=" + chr(34) + EX_BG + chr(34) if rank in given else ""}/>')
        if rank in given:
            txt.append(f'<text x="{cx:.1f}" y="159">{i18n.ordinal(L.wl, rank)}</text>')
    px = 656 if pond_right else 58
    lx1, lx2 = (0, 600) if pond_right else (114, 714)
    svg = ('<svg width="672" height="188" viewBox="0 0 714 200" style="font-weight:800">'
           f'<defs><g id="dk" {S}>{DUCK}</g></defs>' + "".join(parts) +
           f'<ellipse cx="{px}" cy="98" rx="52" ry="20" fill="#fff" stroke="#111" stroke-width="2.5"/>'
           f'<path d="M{px - 26} 96 Q{px - 18} 90 {px - 10} 96 Q{px - 2} 102 {px + 6} 96 M{px - 6} 104 Q{px + 2} 98 {px + 10} 104 Q{px + 18} 110 {px + 26} 104" fill="none" stroke="#111" stroke-width="2" stroke-linecap="round"/>'
           f'<text x="{px}" y="66" font-size="16" text-anchor="middle" fill="#111">{L.w["pond"]}</text>'
           f'<line x1="{lx1}" y1="110" x2="{lx2}" y2="110" stroke="#111" stroke-width="3"/>'
           f'<g fill="#fff" stroke="#111" stroke-width="2.5">{"".join(circ)}</g>'
           f'<g font-size="{19 if n < 10 else 17}" text-anchor="middle" fill="#111">{"".join(txt)}</g></svg>')
    order = [i18n.ordinal(L.wl, n - i if pond_right else i + 1) for i in range(n)]
    sub = text(L.w["t18_sub"], first=i18n.ordinal(L.wl, 1))
    return (sec(18, L.w["t18"], svg, sub=sub, grow=True),
            f'{L.a["left_right"]}: <b>{", ".join(order)}</b>')


# ---------------------------------------------------------------- curriculum (England, National Curriculum + White Rose)
# When each task is taught, per level (the level changes the number range): Y1A / Y1Sp / Y1Su = Year 1 autumn /
# spring / summer term, Y2 = Year 2. Shown as a tag on the answer page so parents see what the task checks.
CURRICULUM = {
    1: ("Y1A", "Y1Sp", "Y1Sp"),    # count objects: within 10 autumn, within 20 spring
    2: ("Y1A", "Y1Sp", "Y1Sp"),    # estimate, then count (estimating is enrichment)
    3: ("Y2", "Y2", "Y2"),         # odd and even numbers
    4: ("Y1A", "Y1Sp", "Y1Su"),    # number line: to 10 / to 20 / to 100
    5: ("Y1A", "Y1Sp", "Y1Su"),    # compare with < > =
    6: ("Y1A", "Y1Sp", "Y2"),      # numbers in words: to 20 is Year 1, to 100 is Year 2
    7: ("Y2", "Y2", "Y2"),         # 3D shapes: naming is Y1 autumn, counting faces and edges is Year 2
    8: ("Y1A", "Y1A", "Y1A"),      # name and count 2D shapes
    9: ("Y2", "Y2", "Y2"),         # count sides, pentagon / hexagon
    10: ("Y1Su", "Y1Su", "Y2"),    # halves, quarters (Y1); thirds and three quarters (Y2)
    11: ("Y1Su", "Y1Su", "Y2"),    # equal parts
    12: ("Y1Sp", "Y1Sp", "Y1Sp"),  # length and height
    13: ("Y1A", "Y1A", "Y1Sp"),    # number bonds within 10 / to 12
    14: ("Y1Su", "Y1Su", "Y1Su"),  # counting in steps (task_steps returns the exact period for its step)
    15: ("Y1A", "Y1Sp", "Y2"),     # add and subtract within 10 / 20 / crossing ten up to 30
    16: ("Y1A", "Y1Sp", "Y2"),     # number walls (addition; the format itself is enrichment)
    17: ("Y1Su", "Y1Su", "Y1Su"),  # position and direction
    18: ("Y1Su", "Y1Su", "Y1Su"),  # ordinal numbers
}


def curriculum(task_no, level):
    return CURRICULUM[task_no][level - 1]


# ---------------------------------------------------------------- assemble
def page(content, extra_style=""):
    return f'<div class="page" style="{extra_style}">{content}</div>'


def header(L, badge):
    """Title, Name / Date lines and the level badge (first page of every worksheet)."""
    w = L.w
    # the badge sits in the Name/Date row, so a long title in any language can never run into it
    return ('<div style="display:flex;justify-content:center">'
            f'<div style="background:#111;color:#fff;border-radius:40px;padding:4px 40px;font-size:34px;font-weight:900;letter-spacing:1px">{w["title"]}</div></div>'
            '<div style="display:flex;gap:24px;font-size:20px;font-weight:800;margin-bottom:4px;align-items:flex-end">'
            f'<div style="display:flex;flex:2;align-items:flex-end;gap:8px">{w["name"]}<span class="line"></span></div>'
            f'<div style="display:flex;flex:1.4;align-items:flex-end;gap:8px">{w["date"]}<span class="line"></span></div>'
            '<div style="flex:none;font-size:15px;font-weight:800;border:2px solid #111;border-radius:14px;padding:2px 10px;white-space:nowrap">'
            f'{badge}</div></div>')


def parse_level(level):
    """1, 2, 3 (Year 1 review, by difficulty), a stage "R" (Reception) / "Y1A" (Year 1 autumn),
    or chosen topics "T:r1_v4a_..." (see topics.py)."""
    if str(level) in ("R", "Y1A"):
        return str(level)
    import topics
    if str(level).startswith("T:"):
        return "T:" + "_".join(topics.parse(str(level)))
    # Year 1 review: 1, 2, 3 (= part 1) or 1a/1b, 2a/2b, 3a/3b; each part is a sheet of 9 topics (STANDARDS L7)
    m = str(level).strip().lower()
    if m[:1] in ("1", "2", "3") and m[1:] in ("", "a", "b"):
        return topics.review_spec(int(m[0]), 2 if m[1:] == "b" else 1)
    raise ValueError("level must be 1, 2, 3 (1a ... 3b), R, Y1A or T:<topics>")


def build(level, seed, lang=i18n.DEFAULT, answers_lang=i18n.DEFAULT):
    """Return (worksheet pages, answer page) as HTML. Numbers and pictures depend only on level and seed."""
    L = Lang(lang, answers_lang)
    level = parse_level(level)
    if level.startswith("T:"):
        import topics  # a sheet made of chosen topics (also the Year 1 review sheets)
        return topics.build(level, seed, L)
    import stages  # Reception / Year 1 autumn: icon-led tasks for children who cannot read yet
    return stages.build(level, seed, L)


def cheats(level, seed, lang=i18n.DEFAULT, which=None):
    """Cheat-sheet pages (two cards per A4) for the chosen task numbers; for the stages R, Y1A and topic sheets."""
    level = parse_level(level)
    import cheats as c
    return c.build(level, seed, Lang(lang, lang), which)


def cheat_titles(level, lang=i18n.DEFAULT):
    import cheats as c
    return c.titles(parse_level(level), lang)


def font_link():
    """Local fonts (scripts/fetch_fonts.py) if present, otherwise Google Fonts (needs internet, no Greek)."""
    local = FONTS / "fonts.css"
    return f'<link rel="stylesheet" href="{local.as_uri()}">' if local.exists() else FONT_LINK


def html_doc(body, lang=i18n.DEFAULT):
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">{font_link()}'
            f'<style>{CSS}</style></head><body>{body}</body></html>')


def stem_of(level, seed, lang=i18n.DEFAULT):
    level = parse_level(level)
    if level.startswith("T:"):
        import topics
        return f"Worksheet_T{topics.short_id(topics.parse(level))}_{seed}_{lang}"
    return f"Worksheet_{level}_{seed}_{lang}"


def answers_stem(level, seed, lang=i18n.DEFAULT, answers_lang=i18n.DEFAULT):
    return f"{stem_of(level, seed, lang)}_answers_{answers_lang}"


async def _render_one(pg, job, png=True, log=print):
    """Render one worksheet + answers with an open Playwright page. Returns a result dict."""
    from pypdf import PdfWriter
    level, seed, lang, alang = job
    pages, answers = build(level, seed, lang, alang)
    stem, astem = stem_of(level, seed, lang), answers_stem(level, seed, lang, alang)
    res = {"level": level, "seed": seed, "lang": lang, "answers_lang": alang, "stem": stem,
           "warnings": [], "previews": [], "answer_previews": []}
    for name, plist, key, doc_lang in [(stem, pages, "previews", lang), (astem, [answers], "answer_previews", alang)]:
        writer = PdfWriter()
        for i, body in enumerate(plist, 1):
            f = OUT / f"{name}_p{i}.html"
            f.write_text(html_doc(body, doc_lang), encoding="utf-8")
            try:
                await pg.goto(f.as_uri())
                await pg.wait_for_load_state("networkidle")
                await pg.evaluate("document.fonts.ready")
                overflow = await pg.evaluate(
                    "[...document.querySelectorAll('.page')].some(p => p.scrollHeight > p.clientHeight + 1)")
                if overflow:
                    msg = f"{f.name} content does not fit the page!"
                    res["warnings"].append(msg)
                    log(f"  WARNING: {msg}")
                pdf = OUT / f"{name}_p{i}.pdf"
                await pg.pdf(path=str(pdf), width="794px", height="1123px", print_background=True, page_ranges="1")
                if png:
                    await pg.screenshot(path=str(OUT / f"{name}_p{i}.png"))
                    res[key].append(f"{name}_p{i}.png")
                writer.append(str(pdf))
                pdf.unlink()
            finally:
                f.unlink(missing_ok=True)
        writer.write(str(OUT / f"{name}.pdf"))
    res["pdf"], res["answers_pdf"] = f"{stem}.pdf", f"{astem}.pdf"
    log(f"  out/{stem}.pdf  +  out/{astem}.pdf")
    return res


def _job(j):
    """(level, seed) or (level, seed, lang, answers_lang)."""
    return tuple(j) if len(j) == 4 else (j[0], j[1], i18n.DEFAULT, i18n.DEFAULT)


async def render_many(jobs, png=True, log=print):
    """jobs: list of (level, seed[, lang, answers_lang]). One browser for all worksheets."""
    from playwright.async_api import async_playwright
    OUT.mkdir(exist_ok=True)
    results = []
    async with async_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH")  # optional custom browser
        browser = await p.chromium.launch(executable_path=exe) if exe else await p.chromium.launch()
        try:
            pg = await browser.new_page(viewport={"width": 794, "height": 1123})
            for j in map(_job, jobs):
                log(f"Level {j[0]} ({LEVEL_NAMES.get(j[0], 'topics')}), worksheet №{j[1]}, {j[2]} / answers {j[3]}")
                results.append(await _render_one(pg, j, png, log))
        finally:
            await browser.close()
    return results


def generate(jobs, png=True, log=print):
    """Synchronous wrapper (used by the CLI and by scripts/server.py)."""
    return asyncio.run(render_many(jobs, png, log))


def main():
    ap = argparse.ArgumentParser(description="Generate LET'S PRACTICE! maths worksheets")
    ap.add_argument("--level", type=parse_level, default=2,
                    help="R = Reception, Y1A = Year 1 autumn, 1/2/3 = Year 1 review easy/medium/hard")
    ap.add_argument("--seed", type=int, help="worksheet number (same number = same worksheet)")
    ap.add_argument("--count", type=int, default=1, help="how many worksheets to make")
    ap.add_argument("--lang", choices=list(i18n.LANGS), default=i18n.DEFAULT, help="language of the tasks")
    ap.add_argument("--answers-lang", choices=list(i18n.LANGS), default=i18n.DEFAULT, help="language of the answer page")
    ap.add_argument("--no-png", action="store_true", help="do not save PNG previews")
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else random.randint(100, 9999)
    generate([(a.level, seed + i, a.lang, a.answers_lang) for i in range(a.count)], png=not a.no_png)


if __name__ == "__main__":
    main()
