"""Worksheets for children who are only starting to read: Reception (EYFS, ages 4-5) and Year 1 autumn term.

Rules that make the tasks clear without reading:
  * every task has an ACTION ICON (one picture = one action: count, circle, match, colour, trace, write, tick,
    cross out, draw); the text next to it is for the adult;
  * the first item of every task is a WORKED EXAMPLE on a grey background ("grey = do it like this");
  * answers are given by circling, matching, ticking or drawing; writing only where the stage expects it;
  * friendly pictures (ladybirds, apples, fish...) and few items per page.

build(stage, seed, L) returns (pages, answers) like generate.build. Numbers depend only on stage and seed.
Curriculum: EYFS early learning goals (Number, Numerical Patterns) and Year 1 autumn blocks of the National
Curriculum (place value within 10, addition and subtraction within 10, shape); see reference/curriculum.
"""
import random

import generate as g
from i18n import text

ST = g.S
EX = "background:#e9e9e9;border-radius:12px"  # worked example
STAGES = ("R", "Y1A")


# ---------------------------------------------------------------- action icons (48x48)
def _pencil(x, y, a=45):
    return (f'<g transform="translate({x},{y}) rotate({a})"><rect x="-3.5" y="-17" width="7" height="19" rx="1"/>'
            '<path d="M-3.5 2 L0 9 L3.5 2 Z"/><path d="M-1.2 6.3 L0 9 L1.2 6.3 Z" fill="#111" stroke="none"/></g>')


ACTIONS = {
    "count": ('<circle cx="9" cy="15" r="6" fill="#111"/><circle cx="24" cy="15" r="6" fill="#111"/><circle cx="39" cy="15" r="6" fill="#111"/>'
              '<g fill="#111" stroke="none" font-size="15" font-weight="900" text-anchor="middle">'
              '<text x="9" y="42">1</text><text x="24" y="42">2</text><text x="39" y="42">3</text></g>'),
    "circle": ('<ellipse cx="22" cy="27" rx="18" ry="14" fill="none"/>'
               '<path d="M22 18 L24.6 24 L31 24.4 L26 28.5 L27.6 35 L22 31.4 L16.4 35 L18 28.5 L13 24.4 L19.4 24 Z" fill="#111" stroke="none"/>'
               + _pencil(38, 12)),
    "match": '<circle cx="7" cy="12" r="4.5" fill="#111"/><circle cx="41" cy="38" r="4.5" fill="#111"/><path d="M7 12 C26 10 22 38 41 38" fill="none"/>',
    "colour": ('<path d="M20 42 C6 32 3 24 6 17 C9 10 17 10 20 17 C23 10 31 10 34 17 C37 24 34 32 20 42 Z"/>'
               '<path d="M20 42 C6 32 3 24 6 17 C9 10 17 10 20 17 Z" fill="#111"/>' + _pencil(40, 12)),
    "trace": ('<path d="M10 14 C12 6 30 6 30 15 C30 22 20 24 18 25 C24 25 32 28 31 36 C30 44 13 44 10 37" fill="none" stroke-dasharray="1 5"/>'
              + _pencil(38, 30, 30)),
    "write": '<rect x="4" y="12" width="28" height="28" rx="7"/><path d="M12 32 L24 20" fill="none"/>' + _pencil(36, 16),
    "tick": '<rect x="6" y="8" width="34" height="34" rx="8"/><path d="M13 26 L21 33 L35 15" fill="none" stroke-width="4"/>',
    "cross": ('<path d="M24 12 C14 6 4 12 6 24 C8 36 16 42 24 39 C32 42 40 36 42 24 C44 12 34 6 24 12 Z"/>'
              '<path d="M24 12 L24 5" fill="none"/><path d="M9 9 L39 41 M39 9 L9 41" fill="none" stroke-width="4"/>'),
    "draw": ('<circle cx="9" cy="38" r="4.5" fill="#111"/><circle cx="21" cy="38" r="4.5" fill="#111"/>'
             '<circle cx="33" cy="38" r="4.5" stroke-dasharray="2 3"/>' + _pencil(36, 18, 30)),
}


def action(k, size=48):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" style="flex:none"><g {ST}>{ACTIONS[k]}</g></svg>'


def isec(num, act, title, body, grow=False, extra=""):
    """Section with number, action icon and a small instruction for the adult."""
    head = f'<div class="ih"><span class="n">{num}</span>{action(act)}<span class="it">{title}</span>{extra}{g.DONE}</div>'
    if grow:
        return (f'<section class="sec" style="flex:1;display:flex;flex-direction:column">{head}'
                f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">{body}</div></section>')
    return f'<section class="sec">{head}{body}</section>'


# ---------------------------------------------------------------- pictures
def obj(key, x, y, size):
    """One object picture (generate.ICONS) with its top-left corner at x, y."""
    body, w, h = g.ICONS[key]
    s = size / max(w, h)
    return f'<g transform="translate({x + (size - w * s) / 2:.1f},{y + (size - h * s) / 2:.1f}) scale({s:.3f})">{body}</g>'


def objects(key, k, size=30, per_row=5, gap=6, crossed=0):
    """k objects in rows of five (rows of 5 help counting); the last `crossed` ones are crossed out."""
    rows = max(1, (k + per_row - 1) // per_row)
    cols = min(k, per_row) if k else 1
    W, H = cols * (size + gap) - gap + 4, rows * (size + gap) - gap + 4
    parts = []
    for i in range(k):
        x, y = 2 + (i % per_row) * (size + gap), 2 + (i // per_row) * (size + gap)
        parts.append(obj(key, x, y, size))
        if i >= k - crossed:
            parts.append(f'<path d="M{x} {y} L{x + size} {y + size} M{x + size} {y} L{x} {y + size}" fill="none" stroke-width="3.5"/>')
    return f'<svg width="{W}" height="{H}" style="flex:none"><g {ST}>{"".join(parts)}</g></svg>'


def tenframe(k, cell=38):
    cells = "".join(f'<rect x="{2 + (i % 5) * cell}" y="{2 + (i // 5) * cell}" width="{cell}" height="{cell}" fill="#fff"/>' for i in range(10))
    dots = "".join(f'<circle cx="{2 + (i % 5) * cell + cell / 2}" cy="{2 + (i // 5) * cell + cell / 2}" r="{cell * 0.32:.1f}" fill="#111"/>'
                   for i in range(k))
    return f'<svg width="{5 * cell + 4}" height="{2 * cell + 4}" style="flex:none"><g stroke="#111" stroke-width="2.5">{cells}</g>{dots}</svg>'


RING = ('<svg width="72" height="64" style="position:absolute;left:-8px;top:-4px">'
        '<ellipse cx="36" cy="32" rx="32" ry="28" fill="none" stroke="#111" stroke-width="3"/></svg>')


def options(rng, k, lo=1, hi=10, n=3):
    """k and n-1 nearby distractors, in increasing order."""
    near = [x for x in range(lo, hi + 1) if 0 < abs(x - k) <= 3]
    return sorted({k, *rng.sample(near, n - 1)})


def choice_row(opts, answer=None):
    """Numbers to circle; when answer is given (worked example) it is circled."""
    return '<div style="display:flex;gap:22px">' + "".join(
        f'<span class="opt">{o}{RING if o == answer else ""}</span>' for o in opts) + "</div>"


def row(content, example, gap=34):
    style = EX if example else "border-top:2px dashed #aaa"
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:{gap}px;padding:7px 14px;{style}">{content}</div>'


SHAPE = {  # outline shapes drawn in a 44x44 box
    "circle": '<circle cx="22" cy="22" r="18"/>',
    "square": '<rect x="5" y="5" width="34" height="34"/>',
    "triangle": '<path d="M22 4 L40 38 L4 38 Z"/>',
    "rect": '<rect x="2" y="11" width="40" height="22"/>',
    "diamond": '<path d="M22 3 L40 22 L22 41 L4 22 Z"/>',
    "star": '<path d="M22 3 L27 16 L41 16 L30 25 L34 39 L22 31 L10 39 L14 25 L3 16 L17 16 Z"/>',
}


def shape(kind, size=44, fill="#fff"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 44 44" style="flex:none">'
            f'<g fill="{fill}" stroke="#111" stroke-width="2.5" stroke-linejoin="round">{SHAPE[kind]}</g></svg>')


def plus(sym="+"):
    return f'<span style="font-size:34px;font-weight:900">{sym}</span>'


# ================================================================ Reception
SPOTS = {1: [(0, 3)], 2: [(-8, -5), (8, 9)], 3: [(-9, -7), (0, 3), (9, 12)],
         4: [(-8, -5), (8, -5), (-8, 10), (8, 10)], 5: [(-8, -5), (8, -5), (0, 3), (-8, 11), (8, 11)]}


def ladybird(x, y, k, s=1.2):
    # no centre line on the back: the spots, in dice patterns, must be seen at a glance (subitising)
    spots = "".join(f'<circle cx="{dx * 1.1:.1f}" cy="{dy * 1.1:.1f}" r="4.6" fill="#111" stroke="none"/>' for dx, dy in SPOTS[k])
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-11 -22 Q0 -36 11 -22" fill="#111"/>'
            '<circle cx="-5" cy="-28" r="1.8" fill="#fff" stroke="none"/><circle cx="5" cy="-28" r="1.8" fill="#fff" stroke="none"/>'
            '<path d="M-6 -32 q-6 -8 -10 -6 M6 -32 q6 -8 10 -6" fill="none"/>'
            f'<ellipse cx="0" cy="0" rx="24" ry="23"/>{spots}</g>')


def r_ladybirds(rng, L, num):
    counts, nums = rng.sample([1, 2, 3, 4, 5], 5), rng.sample([1, 2, 3, 4, 5], 5)
    rh, top = 86, 50
    parts = []
    for i, k in enumerate(counts):
        y = top + i * rh
        parts.append(ladybird(90, y, k) + f'<circle cx="136" cy="{y}" r="5" fill="#111" stroke="none"/>')
    for i, n in enumerate(nums):
        y = top + i * rh
        parts.append(f'<circle cx="505" cy="{y}" r="5" fill="#111" stroke="none"/><circle cx="552" cy="{y}" r="27"/>'
                     f'<text x="552" y="{y + 11}" font-size="32" font-weight="900" text-anchor="middle" fill="#111" stroke="none">{n}</text>')
    y2 = top + nums.index(counts[0]) * rh
    parts.append(f'<path d="M136 {top} C320 {top} 320 {y2} 505 {y2}" fill="none" stroke-width="3"/>')  # worked example
    ex_bg = f'<rect x="40" y="{top - 42}" width="120" height="84" rx="12" fill="#e9e9e9" stroke="none"/>'
    svg = f'<svg width="620" height="{top + 4 * rh + 44}"><g {ST}>{ex_bg}{"".join(parts)}</g></svg>'
    body = f'<div style="display:flex;justify-content:center">{svg}</div>'
    return isec(num, "match", L.w["r1"], body), f'<b>{", ".join(map(str, counts))}</b> {L.a["top_down"]}'


def easy_first(ks):
    """Keep the worked example first, then the rest from easy to harder (STANDARDS D2)."""
    return ks[:1] + sorted(ks[1:])


def r_count_circle(rng, L, num, key):
    ks = easy_first(rng.sample(range(1, 11), 3))
    rows, ans = [], []
    for i, k in enumerate(ks):
        opts = options(rng, k)
        rows.append(row(f'<div style="width:200px;display:flex;justify-content:center">{objects(key, k, 34)}</div>'
                        + choice_row(opts, k if i == 0 else None), i == 0, 50))
        ans.append(k)
    return isec(num, "circle", L.w["r2"], "".join(rows)), f'<b>{", ".join(map(str, ans[1:]))}</b> {L.a["top_down"]}'


def plate(key, k):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px">'
            f'<div style="width:220px;height:100px;border:2.5px solid #111;border-radius:50%;display:flex;align-items:center;justify-content:center">'
            f'{objects(key, k, 24, 5, 5)}</div>')


def r_more(rng, L, num, key):
    rows, ans = [], []
    for i in range(3):
        while True:
            a, b = rng.randint(1, 10), rng.randint(1, 10)
            if abs(a - b) >= 2:
                break
        tick = '<path d="M9 22 L17 30 L33 11" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>'
        boxes = [f'<svg width="42" height="42"><rect x="2" y="2" width="38" height="38" rx="9" fill="#fff" stroke="#111" stroke-width="2.5"/>'
                 f'{tick if i == 0 and (v == max(a, b)) else ""}</svg></div>' for v in (a, b)]
        rows.append(row(plate(key, a) + boxes[0] + plate(key, b) + boxes[1], i == 0, 60))
        ans.append(f'{a} {"&gt;" if a > b else "&lt;"} {b}')
    return isec(num, "tick", L.w["r3"], "".join(rows)), "<b>" + ", ".join(ans[1:]) + "</b>"


def big_num(n, size=62):
    return (f'<span style="display:inline-flex;width:{size}px;height:{size}px;border:2.5px solid #111;border-radius:50%;'
            f'align-items:center;justify-content:center;font-size:34px;font-weight:900;flex:none">{n}</span>')


def arrow():
    return ('<svg width="60" height="24" style="flex:none"><path d="M4 12 L50 12 M40 4 L52 12 L40 20" fill="none" stroke="#111" '
            'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def r_draw_dots(rng, L, num):
    ks = easy_first(rng.sample(range(1, 11), 3))
    rows = [row(big_num(k) + arrow() + tenframe(k if i == 0 else 0, 40), i == 0, 26) for i, k in enumerate(ks)]
    return isec(num, "draw", L.w["r4"], "".join(rows)), f'<b>{", ".join(map(str, ks[1:]))}</b> {L.a["top_down"]}'


def group(key, k, size=30):
    return (f'<div style="border:2.5px solid #111;border-radius:14px;padding:8px 10px;display:flex;align-items:center;'
            f'justify-content:center;min-width:90px">{objects(key, k, size, 5, 5)}</div>')


def r_altogether(rng, L, num, key):
    rows, ans = [], []
    for i in range(3):
        a = rng.randint(1, 4)
        b = rng.randint(1, 5 - a)
        rows.append(row(group(key, a) + plus() + group(key, b) + plus("=") + choice_row(options(rng, a + b, 1, 6), a + b if i == 0 else None),
                        i == 0, 18))
        ans.append(a + b)
    return isec(num, "circle", L.w["r5"], "".join(rows)), f'<b>{", ".join(map(str, ans[1:]))}</b> {L.a["top_down"]}'


# Digits as ONE pen line each (the way they are written by hand), in a 40 x 60 box, starting where the pen starts.
DIGIT_PATHS = {
    0: "M20 5 C9 5 7 20 7 30 C7 42 10 55 20 55 C30 55 33 42 33 30 C33 18 30 5 20 5",
    1: "M11 15 L22 6 L22 54",
    2: "M8 16 C8 6 32 4 32 17 C32 28 16 38 8 54 L33 54",
    3: "M9 12 C14 4 32 5 31 16 C30 25 22 28 17 28 C26 28 33 33 32 42 C31 54 12 56 8 47",
    4: "M26 6 L6 38 L35 38 M26 6 L26 54",
    5: "M31 6 L11 6 L9 26 C14 22 32 20 32 38 C32 54 13 56 8 47",
    6: "M29 9 C22 4 8 8 8 30 C8 50 16 55 21 55 C28 55 33 49 33 41 C33 32 27 27 21 27 C14 27 9 32 8 37",
    7: "M7 6 L33 6 L16 54",
    8: ("M30 10 C27 5 13 5 10 12 C7 20 16 25 20 28 C26 32 33 36 33 43 C33 51 27 55 20 55 "
        "C13 55 7 51 7 43 C7 36 14 32 20 28 C25 25 31 20 30 12"),
    9: "M32 22 C32 14 27 6 20 6 C13 6 8 12 8 19 C8 27 14 32 20 32 C27 32 32 27 32 21 L32 30 C32 48 26 55 18 55 C13 55 10 53 9 51",
}


def digit(d, dotted, size=84):
    """A digit to trace: small dots along the pen line and a bigger dot where to start; or solid as the model."""
    path = DIGIT_PATHS[d]
    sx, sy = (float(v) for v in path[1:].split(" ")[:2])
    if dotted:
        line = (f'<path d="{path}" fill="none" stroke="#111" stroke-width="3.6" stroke-linecap="round" '
                'stroke-linejoin="round" stroke-dasharray="0.01 6.5"/>'
                f'<circle cx="{sx}" cy="{sy}" r="3.6" fill="#111"/>')
    else:
        line = f'<path d="{path}" fill="none" stroke="#111" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<svg width="{size * 2 // 3}" height="{size}" viewBox="0 0 40 60" style="flex:none">{line}</svg>'


def r_trace(rng, L, num):
    ds = rng.sample(range(1, 10), 4)
    rows = []
    for i, d in enumerate(ds):
        line = digit(d, False) + '<span style="width:14px"></span>' + "".join(digit(d, True) for _ in range(5))
        rows.append(row(f'<div style="display:flex;align-items:center;gap:22px">{line}</div>', i == 0, 30))
    return isec(num, "trace", L.w["r6"], "".join(rows)), "<b>" + ", ".join(map(str, ds)) + "</b>"


def r_pattern(rng, L, num):
    kinds = ["circle", "square", "triangle", "diamond", "star"]
    rows, ans = [], []
    for i in range(3):
        a, b, c = rng.sample(kinds, 3)
        unit = rng.choice([[a, b], [a, b], [a, a, b], [a, b, c]])
        seq = [unit[j % len(unit)] for j in range(8)]
        shown, missing = seq[:6], seq[6:]
        cells = "".join(shape(s, 46) for s in shown)
        if i == 0:
            blanks = "".join(f'<span style="border:2.5px dashed #111;border-radius:10px;padding:3px;display:inline-flex">{shape(s, 46)}</span>'
                             for s in missing)
        else:
            blanks = "".join('<span style="border:2.5px dashed #111;border-radius:10px;width:58px;height:58px;display:inline-block"></span>'
                             for _ in missing)
        rows.append(row(f'<div style="display:flex;gap:12px;align-items:center">{cells}</div>'
                        f'<div style="display:flex;gap:10px">{blanks}</div>', i == 0, 26))
        if i:
            ans.append(" ".join(shape(s, 18) for s in missing))
    return isec(num, "draw", L.w["r7"], "".join(rows)), " · ".join(ans)


def r_colour(rng, L, num):
    target = rng.choice(["circle", "square", "triangle", "rect"])
    others = [k for k in ("circle", "square", "triangle", "rect", "star") if k != target]
    n_target = rng.randint(3, 6)
    kinds = [target] * n_target + [rng.choice(others) for _ in range(14 - n_target)]
    rng.shuffle(kinds)
    cells = rng.sample(range(21), 14)  # 7 x 3 grid with jitter
    parts, example_done = [], False
    for kind, c in zip(kinds, cells):
        x, y = 12 + (c % 7) * 88 + rng.randint(-8, 8), 8 + (c // 7) * 92 + rng.randint(-6, 6)
        rot = rng.choice([0, 0, 15, -15, 30])
        fill = "#fff"
        if kind == target and not example_done:  # worked example: one target already coloured grey
            fill, example_done = "#bdbdbd", True
        parts.append(f'<g transform="translate({x},{y}) rotate({rot} 30 30) scale(1.36)" fill="{fill}">{SHAPE[kind]}</g>')
    svg = f'<svg width="640" height="290"><g stroke="#111" stroke-width="2" stroke-linejoin="round">{"".join(parts)}</g></svg>'
    sample = f'<span style="margin-left:6px">{shape(target, 40)}</span>'
    body = f'<div style="display:flex;justify-content:center">{svg}</div>'
    return isec(num, "colour", L.w["r8"], body, extra=sample), f'{shape(target, 18)} <b>{n_target}</b>'


# ================================================================ Year 1 autumn
def y_count_write(rng, L, num, key):
    ks = easy_first(rng.sample(range(1, 11), 3))
    rows = [row(f'<div style="width:220px;display:flex;justify-content:center">{objects(key, k, 30)}</div>'
                + (g.filled(k, 52) if i == 0 else g.box(52)), i == 0, 60) for i, k in enumerate(ks)]
    return isec(num, "write", L.w["y1"], "".join(rows)), f'<b>{", ".join(map(str, ks[1:]))}</b> {L.a["top_down"]}'


def y_tenframe_circle(rng, L, num):
    ks = easy_first(rng.sample(range(3, 11), 3))
    rows = [row(tenframe(k, 32) + choice_row(options(rng, k), k if i == 0 else None), i == 0, 50) for i, k in enumerate(ks)]
    return isec(num, "circle", L.w["y2"], "".join(rows)), f'<b>{", ".join(map(str, ks[1:]))}</b> {L.a["top_down"]}'


def side_arrow(label, to_left, w=70):
    """An arrow that goes FROM the middle number to a box, with -1 or +1 above it."""
    head = "M14 22 L4 30 L14 38" if to_left else f"M{w - 14} 22 L{w - 4} 30 L{w - 14} 38"
    return (f'<svg width="{w}" height="42" style="flex:none"><text x="{w / 2}" y="15" font-size="18" font-weight="900" '
            f'text-anchor="middle" fill="#111">{label}</text><g fill="none" stroke="#111" stroke-width="3" stroke-linecap="round" '
            f'stroke-linejoin="round"><path d="M4 30 L{w - 4} 30"/><path d="{head}"/></g></svg>')


def track(k, lo=None, hi=None, cell=25):
    """A small number track around k: the neighbours (1 less, 1 more) are grey, k is circled."""
    lo = max(0, k - 3) if lo is None else lo
    hi = lo + 6 if hi is None else hi
    cells = []
    for v in range(lo, hi + 1):
        bg = "#bdbdbd" if abs(v - k) == 1 else "#fff"
        ring = "border-radius:50%;" if v == k else "border-radius:6px;"
        cells.append(f'<span style="width:{cell}px;height:{cell}px;display:inline-flex;align-items:center;justify-content:center;'
                     f'border:2px solid #111;{ring}background:{bg};font-size:14px;font-weight:900">{v}</span>')
    return f'<div style="display:flex;gap:3px;justify-content:center">{"".join(cells)}</div>'


def more_less(k, left, right, with_track=False, mid_size=56):
    """1 less / 1 more: the number in the middle, arrows from it to the two boxes (no '2 -1 3 +1 4' reading)."""
    mid = big_num(k, mid_size)
    row_ = (f'<div style="display:flex;align-items:center;gap:2px">{left}{side_arrow("−1", True)}{mid}'
            f'{side_arrow("+1", False)}{right}</div>')
    if with_track:
        return f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px">{row_}{track(k)}</div>'
    return row_


def y_more_less(rng, L, num):
    ks = easy_first(rng.sample(range(1, 10), 4))
    items, ans = [], []
    for i, k in enumerate(ks):
        left = g.filled(k - 1, 50) if i == 0 else g.box(50)
        right = g.filled(k + 1, 50) if i == 0 else g.box(50)
        items.append(f'<div style="padding:6px 10px;{EX if i == 0 else ""}">{more_less(k, left, right, i == 0)}</div>')
        if i:
            ans.append(f"{k - 1} | {k} | {k + 1}")
    body = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;justify-items:center">{"".join(items)}</div>'
    return isec(num, "write", L.w["y3"], body), "<b>" + ", ".join(ans) + "</b>"


def y_compare(rng, L, num, key):
    items, ans = [], []
    for i in range(4):
        while True:
            a, b = rng.randint(1, 10), rng.randint(1, 10)
            if i == 0 and a != b or i > 0:
                break
        sym = "&gt;" if a > b else "&lt;" if a < b else "="
        mid = (f'<span class="box" style="width:48px;height:48px;display:inline-flex;align-items:center;justify-content:center;'
               f'font-size:28px;font-weight:900">{sym}</span>') if i == 0 else g.box(48)
        if i < 2:  # pictures first, then numbers
            l, r = objects(key, a, 22, 5, 3), objects(key, b, 22, 5, 3)
        else:
            l, r = g.num(a), g.num(b)
        items.append(f'<div style="display:flex;align-items:center;gap:8px;padding:8px 10px;{EX if i == 0 else ""}">{l}{mid}{r}</div>')
        if i:
            ans.append(f"{a} {sym} {b}")
    body = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;justify-items:center;align-items:center">{"".join(items)}</div>'
    return isec(num, "write", L.w["y4"], body), "<b>" + ", ".join(ans) + "</b>"


def numline(vals, miss, example):
    xs = [36 + 62 * i for i in range(11)]
    parts = ['<line x1="10" y1="22" x2="694" y2="22" stroke="#111" stroke-width="3"/>']
    for i, (x, v) in enumerate(zip(xs, vals)):
        parts.append(f'<line x1="{x}" y1="14" x2="{x}" y2="30" stroke="#111" stroke-width="3"/>')
        if i in miss:
            fill = "#e9e9e9" if i == example else "#fff"
            parts.append(f'<rect x="{x - 23}" y="40" width="46" height="40" rx="9" fill="{fill}" stroke="#111" stroke-width="2.5"/>')
            if i == example:
                parts.append(f'<text x="{x}" y="69" font-size="24" text-anchor="middle">{v}</text>')
        else:
            parts.append(f'<text x="{x}" y="69" font-size="24" text-anchor="middle">{v}</text>')
    return f'<svg width="704" height="86" style="font-weight:800">{"".join(parts)}</svg>'


def y_numberline(rng, L, num):
    lines, ans = [], []
    for back in (False, True):
        vals = list(range(10, -1, -1)) if back else list(range(11))
        miss = sorted(rng.sample(range(1, 11), 3))
        example = miss[0] if not back else None
        lines.append(numline(vals, miss, example))
        ans.append(", ".join(str(vals[i]) for i in miss if i != example))
    return isec(num, "write", L.w["y5"], '<div style="display:flex;flex-direction:column;align-items:center;gap:6px">'
                + "".join(lines) + "</div>"), "<b>" + " · ".join(ans) + "</b>"


def cherry(whole, a, b, hide, example):
    """Part-whole model: whole on top, two parts below. hide: 'whole', 'a' or 'b'."""
    def circ(x, y, v, hidden):
        txt = "" if hidden and not example else f'<text x="{x}" y="{y + 11}" font-size="30" text-anchor="middle" fill="#111">{v}</text>'
        fill = "#e9e9e9" if hidden and example else "#fff"
        return f'<circle cx="{x}" cy="{y}" r="30" fill="{fill}" stroke="#111" stroke-width="2.5"/>{txt}'
    return (f'<svg width="190" height="160" style="font-weight:900">'
            '<path d="M95 52 L45 112 M95 52 L145 112" stroke="#111" stroke-width="2.5"/>'
            f'{circ(95, 36, whole, hide == "whole")}{circ(45, 122, a, hide == "a")}{circ(145, 122, b, hide == "b")}</svg>')


def y_part_whole(rng, L, num):
    models, ans = [], []
    for i in range(3):
        whole = rng.randint(3, 10)
        a = rng.randint(1, whole - 1)
        hide = rng.choice(["whole", "a", "b"])
        models.append(f'<div style="padding:6px 10px;{EX if i == 0 else ""}">{cherry(whole, a, whole - a, hide, i == 0)}</div>')
        if i:
            ans.append(str({"whole": whole, "a": a, "b": whole - a}[hide]))
    body = f'<div style="display:flex;justify-content:space-around">{"".join(models)}</div>'
    return isec(num, "write", L.w["y6"], body), f'<b>{", ".join(ans)}</b>'


def y_add_story(rng, L, num, key):
    rows, ans = [], []
    for i in range(3):
        a = rng.randint(1, 6)
        b = rng.randint(1, 10 - a)
        res = g.filled(a + b, 52) if i == 0 else g.box(52)
        rows.append(row(group(key, a, 26) + plus() + group(key, b, 26) + plus("=") + res, i == 0, 16))
        if i:
            ans.append(f"{a} + {b} = {a + b}")
    return isec(num, "write", L.w["y7"], "".join(rows)), "<b>" + ", ".join(ans) + "</b>"


def y_take_away(rng, L, num, key):
    rows, ans = [], []
    for i in range(3):
        k = rng.randint(3, 10)
        b = rng.randint(1, k - 1)
        pic = objects(key, k, 30, 5, 6, crossed=b if i == 0 else 0)
        eq = (f'<span style="font-size:30px;font-weight:900;white-space:nowrap">{k} − {b} =</span>'
              + (g.filled(k - b, 52) if i == 0 else g.box(52)))
        rows.append(row(f'<div style="width:200px;display:flex;justify-content:center">{pic}</div>' + eq, i == 0, 40))
        if i:
            ans.append(f"{k} − {b} = {k - b}")
    return isec(num, "cross", L.w["y8"], "".join(rows)), "<b>" + ", ".join(ans) + "</b>"


def y_make_ten(rng, L, num):
    ks = rng.sample(range(1, 10), 4)
    items, ans = [], []
    for i, k in enumerate(ks):
        eq = (f'<span style="font-size:26px;font-weight:900;white-space:nowrap">{k} +</span>'
              + (g.filled(10 - k, 46) if i == 0 else g.box(46)) + '<span style="font-size:26px;font-weight:900">= 10</span>')
        items.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:8px 12px;{EX if i == 0 else ""}">'
                     f'{tenframe(k, 30)}<div style="display:flex;align-items:center;gap:8px">{eq}</div></div>')
        if i:
            ans.append(str(10 - k))
    body = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;justify-items:center">{"".join(items)}</div>'
    return isec(num, "write", L.w["y9"], body), "<b>" + ", ".join(ans) + "</b>"


SOLIDS = {k: v[0] for k, v in g.SHAPES3D.items()}


def y_shapes_match(rng, L, num):
    flat = rng.sample(["circle", "triangle", "square", "rect"], 2)
    solid = rng.sample(["cube", "cuboid", "sphere", "cone", "cylinder", "pyramid"], 3)
    pics = [("2d", k) for k in flat] + [("3d", k) for k in solid]
    rng.shuffle(pics)
    names = pics[:]
    rng.shuffle(names)
    name = lambda p: L.w["shape1"][p[1]] if p[0] == "2d" else L.w["shapes3d"][p[1]]
    rh, top, parts = 72, 42, []
    for i, (d, k) in enumerate(pics):
        y = top + i * rh
        pic = (f'<g transform="translate(70,{y - 30}) scale(1.36)">{SHAPE[k]}</g>' if d == "2d"
               else f'<g transform="translate(60,{y - 36}) scale(1.05)">{SOLIDS[k]}</g>')
        parts.append(pic + f'<circle cx="160" cy="{y}" r="5" fill="#111" stroke="none"/>')
    for i, p in enumerate(names):
        y = top + i * rh
        parts.append(f'<circle cx="400" cy="{y}" r="5" fill="#111" stroke="none"/>'
                     f'<text x="420" y="{y + 8}" font-size="24" font-weight="800" fill="#111" stroke="none">{name(p)}</text>')
    y2 = top + names.index(pics[0]) * rh
    parts.append(f'<path d="M160 {top} C280 {top} 280 {y2} 400 {y2}" fill="none" stroke-width="3"/>')  # worked example
    ex_bg = f'<rect x="50" y="{top - 34}" width="124" height="68" rx="12" fill="#e9e9e9" stroke="none"/>'
    svg = f'<svg width="640" height="{top + 4 * rh + 40}"><g {ST}>{ex_bg}<g fill="#fff">{"".join(parts)}</g></g></svg>'
    ans = ", ".join(name(p) for p in pics[1:])
    return isec(num, "match", L.w["y10"], f'<div style="display:flex;justify-content:center">{svg}</div>'), f'<b>{ans}</b> {L.a["top_down"]}'


# ================================================================ assemble
LAYOUT = {  # tasks per page; the last task of every page stretches to fill it
    "R": [(r_ladybirds, r_count_circle), (r_more, r_draw_dots), (r_altogether, r_trace), (r_pattern, r_colour)],
    "Y1A": [(y_count_write, y_tenframe_circle, y_more_less), (y_compare, y_numberline, y_part_whole),
            (y_add_story, y_take_away), (y_make_ten, y_shapes_match)],
}
NEEDS_OBJECT = {r_count_circle, r_more, r_altogether, y_count_write, y_compare, y_add_story, y_take_away}


def build(stage, seed, L):
    rng = random.Random(seed)
    keys = rng.sample(["apple", "star", "flower", "ball", "heart"], 4)  # no fish: too flat when drawn small
    pages_html, answers, num = [], [], 0
    for pi, group_ in enumerate(LAYOUT[stage]):
        secs = []
        for j, task in enumerate(group_):
            num += 1
            args = (rng, L, num) + ((keys[num % 4],) if task in NEEDS_OBJECT else ())
            html, ans = task(*args)
            if j == len(group_) - 1:  # last section on the page fills the rest of it
                # the title stays on top; the spare space is shared above and below the task (CSS .stretch, as in topics)
                html = html.replace('<section class="sec">', '<section class="sec stretch" style="flex:1;display:flex;flex-direction:column">', 1)
            secs.append(html)
            answers.append(ans)
        head = g.header(L, text(L.w["badge_stage"], stage=L.w["stages"][stage], seed=seed)) if pi == 0 else ""
        pages_html.append(g.page(head + "".join(secs), "padding-bottom:36px" if pi == 0 else ""))
    pages_html = g.number_pages(pages_html)
    a = L.a
    rows = "".join(f'<div class="a"{' style="border-bottom:none"' if i == len(answers) - 1 else ""}><span class="n">{i + 1}</span>'
                   f'<span style="flex:1">{x}</span><span class="tag">{a["period"][stage]}</span></div>' for i, x in enumerate(answers))
    sub = text(a["sub_stage"], seed=seed, stage=a["stages"][stage])
    answer_page = g.page(f'<h1 style="margin:0 0 2px;font-size:32px;font-weight:900">{a["answers"]}</h1>'
                         f'<p style="margin:0 0 8px;font-size:15px;font-weight:600">{sub}<br>{a["legend"]}</p>' + rows,
                         "padding:40px 52px;gap:0")
    return pages_html, answer_page
