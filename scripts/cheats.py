"""Help cards ("cheat sheets"): one card per task type, to study before doing the worksheet.
Cards exist for every topic: Reception (R1-R8), Year 1 autumn (Y1-Y10) and the Year 1 review tasks (V1-V18).

A parent or teacher picks the tasks the child needs help with. Every card has the same order, so the child
always knows where to look:  title · LOOK (a worked example) · DO (3 short steps) · CHECK · TRY (one mini task)
· "I can do it!" box. Two cards per A4 page. The numbers differ from the worksheet (own random generator),
so a card never gives away the worksheet's answers. Texts: i18n.CHEAT, in the worksheet language.
"""
import random

import generate as g
import i18n
import stages as s
from i18n import CHEAT

ST = g.S
TASK_ACTION = {  # card key -> action icon of the task it explains
    "R1": "match", "R2": "circle", "R3": "tick", "R4": "draw", "R5": "circle", "R6": "trace", "R7": "draw", "R8": "colour",
    "Y1": "write", "Y2": "circle", "Y3": "write", "Y4": "write", "Y5": "write", "Y6": "write", "Y7": "write", "Y8": "cross",
    "Y9": "write", "Y10": "match",
    **{f"V{t}": a for t, a in g.TASK_ACTION.items()},  # Year 1 review topics: the same icon as the task
}
COUNT = {"R": 8, "Y1A": 10}
LOOK_ZOOM = {"R1": 1.35, "R2": 1.45, "R3": 1.15, "R4": 1.2, "R5": 0.95, "R6": 1.15, "R7": 1.35, "R8": 1.15,
             "Y1": 1.05, "Y2": 1.3, "Y3": 1.45, "Y4": 1.45, "Y5": 1.45, "Y6": 0.95, "Y7": 0.9, "Y8": 0.95, "Y9": 1.0, "Y10": 1.45}
TRY_ZOOM = {"Y6": 0.6, "V9": 1.1, "V12": 1.2, "V17": 1.2, "V18": 1.3}
LOOK_ZOOM.update({"V1": 1.45, "V2": 1.35, "V3": 1.4, "V4": 1.4, "V5": 1.3, "V6": 1.25, "V7": 1.5, "V8": 1.2, "V9": 1.7,
                  "V10": 1.35, "V11": 1.3, "V12": 1.6, "V13": 1.0, "V14": 1.4, "V15": 1.25, "V16": 1.6, "V17": 1.6, "V18": 1.5})


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
    if key.startswith("V"):
        return review_pictures(key, rng, obj, L)
    raise KeyError(key)


# ---------------------------------------------------------------- Year 1 review topics (V1..V18): helpers
def col(*parts, gap=8):
    return f'<div style="display:flex;flex-direction:column;align-items:center;gap:{gap}px">{"".join(parts)}</div>'


def small(t, size=16):
    return f'<span style="font-size:{size}px;font-weight:800;white-space:nowrap">{t}</span>'


def grey(html, pad=4):
    return f'<span style="background:#e9e9e9;border-radius:10px;padding:{pad}px;display:inline-flex;align-items:center">{html}</span>'


def pairs(k, r=8, odd_ring=False):
    """k dots in pairs (two rows); an odd number leaves one dot alone, circled when odd_ring."""
    cols_ = (k + 1) // 2
    parts = []
    for i in range(k):
        cx, cy = 14 + (i // 2) * 26, 14 + (i % 2) * 26
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111"/>')
    for c in range(k // 2):  # a frame around every pair
        parts.append(f'<rect x="{2 + c * 26}" y="2" width="24" height="50" rx="11" fill="none" stroke="#111" stroke-width="2"/>')
    if k % 2 and odd_ring:
        cx = 14 + (k // 2) * 26
        parts.append(f'<circle cx="{cx}" cy="14" r="{r + 5}" fill="none" stroke="#111" stroke-width="2.5" stroke-dasharray="3 3"/>')
    return f'<svg width="{cols_ * 26 + 4}" height="56" style="flex:none">{"".join(parts)}</svg>'


def jumps(vals, blank, shown=False, step_label=None):
    """A number track with '+n' above every jump."""
    w = 52
    parts = []
    for i, v in enumerate(vals):
        x = 4 + i * w
        fill = "#e9e9e9" if i == blank and shown else "#fff"
        parts.append(f'<rect x="{x}" y="30" width="42" height="38" rx="8" fill="{fill}" stroke="#111" stroke-width="2.5"/>')
        if i != blank or shown:
            parts.append(f'<text x="{x + 21}" y="57" font-size="20" font-weight="900" text-anchor="middle">{v}</text>')
        if i and step_label:
            parts.append(f'<path d="M{x - w + 26} 28 Q{x - w / 2 + 21} 8 {x + 16} 28" fill="none" stroke="#111" stroke-width="2"/>'
                         f'<text x="{x - w / 2 + 21}" y="12" font-size="13" font-weight="900" text-anchor="middle">{step_label}</text>')
    return f'<svg width="{len(vals) * w}" height="72" style="flex:none">{"".join(parts)}</svg>'


def sided(n, size=70, numbers=True):
    """A regular polygon with its sides numbered 1..n."""
    import math
    pts = [(45 + 38 * math.cos(math.radians(-90 + 360 * i / n)), 45 + 38 * math.sin(math.radians(-90 + 360 * i / n))) for i in range(n)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    labels = ""
    if numbers:
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            lx, ly = 45 + (mx - 45) * 1.32, 45 + (my - 45) * 1.32
            labels += f'<text x="{lx:.1f}" y="{ly + 5:.1f}" font-size="13" font-weight="900" text-anchor="middle">{i + 1}</text>'
    return (f'<svg width="{size}" height="{size}" viewBox="-6 -6 102 102" style="flex:none"><path d="{d}" fill="#fff" stroke="#111" '
            f'stroke-width="3" stroke-linejoin="round"/>{labels}</svg>')


def bars(lengths, ring=None, h=14):
    parts = []
    for i, ln in enumerate(lengths):
        y = 8 + i * (h + 14)
        parts.append(f'<rect x="4" y="{y}" width="{ln}" height="{h}" rx="4" fill="#fff" stroke="#111" stroke-width="2.5"/>')
        if ring == i:
            parts.append(f'<rect x="-2" y="{y - 5}" width="{ln + 12}" height="{h + 10}" rx="{(h + 10) / 2}" fill="none" stroke="#111" stroke-width="2.5"/>')
    parts.append(f'<line x1="4" y1="0" x2="4" y2="{len(lengths) * (h + 14) + 6}" stroke="#111" stroke-width="2" stroke-dasharray="3 3"/>')
    return (f'<svg width="{max(lengths) + 26}" height="{len(lengths) * (h + 14) + 10}" viewBox="-4 0 {max(lengths) + 30} {len(lengths) * (h + 14) + 10}" '
            f'style="flex:none">{"".join(parts)}</svg>')


def wall(rows, blanks=(), shown=False, bw=46):
    """rows bottom-up, e.g. [[2, 3], [5]]; blanks = {(r, i)} empty unless shown (then grey)."""
    html = []
    for r in range(len(rows) - 1, -1, -1):
        cells = []
        for i, v in enumerate(rows[r]):
            empty = (r, i) in blanks
            bg = "#e9e9e9" if empty and shown else "#fff"
            cells.append(f'<span class="brick" style="width:{bw}px;height:40px;font-size:20px;background:{bg}">{"" if empty and not shown else v}</span>')
        html.append(f'<div class="row">{"".join(cells)}</div>')
    return f'<div style="display:flex;flex-direction:column;gap:2px">{"".join(html)}</div>'


def box_scene(item, where, size=0.95):
    """A box and an item (generate.ITEMS) in / on / under / next to it."""
    pos = {"on": (60, 48), "in": (60, 108), "under": (60, 132), "next to": (132, 112)}[where]
    lid = '' if where == "in" else ''
    body = (f'<rect x="20" y="48" width="80" height="62" rx="4" fill="#fff" stroke="#111" stroke-width="3"/>'
            f'<line x1="0" y1="112" x2="160" y2="112" stroke="#111" stroke-width="2.5"/>')
    obj_ = f'<g transform="translate({pos[0]},{pos[1]}) scale({size})" fill="#fff" stroke="#111" stroke-width="4">{g.ITEMS[item]}</g>'
    if where == "under":  # the box stands on a little table; the item is under it
        body = (f'<rect x="20" y="20" width="80" height="50" rx="4" fill="#fff" stroke="#111" stroke-width="3"/>'
                f'<line x1="14" y1="72" x2="106" y2="72" stroke="#111" stroke-width="4"/><line x1="22" y1="72" x2="22" y2="132" stroke="#111" stroke-width="3"/>'
                f'<line x1="98" y1="72" x2="98" y2="132" stroke="#111" stroke-width="3"/><line x1="0" y1="133" x2="160" y2="133" stroke="#111" stroke-width="2.5"/>')
    front = f'<rect x="20" y="70" width="80" height="40" fill="#fff" stroke="#111" stroke-width="3"/>' if where == "in" else ""
    return f'<svg width="120" height="110" viewBox="0 -20 170 150" style="flex:none">{body}{obj_}{front}</svg>'


def ducks(n, labels, scale=0.62):
    """n ducks walking to the pond on the right; labels[i] under duck i (counted from the pond)."""
    w = 64 * scale + 8
    parts = []
    for i in range(n):
        x = 4 + i * w
        parts.append(f'<g transform="translate({x},6) scale({scale})" fill="#fff" stroke="#111" stroke-width="4">{g.DUCK}</g>')
        lab = labels[n - 1 - i]
        if lab is not None:
            parts.append(f'<rect x="{x + 1}" y="50" width="{w - 6}" height="26" rx="13" fill="{"#e9e9e9" if lab else "#fff"}" stroke="#111" stroke-width="2"/>'
                         f'<text x="{x + w / 2 - 2}" y="68" font-size="15" font-weight="900" text-anchor="middle">{lab}</text>')
    px = 4 + n * w
    parts.append(f'<ellipse cx="{px + 30}" cy="30" rx="28" ry="12" fill="#fff" stroke="#111" stroke-width="2.5"/>'
                 f'<path d="M{px + 16} 30 q7 -6 14 0 t14 0" fill="none" stroke="#111" stroke-width="2"/>')
    return f'<svg width="{px + 64}" height="80" style="flex:none">{"".join(parts)}</svg>'


def review_pictures(key, rng, obj, L):
    """(look, try) for the Year 1 review cards V1..V18. Numbers are the card's own, never the worksheet's."""
    t = int(key[1:])
    if t == 1:  # count a large group: rows of 5
        k = rng.randint(11, 16)
        look = flex(col(s.objects(obj, 12, 22, 5, 4), small("5, 10 … 11, 12", 16)), g.filled(12, 48))
        return look, flex(s.objects(obj, k, 20, 5, 4), g.box(48))
    if t == 2:  # estimate, then count
        lab = lambda w_, v: col(small(w_, 14), g.filled(v, 40) if v is not None else g.box(40), gap=3)
        k = rng.randint(7, 14)
        look = flex(s.objects(obj, 9, 18, 5, 3), lab(L.w["estimate"], 10), lab(L.w["counted"], 9), gap=10)
        return look, flex(s.objects(obj, k, 18, 5, 3), lab(L.w["estimate"], None), lab(L.w["counted"], None), gap=10)
    if t == 3:  # odd and even: make pairs
        k = rng.choice([5, 6, 7, 8, 9])
        word = lambda w_: f'<span style="font-size:19px;font-weight:900;border-bottom:2px dotted #111">{w_}</span>'
        look = col(flex(pairs(6), small("6 →", 18), grey(small(L.a["even"], 18))),
                   flex(pairs(5, odd_ring=True), small("5 →", 18), grey(small(L.a["odd"], 18))), gap=6)
        return look, flex(pairs(k), word(L.a["odd"]), word(L.a["even"]), gap=16)
    if t == 4:  # number line with a jump
        st = rng.choice([1, 2, 5])
        a = rng.randint(0, 4) * st
        return (jumps([2, 4, 6, 8, 10], 3, True, "+2"),
                jumps([a + i * st for i in range(5)], rng.randint(2, 4), False, None))
    if t == 5:  # compare: tens first
        a, b = rng.sample(range(11, 50), 2)
        sym = lambda c: (f'<span class="box" style="width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;'
                         f'font-size:26px;font-weight:900;background:#e9e9e9">{c}</span>')
        look = col(flex(g.num(7), sym("&gt;"), g.num(3), gap=8), flex(g.num(32), sym("&gt;"), g.num(23), gap=8))
        return look, flex(g.num(a), g.box(44), g.num(b), gap=8)
    if t == 6:  # numbers in words: a little word list
        k = rng.randint(3, 8)
        row_ = lambda v, done=True: flex(g.num(v), small(i18n.numwords(L.wl, v), 20), gap=10)
        look = col(*(row_(v) for v in (k, k + 1, k + 2)), gap=4)
        line = '<span style="display:inline-block;width:150px;border-bottom:2.5px solid #111;height:26px"></span>'
        return look, flex(g.num(k + 1), line, gap=10)
    if t == 7:  # faces and edges
        head = L.w["th3"]
        k = rng.choice(["cuboid", "cylinder", "cone", "pyramid"])
        look = flex(solid("cube", 70), col(small(head[2], 15), g.filled(6, 40), gap=2), col(small(head[3], 15), g.filled(12, 40), gap=2))
        return look, flex(solid(k, 64), col(small(head[2], 15), g.box(40), gap=2), col(small(head[3], 15), g.box(40), gap=2))
    if t == 8:  # find one kind of shape in a picture
        seq = ["circle", "triangle", "circle", "square", "circle", "rect"]
        tick = '<svg width="20" height="16"><path d="M3 8 L8 13 L17 3" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round"/></svg>'
        look = flex(*(col(tick if k == "circle" else '<span style="height:16px"></span>', s.shape(k, 34), gap=1) for k in seq),
                    s.arrow(), g.filled(3, 42), gap=6)
        target = rng.choice(["triangle", "square", "circle"])
        mix = [target] * rng.randint(2, 4) + rng.sample(["circle", "square", "triangle", "rect", "star"], 3)
        rng.shuffle(mix)
        return look, flex(grey(s.shape(target, 30)), small("→", 20), *(s.shape(k, 30) for k in mix), g.box(40), gap=6)
    if t == 9:  # count the sides
        n = rng.choice([3, 4, 6, 8])
        return flex(sided(5, 92), s.arrow(), g.filled(5, 46)), flex(sided(n, 76, False), g.box(46))
    if t == 10:  # shade a part
        d = rng.choice([2, 4])
        kind = rng.choice(["circle", "square"])
        frac = {2: "½", 4: "¼"}
        look = flex(col(g.frac_shape("square", 4, True, rng, 1), small("¼", 26), gap=2),
                    col(g.frac_shape("circle", 2, True, rng, 1), small("½", 26), gap=2), gap=24)
        return look, flex(g.frac_shape(kind, d, True, rng), small(frac[d], 30), gap=12)
    if t == 11:  # equal parts
        cross = '<svg width="34" height="34"><path d="M8 8 L26 26 M26 8 L8 26" stroke="#111" stroke-width="3.5" stroke-linecap="round"/></svg>'
        look = flex(col(g.frac_shape("square", 4, True, rng), g.filled("✓", 36), gap=4),
                    col(g.frac_shape("rect", 3, False, rng), cross, gap=4), gap=26)
        k = rng.choice(["circle", "square", "rect"])
        return look, flex(g.frac_shape(k, rng.choice([2, 4]) if k != "rect" else 4, rng.random() < 0.5, rng), g.box(40), gap=14)
    if t == 12:  # longest / tallest: line them up at one end
        ls = rng.sample([70, 100, 130, 160], 3)
        return bars([90, 150, 60], ring=1), bars(ls)
    if t == 13:  # number bonds: a system
        n = rng.randint(5, 8)
        eq = lambda a, b, tot, done=True: flex(g.filled(a, 32) if done else g.box(32), small("+", 20), g.filled(b, 32) if done else g.box(32),
                                              small(f"= {tot}", 20), gap=4)
        look = col(*(eq(a, 4 - a, 4) for a in range(5)), gap=2)
        return look, col(flex(g.filled(0, 32), small("+", 20), g.box(32), small(f"= {n}", 20), gap=4),
                         flex(g.filled(1, 32), small("+", 20), g.box(32), small(f"= {n}", 20), gap=4), gap=4)
    if t == 14:  # counting in steps
        st = rng.choice([2, 5, 10])
        return jumps([0, 5, 10, 15, 20], 4, True, "+5"), jumps([i * st for i in range(5)], 4, False, None)
    if t == 15:  # number sentences, also with "=" on the left
        a = rng.randint(1, 6)
        b = rng.randint(a + 1, 10)
        look = col(flex(small("3 + 4 =", 26), g.filled(7, 42), gap=6), flex(g.filled(5, 42), small("= 2 + 3", 26), gap=6), gap=6)
        return look, flex(small(f"{a} +", 26), g.box(42), small(f"= {b}", 26), gap=6)
    if t == 16:  # number walls
        a, b, c = (rng.randint(1, 5) for _ in range(3))
        look = wall([[2, 3], [5]], {(1, 0)}, True)
        return look, wall([[a, b, c], [a + b, b + c], [a + 2 * b + c]], {(1, 0), (1, 1), (2, 0)}, False, 42)
    if t == 17:  # where is it?
        word = lambda w_, shown: (f'<span style="font-size:20px;font-weight:900;border-bottom:2.5px solid #111;min-width:96px;'
                                  f'display:inline-block;text-align:center;{"background:#e9e9e9" if shown else ""}">{w_ if shown else "&nbsp;"}</span>')
        look = flex(box_scene("ball", "on"), word(L.w["pos"]["on"], True), gap=10)
        where = rng.choice(["in", "next to"])
        return look, flex(box_scene(rng.choice(["cat", "teddy"]), where), word("", False), gap=10)
    if t == 18:  # ordinals: count from the start of the line (next to the pond)
        ords = [i18n.ordinal(L.wl, i) for i in (1, 2, 3)]
        n = rng.randint(4, 5)
        ask = rng.randint(2, n)
        labels = [None] * n
        labels[ask - 1] = ""
        return ducks(3, ords), ducks(n, labels)
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
