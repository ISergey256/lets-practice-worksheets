"""Topics: worksheets built from the topics a parent or teacher picks (year -> subject -> topics).

Every task type of the project is a topic with metadata: year (R, Y1, Y2), curriculum period (R, Y1A, Y1Sp, Y1Su, Y2),
strand (place, addsub, ...) and a stable id used in links:
    r1..r8      Reception tasks (stages.py)
    y1..y10     Year 1 autumn tasks (stages.py)
    v<task><a|b|c>   Year 1 review task 1..18 (generate.py) at level 1, 2 or 3, e.g. v4a = number line, level 1.

Pages are packed from the measured height of every topic (scripts/topic_heights.json, written by
scripts/measure_topics.py: the tallest version over many numbers and all languages), so any choice of topics fits A4.
"""
import hashlib
import json
import random
import re
from pathlib import Path

import generate as g
import i18n
import stages as s
from i18n import text

MAX_TOPICS = 12
YEARS = ("R", "Y1", "Y2")
SUBJECTS = ("maths",)
STRANDS = ("place", "addsub", "muldiv", "fractions", "measure", "shape", "position", "patterns")
PERIOD_ORDER = {"R": 0, "Y1A": 1, "Y1Sp": 2, "Y1Su": 3, "Y2": 4}
LEVEL_LETTER = {1: "a", 2: "b", 3: "c"}

REVIEW_TASKS = (g.task_count, g.task_estimate, g.task_odd_even, g.task_number_line, g.task_compare, g.task_words,
                g.task_3d, g.task_2d_picture, g.task_sides, g.task_shade, g.task_equal_parts, g.task_lengths,
                g.task_bonds, g.task_steps, g.task_equations, g.task_walls, g.task_positions, g.task_ordinals)
REVIEW_STRAND = ("place", "place", "place", "place", "place", "place", "shape", "shape", "shape", "fractions", "fractions",
                 "measure", "addsub", "muldiv", "addsub", "addsub", "position", "position")
STAGE_TASKS = {  # id: (function, strand, period, cheat-card key)
    "r1": (s.r_ladybirds, "place", "R", "R1"), "r2": (s.r_count_circle, "place", "R", "R2"),
    "r3": (s.r_more, "place", "R", "R3"), "r4": (s.r_draw_dots, "place", "R", "R4"),
    "r5": (s.r_altogether, "addsub", "R", "R5"), "r6": (s.r_trace, "place", "R", "R6"),
    "r7": (s.r_pattern, "patterns", "R", "R7"), "r8": (s.r_colour, "shape", "R", "R8"),
    "y1": (s.y_count_write, "place", "Y1A", "Y1"), "y2": (s.y_tenframe_circle, "place", "Y1A", "Y2"),
    "y3": (s.y_more_less, "place", "Y1A", "Y3"), "y4": (s.y_compare, "place", "Y1A", "Y4"),
    "y5": (s.y_numberline, "place", "Y1A", "Y5"), "y6": (s.y_part_whole, "addsub", "Y1A", "Y6"),
    "y7": (s.y_add_story, "addsub", "Y1A", "Y7"), "y8": (s.y_take_away, "addsub", "Y1A", "Y8"),
    "y9": (s.y_make_ten, "addsub", "Y1A", "Y9"), "y10": (s.y_shapes_match, "shape", "Y1A", "Y10"),
}
OBJECTS = ["apple", "star", "flower", "ball", "heart"]
# Year 1 autumn tasks that practise the same thing as a review task: one row in the picker, "first steps" variant first
MERGE = {"y1": 1, "y4": 5, "y5": 4}
HEIGHTS_FILE = Path(__file__).with_name("topic_heights.json")


def year_of(period):
    return "R" if period == "R" else "Y2" if period == "Y2" else "Y1"


def topic_meta():
    """All topics: id -> dict(year, period, strand, task (1..18 for review topics), level, card)."""
    meta = {}
    for tid, (_, strand, period, card) in STAGE_TASKS.items():
        meta[tid] = {"year": year_of(period), "period": period, "strand": strand, "task": None, "level": None, "card": card}
    for t in range(1, 19):
        for lvl in (1, 2, 3):
            period = g.curriculum(t, lvl)
            meta[f"v{t}{LEVEL_LETTER[lvl]}"] = {"year": year_of(period), "period": period, "strand": REVIEW_STRAND[t - 1],
                                                "task": t, "level": lvl, "card": None}
    return meta


META = topic_meta()


def catalog(lang=i18n.DEFAULT):
    """Topics for the website picker, grouped as rows: one row per task type, with its difficulty variants."""
    names, cheat = i18n.TOPIC[lang]["names"], i18n.CHEAT[lang]
    levels = i18n.A[lang]["levels"]
    rows = []
    merged = {t: tid for tid, t in MERGE.items()}
    for tid, m in META.items():
        if m["task"] is None and tid not in MERGE:  # Reception / Year 1 autumn task: one variant
            rows.append({"row": tid, "year": m["year"], "strand": m["strand"], "title": cheat[m["card"]][0],
                         "variants": [{"id": tid, "period": m["period"], "label": ""}]})
    for t in range(1, 19):
        by_year = {}
        for lvl in (1, 2, 3):
            tid = f"v{t}{LEVEL_LETTER[lvl]}"
            m = META[tid]
            by_year.setdefault(m["year"], []).append({"id": tid, "period": m["period"], "label": levels[lvl]})
        for year, variants in by_year.items():
            if t in merged and year == META[merged[t]]["year"]:
                variants.insert(0, {"id": merged[t], "period": META[merged[t]]["period"], "label": i18n.TOPIC[lang]["pictures"]})
            if len(variants) == 1:
                variants[0]["label"] = ""
            rows.append({"row": f"v{t}-{year}", "year": year, "strand": REVIEW_STRAND[t - 1], "title": names[t - 1],
                         "variants": variants})
    rows.sort(key=lambda r: (YEARS.index(r["year"]), STRANDS.index(r["strand"]),
                             PERIOD_ORDER[r["variants"][0]["period"]], r["title"]))
    return {"rows": rows, "strands": i18n.TOPIC[lang]["strands"], "periods": i18n.A[lang]["period"],
            "max": MAX_TOPICS, "presets": presets()}


def review_spec(level, part):
    """Year 1 review at level 1-3, part 1 (tasks 1-9) or part 2 (tasks 10-18): a topic sheet of 9 topics."""
    tasks = range(1, 10) if part == 1 else range(10, 19)
    return "T:" + "_".join(f"v{t}{LEVEL_LETTER[level]}" for t in tasks)


def presets():
    """Ready-made sheets per year: [{"id": level for build(), "key": label key on the site, "part": 1 | 2 | None}]."""
    review = [{"id": review_spec(lv, part), "key": str(lv), "part": part} for lv in (1, 2, 3) for part in (1, 2)]
    return {"R": [{"id": "R", "key": "R", "part": None}],
            "Y1": [{"id": "Y1A", "key": "Y1A", "part": None}] + review,
            "Y2": [{"id": "T:" + "_".join(year_topics("Y2")), "key": "Y2", "part": None}]}


def year_topics(year):
    """One variant per task type for a year (the middle difficulty when there are several), in curriculum order."""
    picked = {}
    for tid, m in META.items():
        if m["year"] == year:
            picked.setdefault(m["task"] or tid, []).append(tid)
    ids = [v[len(v) // 2] for v in picked.values()]
    return sorted(ids, key=lambda t: (STRANDS.index(META[t]["strand"]), PERIOD_ORDER[META[t]["period"]], t))


def parse(spec):
    """'T:r1_v4a' -> ['r1', 'v4a'] (validated, unique, in the given order)."""
    ids = [x for x in spec[2:].split("_") if x]
    bad = [x for x in ids if x not in META]
    if bad or not ids:
        raise ValueError(f"unknown topics: {', '.join(bad) or 'none'}")
    if len(ids) > MAX_TOPICS:
        raise ValueError(f"at most {MAX_TOPICS} topics per worksheet")
    return list(dict.fromkeys(ids))


def short_id(ids):
    return hashlib.sha1("_".join(ids).encode()).hexdigest()[:8]


# ---------------------------------------------------------------- making one topic
def make(tid, rng, L, num):
    """(section html, answer html, period) of topic tid, numbered num."""
    m = META[tid]
    if m["task"] is None:
        fn = STAGE_TASKS[tid][0]
        args = (rng, L, num) + ((rng.choice(OBJECTS),) if fn in s.NEEDS_OBJECT else ())
        html, ans = fn(*args)
        return html, ans, m["period"]
    task = REVIEW_TASKS[m["task"] - 1]
    key = (rng.choice(["fish"] + OBJECTS),) if task in (g.task_count, g.task_estimate) else ()
    html, ans, *rest = task(rng, m["level"], L, *key)
    html = re.sub(r'<span class="n">\d+</span>', f'<span class="n">{num}</span>', html, count=1)
    # sections of the review sheet that stretched to the page end are packed like any other section here
    html = html.replace('<section class="sec" style="flex:1;display:flex;flex-direction:column">', '<section class="sec">', 1)
    return html, ans, rest[0] if rest else m["period"]


def stretch(html):
    """The last section on a page fills the rest of it."""
    # the task stays together under its title; the spare space is shared above and below it (CSS .stretch)
    return html.replace('<section class="sec">', '<section class="sec stretch" style="flex:1;display:flex;flex-direction:column">', 1)


def heights():
    try:
        return json.loads(HEIGHTS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:  # not measured yet: one topic per page is always safe
        return {}


PAGE_INNER = 1123 - 80   # A4 height minus the 40 px padding top and bottom
MAX_PER_PAGE = {"R": 2, "Y1": 3, "Y2": 4}  # STANDARDS L3
GAP = 9                  # gap between sections (.page gap)
SAFETY = 6


def sheet_year(ids):
    """The youngest year among the topics decides the page rules."""
    return min((META[t]["year"] for t in ids), key=YEARS.index)


def pack(ids, H):
    """Group topic ids into pages using measured heights and the per-page limit; keeps the chosen order."""
    limit = MAX_PER_PAGE[sheet_year(ids)]
    pages, cur, used = [], [], H.get("_header", 120)
    for tid in ids:
        h = H.get(tid, PAGE_INNER) + SAFETY
        if cur and (used + GAP + h > PAGE_INNER or len(cur) >= limit):
            pages.append(cur)
            cur, used = [], 0
        used += (GAP if cur else 0) + h
        cur.append(tid)
    if cur:
        pages.append(cur)
    return pages


def build(spec, seed, L):
    ids = parse(spec)
    rng = random.Random(f"topics-{'_'.join(ids)}-{seed}")  # str seed: same in CPython and Pyodide
    made = {tid: make(tid, rng, L, i + 1) for i, tid in enumerate(ids)}
    H = heights()
    year = sheet_year(ids)
    badge = text(L.w["badge_stage"], stage={"R": "Reception", "Y1": "Year 1", "Y2": "Year 2"}[year], seed=seed)
    pages = []
    for pi, group in enumerate(pack(ids, H)):
        secs = [made[t][0] for t in group]
        secs[-1] = stretch(secs[-1])
        secs = [g.tag_task(h, t) for h, t in zip(secs, group)]
        head = g.header(L, badge) if pi == 0 else ""
        pages.append(g.page(head + "".join(secs), "padding-bottom:36px" if pi == 0 else ""))
    pages = g.number_pages(pages)
    a = L.a
    rows = [f'<div class="a"><span class="n">{i + 1}</span><span style="flex:1">{made[t][1]}</span>'
            f'<span class="tag">{a["period"][made[t][2]]}</span></div>' for i, t in enumerate(ids)]
    head = (f'<h1 style="margin:0 0 2px;font-size:32px;font-weight:900">{a["answers"]}</h1>'
            f'<p style="margin:0 0 8px;font-size:15px;font-weight:600">'
            f'{text(a["sub_stage"], seed=seed, stage={"R": "Reception", "Y1": "Year 1", "Y2": "Year 2"}[year])}<br>{a["legend"]}</p>')
    # answer rows go on as many pages as needed (measured row heights)
    answer_pages, cur, used = [], [], H.get("_answers_head", 110)
    for tid, r in zip(ids, rows):
        h = H.get("a:" + tid, 60) + 2
        if cur and used + h > PAGE_INNER:
            answer_pages.append(cur)
            cur, used = [], 0
        cur.append(r)
        used += h
    answer_pages.append(cur)
    answers = "".join(g.page((head if i == 0 else "") + "".join(p), "padding:40px 52px;gap:0") for i, p in enumerate(answer_pages))
    return pages, answers


def cards(spec):
    """Cheat-card keys available for the chosen topics, as (number on the sheet, card key)."""
    return [(i + 1, META[t]["card"]) for i, t in enumerate(parse(spec)) if META[t]["card"]]
