"""MkDocs hook: expand Proposals nav, collapse quarter sections by default."""
import re

def _ensure_checked(html, nav_id):
    pattern = re.compile(r'(<input[^>]*id="' + re.escape(nav_id) + r'"[^>]*?)(\s*/?>)')
    match = pattern.search(html)
    if match:
        attrs = match.group(1)
        suffix = match.group(2)
        if 'checked' not in attrs:
            html = html[:match.start()] + attrs + ' checked' + suffix + html[match.end():]
    return html

def _ensure_unchecked(html, nav_id):
    """Remove checked attribute from a nav checkbox."""
    pattern = re.compile(r'(<input[^>]*id="' + re.escape(nav_id) + r'"[^>]*?)\s+checked(\s*/?>)')
    match = pattern.search(html)
    if match:
        attrs = match.group(1)
        suffix = match.group(2)
        html = html[:match.start()] + attrs + suffix + html[match.end():]
    return html

def on_post_page(output, page=None, config=None):
    if page is None or page.file is None:
        return output
    src_path = page.file.src_path.replace("\\", "/")
    if src_path.startswith("proposals/proposals/"):
        # Keep Proposals section expanded
        output = _ensure_checked(output, "__nav_3")
        # Collapse all quarter subsections (nav_3_2 through nav_3_6)
        for i in range(2, 7):
            output = _ensure_unchecked(output, f"__nav_3_{i}")
    return output
