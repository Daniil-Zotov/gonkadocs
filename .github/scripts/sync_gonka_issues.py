#!/usr/bin/env python3
"""Sync all GitHub Issues from gonka-ai/gonka into community/issues/."""

import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

OWNER = os.environ.get("REPO_OWNER", "gonka-ai")
REPO = os.environ.get("REPO_NAME", "gonka")
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/community/issues"))
GH_TOKEN = os.environ.get("GH_TOKEN", "")

API_BASE = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if GH_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"


def gh_get(path, params=None, retries=3):
    url = f"{API_BASE}{path}"
    for attempt in range(retries):
        r = requests.get(url, headers=HEADERS, params=params, timeout=60)
        if r.status_code in (502, 503) and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset - int(time.time()), 10)
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(min(wait, 300))
            continue
        r.raise_for_status()
        return r.json()
    return None


def list_all_issues():
    """Fetch all issues (excluding pull requests) with pagination."""
    issues = []
    page = 1
    while True:
        data = gh_get(f"/repos/{OWNER}/{REPO}/issues", {
            "state": "all",
            "per_page": 100,
            "page": page,
            "sort": "updated",
            "direction": "desc",
        })
        if not data:
            break
        for item in data:
            if "pull_request" in item:
                continue
            issues.append(item)
        if len(data) < 100:
            break
        page += 1
    return issues


def fetch_issue(number):
    """Fetch single issue with all comments."""
    issue = gh_get(f"/repos/{OWNER}/{REPO}/issues/{number}")
    if not issue:
        return None, []
    comments = []
    page = 1
    while True:
        cdata = gh_get(f"/repos/{OWNER}/{REPO}/issues/{number}/comments", {
            "per_page": 100,
            "page": page,
        })
        if not cdata:
            break
        comments.extend(cdata)
        if len(cdata) < 100:
            break
        page += 1
    return issue, comments


def slugify(text, max_len=60):
    text = (text or "").strip().lower()
    text = re.sub(r"[^\w\s\-а-яё]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled"


def fmt_date(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso or "unknown"


def fmt_date_short(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return (iso or "")[:10]


def user_link(user):
    if not user:
        return "*[deleted]*"
    return f"[@{user['login']}]({user['html_url']})"


def label_badges(labels):
    if not labels:
        return ""
    return " ".join(f"`{l['name']}`" for l in labels)


def state_icon(state):
    return {"open": "\U0001f7e2", "closed": "\U0001f534"}.get(state, "\u26aa")


def indent_body(body, prefix="> "):
    return "\n".join(prefix + l if l else prefix.rstrip() for l in (body or "").splitlines())


def build_issue_md(issue, comments):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title_escaped = issue["title"].replace('"', '\\"')
    labels = issue.get("labels", [])

    out = [
        "---",
        f'title: "#{issue["number"]} — {title_escaped}"',
        f"source: {issue['html_url']}",
        f"issue_number: {issue['number']}",
        f"synced_at: {sync_time}",
        "---",
        "",
        f"> \U0001f504 **Авто-синхронизация:** из [Issue #{issue['number']}]({issue['html_url']}) каждые 6 часов. ",
        "",
        f"# {state_icon(issue['state'])} {issue['title']}",
        "",
        f"**Автор:** {user_link(issue.get('user'))} · "
        f"**Состояние:** {issue['state'].title()} · "
        f"**Создано:** {fmt_date(issue['created_at'])} · "
        f"**Обновлено:** {fmt_date(issue['updated_at'])}",
    ]

    if labels:
        out.append(f"\n**Метки:** {label_badges(labels)}")

    if issue.get("milestone"):
        out.append(f"\n**Веха:** {issue['milestone']['title']}")

    out += [
        "",
        "---",
        "",
        "## \U0001f4dd Описание",
        "",
        issue.get("body") or "*(пусто)*",
        "",
    ]

    if comments:
        out += ["---", "", f"## \U0001f4ac Комментарии ({len(comments)})", ""]
        for i, c in enumerate(comments, 1):
            out += [
                f"### Комментарий {i} — {user_link(c.get('user'))}", "",
                f"*{fmt_date(c['created_at'])}*", "",
                c.get("body") or "*(пусто)*", "",
            ]

    return "\n".join(out)


def build_label_index(label_name, label_slug, items):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    items_sorted = sorted(items, key=lambda x: x["number"], reverse=True)
    out = [
        "---",
        f'title: "Issues: {label_name}"',
        "---",
        "",
        f"# Issues: {label_name}",
        "",
        f"Issues с меткой **{label_name}**. Всего: **{len(items_sorted)}**. "
        f"Обновлено: `{sync_time}`.",
        "",
        "[\u2190 ко всемIssues](../index.md)",
        "",
        "| # | Заголовок | Состояние | Автор | Обновлено |",
        "|---:|---|---|---|---|",
    ]
    for it in items_sorted:
        title_clean = it["title"].replace("|", "\\|")
        out.append(
            f"| [{it['number']}]({it['_filename']}) "
            f"| [{title_clean}]({it['_filename']}) "
            f"| {state_icon(it['state'])} {it['state'].title()} "
            f"| {user_link(it.get('user'))} "
            f"| {fmt_date_short(it['updated_at'])} |"
        )
    out.append("")
    return "\n".join(out)


def build_global_index(by_label, by_state, total):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    open_count = by_state.get("open", 0)
    closed_count = by_state.get("closed", 0)

    out = [
        "---",
        'title: "GitHub Issues"',
        "---",
        "",
        f"# GitHub Issues \u2014 `{OWNER}/{REPO}`",
        "",
        f"Все issues из репозитория "
        f"[{OWNER}/{REPO}](https://github.com/{OWNER}/{REPO}/issues). "
        f"Всего: **{total}** (\U0001f7e2 открыто: **{open_count}**, "
        f"\U0001f534 закрыто: **{closed_count}**). "
        f"Обновлено: `{sync_time}`.",
        "",
        "## \U0001f4c2 Метки",
        "",
        "| Метка | Issues |",
        "|---|---:|",
    ]
    for label_name in sorted(by_label.keys()):
        items = by_label[label_name]
        label_slug = items[0]["_label_slug"]
        out.append(f"| [{label_name}](labels/{label_slug}/index.md) | {len(items)} |")
    out.append("")

    # Последние 20 обновлённых issues
    flat = [it for items in by_label.values() for it in items]
    flat.sort(key=lambda x: x["updated_at"], reverse=True)
    recent = flat[:20]

    out += [
        "## \U0001f552 Последние обновлённые",
        "",
        "| # | Заголовок | Состояние | Автор | Обновлено |",
        "|---:|---|---|---|---|",
    ]
    for it in recent:
        title_clean = it["title"].replace("|", "\\|")
        out.append(
            f"| [{it['number']}]({it['_filename']}) "
            f"| [{title_clean}]({it['_filename']}) "
            f"| {state_icon(it['state'])} {it['state'].title()} "
            f"| {user_link(it.get('user'))} "
            f"| {fmt_date_short(it['updated_at'])} |"
        )
    out.append("")
    return "\n".join(out)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Listing issues in {OWNER}/{REPO}...")
    listing = list_all_issues()
    print(f"Found {len(listing)} issues.")

    by_label = defaultdict(list)
    by_state = defaultdict(int)
    seen_paths = {Path("index.md")}

    labels_dir = OUTPUT_DIR / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    for meta in listing:
        number = meta["number"]
        print(f"  \u2192 #{number} {meta['title'][:60]}")
        issue, comments = fetch_issue(number)
        if issue is None:
            continue

        labels = issue.get("labels", [])
        state = issue.get("state", "open")
        by_state[state] += 1

        slug = slugify(issue["title"])
        filename = f"{number:05d}-{slug}.md"

        (OUTPUT_DIR / filename).write_text(
            build_issue_md(issue, comments), encoding="utf-8"
        )
        seen_paths.add(Path(filename))

        label_names = [l["name"] for l in labels] if labels else ["no-label"]
        for label_name in label_names:
            label_slug = slugify(label_name, max_len=40)
            by_label[label_name].append({
                "number": issue["number"],
                "title": issue["title"],
                "user": issue.get("user"),
                "state": state,
                "updated_at": issue["updated_at"],
                "_filename": filename,
                "_label_slug": label_slug,
            })

    # Index по меткам
    for label_name, items in by_label.items():
        label_slug = items[0]["_label_slug"]
        label_dir = labels_dir / label_slug
        label_dir.mkdir(parents=True, exist_ok=True)
        (label_dir / "index.md").write_text(
            build_label_index(label_name, label_slug, items), encoding="utf-8"
        )
        seen_paths.add(Path("labels") / label_slug / "index.md")

    # Глобальный index.md
    (OUTPUT_DIR / "index.md").write_text(
        build_global_index(by_label, by_state, len(listing)), encoding="utf-8"
    )

    # Удаляем stale файлы
    for path in OUTPUT_DIR.rglob("*.md"):
        rel = path.relative_to(OUTPUT_DIR)
        if rel not in seen_paths:
            print(f"  \u2717 removing stale {rel}")
            path.unlink()
    for p in sorted(OUTPUT_DIR.glob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()

    print(f"Done. {len(listing)} issues, {len(by_label)} labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
