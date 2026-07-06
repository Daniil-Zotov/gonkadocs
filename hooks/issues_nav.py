"""MkDocs hook: expand Community and Issues nav sections on issue pages.

Injects `checked` attribute into the left sidebar navigation checkboxes
for pages under community/issues/, so the nav tree is expanded by default.
This runs at build time, so it's guaranteed to work before any browser JS/CSS.
"""
import re


def _ensure_checked(html, nav_id):
    """Add checked attribute to a nav checkbox if not already present."""
    pattern = re.compile(
        r'(<input[^>]*id="' + re.escape(nav_id) + r'"[^>]*?)(\s*/?>)'
    )
    match = pattern.search(html)
    if match:
        attrs = match.group(1)
        suffix = match.group(2)
        if 'checked' not in attrs:
            html = html[:match.start()] + attrs + ' checked' + suffix + html[match.end():]
    return html


def on_post_page(output, page=None, config=None):
    """Modify the final rendered HTML to check nav toggles on issue pages."""
    if page is None or page.file is None:
        return output

    src_path = page.file.src_path
    if not src_path.startswith("community/issues/"):
        return output

    output = _ensure_checked(output, "__nav_2")
    output = _ensure_checked(output, "__nav_2_6")
    return output
