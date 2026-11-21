"""Local website for making worksheets: python scripts/server.py  ->  http://127.0.0.1:8000

It serves the same page as the public GitHub Pages site (site/index.html). Here the page asks this server
to build the worksheets (works offline, no WebAssembly download) and can download real PDF files,
made by Chromium exactly like scripts/generate.py does. PDFs are saved in out/.
Only the standard library is used on top of what generate.py needs (playwright, pypdf).
"""
import argparse
import json
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402
import i18n  # noqa: E402

SITE = g.ROOT / "site"
MAX_SEED = 999_999
OUT_FILE = re.compile(r"^Worksheet_(L[123]|R|Y1A)_\d{1,6}_[a-z]{2}(_answers_[a-z]{2})?\.pdf$")
FONT_FILE = re.compile(r"^[\w-]+\.(css|woff2|txt)$")
TYPES = {".html": "text/html; charset=utf-8", ".pdf": "application/pdf", ".css": "text/css; charset=utf-8",
         ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8"}

pdf_lock = threading.Lock()  # one Chromium at a time is plenty for a home printer


def parse_job(q):
    """Validate level / seed / languages from a query or JSON body. Raises ValueError."""
    level, seed = g.parse_level(q.get("level", 2)), int(q.get("seed", 0))
    lang, alang = q.get("lang", i18n.DEFAULT), q.get("alang", i18n.DEFAULT)
    if not 0 <= seed <= MAX_SEED:
        raise ValueError(f"worksheet number must be 0..{MAX_SEED}")
    if lang not in i18n.LANGS or alang not in i18n.LANGS:
        raise ValueError(f"language must be one of {', '.join(i18n.LANGS)}")
    return level, seed, lang, alang


class Handler(BaseHTTPRequestHandler):
    server_version = "LetsPractice/2.0"

    def log_message(self, fmt, *args):  # quieter console: only API calls
        if "/api/" in self.path:
            sys.stderr.write(f"[{self.log_date_time_string()}] {fmt % args}\n")

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, download=False):
        if not path.is_file():
            return self.send_error(404)
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{path.name}"')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        path, q = unquote(u.path), {k: v[0] for k, v in parse_qs(u.query).items()}
        if path in ("/", "/index.html"):
            return self.send_file(SITE / "index.html")
        if path == "/api/info":
            return self.send_json({"langs": i18n.LANGS, "pdf": True})
        if path == "/api/build":
            try:
                pages, answers = g.build(*parse_job(q))
            except ValueError as e:
                return self.send_json({"error": str(e)}, 400)
            return self.send_json({"pages": pages, "answers": answers, "css": g.CSS})
        if path.startswith("/out/") and OUT_FILE.match(path[5:]):
            return self.send_file(g.OUT / path[5:], download="download" in q)
        if path.startswith("/fonts/") and FONT_FILE.match(path[7:]):
            return self.send_file(g.FONTS / path[7:])
        self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/pdf":
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 10_000:
                raise ValueError("request too large")
            job = parse_job(json.loads(self.rfile.read(n) or b"{}"))
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            return self.send_json({"error": f"bad request: {e}"}, 400)
        with pdf_lock:
            try:
                res = g.generate([job], png=False, log=lambda *_: None)[0]
            except Exception as e:  # show the reason in the page instead of a silent failure
                return self.send_json({"error": str(e)}, 500)
        self.send_json({"pdf": res["pdf"], "answers_pdf": res["answers_pdf"], "warnings": res["warnings"]})


def main():
    ap = argparse.ArgumentParser(description="Website for LET'S PRACTICE! worksheets")
    ap.add_argument("--host", default="127.0.0.1", help="0.0.0.0 to open it from other devices in your Wi-Fi")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true", help="do not open the browser automatically")
    a = ap.parse_args()
    g.OUT.mkdir(exist_ok=True)
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    url = f"http://{'127.0.0.1' if a.host == '0.0.0.0' else a.host}:{a.port}"
    print(f"LET'S PRACTICE! {url}   (Ctrl+C to stop)")
    if not a.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
