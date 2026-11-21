"""Measure every topic so topic sheets can be packed onto A4 pages safely (needs playwright + chromium).

Usage:  python scripts/measure_topics.py            # writes scripts/topic_heights.json
Run it after changing a task, its pictures or a translation. For every topic it renders many numbers in every
language and keeps the tallest section height and the tallest answer-row height.
"""
import asyncio
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402
import i18n  # noqa: E402
import topics  # noqa: E402

SEEDS = range(12)
MEASURE = """(() => ({
  secs: [...document.querySelectorAll('#secs section')].map(e => e.getBoundingClientRect().height),
  rows: [...document.querySelectorAll('#ans .a')].map(e => e.getBoundingClientRect().height),
  head: document.querySelector('#head') ? document.querySelector('#head').getBoundingClientRect().height : 0,
  ahead: document.querySelector('#ahead') ? document.querySelector('#ahead').getBoundingClientRect().height : 0,
}))()"""


async def main():
    from playwright.async_api import async_playwright
    g.OUT.mkdir(exist_ok=True)
    tmp = g.OUT / "_measure.html"
    H = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        pg = await browser.new_page(viewport={"width": 794, "height": 1123})
        try:
            for lang in i18n.LANGS:
                L = g.Lang(lang, lang)
                for tid in topics.META:
                    secs, rows = [], []
                    for seed in SEEDS:
                        html, ans, period = topics.make(tid, random.Random(f"m-{tid}-{seed}"), L, 12)
                        secs.append(f'<div class="page" style="height:auto">{html}</div>')
                        rows.append(f'<div class="a"><span class="n">12</span><span style="flex:1">{ans}</span>'
                                    f'<span class="tag">{L.a["period"][period]}</span></div>')
                    extra = ""
                    if tid == "r1":  # header of page 1 and of the answer page (longest year name, 6-digit number)
                        badge = text_badge(L)
                        a = L.a
                        extra = (f'<div class="page" style="height:auto"><div id="head">{g.header(L, badge)}</div></div>'
                                 f'<div class="page" style="height:auto;padding:40px 52px;gap:0"><div id="ahead">'
                                 f'<h1 style="margin:0 0 2px;font-size:32px;font-weight:900">{a["answers"]}</h1>'
                                 f'<p style="margin:0 0 8px;font-size:15px;font-weight:600">'
                                 f'{i18n.text(a["sub_stage"], seed=999999, stage="Reception")}<br>{a["legend"]}</p></div></div>')
                    body = (f'<div id="secs">{"".join(secs)}</div>'
                            f'<div id="ans" class="page" style="height:auto;padding:40px 52px;gap:0">{"".join(rows)}</div>{extra}')
                    tmp.write_text(g.html_doc(body, lang), encoding="utf-8")
                    await pg.goto(tmp.as_uri())
                    await pg.evaluate("document.fonts.ready")
                    m = await pg.evaluate(MEASURE)
                    H[tid] = max(H.get(tid, 0), *m["secs"])
                    H["a:" + tid] = max(H.get("a:" + tid, 0), *m["rows"])
                    if extra:
                        H["_header"] = max(H.get("_header", 0), m["head"] + 9)  # + gap to the first section
                        H["_answers_head"] = max(H.get("_answers_head", 0), m["ahead"])
                print(f"  {lang}: {len(topics.META)} topics measured")
        finally:
            tmp.unlink(missing_ok=True)
            await browser.close()
    H = {k: int(v) + 1 for k, v in sorted(H.items())}
    topics.HEIGHTS_FILE.write_text(json.dumps(H, indent=1) + "\n", encoding="utf-8")
    print(f"  written {topics.HEIGHTS_FILE.name}: {len(H)} values")


def text_badge(L):
    return i18n.text(L.w["badge_stage"], stage="Reception", seed=999999)


if __name__ == "__main__":
    asyncio.run(main())
