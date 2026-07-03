#!/usr/bin/env python3
"""
Post-build: generate .md versions of all HTML pages in _site/.

Follows the llms.txt standard: each page available at {url}.md
(e.g. /gonka/docs/architecture/index.html -> /gonka/docs/architecture/index.html.md)

Usage:
    python3 buildtools/generate-page-md.py [_site_dir]

Output:
    Adds .html.md files alongside each index.html in the site directory.
"""
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class ContentExtractor(HTMLParser):
    """Extract readable text from MkDocs Material HTML pages."""

    def __init__(self):
        super().__init__()
        self.in_content = False
        self.skip_tags = {"script", "style", "nav", "header", "footer", "aside"}
        self.skip_depth = 0
        self.parts = []
        self.current_tag = None
        self.list_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "")

        if tag in self.skip_tags:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        if tag == "article" or "md-content" in classes:
            self.in_content = True

        if not self.in_content:
            return

        self.current_tag = tag

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.parts.append("\n\n" + "#" * level + " ")
        elif tag == "p":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "code":
            if "highlight" in classes or "highlight-code" in classes:
                self.parts.append("\n```\n")
        elif tag == "pre":
            pass
        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href and not href.startswith("#"):
                self.parts.append("[")
        elif tag == "strong" or tag == "b":
            self.parts.append("**")
        elif tag == "em" or tag == "i":
            self.parts.append("*")
        elif tag == "blockquote":
            self.parts.append("\n> ")
        elif tag == "hr":
            self.parts.append("\n\n---\n\n")
        elif tag == "table":
            self.parts.append("\n\n")
        elif tag == "tr":
            self.parts.append("\n")
        elif tag in ("td", "th"):
            self.parts.append(" | ")

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        if self.skip_depth:
            return

        if not self.in_content:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n")
        elif tag == "code":
            classes = getattr(self, '_current_code_classes', '')
            if "highlight" in classes or "highlight-code" in classes:
                self.parts.append("\n```\n")
        elif tag == "a":
            self.parts.append(")")
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "table":
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth:
            return
        if not self.in_content:
            return

        text = data.strip()
        if text:
            self.parts.append(text)

    def get_text(self):
        result = "".join(self.parts)
        result = re.sub(r'\n{3,}', '\n\n', result)
        result = re.sub(r'\[([^\]]*)\]\(([^)]*)\)', r'[\1](\2)', result)
        return result.strip()


def extract_from_html(html_content: str) -> str:
    """Extract main content from MkDocs HTML page."""
    extractor = ContentExtractor()
    try:
        extractor.feed(html_content)
    except Exception:
        pass
    return extractor.get_text()


def process_site(site_dir: Path):
    """Generate .html.md for every index.html in the site."""
    count = 0
    for dirpath, _, filenames in os.walk(site_dir):
        for fn in filenames:
            if fn == "index.html":
                html_path = Path(dirpath) / fn
                md_path = html_path.parent / "index.html.md"

                if md_path.exists():
                    continue

                html_content = html_path.read_text(encoding="utf-8")
                md_content = extract_from_html(html_content)

                if md_content:
                    md_path.write_text(md_content, encoding="utf-8")
                    rel = md_path.relative_to(site_dir)
                    count += 1

    print(f"  Generated {count} .html.md files", file=sys.stderr)


def main():
    if len(sys.argv) > 1:
        site_dir = Path(sys.argv[1])
    else:
        site_dir = Path(__file__).resolve().parent.parent / "_site"

    if not site_dir.exists():
        print(f"  Site directory not found: {site_dir}", file=sys.stderr)
        sys.exit(1)

    process_site(site_dir)


if __name__ == "__main__":
    main()
