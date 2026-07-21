"""MkDocs hook: inject report blocks from report*.md into proposal pages.

Scans each proposal detail page's directory for files matching report*.md.
For each report found, injects a section with the publication date and the
full report content inside a collapsible <details> block at the bottom of
the page.
"""

import glob
import os
import re


_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?^---\s*\n", re.DOTALL | re.MULTILINE)
_DATE_RE = re.compile(r"^\*\*Дата публикации:\*\*\s*(\S+)", re.MULTILINE)


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


def _extract_date(content: str, filename: str) -> str:
    m = _DATE_RE.search(content)
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if m:
        return m.group(1)
    return ""


def _sanitize_headers(text: str) -> str:
    return re.sub(r"^# ", "## ", text, flags=re.MULTILINE)


def _build_report_block(report_num: str, date: str, content: str, rel_path: str) -> str:
    safe_content = _sanitize_headers(content)
    return (
        f"### Report #{report_num} — {date}\n\n"
        f"<details class=\"prop-contracts\" markdown=\"1\">\n"
        f"<summary markdown=\"1\">Gonka Labs — Monthly Report No.{report_num}</summary>\n\n"
        f"[Открыть отдельной страницей]({rel_path}) · "
        f"[Обсуждение на GitHub](https://github.com/gonka-ai/gonka/discussions/1477)\n\n"
        f"{safe_content}\n\n"
        f"</details>\n"
    )


def on_page_markdown(markdown: str, page=None, config=None, **kwargs):
    if page is None or page.file is None:
        return markdown

    src_path = page.file.src_path.replace("\\", "/")
    if not _is_detail_page(src_path):
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
        date = _extract_date(content, fname)
        num = os.path.splitext(fname)[0].replace("report", "")
        blocks.append(_build_report_block(num, date, content, fname))

    if not blocks:
        return markdown

    section = (
        "\n\n---\n\n## Отчёты\n\n<!-- reports-injected -->\n\n" +
        "\n".join(blocks) +
        "\n"
    )

    return markdown.rstrip() + section
