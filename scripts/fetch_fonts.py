"""Download the fonts into fonts/ so worksheets render the same without internet.

Usage:  python scripts/fetch_fonts.py
Creates fonts/fonts.css (with local urls), the .woff2 files and the font licences.
Nunito covers Latin and Cyrillic; it has no Greek, so Greek letters use the
similar rounded "M PLUS Rounded 1c" (only its Greek subset is downloaded).
generate.py and the website use fonts/fonts.css automatically.
"""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
# a modern browser UA makes Google Fonts answer with woff2 files
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
FAMILIES = [  # (css2 family spec, file prefix, subsets to keep, licence url)
    ("Nunito:wght@600;700;800;900", "nunito", {"latin", "latin-ext", "cyrillic", "cyrillic-ext"},
     "https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/OFL.txt"),
    # google/fonts keeps no OFL.txt for this family (METADATA.pb: license "OFL"); build it from the standard text
    ("M+PLUS+Rounded+1c:wght@700;800;900", "mplusrounded", {"greek", "greek-ext"},
     "Copyright 2016 The Rounded M+ Project Authors."),
]
OFL_TEMPLATE = "https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/OFL.txt"


def licence_text(licence):
    if licence.startswith("https://"):
        return get(licence)
    body = get(OFL_TEMPLATE).decode().split("\n", 1)[1]  # drop Nunito's copyright line
    return (licence + "\n" + body).encode()


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def main():
    FONTS.mkdir(exist_ok=True)
    for old in FONTS.glob("*"):
        old.unlink()
    out = []
    for spec, prefix, subsets, licence in FAMILIES:
        css = get(f"https://fonts.googleapis.com/css2?family={spec}&display=block").decode()
        files = {}
        for subset, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
            if subset not in subsets:
                continue
            url = re.search(r"url\((https://[^)]+)\)", block).group(1)
            weight = re.search(r"font-weight: (\d+)", block).group(1)
            name = files.setdefault(url, f"{prefix}-{subset}-{weight}.woff2")  # variable fonts share one file
            out.append(f"/* {prefix} {subset} {weight} */\n" + block.replace(url, name))
        for url, name in files.items():
            (FONTS / name).write_bytes(get(url))
            print(f"  fonts/{name}")
        (FONTS / f"OFL-{prefix}.txt").write_bytes(licence_text(licence))
    (FONTS / "fonts.css").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  fonts/fonts.css ({len(out)} faces)")


if __name__ == "__main__":
    main()
