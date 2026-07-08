"""MkDocs hook: appends full-proposal.md content inside a spoiler block.

Looks for a file named `full-proposal.md` in the same directory as each
proposal page (both on-chain and pre-proposals). If found, its content is
appended at the bottom of the page under a collapsible <details> block.
"""

import os
import re


_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?^---\s*\n", re.DOTALL | re.MULTILINE)


def _is_overview_page(src_path: str) -> bool:
    """Return True for overview/index pages, False for proposal detail pages.

    On-chain:
      proposals/proposals/2026-q2/index.md     → overview (exclude)
      proposals/proposals/2026-q2/74/index.md  → detail  (keep)
    Pre-proposals:
      proposals/preproposals/index.md          → overview (exclude)
      proposals/preproposals/{uuid}/index.md   → detail  (keep)
    """
    if src_path.startswith("proposals/proposals/"):
        rest = src_path[len("proposals/proposals/"):]
        parts = rest.split("/")
        # ["2026-q2", "index.md"]          → overview
        # ["2026-q2", "74", "index.md"]    → detail
        return len(parts) == 2
    if src_path.startswith("proposals/preproposals/"):
        rest = src_path[len("proposals/preproposals/"):]
        parts = rest.split("/")
        # ["index.md"]             → overview
        # ["uuid", "index.md"]     → detail
        return len(parts) == 1
    return False


def _read_without_frontmatter(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception:
        return ""
    cleaned = _FRONTMATTER_RE.sub("", raw, count=1)
    return cleaned.strip()


def _sanitize_header(text: str) -> str:
    """Downgrade H1 (#) inside the injected content to H2 (##)."""
    return re.sub(r"^# ", "## ", text, flags=re.MULTILINE)


def on_page_markdown(markdown: str, page=None, config=None, **kwargs):
    if page is None or page.file is None:
        return markdown

    src_path = page.file.src_path.replace("\\", "/")

    # Only process proposal detail pages
    if not (src_path.startswith("proposals/proposals/") or src_path.startswith("proposals/preproposals/")):
        return markdown

    if _is_overview_page(src_path):
        return markdown

    # Prevent double-injection on reload
    if "<details class=\"prop-full\">" in markdown:
        return markdown

    page_dir = os.path.dirname(page.file.abs_src_path)
    full_proposal_path = os.path.join(page_dir, "full-proposal.md")

    if not os.path.isfile(full_proposal_path):
        return markdown

    extra = _read_without_frontmatter(full_proposal_path)
    if not extra:
        return markdown

    extra = _sanitize_header(extra)

    append_block = (
        "\n\n"
        "---\n\n"
        "## Full Proposal\n\n"
        "<details class=\"prop-full\" markdown=\"1\">\n"
        "<summary markdown=\"1\"><strong>Click to expand full proposal</strong></summary>\n\n"
        f"{extra}\n"
        "\n"
        "</details>\n"
    )

    return markdown + append_block
