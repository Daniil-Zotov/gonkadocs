#!/usr/bin/env python3
"""
Generate llms-full.txt — a single markdown file containing ALL documentation
from gonkadocs.com, optimized for AI agent consumption.

Dynamically scans all markdown files in the docs directory, so new pages
from upstream sync are automatically included.

Usage:
    python3 buildtools/generate-llms-full.py

Output:
    docs/llms-full.txt  (included in MkDocs build -> _site/llms-full.txt)
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Section definitions: (scan_dir, section_header, url_prefix)
SECTIONS = [
    ("gonka/docs/docs", "# Gonka Protocol Documentation\n\n", "/gonka/docs/"),
    ("community", "# Community Documentation\n\n", "/community/"),
    ("proposals", "# On-Chain Proposals\n\n", "/proposals/"),
]

# Files to skip unconditionally (at any directory level)
SKIP_PATTERNS_ALWAYS = {
    "CNAME",
    ".gitignore",
    "login.md",
    "signup.md",
    "disclaimer.md",
}

# Files to skip ONLY at the root of their scan directory, but include in subdirs
SKIP_PATTERNS_ROOT_ONLY = {
    "index.md",  # Keep index.md in subdirs (e.g. proposals/preproposals/<uuid>/index.md)
    "README.md",
}

# Directories to skip entirely
SKIP_DIRS = {
    "images",
    "overrides",
    "stylesheets",
    "gonka/docs/images",
    "gonka/docs/overrides",
    "gonka/docs/buildtools",
    "gonka/docs/.git",
    "gonka/docs/docs/zh",  # Chinese translations — separate file if needed
    "gonka/docs/docs/participant",  # Duplicate of host/
    "community/discussion",  # 70+ discussions — linked from llms.txt, too large
    "community/issues",  # 100+ issues — linked from llms.txt, too large
    "community/activity",  # dynamic JS-rendered page, not static content
    "gonka-code",  # raw source mirror — indexed via gonka-code-map.txt
}


def should_skip(rel_path: str, scan_dir: str = "") -> bool:
    """Check if a file should be skipped."""
    parts = Path(rel_path).parts

    # Skip if in a skip directory
    for skip_dir in SKIP_DIRS:
        if rel_path.startswith(skip_dir):
            return True

    # Skip specific files unconditionally
    if Path(rel_path).name in SKIP_PATTERNS_ALWAYS:
        return True

    # Skip index/README only at the ROOT of scan_dir, not in subdirs
    if Path(rel_path).name in SKIP_PATTERNS_ROOT_ONLY:
        if scan_dir:
            # If file is exactly at scan_dir root (no subdirs between)
            rel_to_scan = Path(rel_path).relative_to(scan_dir)
            if rel_to_scan.parent == Path('.'):
                return True
        else:
            return True

    # Skip .gitignore, etc
    if rel_path.startswith(".") or rel_path.startswith("_"):
        return True

    return False


def extract_title_from_content(content: str, file_path: Path) -> str:
    """Extract a title from markdown content or filename."""
    # Try to find H1
    for match in re.finditer(r'^#\s+(.+)$', content, re.MULTILINE):
        title = match.group(1).strip()
        if title and len(title) < 200:
            return title

    # Fall back to filename
    name = file_path.stem
    if name == "README":
        name = file_path.parent.name
    return name.replace("-", " ").replace("_", " ").title()


def strip_frontmatter(text: str) -> str:
    """Remove YAML front-matter from markdown."""
    return re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)


def strip_admonitions(text: str) -> str:
    """Convert admonition blocks to plain text."""
    text = re.sub(r'^!!!\s+\w+\s+"([^"]*)"', r'> **\1**', text, flags=re.MULTILINE)
    text = re.sub(r'^!!!\s+\w+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\?\?\?\s+note\s+"([^"]*)"', '> **\1**', text, flags=re.MULTILINE)
    text = re.sub(r'^\?\?\?\s+\w+\s+"([^"]*)"', '> **\1**', text, flags=re.MULTILINE)
    text = re.sub(r'^\?\?\?\s+\w+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\?\?\?$', '', text, flags=re.MULTILINE)
    return text


def clean_markdown(text: str) -> str:
    """Light cleanup for LLM consumption."""
    text = strip_frontmatter(text)
    text = strip_admonitions(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'```mermaid\n.*?```', '[diagram]', text, flags=re.DOTALL)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def scan_section(section_dir: str) -> list[tuple[Path, str]]:
    """Scan a section directory and return (abs_path, rel_path) pairs."""
    scan_path = DOCS / section_dir
    if not scan_path.exists():
        return []

    pages = []
    for root, dirs, files in os.walk(scan_path):
        dirs.sort()  # deterministic order across platforms (macOS APFS vs Linux ext4)
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            abs_path = Path(root) / fn
            rel_path = abs_path.relative_to(DOCS)
            if not should_skip(str(rel_path), section_dir):
                pages.append((abs_path, str(rel_path)))

    return pages


def main():
    all_pages = []

    for section_dir, header, url_prefix in SECTIONS:
        pages = scan_section(section_dir)
        all_pages.append((header, url_prefix, pages))
        for abs_path, rel_path in pages:
            print(f"  FOUND: {rel_path}", file=sys.stderr)

    # Assemble output
    out_parts = []
    out_parts.append("# Gonka Docs — Full Documentation\n")
    out_parts.append("> This file contains the complete text of all documentation from gonkadocs.com,")
    out_parts.append("> formatted for AI agent consumption. Generated from markdown sources.\n")
    out_parts.append("> Source: https://gonkadocs.com\n")
    out_parts.append("> Auto-generated — always reflects the latest synced content.\n")
    out_parts.append("---\n")

    total_files = 0
    for header, url_prefix, pages in all_pages:
        if pages:
            out_parts.append(header)
            for abs_path, rel_path in pages:
                content = abs_path.read_text(encoding="utf-8")
                title = extract_title_from_content(content, abs_path)
                cleaned = clean_markdown(content)
                out_parts.append(f"## {title}\n\n{cleaned}\n\n---\n")
                total_files += 1

    output = "\n".join(out_parts)

    out_path = DOCS / "llms-full.txt"
    out_path.write_text(output, encoding="utf-8")
    print(f"\nGenerated: {out_path} ({len(output)} bytes, {total_files} files)", file=sys.stderr)


if __name__ == "__main__":
    main()
