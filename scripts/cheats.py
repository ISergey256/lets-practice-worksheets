"""Cheat sheets: one card per task type, to study before doing the worksheet (Reception and Year 1 autumn).

A parent or teacher picks the tasks the child needs help with. Every card has the same order, so the child
always knows where to look:  title · LOOK (a worked example) · DO (3 short steps) · CHECK · TRY (one mini task)
· "I can do it!" box. Two cards per A4 page. The numbers differ from the worksheet (own random generator),
so a card never gives away the worksheet's answers. Texts: i18n.CHEAT, in the worksheet language.
"""
import random

import generate as g
import stages as s
from i18n import CHEAT

ST = g.S
TASK_ACTION = {  # card key -> action icon of the task it explains
    "R1": "match", "R2": "circle", "R3": "tick", "R4": "draw", "R5": "circle", "R6": "trace", "R7": "draw", "R8": "colour",
    "Y1": "write", "Y2": "circle", "Y3": "write", "Y4": "write", "Y5": "write", "Y6": "write", "Y7": "write", "Y8": "cross",
    "Y9": "write", "Y10": "match",
}
COUNT = {"R": 8, "Y1A": 10}
LOOK_ZOOM = {"R1": 1.35, "R2": 1.45, "R3": 1.15, "R4": 1.2, "R5": 0.95, "R6": 1.15, "R7": 1.35, "R8": 1.15,
             "Y1": 1.05, "Y2": 1.3, "Y3": 1.45, "Y4": 1.45, "Y5": 1.45, "Y6": 0.95, "Y7": 0.9, "Y8": 0.95, "Y9": 1.0, "Y10": 1.45}
TRY_ZOOM = {"Y6": 0.6}


def card_keys(stage):
    return [f'{"R" if stage == "R" else "Y"}{i}' for i in range(1, COUNT[stage] + 1)]


def titles(level, lang):
    """[(task number on the sheet, card title)] for the website check boxes."""
    return [(n, CHEAT[lang][k][0]) for n, k in available(level)]


# ---------------------------------------------------------------- small pictures
def lady(k, scale=1.0):
    return (f'<svg width="{62 * scale:.0f}" height="{74 * scale:.0f}" viewBox="-31 -42 62 74" style="flex:none">'
            f'<g {ST}>{s.ladybird(0, 0, k, 1)}</g></svg>')


def ringed(n, size=34):
    return f'<span class="opt" style="font-size:{size}px">{n}{s.RING}</span>'


def counted(key, k, size=36):
    """Objects in a row with 1, 2, 3 ... under them (the last number is the answer)."""
    parts = []
    for i in range(k):
        x = 2 + i * (size + 8)
        parts.append(s.obj(key, x, 2, size))
        weight, fs = ("900", 22) if i == k - 1 else ("700", 17)
        parts.append(f'<text x="{x + size / 2}" y="{size + 26}" font-size="{fs}" font-weight="{weight}" text-anchor="middle" '
                     f'fill="#111" stroke="none">{i + 1}</text>')
    return f'<svg width="{k * (size + 8)}" height="{size + 34}" style="flex:none"><g {ST}>{"".join(parts)}</g></svg>'


def mini_plate(key, k, ticked=None):
    tick = '<path d="M7 16 L13 22 L25 8" fill="none" stroke="#111" stroke-width="3.5" stroke-linecap="round"/>'
    box = (f'<svg width="32" height="32"><rect x="2" y="2" width="28" height="28" rx="7" fill="#fff" stroke="#111" stroke-width="2.5"/>'
           f'{tick if ticked else ""}</svg>')
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">'
            f'<div style="width:136px;height:70px;border:2.5px solid #111;border-radius:50%;display:flex;align-items:center;justify-content:center">'
            f'{s.objects(key, k, 18, 5, 4)}</div>{box}</div>')


def flex(*parts, gap=14):  # one line: a worked example must read left to right, never wrap
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:{gap}px">{"".join(parts)}</div>'


def bigtext(t, size=30):
    return f'<span style="font-size:{size}px;font-weight:900;white-space:nowrap">{t}</span>'


def mini_line(vals, blank, shown_answer=False):
    xs = [24 + 56 * i for i in range(len(vals))]
    parts = [f'<line x1="6" y1="16" x2="{xs[-1] + 18}" y2="16" stroke="#111" stroke-width="3"/>']
    for i, (x, v) in enumerate(zip(xs, vals)):
        parts.append(f'<line x1="{x}" y1="8" x2="{x}" y2="24" stroke="#111" stroke-width="3"/>')
        if i == blank:
            fill = "#e9e9e9" if shown_answer else "#fff"
            parts.append(f'<rect x="{x - 21}" y="32" width="42" height="36" rx="8" fill="{fill}" stroke="#111" stroke-width="2.5"/>')
        if i != blank or shown_answer:
            parts.append(f'<text x="{x}" y="58" font-size="22" font-weight="800" text-anchor="middle">{v}</text>')
    return f'<svg width="{xs[-1] + 26}" height="72" style="flex:none">{"".join(parts)}</svg>'


def pattern_row(seq, blank_answer=None, size=34):
    cells = "".join(s.shape(k, size) for k in seq)
    inner = s.shape(blank_answer, size) if blank_answer else ""
    blank = (f'<span style="border:2.5px dashed #111;border-radius:9px;width:{size + 8}px;height:{size + 8}px;'
             f'display:inline-flex;align-items:center;justify-content:center">{inner}</span>')
    return flex(cells, blank, gap=8)


def labelled_shape(pic, name):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">{pic}'
            f'<span style="font-size:15px;font-weight:800">{name}</span></div>')


def solid(k, size=60):
    return f'<svg width="{size}" height="{size * 7 // 8}" viewBox="0 0 80 70" style="flex:none">{g.SHAPES3D[k][0]}</svg>'


# ---------------------------------------------------------------- LOOK (worked example) and TRY per card
def pictures(key, rng, obj, L):
    """Return (look_html, try_html) for one card."""
    opts = lambda k, lo=1, hi=10: s.choice_row(s.options(rng, k, lo, hi))
    if key == "R1":
        k = rng.randint(1, 5)
        return flex(lady(4, 1.5), s.arrow(), ringed(4)), flex(lady(k, 1.1), opts(k, 1, 5))
    if key == "R2":
        k = rng.randint(3, 8)
        return flex(counted(obj, 4), ringed(4), gap=10), flex(s.objects(obj, k, 26), opts(k))
    if key == "R3":
        a, b = rng.sample([2, 3, 4, 6, 7, 8], 2)
        return flex(mini_plate(obj, 5, True), mini_plate(obj, 2, False)), flex(mini_plate(obj, a), mini_plate(obj, b))
    if key == "R4":
        k = rng.randint(2, 9)
        return flex(s.big_num(6, 50), s.arrow(), s.tenframe(6, 30)), flex(s.big_num(k, 44), s.tenframe(0, 26))
    if key == "R5":
        a = rng.randint(1, 3)
        b = rng.randint(1, 5 - a)
        return (flex(s.group(obj, 2, 17), s.plus(), s.group(obj, 3, 17), s.plus("="), ringed(5, 30), gap=6),
                flex(s.group(obj, a, 20), s.plus(), s.group(obj, b, 20), s.plus("="), opts(a + b, 1, 6), gap=8))
    if key == "R6":
        d = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return flex(s.digit(3, False, 96), s.arrow(), s.digit(3, True, 96)), flex(*(s.digit(d, True, 70) for _ in range(4)), gap=18)
    if key == "R7":
        a, b, c = rng.sample(["circle", "square", "triangle", "star", "diamond"], 3)
        return (pattern_row(["circle", "square", "circle", "square", "circle"], "square"),
                pattern_row([a, a, b, a, a, b, a], "") if rng.random() < 0.5 else pattern_row([a, b, c, a, b], ""))
    if key == "R8":
        t = rng.choice(["square", "triangle", "circle"])
        others = [x for x in ("circle", "square", "triangle", "rect", "star") if x != t]
        row_ = [t, rng.choice(others), t, rng.choice(others), t]
        rng.shuffle(row_)
        look = flex(f'<span style="background:#e9e9e9;border-radius:10px;padding:4px;display:inline-flex">{s.shape("triangle", 46)}</span>',
                    s.arrow(), s.shape("triangle", 40, "#bdbdbd"), s.shape("square", 40),
                    f'<span style="display:inline-flex;transform:rotate(25deg)">{s.shape("triangle", 40, "#bdbdbd")}</span>',
                    s.shape("circle", 40), gap=8)
        return look, flex(s.shape(t, 34), bigtext("→", 24), *(s.shape(x, 34) for x in row_), gap=8)
    if key == "Y1":
        k = rng.randint(3, 9)
        return flex(counted(obj, 5, 32), g.filled(5, 50), gap=12), flex(s.objects(obj, k, 26), g.box(50))
    if key == "Y2":
        k = rng.randint(6, 10)
        look = flex('<div style="display:flex;flex-direction:column;align-items:center;gap:4px">'
                    f'{s.tenframe(7, 32)}<span style="font-size:16px;font-weight:800">5 … 6, 7</span></div>', ringed(7))
        return look, flex(s.tenframe(k, 26), opts(k))
    if key == "Y3":
        k = rng.randint(2, 9)
        return (s.more_less(4, g.filled(3, 48), g.filled(5, 48), True, 52),
                s.more_less(k, g.box(46), g.box(46), False, 52))
    if key == "Y4":
        a, b = rng.sample(range(1, 11), 2)
        sym_box = lambda t: (f'<span class="box" style="width:46px;height:46px;display:inline-flex;align-items:center;'
                             f'justify-content:center;font-size:28px;font-weight:900">{t}</span>')
        look = ('<div style="display:flex;flex-direction:column;gap:10px;align-items:center">'
                + flex(g.num(7), sym_box("&gt;"), g.num(3), gap=8) + flex(g.num(5), sym_box("="), g.num(5), gap=8) + "</div>")
        return look, flex(g.num(a), g.box(46), g.num(b), gap=8)
    if key == "Y5":
        st = rng.randint(0, 5)
        return mini_line([4, 5, 6, 7, 8], 2, True), mini_line(list(range(st, st + 5)), rng.randint(1, 3))
    if key == "Y6":
        w = rng.randint(4, 10)
        a = rng.randint(1, w - 1)
        return (flex(s.cherry(7, 4, 3, "b", True), bigtext("4 + 3 = 7", 24), gap=8),
                s.cherry(w, a, w - a, rng.choice(["whole", "a", "b"]), False))
    if key == "Y7":
        a = rng.randint(1, 5)
        b = rng.randint(1, 9 - a)
        return (flex(s.group(obj, 3, 17), s.plus(), s.group(obj, 2, 17), s.plus("="), g.filled(5, 46), gap=6),
                flex(s.group(obj, a, 20), s.plus(), s.group(obj, b, 20), s.plus("="), g.box(46), gap=8))
    if key == "Y8":
        k = rng.randint(4, 9)
        b = rng.randint(1, k - 1)
        return (flex(s.objects(obj, 6, 22, 6, 4, crossed=2), bigtext("6 − 2 =", 26), g.filled(4, 44), gap=8),
                flex(s.objects(obj, k, 24, 5, 5), bigtext(f"{k} − {b} ="), g.box(46), gap=10))
    if key == "Y9":
        k = rng.randint(1, 9)
        return (flex(s.tenframe(7, 30), bigtext("7 +", 26), g.filled(3, 44), bigtext("= 10", 26), gap=8),
                flex(s.tenframe(k, 26), bigtext(f"{k} +", 26), g.box(44), bigtext("= 10", 26), gap=8))
    if key == "Y10":
        names = L.w["shape1"]
        flat = flex(labelled_shape(s.shape("circle", 40), names["circle"]), labelled_shape(s.shape("square", 40), names["square"]),
                    labelled_shape(s.shape("triangle", 40), names["triangle"]), gap=12)
        solids = flex(labelled_shape(solid("cube", 54), L.w["shapes3d"]["cube"]),
                      labelled_shape(solid("cone", 54), L.w["shapes3d"]["cone"]), gap=12)
        k = rng.choice(["circle", "square", "triangle", "rect"])
        wrong = rng.choice([x for x in ("circle", "square", "triangle", "rect") if x != k])
        pair = sorted([names[k], names[wrong]])
        try_ = flex(s.shape(k, 46), *(f'<span style="font-size:20px;font-weight:800;border-bottom:2px dotted #111">{n}</span>' for n in pair), gap=18)
        return f'<div style="display:flex;flex-direction:column;gap:8px">{flat}{solids}</div>', try_
    raise KeyError(key)


def card(num, key, look, try_, C):
    title, s1, s2, s3, check = C[key]
    look_l, do_l, check_l, try_l, ican = C["labels"]
    steps = "".join(f'<div class="cs"><span class="csn">{i}</span><span>{t}</span></div>' for i, t in enumerate((s1, s2, s3), 1))
    return (f'<div class="card" data-task="{key}"><div class="ch"><span class="n">{num}</span>{s.action(TASK_ACTION[key], 50)}'
            f'<span class="ct">{title}</span></div>'
            f'<div class="cm"><div class="cl"><span class="lab">{look_l}</span>'
            f'<div class="cpic"><div style="zoom:{LOOK_ZOOM.get(key, 1)}">{look}</div></div></div>'
            f'<div class="cd"><span class="lab">{do_l}</span>{steps}</div></div>'
            f'<div class="cc"><span class="lab">{check_l}</span>'
            f'<svg width="26" height="26" viewBox="0 0 26 26" style="flex:none"><path d="M4 14 L10 20 L22 6" fill="none" stroke="#111" '
            f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg><span>{check}</span></div>'
            f'<div class="ctr"><span class="lab">{try_l}</span><div style="flex:1;zoom:{TRY_ZOOM.get(key, 1)}">{try_}</div>'
            f'<span class="ican">{g.box(30, r=7)}{ican}</span></div></div>')


def available(level):
    """Cards for a sheet: [(task number on the sheet, card key)]. level: "R", "Y1A" or a topic spec "T:..."."""
    if level.startswith("T:"):
        import topics
        return topics.cards(level)
    return [(i + 1, k) for i, k in enumerate(card_keys(level))]


def build(level, seed, L, which=None):
    """Cheat-sheet pages for the chosen task numbers (default: all available cards), two cards per page."""
    cards = available(level)
    nums = {n for n, _ in cards}
    which = sorted({int(w) for w in which} if which else nums)
    if any(w not in nums for w in which):
        raise ValueError(f"cheat cards exist for tasks {sorted(nums)}")
    rng = random.Random(f"cheat-{level}-{seed}")  # str seed: same numbers in CPython and in Pyodide
    obj = rng.choice(["apple", "star", "flower", "ball", "heart"])
    C = CHEAT[L.wl]
    out = []
    for n, key in cards:
        if n in which:
            look, try_ = pictures(key, rng, obj, L)
            out.append(card(n, key, look, try_, C))
    return g.number_pages([g.page("".join(out[i:i + 2]), "gap:16px") for i in range(0, len(out), 2)])
