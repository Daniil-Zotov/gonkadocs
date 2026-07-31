#!/usr/bin/env python3
"""Sync gonka-ai/gonka source code mirror into docs/gonka-code/.

Filters out everything an AI agent does not need:
- binaries (cosmovisor upgrade bundles)
- Jupyter notebooks (*.ipynb)
- lock files (*.lock, package-lock.json)
- model/tokenizer resources (*.model)
- images (*.png, *.jpg, *.jpeg, *.gif, *.svg)
- compiled artifacts (*.wasm, *.pdf)
- Go test files (*_test.go)
- editor/CI cruft (.git, __pycache__, node_modules, .venv, .idea, etc.)

Usage:
    python3 buildtools/sync-gonka-code.py --src <upstream_repo> --dest docs/gonka-code

Mirrors src -> dest: copies new/changed files and deletes stale ones.
"""
import argparse
import shutil
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    ".run",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "cosmovisor",
    "build",
    "dist",
    "artifacts",
    "third_party",
}

SKIP_FILE_SUFFIXES = (
    ".ipynb",
    ".lock",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".pdf",
    ".model",
    ".wasm",
    ".zip",
    ".tar",
    ".gz",
    ".bin",
    ".so",
    ".dylib",
    ".exe",
)

SKIP_FILES = {
    "package-lock.json",
    "go.sum",
    "pnpm-lock.yaml",
    "yarn.lock",
    ".DS_Store",
}


def should_skip_file(path: Path) -> bool:
    name = path.name
    if name in SKIP_FILES:
        return True
    if name.endswith("_test.go"):
        return True
    if name.lower().endswith(SKIP_FILE_SUFFIXES):
        return True
    return False


def should_skip_dir(rel: Path) -> bool:
    return any(part in SKIP_DIRS for part in rel.parts)


def sync(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for skip_dir in SKIP_DIRS:
        stale = dest / skip_dir
        if stale.exists():
            shutil.rmtree(stale)
    copied = 0
    skipped = 0

    for s in sorted(src.rglob("*")):
        rel = s.relative_to(src)
        if should_skip_dir(rel):
            continue
        if s.is_file():
            if should_skip_file(s):
                skipped += 1
                continue
            d = dest / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            if not d.exists() or d.stat().st_size != s.stat().st_size or d.stat().st_mtime_ns < s.stat().st_mtime_ns:
                shutil.copy2(s, d)
                copied += 1

    stale = [p for p in dest.rglob("*") if p.is_file() and not (src / p.relative_to(dest)).exists()]
    for p in stale:
        p.unlink()
    for d in sorted(dest.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    total = sum(1 for _ in dest.rglob("*") if _.is_file())
    size = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    print(f"  copied/updated: {copied}, skipped: {skipped}, removed: {len(stale)}")
    print(f"  mirror: {total} files, {size / 1024 / 1024:.1f} MB")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", required=True, help="Path to upstream gonka-ai/gonka checkout")
    ap.add_argument("--dest", default="docs/gonka-code", help="Destination mirror dir")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    dest = Path(args.dest).resolve()
    if not src.is_dir():
        print(f"ERROR: source dir not found: {src}", file=sys.stderr)
        sys.exit(1)
    sync(src, dest)


if __name__ == "__main__":
    main()
