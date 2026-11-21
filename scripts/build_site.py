"""Assemble the static GitHub Pages site into _site/ (the generator runs in the browser via Pyodide).

Usage:
    python scripts/build_site.py            # check the generator, then build _site/
    python scripts/build_site.py --serve    # ... and open it at http://127.0.0.1:8001

The site uses scripts/generate.py itself, so the website and the local PDF generator never drift apart.
"""
import argparse
import functools
import http.server
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DEST = ROOT / "_site"
sys.path.insert(0, str(ROOT / "scripts"))


def check(seeds=100):
    """Build many worksheets without rendering: every level, number and language must work."""
    import generate as g
    import i18n
    i18n.check()
    for lang in i18n.LANGS:
        for level in ("1a", "1b", "2a", "2b", "3a", "3b", "R", "Y1A"):
            for seed in range(seeds):
                pages, answers = g.build(level, seed, lang, lang)
                assert 1 <= len(pages) <= 4 and answers, (lang, level, seed, len(pages))  # STANDARDS L7
    for lang in i18n.LANGS:  # help cards: every card of both stages and of the review parts
        for stage in ("R", "Y1A", "1a", "1b", "2a", "2b", "3a", "3b"):
            for seed in range(seeds // 5):
                assert g.cheats(stage, seed, lang), (lang, stage, seed)
    import importlib, registry, topics
    for sub in registry.SUBJECTS:  # every ready year of a subject must have topics in its module
        if sub["ready"]:
            mod = importlib.import_module(sub["module"])
            have = {r["year"] for r in mod.catalog()["rows"]}
            assert set(sub["ready"]) <= have, (sub["id"], set(sub["ready"]) - have)
    print(f"  generator ok: {len(i18n.LANGS)} languages x 8 sheets x {seeds} worksheets, plus cheat sheets")


def changelog():
    """Project history for the site: every commit (hash, date, subject only; never names or e-mails), newest first,
    with the plain-words description from site/history.json in each language."""
    texts = json.loads((SITE / "history.json").read_text(encoding="utf-8"))
    try:
        log = subprocess.run(["git", "log", "--format=%H%x09%ad%x09%s", "--date=short"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    out = []
    for line in log.splitlines():
        h, d, subject = line.split("\t", 2)
        out.append({"hash": h, "date": d, "subject": subject, "text": texts.get(subject, {})})
    return out


def build():
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(SITE, DEST)
    for f in ("generate.py", "i18n.py", "registry.py", "stages.py", "cheats.py", "topics.py", "topic_heights.json"):  # the page loads them into Pyodide
        shutil.copy2(ROOT / "scripts" / f, DEST / f)
    (DEST / "fonts").mkdir()
    for f in (ROOT / "fonts").iterdir():
        if f.suffix in (".css", ".woff2", ".txt"):
            shutil.copy2(f, DEST / "fonts" / f.name)
    (DEST / "changelog.json").write_text(json.dumps(changelog(), ensure_ascii=False), encoding="utf-8")
    (DEST / "history.json").unlink()  # merged into changelog.json
    (DEST / ".nojekyll").write_text("")  # serve files as they are
    print(f"  site built: {DEST.relative_to(ROOT)}/ ({sum(1 for p in DEST.rglob('*') if p.is_file())} files)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true", help="serve _site/ locally after building")
    ap.add_argument("--port", type=int, default=8001)
    a = ap.parse_args()
    check()
    build()
    if a.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DEST))
        print(f"  http://127.0.0.1:{a.port}   (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler).serve_forever()


if __name__ == "__main__":
    main()
