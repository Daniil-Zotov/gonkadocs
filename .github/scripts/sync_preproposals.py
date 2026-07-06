#!/usr/bin/env python3
"""Sync community pre-proposals from gonka.vote into proposals/preproposals/.

Fetches all proposals from gonka.vote/api/proposal, then for each one:
- Fetches full detail (description) from /api/proposal/{id}
- Fetches comments from /api/proposal/{id}/comments
- Generates individual .md files
- Generates overview index with Active / Expired sections
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

API_BASE = "https://gonka.vote/api"
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/proposals/preproposals"))


def vote_get(path, retries=3):
    url = f"{API_BASE}{path}"
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code in (502, 503) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"  Error fetching {url}: {e}")
            return None


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')


def clean_title(title):
    return re.sub(r'^#+\s*', '', title).strip()


def format_gnk(ngonka_str):
    try:
        val = int(ngonka_str) / 1_000_000_000
        if val >= 1_000_000:
            return f"{val/1_000_000:.1f}M GNK"
        elif val >= 1_000:
            return f"{val/1_000:.1f}K GNK"
        else:
            return f"{val:.2f} GNK"
    except (ValueError, TypeError):
        return "—"


def format_usdt(ngonka_str, community_weight_str):
    try:
        bid = int(ngonka_str)
        weight = int(community_weight_str)
        if weight > 0:
            usdt = bid / weight * 1_000_000
            if usdt >= 1_000:
                return f"~${usdt/1_000:.0f}K"
            return f"~${usdt:.0f}"
    except (ValueError, TypeError):
        pass
    return "—"


def is_active(proposal):
    if proposal.get("status") == "open":
        closes_at = proposal.get("closes_at")
        if closes_at:
            try:
                close_dt = datetime.fromisoformat(closes_at.replace("Z", "+00:00"))
                return close_dt > datetime.now(timezone.utc)
            except (ValueError, TypeError):
                return True
        return True
    return False


def render_status_badge(proposal):
    if is_active(proposal):
        return "🟢 Active"
    return "🔴 Expired"


def render_voters_table(voters):
    if not voters:
        return ""
    lines = [
        "| Voter | Amount | Date |",
        "| :----- | :----- | :--- |",
    ]
    for v in voters:
        addr = v.get("voter", "—")
        if len(addr) > 20:
            addr = addr[:8] + "..." + addr[-6:]
        amount = format_gnk(v.get("amount_ngonka", "0"))
        voted_at = v.get("voted_at", "")
        if voted_at:
            try:
                dt = datetime.fromisoformat(voted_at.replace("Z", "+00:00"))
                voted_at = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                pass
        lines.append(f"| `{addr}` | {amount} | {voted_at} |")
    return "\n".join(lines)


def render_comments(comments):
    if not comments:
        return "No comments yet."
    lines = []
    for c in comments:
        author = c.get("author_name", "Anonymous")
        body = c.get("body", "")
        created = c.get("created_at", "")
        likes = c.get("likes", 0)
        dislikes = c.get("dislikes", 0)

        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                pass

        lines.append(f"### 💬 {author}")
        lines.append(f"*{created}* · 👍 {likes} · 👎 {dislikes}")
        lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def generate_proposal_page(proposal, detail, comments):
    pid = proposal["id"]
    title = clean_title(proposal.get("title", "Untitled"))
    summary = proposal.get("summary", "")
    description = detail.get("description", "") if detail else ""
    creator_name = proposal.get("creator_name", "Anonymous")
    creator_image = proposal.get("creator_image", "")
    created_at = proposal.get("created_at", "")
    closes_at = proposal.get("closes_at", "")
    tally = proposal.get("tally", {})
    voters = detail.get("voters", []) if detail else []
    status = render_status_badge(proposal)
    source_lang = proposal.get("source_lang", "en")

    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            created_at = dt.strftime("%Y-%m-%d %H:%M UTC")
        except (ValueError, TypeError):
            pass

    if closes_at:
        try:
            dt = datetime.fromisoformat(closes_at.replace("Z", "+00:00"))
            closes_at = dt.strftime("%Y-%m-%d %H:%M UTC")
        except (ValueError, TypeError):
            pass

    voter_count = tally.get("voter_count", 0)
    weighted_bid = format_gnk(tally.get("weighted_avg_bid_ngonka", "0"))

    md = f"""---
title: "{title}"
template: proposals-main.html
---

# {title}

<div class="preproposal-header">

<div class="preproposal-status">{status}</div>

| | |
|:---|:---|
| **Author** | {creator_name} |
| **Created** | {created_at} |
| **Closes** | {closes_at} |
| **Language** | {source_lang.upper()} |
| **Votes** | {voter_count} |
| **Avg. Bid** | {weighted_bid} |

</div>

{summary}

---

## Full Proposal

{description}

"""

    if voters:
        md += f"""---

## Votes ({len(voters)})

{render_voters_table(voters)}

"""

    if comments:
        md += f"""---

## Comments ({len(comments)})

{render_comments(comments)}
"""

    md += f"""
---

<div class="preproposal-link">

[View on gonka.vote](https://gonka.vote/proposal/{pid})

</div>
"""
    return md


def generate_index(proposals_by_status):
    active = proposals_by_status.get("active", [])
    expired = proposals_by_status.get("expired", [])

    md = """---
title: Pre-Proposals
template: proposals-main.html
---

# Gonka Community Pre-Proposals

Community proposals from [gonka.vote](https://gonka.vote). These are off-chain indicative polls where GNK holders signal support for potential on-chain governance proposals.

---

## 🟢 Active Proposals

"""
    if active:
        md += "| Status | Title | Author | Votes | Avg. Bid | Closes |\n"
        md += "| :----- | :----- | :----- | ----: | -------: | :----- |\n"
        for p in sorted(active, key=lambda x: x.get("closes_at", ""), reverse=False):
            pid = p["id"]
            title = clean_title(p.get("title", "Untitled"))
            author = p.get("creator_name", "—")
            tally = p.get("tally", {})
            voter_count = tally.get("voter_count", 0)
            weighted_bid = format_gnk(tally.get("weighted_avg_bid_ngonka", "0"))
            closes_at = p.get("closes_at", "")
            if closes_at:
                try:
                    dt = datetime.fromisoformat(closes_at.replace("Z", "+00:00"))
                    closes_at = dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
            slug = slugify(title)
            md += f"| 🟢 | [{title}](./{pid}/) | {author} | {voter_count} | {weighted_bid} | {closes_at} |\n"
    else:
        md += "*No active proposals.*\n"

    md += """

---

## 🔴 Expired Proposals

"""
    if expired:
        md += "| Status | Title | Author | Votes | Avg. Bid | Closed |\n"
        md += "| :----- | :----- | :----- | ----: | -------: | :----- |\n"
        for p in sorted(expired, key=lambda x: x.get("closes_at", ""), reverse=True):
            pid = p["id"]
            title = clean_title(p.get("title", "Untitled"))
            author = p.get("creator_name", "—")
            tally = p.get("tally", {})
            voter_count = tally.get("voter_count", 0)
            weighted_bid = format_gnk(tally.get("weighted_avg_bid_ngonka", "0"))
            closes_at = p.get("closes_at", "")
            if closes_at:
                try:
                    dt = datetime.fromisoformat(closes_at.replace("Z", "+00:00"))
                    closes_at = dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
            md += f"| 🔴 | [{title}](./{pid}/) | {author} | {voter_count} | {weighted_bid} | {closes_at} |\n"
    else:
        md += "*No expired proposals.*\n"

    md += """

---

*Data synced from [gonka.vote](https://gonka.vote). Last updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") + """*
"""
    return md


def main():
    print("Fetching proposals from gonka.vote...")
    proposals = vote_get("/proposal")
    if not proposals:
        print("Failed to fetch proposals")
        return

    print(f"Found {len(proposals)} proposals")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    active = []
    expired = []

    for i, proposal in enumerate(proposals):
        pid = proposal["id"]
        title = proposal.get("title", "Untitled")
        print(f"  [{i+1}/{len(proposals)}] {title[:60]}...")

        detail = vote_get(f"/proposal/{pid}")
        time.sleep(0.3)

        comments = vote_get(f"/proposal/{pid}/comments")
        time.sleep(0.3)

        page_md = generate_proposal_page(proposal, detail, comments)
        prop_dir = OUTPUT_DIR / pid
        prop_dir.mkdir(exist_ok=True)
        (prop_dir / "index.md").write_text(page_md, encoding="utf-8")

        if is_active(proposal):
            active.append(proposal)
        else:
            expired.append(proposal)

    print(f"\nActive: {len(active)}, Expired: {len(expired)}")

    index_md = generate_index({"active": active, "expired": expired})
    (OUTPUT_DIR / "index.md").write_text(index_md, encoding="utf-8")

    print(f"Done. Written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
