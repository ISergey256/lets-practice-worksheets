"""Check that every page fits A4 in every language (needs playwright + chromium).

Usage:  python scripts/check_layout.py              # all languages, all levels and stages, numbers 101-108,
                                                     # plus random topic sheets (scripts/topics.py)
        python scripts/check_layout.py --lang el    # one language
Run it after changing a task or a translation: longer texts can push a page over the bottom edge.
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import random  # noqa: E402

import generate as g  # noqa: E402
import i18n  # noqa: E402
import topics  # noqa: E402

LEVELS = ("1a", "1b", "2a", "2b", "3a", "3b", "R", "Y1A")
OVER = "Math.max(...[...document.querySelectorAll('.page')].map(p => p.scrollHeight - p.clientHeight))"


def topic_specs(n=6):
    """Random topic sheets per year (fixed random seed): a few small and some with the maximum number of topics."""
    rng = random.Random(2026)
    specs = [topics.presets()["Y2"][0]["id"]]
    for year in topics.YEARS:
        ids = [t for t, m in topics.META.items() if m["year"] == year]
        if not ids:  # years without maths worksheets yet (registry: "soon")
            continue
        for i in range(n):
            k = min(len(ids), topics.MAX_TOPICS if i % 2 else rng.randint(2, 6))
            specs.append("T:" + "_".join(rng.sample(ids, k)))
    return specs


async def main(langs, seeds):
    from playwright.async_api import async_playwright
    g.OUT.mkdir(exist_ok=True)
    tmp, bad, total = g.OUT / "_check.html", [], 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        pg = await browser.new_page(viewport={"width": 794, "height": 1123})
        try:
            for lang in langs:
                for level in LEVELS + tuple(topic_specs()):
                    for seed in seeds:
                        pages, answers = g.build(level, seed, lang, lang)
                        for name, body in [*((f"p{i}", b) for i, b in enumerate(pages, 1)), ("answers", answers)]:
                            tmp.write_text(g.html_doc(body, lang), encoding="utf-8")
                            await pg.goto(tmp.as_uri())
                            await pg.evaluate("document.fonts.ready")
                            total += 1
                            over = await pg.evaluate(OVER)
                            if over > 1:
                                bad.append(f"{lang} level {level} No. {seed} {name}: {over}px too tall")
                            if name == "p1" and len(pages) > 6:
                                bad.append(f"{lang} level {level} No. {seed}: {len(pages)} pages, packing is wasteful")
        finally:
            tmp.unlink(missing_ok=True)
            await browser.close()
    print("\n".join(bad) or f"all {total} pages fit")
    return not bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=list(i18n.LANGS), help="only this language")
    ap.add_argument("--seeds", default="101-108", help="range of worksheet numbers, e.g. 1-50")
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    sys.exit(0 if asyncio.run(main([a.lang] if a.lang else list(i18n.LANGS), range(lo, hi + 1))) else 1)
