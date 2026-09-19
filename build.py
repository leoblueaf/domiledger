"""Builds the DomiLedger static site (GitHub Pages).

Edit the page bodies in pages/*.html, then run:  python build.py
Generated .html files are committed; GitHub Pages serves them as-is.
To set the support address everywhere, change SUPPORT_EMAIL below and rebuild.
"""
import pathlib
import re

SUPPORT_EMAIL = "leoblueaf@yahoo.com"
SITE = "https://leoblueaf.github.io/domiledger/"
UPDATED = "September 20, 2026"

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "pages"

NAV = [("index.html", "Home"), ("guides/index.html", "Guides"),
       ("support.html", "Support"), ("privacy.html", "Privacy")]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}icon.png">
<meta name="theme-color" content="#2F5D50">
<link rel="icon" type="image/png" href="{up}favicon.png">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="site"><div class="wrap wide">
<a class="brand" href="{up}index.html"><img src="{up}icon.png" alt="" width="32" height="32">DomiLedger</a>
<nav class="site" aria-label="Main">{nav}</nav>
</div></header>
{body}
<footer class="site"><div class="wrap wide">
<span>&copy; 2026 DomiLedger. Private by design: no account, no ads, no tracking.</span>
<nav aria-label="Footer"><a href="{up}support.html">Support</a><a href="{up}privacy.html">Privacy</a><a href="{up}terms.html">Terms</a><a href="{up}guides/index.html">Guides</a></nav>
</div></footer>
</body>
</html>
"""


def build():
    pages = sorted(SRC.rglob("*.html"))
    urls = []
    for src in pages:
        rel = src.relative_to(SRC).as_posix()
        raw = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", raw.split("\n\n", 1)[0]))
        body = re.sub(r"^(<!--.*?-->\s*)+", "", raw, flags=re.S)
        depth = rel.count("/")
        up = "../" * depth
        current = ' aria-current="page"'
        nav = "".join(
            f'<a href="{up}{href}"{current if href == rel else ""}>{label}</a>'
            for href, label in NAV)
        canonical = SITE + ("" if rel == "index.html" else rel)
        body = (body.replace("{SUPPORT_EMAIL}", SUPPORT_EMAIL)
                    .replace("{UPDATED}", UPDATED).replace("{up}", up))
        html = TEMPLATE.format(title=meta["title"], desc=meta["desc"], canonical=canonical,
                               site=SITE, up=up, nav=nav, body=body)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8", newline="\n")
        urls.append(canonical)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
               + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n",
                                     encoding="utf-8", newline="\n")
    print(f"Built {len(urls)} pages")


if __name__ == "__main__":
    build()
