#!/usr/bin/env python3
"""Sync all GitHub Discussions from a repository to Markdown files."""

import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

OWNER = os.environ["REPO_OWNER"]
REPO = os.environ["REPO_NAME"]
OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
GH_TOKEN = os.environ["GH_TOKEN"]

API_URL = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
}

# --- GraphQL: список дискуссий (с пагинацией) ---------------------
LIST_QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 50, after: $cursor, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        updatedAt
      }
    }
  }
}
"""

# --- GraphQL: полная дискуссия (с пагинацией комментариев) --------
DETAIL_QUERY = """
query($owner: String!, $repo: String!, $number: Int!, $commentsCursor: String) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      title
      url
      number
      createdAt
      updatedAt
      author { login url }
      category { name emoji }
      body
      answerChosenAt
      answer {
        author { login url }
        createdAt
        body
      }
      comments(first: 50, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        totalCount
        nodes {
          author { login url }
          createdAt
          body
          isAnswer
          replies(first: 100) {
            nodes {
              author { login url }
              createdAt
              body
            }
          }
        }
      }
    }
  }
}
"""


def gh_graphql(query: str, variables: dict, retries: int = 3) -> dict:
    for attempt in range(retries):
        r = requests.post(API_URL, headers=HEADERS, json={"query": query, "variables": variables}, timeout=60)
        if r.status_code == 502 and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")
        return data["data"]
    raise RuntimeError("GraphQL request failed after retries")


def list_all_discussions() -> list[dict]:
    out, cursor = [], None
    while True:
        data = gh_graphql(LIST_QUERY, {"owner": OWNER, "repo": REPO, "cursor": cursor})
        page = data["repository"]["discussions"]
        out.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return out


def fetch_discussion(number: int) -> dict:
    """Тянет дискуссию + все страницы комментариев."""
    first = gh_graphql(DETAIL_QUERY, {"owner": OWNER, "repo": REPO, "number": number, "commentsCursor": None})
    disc = first["repository"]["discussion"]
    if disc is None:
        return None
    all_comments = list(disc["comments"]["nodes"])
    page_info = disc["comments"]["pageInfo"]
    while page_info["hasNextPage"]:
        nxt = gh_graphql(DETAIL_QUERY, {
            "owner": OWNER, "repo": REPO, "number": number, "commentsCursor": page_info["endCursor"]
        })
        more = nxt["repository"]["discussion"]["comments"]
        all_comments.extend(more["nodes"])
        page_info = more["pageInfo"]
    disc["comments"]["nodes"] = all_comments
    return disc


# --- Утилиты форматирования ---------------------------------------

def slugify(text: str, max_len: int = 60) -> str:
    """Заголовок → имя файла. Поддерживает кириллицу."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s\-а-яё]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled"


def fmt_date(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def fmt_date_short(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")


def user_link(author: dict | None) -> str:
    if not author:
        return "*[deleted]*"
    return f"[@{author['login']}]({author['url']})"


def indent_body(body: str, prefix: str = "> ") -> str:
    return "\n".join(prefix + line if line else prefix.rstrip() for line in body.splitlines())


def build_discussion_md(d: dict) -> str:
    out = []
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title_escaped = d["title"].replace('"', '\\"')

    out.append("---")
    out.append(f'title: "#{d["number"]} — {title_escaped}"')
    out.append(f"source: {d['url']}")
    out.append(f"discussion_number: {d['number']}")
    out.append(f"synced_at: {sync_time}")
    out.append("---")
    out.append("")
    out.append(
        f"> 🔄 **Авто-синхронизация:** из [GitHub Discussion #{d['number']}]({d['url']}) каждые 6 часов. "
        f"Прямые правки будут перезаписаны."
    )
    out.append("")

    out.append(f"# {d['title']}")
    out.append("")
    cat = d.get("category") or {}
    cat_str = f"{cat.get('emoji', '')} {cat.get('name', '')}".strip()
    out.append(
        f"**Автор:** {user_link(d['author'])} · "
        f"**Категория:** {cat_str} · "
        f"**Создано:** {fmt_date(d['createdAt'])} · "
        f"**Обновлено:** {fmt_date(d['updatedAt'])}"
    )
    out.append("")
    out.append("---")
    out.append("")

    out.append("## 📝 Описание")
    out.append("")
    out.append(d["body"] or "*(пусто)*")
    out.append("")

    if d.get("answer"):
        out.append("---")
        out.append("")
        out.append("## ✅ Выбранный ответ")
        out.append("")
        a = d["answer"]
        out.append(f"**От:** {user_link(a['author'])} · *{fmt_date(a['createdAt'])}*")
        out.append("")
        out.append(a["body"] or "*(пусто)*")
        out.append("")

    comments = d["comments"]["nodes"]
    if comments:
        out.append("---")
        out.append("")
        out.append(f"## 💬 Комментарии ({len(comments)})")
        out.append("")
        for i, c in enumerate(comments, 1):
            answer_mark = " ✅" if c.get("isAnswer") else ""
            out.append(f"### Комментарий {i}{answer_mark} — {user_link(c['author'])}")
            out.append("")
            out.append(f"*{fmt_date(c['createdAt'])}*")
            out.append("")
            out.append(c["body"] or "*(пусто)*")
            out.append("")
            for r in c.get("replies", {}).get("nodes", []):
                out.append(f"**↳ Ответ от {user_link(r['author'])}** · *{fmt_date(r['createdAt'])}*")
                out.append("")
                out.append(indent_body(r["body"] or "*(пусто)*"))
                out.append("")

    return "\n".join(out)


def build_index_md(items: list[dict]) -> str:
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = []
    out.append("---")
    out.append('title: "GitHub Discussions"')
    out.append("---")
    out.append("")
    out.append("# GitHub Discussions — `gonka-ai/gonka`")
    out.append("")
    out.append(
        f"Автоматический срез обсуждений из репозитория "
        f"[gonka-ai/gonka](https://github.com/{OWNER}/{REPO}/discussions). "
        f"Всего: **{len(items)}**. Последнее обновление: `{sync_time}`."
    )
    out.append("")
    out.append("| # | Заголовок | Категория | Автор | Обновлено |")
    out.append("|---:|---|---|---|---|")
    for it in items:
        cat = it.get("category") or {}
        cat_str = f"{cat.get('emoji', '')} {cat.get('name', '')}".strip() or "—"
        title_clean = it["title"].replace("|", "\\|")
        out.append(
            f"| [{it['number']}]({it['_local_path']}) "
            f"| [{title_clean}]({it['_local_path']}) "
            f"| {cat_str} "
            f"| {user_link(it.get('author'))} "
            f"| {fmt_date_short(it['updatedAt'])} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Listing all discussions in {OWNER}/{REPO}...")
    listing = list_all_discussions()
    print(f"Found {len(listing)} discussions.")

    index_items: list[dict] = []
    seen_files: set[str] = {"index.md"}

    for meta in listing:
        number = meta["number"]
        print(f"  → #{number} {meta['title'][:60]}")
        disc = fetch_discussion(number)
        if disc is None:
            print(f"    ⚠️  not found, skipping")
            continue

        slug = slugify(disc["title"])
        filename = f"{number:04d}-{slug}.md"
        seen_files.add(filename)

        (OUTPUT_DIR / filename).write_text(build_discussion_md(disc), encoding="utf-8")

        index_items.append({
            "number": disc["number"],
            "title": disc["title"],
            "author": disc.get("author"),
            "category": disc.get("category"),
            "updatedAt": disc["updatedAt"],
            "_local_path": filename,
        })

    # Index по номеру убывающе (новые сверху)
    index_items.sort(key=lambda x: x["number"], reverse=True)
    (OUTPUT_DIR / "index.md").write_text(build_index_md(index_items), encoding="utf-8")

    # Удаляем файлы, которых больше нет среди дискуссий
    for f in OUTPUT_DIR.glob("*.md"):
        if f.name not in seen_files:
            print(f"  ✗ removing stale {f.name}")
            f.unlink()

    print(f"Done. Wrote {len(index_items)} discussions + index.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
