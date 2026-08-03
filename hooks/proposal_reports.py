"""MkDocs hook: inject report blocks from report*.md into proposal pages.

Scans each proposal detail page's directory for files matching report*.md.
For each report found, injects a section with the publication date and the
full report content inside a collapsible <details> block at the bottom of
the page.
"""

import glob
import os
import re


_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?^---\s*\n", re.DOTALL | re.MULTILINE)


def _is_detail_page(src_path: str) -> bool:
    if src_path.startswith("proposals/proposals/"):
        rest = src_path[len("proposals/proposals/"):]
        parts = rest.split("/")
        return len(parts) >= 3
    if src_path.startswith("proposals/preproposals/"):
        rest = src_path[len("proposals/preproposals/"):]
        parts = rest.split("/")
        return len(parts) >= 2
    return False


def _read_without_frontmatter(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception:
        return ""
    cleaned = _FRONTMATTER_RE.sub("", raw, count=1)
    return cleaned.strip()


def _sanitize_headers(text: str) -> str:
    return re.sub(r"^# ", "## ", text, flags=re.MULTILINE)


def _extract_title(content: str) -> tuple[str, str]:
    """Extract the first H1 (# Title) from content and return (title, rest).
    If there is no H1, return (f"Report", content).
    """
    m = re.match(r"^#\s+(.+?)(?:\s*\n|$)", content)
    if m:
        title = m.group(1).strip()
        rest = content[m.end():].strip()
        return title, rest
    return "Report", content


def _build_report_block(content: str, rel_path: str) -> str:
    title, body = _extract_title(content)
    safe_body = _sanitize_headers(body)
    return (
        f"<details class=\"prop-contracts\" markdown=\"1\">\n"
        f"<summary markdown=\"1\"><strong>{title}</strong> · "
        f"<a href=\"{rel_path.replace('.md', '/')}\">Open as separate page</a></summary>\n\n"
        f"{safe_body}\n\n"
        f"</details>\n"
    )


def on_page_markdown(markdown: str, page=None, config=None, **kwargs):
    if page is None or page.file is None:
        return markdown

    src_path = page.file.src_path.replace("\\", "/")
    if not _is_detail_page(src_path):
        return markdown

    # Skip report pages themselves (standalone rendering)
    if os.path.basename(page.file.abs_src_path).startswith("report"):
        return markdown

    if "<!-- reports-injected -->" in markdown:
        return markdown

    page_dir = os.path.dirname(page.file.abs_src_path)
    report_files = sorted(glob.glob(os.path.join(page_dir, "report*.md")))

    if not report_files:
        return markdown

    blocks = []
    for fpath in report_files:
        content = _read_without_frontmatter(fpath)
        if not content:
            continue
        fname = os.path.basename(fpath)
        blocks.append(_build_report_block(content, fname))

    if not blocks:
        return markdown

    section = (
        "\n\n---\n\n## Reports\n\n<!-- reports-injected -->\n\n" +
        "\n".join(blocks) +
        "\n"
    )

    return markdown.rstrip() + section
