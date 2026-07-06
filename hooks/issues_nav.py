"""MkDocs hook: expand Community nav on issue and discussion pages.

Injects `checked` into left-sidebar nav toggles for pages under
community/issues/ and community/discussion/, so the nav tree matches
the /community/ overview. Runs at build time before any browser JS.
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
    """Check nav toggles so Community (and Issues/Discussions) stay expanded."""
    if page is None or page.file is None:
        return output

    src_path = page.file.src_path.replace("\\", "/")
    if src_path.startswith("community/issues/"):
        output = _ensure_checked(output, "__nav_2")
        output = _ensure_checked(output, "__nav_2_6")
    elif src_path.startswith("community/discussion/"):
        output = _ensure_checked(output, "__nav_2")
        output = _ensure_checked(output, "__nav_2_5")
    return output
