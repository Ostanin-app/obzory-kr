#!/usr/bin/env python3
# Сборка статического раздела: content/*.md + meta.json -> NN.html, index.html
import json, os, markdown

HERE = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(HERE, "meta.json"), encoding="utf-8"))
BLOCKS = META["blocks"]
MD = markdown.Markdown(extensions=["tables", "attr_list", "md_in_html"])


def render(md_text):
    MD.reset()
    return MD.convert(md_text)


def toc_item(b, current):
    cls = ' class="current"' if b["num"] == current else ""
    extra = ' class="appendix"' if b["num"] == len(BLOCKS) else ""
    return ('<li%s><a href="%02d.html"%s><span class="num">%d.</span>'
            '<span>%s</span></a></li>') % (extra, b["num"], cls, b["num"], b["title"])


def topbar():
    return ('<header class="topbar">\n  <div class="topbar-inner">\n'
            '    <a class="brand" href="index.html">%s</a>\n'
            '    <div class="topbar-meta"><a href="../index.html">Все разборы</a> · %s</div>\n'
            '  </div>\n</header>') % (META["site_name"], META["eyebrow"])


def footer():
    return ('<footer class="footer">\n  <div class="footer-inner">%s</div>\n</footer>'
            % META["source_line"])


PAGE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site}</title>
<link rel="stylesheet" href="../style.css?v=3">
</head>
<body>
{topbar}

<nav class="toc-rail" aria-label="Оглавление">
  <div class="toc-title">Оглавление</div>
  <ol class="toc-list">
{toc}
</ol>
</nav>

<main class="page">
  <details class="toc-inline">
    <summary>Оглавление</summary>
    <ol class="toc-list">
{toc}
</ol>
  </details>
  <article class="card">
    <div class="crumb">Блок {num} из {total}</div>
    <h1>{title}</h1>
{body}
    <nav class="pager">
      {prev}
      <a class="up" href="index.html">Оглавление</a>
      {next}
    </nav>
  </article>
</main>

{footer}
<script src="../zoom.js" defer></script>
</body>
</html>
"""

INDEX = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{site}</title>
<link rel="stylesheet" href="../style.css?v=3">
</head>
<body>
{topbar}

<section class="hero">
  <div class="hero-inner">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{site}</h1>
    <p class="lead">Неофициальный перевод практической части клинических рекомендаций Endocrine Society 2025 — <mark>от скрининга до титрации препаратов</mark>.</p>
    <p class="meta">{source}</p>
  </div>
</section>

<main class="page">
  <ol class="index-list">
{items}
  </ol>
</main>

{footer}
</body>
</html>
"""


def build_page(b, prev_b, next_b):
    body = render(open(os.path.join(HERE, "content", b["file"]), encoding="utf-8").read())
    toc = "\n".join(toc_item(x, b["num"]) for x in BLOCKS)
    prev_html = ('<a class="prev" href="%02d.html">%s</a>' % (prev_b["num"], prev_b["title"])
                 if prev_b else "<span></span>")
    next_html = ('<a class="next" href="%02d.html">%s</a>' % (next_b["num"], next_b["title"])
                 if next_b else "<span></span>")
    html = PAGE.format(title="%d. %s" % (b["num"], b["title"]), site=META["site_name"],
                       topbar=topbar(), toc=toc, body=body, prev=prev_html, next=next_html,
                       footer=footer(), num=b["num"], total=len(BLOCKS))
    open(os.path.join(HERE, "%02d.html" % b["num"]), "w", encoding="utf-8").write(html)


def build_index():
    items = "\n".join(
        '    <li><a href="%02d.html"><span class="num">%d</span><span class="name">%s</span></a></li>'
        % (b["num"], b["num"], b["title"]) for b in BLOCKS)
    html = INDEX.format(site=META["site_name"], eyebrow=META["eyebrow"], source=META["source_line"],
                        topbar=topbar(), items=items, footer=footer())
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)


for i, b in enumerate(BLOCKS):
    build_page(b, BLOCKS[i - 1] if i > 0 else None, BLOCKS[i + 1] if i + 1 < len(BLOCKS) else None)
build_index()
print("built", len(BLOCKS), "pages")
