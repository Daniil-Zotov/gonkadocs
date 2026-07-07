"""One-time migration: pre-render comment body markdown in existing issue files.

Reads all issue .md files, finds comment body <div> with markdown="1",
renders the content with Python-Markdown, removes markdown="1", and writes back.
Also converts markdown user links [@x](url) in comment headers to HTML <a> tags.
"""

import glob
import re
import sys
import os
import textwrap
import markdown

MD_EXT = [
    "markdown.extensions.extra",
    "markdown.extensions.sane_lists",
    "markdown.extensions.md_in_html",
]

COMMENT_BODY_RE = re.compile(
    r'(<div class="issues-comment-body issues-content") markdown="1"(>\n?)(.*?)(\n?\s*</div>)',
    re.DOTALL,
)

USER_LINK_RE = re.compile(r'\[@(\w+)\]\((https://github\.com/\w+)\)')

def render_md(text):
    if not text or text.strip() in ("", "*(empty)*"):
        return text
    # Strip template indentation (4-space indent from HTML formatting)
    text = textwrap.dedent(text).strip()
    # Enable markdown processing inside <details> blocks
    text = text.replace("<details>", '<details markdown="1">')
    text = text.replace("<summary>", '<summary markdown="1">')
    return markdown.markdown(text, extensions=MD_EXT)

def convert_user_link(m):
    return f'<a href="{m.group(2)}">@{m.group(1)}</a>'

def migrate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Render comment bodies
    def replace_body(m):
        prefix = m.group(1)  # <div class="issues-comment-body issues-content"
        between = m.group(2)  # >\n or >
        body = m.group(3)     # the markdown content
        suffix = m.group(4)   # </div>
        rendered = render_md(body)
        return f"{prefix}{between}{rendered}{suffix}"

    new_content = COMMENT_BODY_RE.sub(replace_body, content)

    # 2. Convert markdown user links in headers
    new_content = USER_LINK_RE.sub(convert_user_link, new_content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "docs/community/issues"
    pattern = os.path.join(root, "**/*.md")
    files = glob.glob(pattern, recursive=True)
    total = len(files)
    migrated = 0
    errors = 0
    for path in files:
        try:
            if migrate_file(path):
                migrated += 1
        except Exception as e:
            print(f"ERROR {path}: {e}", file=sys.stderr)
            errors += 1

    print(f"Scanned {total} files, migrated {migrated}, errors {errors}")

if __name__ == "__main__":
    main()
