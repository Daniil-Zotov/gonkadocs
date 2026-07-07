"""MkDocs hook: expand Proposals nav section by default."""
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

def on_post_page(output, page=None, config=None):
    if page is None or page.file is None:
        return output
    src_path = page.file.src_path.replace("\\", "/")
    if src_path.startswith("proposals/proposals/"):
        output = _ensure_checked(output, "__nav_3")
    return output
