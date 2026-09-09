#!/usr/bin/env python3
"""Fix nested page CSS paths and Home links with ?section= deep links.

Run from repo root:
  python3 scripts/fix_nav_and_css.py

Section mapping:
  Brahmarshi Patriji     -> ?section=patriji
  Book Reading Notes     -> ?section=book
  Transformation Journeys-> ?section=sajjana
  Session Classes        -> ?section=classes
  Session Schedules      -> ?section=schedules
"""
import re
from pathlib import Path

SECTION_MAP = [
    ("Brahmarshi Patriji", "patriji"),
    ("Book Reading Notes", "book"),
    ("Transformation Journeys", "sajjana"),
    ("Session Classes", "classes"),
    ("Session Schedules", "schedules"),
]


def section_for(path: Path) -> str:
    s = str(path).replace("\\", "/")
    for prefix, sec in SECTION_MAP:
        if s.startswith(prefix + "/") or s == prefix:
            return sec
    return ""


def main() -> None:
    root = Path(".")
    css_fixed = home_fixed = css_added = touched = 0
    for p in sorted(root.rglob("*.html")):
        if str(p) == "index.html" or p.name.startswith("."):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        depth = len(p.parts) - 1
        expected_css = "../" * depth + "css/site.css"
        home_href = "../" * depth + "index.html"
        sec = section_for(p)
        home_href_sec = home_href + (f"?section={sec}" if sec else "")

        def repl_css(m):
            nonlocal css_fixed
            q, href = m.group(1), m.group(2)
            if href.startswith("http"):
                return m.group(0)
            if "css/site.css" in href:
                css_fixed += 1
                return f"href={q}{expected_css}{q}"
            return m.group(0)

        text = re.sub(r'href=(["\'"'])([^"\'"']*css/site\.css)\1', repl_css, text)

        if "css/site.css" not in text and re.search(r"<head", text, re.I):
            text = re.sub(
                r"(<head[^>]*>)",
                rf'\1\n  <link rel="stylesheet" href="{expected_css}">',
                text,
                count=1,
                flags=re.I,
            )
            css_added += 1

        def repl_home(m):
            nonlocal home_fixed
            q, href = m.group(1), m.group(2)
            if re.fullmatch(r"(?:\.\./)+index\.html", href) or href == "/index.html":
                home_fixed += 1
                return f"href={q}{home_href_sec}{q}"
            return m.group(0)

        text = re.sub(
            r'href=(["\'"'])((?:\.\./)+index\.html|/index\.html)\1',
            repl_home,
            text,
        )

        if sec and f"?section={sec}" not in text:
            home_link = (
                f'<p class="pssm-back-home" style="margin:0 0 12px;font-size:13px;">'
                f'<a href="{home_href_sec}">← Home · PSSM Swadhyaya Notes</a></p>'
            )
            if 'class="site-wrap"' in text:
                text = text.replace(
                    '<div class="site-wrap">',
                    f'<div class="site-wrap">\n    {home_link}',
                    1,
                )
                home_fixed += 1
            elif re.search(r"<body[^>]*>", text, re.I):
                text = re.sub(
                    r"(<body[^>]*>)",
                    rf"\1\n  {home_link}",
                    text,
                    count=1,
                    flags=re.I,
                )
                home_fixed += 1

        if text != original:
            p.write_text(text, encoding="utf-8")
            touched += 1

    print(
        f"touched={touched} css_fixed={css_fixed} "
        f"css_added={css_added} home_fixed={home_fixed}"
    )


if __name__ == "__main__":
    main()
