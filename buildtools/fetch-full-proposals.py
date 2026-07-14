#!/usr/bin/env python3
"""
For proposals without full-proposal.md:
1. Find Metadata URLs pointing to GitHub blobs/commits
2. Convert to raw.githubusercontent.com URLs
3. Fetch raw markdown and save as full-proposal.md

For GitHub discussion/issue/PR/repo pages:
- Fetch via GitHub API to get clean markdown body
"""

import os, re, sys, json, time, urllib.request, urllib.error, ssl

PROPOSALS_DIR = "docs/proposals/proposals"

def find_github_urls(text):
    """Find GitHub content URLs from Metadata field and body."""
    urls = []
    m = re.search(r'\*\*Metadata:\*\*\s*\[([^\]]+)\]\(([^)]+)\)', text)
    if m:
        urls.append(m.group(2))
    m = re.search(r'\*\*Metadata:\*\*\s*(https?://\S+)', text)
    if m:
        urls.append(m.group(1).rstrip(')'))
    for m in re.finditer(
        r'(?:Full PROPOSAL|Full proposal|full proposal):\s*<([^>]+)>',
        text, re.IGNORECASE
    ):
        urls.append(m.group(1).rstrip('.,)'))
    seen = set()
    result = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        if re.match(r'https://(raw\.)?github(?:usercontent)?\.com/', url):
            result.append(url)
        elif re.match(r'https://github\.com/', url):
            result.append(url)
    return result


def github_to_raw(url):
    """Convert GitHub blob/commit URL to raw.githubusercontent.com."""
    m = re.match(r'https://github\.com/([^/]+)/([^/]+)/(blob|commit)/(.+?)(?:\?.*)?$', url)
    if m:
        owner, repo, _, path = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{path}"
    return url


def url_to_api(url):
    """Convert GitHub page URL to API URL."""
    # discussions
    m = re.search(r'github\.com/([^/]+)/([^/]+)/discussions/(\d+)', url)
    if m:
        return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/discussions/{m.group(3)}"
    # issues
    m = re.search(r'github\.com/([^/]+)/([^/]+)/issues/(\d+)', url)
    if m:
        return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/issues/{m.group(3)}"
    # pull
    m = re.search(r'github\.com/([^/]+)/([^/]+)/pull/(\d+)', url)
    if m:
        return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/pulls/{m.group(3)}"
    # repo readme
    m = re.search(r'github\.com/([^/]+)/([^/]+?)(?:/tree/[^/]+)?(?:/blob/[^/]+)?$', url)
    if m:
        return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/readme"
    # raw content URL
    return url


def fetch(url, retries=3):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; GonkaDocsBot/1.0)",
                "Accept": "application/vnd.github.raw+json"
            })
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            print(f"    [attempt {attempt+1}] HTTP {e.code}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(2)
        except Exception as e:
            print(f"    [attempt {attempt+1}] {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(2)
    return None


def extract_body_from_api(data):
    """Extract markdown body from GitHub API JSON response."""
    try:
        obj = json.loads(data)
    except:
        return None
    if isinstance(obj, dict):
        # Discussion/issue/PR API
        if "body" in obj and obj["body"]:
            return obj["body"]
        # Readme API
        if "content" in obj:
            import base64
            try:
                return base64.b64decode(obj["content"]).decode("utf-8")
            except:
                return None
    return None


def clean_github_html(html):
    """Extract readable text from GitHub HTML page (fallback when API fails)."""
    import re
    # Try comment-body div
    m = re.search(r'<td[^>]*class=\"[^\"]*comment-body[^\"]*\"[^>]*>(.*?)</td>', html, re.DOTALL)
    if m:
        raw = m.group(1)
    else:
        # Try task-list div
        m = re.search(r'<div[^>]*class=\"[^\"]*comment-body[^\"]*\"[^>]*>', html, re.DOTALL)
        if m:
            start = m.end()
            depth = 1
            i = start
            while i < len(html) and depth > 0:
                if html[i:i+6] == '</div>': depth -= 1
                elif html[i:i+3] == '<div': depth += 1
                i += 1
            raw = html[start:i-6]
        else:
            # Try article
            m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
            if m:
                raw = m.group(1)
            else:
                raw = html
    # Decode HTML entities
    raw = raw.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    raw = raw.replace('&#39;', "'").replace('&quot;', '"')
    # Convert <br>, <p>, <div> to newlines
    raw = re.sub(r'<br\s*/?>', '\n', raw)
    raw = re.sub(r'</p>', '\n\n', raw)
    raw = re.sub(r'</div>', '\n', raw)
    raw = re.sub(r'</tr>', '\n', raw)
    raw = re.sub(r'</li>', '\n', raw)
    raw = re.sub(r'<[^>]+>', '', raw)
    # Clean excess whitespace
    raw = re.sub(r'[ \t]+', ' ', raw)
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()


def main():
    total = 0
    fetched = 0
    skipped = 0
    failed = 0

    for q in sorted(os.listdir(PROPOSALS_DIR)):
        qdir = os.path.join(PROPOSALS_DIR, q)
        if not os.path.isdir(qdir):
            continue
        for pid in sorted(os.listdir(qdir)):
            pdir = os.path.join(qdir, pid)
            fpath = os.path.join(pdir, "index.md")
            outpath = os.path.join(pdir, "full-proposal.md")
            if not os.path.isfile(fpath) or os.path.isfile(outpath):
                continue

            with open(fpath) as f:
                text = f.read()

            urls = find_github_urls(text)
            if not urls:
                continue

            total += 1
            print(f"\n--- #{pid} ({q}) ---")

            content = None
            for url in urls:
                # Strategy 1: For blob/commit URLs, use raw.githubusercontent.com
                if re.match(r'https://github\.com/[^/]+/[^/]+/(blob|commit)/', url):
                    raw_url = github_to_raw(url)
                    print(f"  raw: {raw_url}")
                    content = fetch(raw_url)
                    if content and len(content.strip()) > 50:
                        print(f"  ✓ {len(content)} chars")
                        break
                    print(f"  ✗ failed, trying next URL...")
                    content = None
                    continue

                # Strategy 2: For other GitHub URLs, use API
                api_url = url_to_api(url)
                if api_url != url:
                    print(f"  api: {api_url}")
                    data = fetch(api_url)
                    if data:
                        body = extract_body_from_api(data)
                        if body and len(body.strip()) > 50:
                            content = body
                            print(f"  ✓ {len(content)} chars")
                            break
                    # Fallback: fetch HTML directly
                    print(f"  page: {url}")
                    html = fetch(url)
                    if html:
                        body = clean_github_html(html)
                        if body and len(body.strip()) > 50:
                            content = body
                            print(f"  ✓ (html) {len(content)} chars")
                            break
                else:
                    print(f"  page: {url}")
                    html = fetch(url)
                    if html:
                        body = clean_github_html(html)
                        if body and len(body.strip()) > 50:
                            content = body
                            print(f"  ✓ (html) {len(content)} chars")
                            break
                print(f"  ✗ failed")

            if content and len(content.strip()) > 50:
                # Don't duplicate heading — the content from GitHub API/raw already has one
                with open(outpath, "w") as f:
                    f.write(content.strip())
                    f.write("\n")
                print(f"  ✓ saved")
                fetched += 1
            else:
                if content:
                    print(f"  ✗ content too short ({len(content.strip())} chars)")
                else:
                    print(f"  ✗ no content")
                failed += 1

    print(f"\n{'='*40}")
    print(f"Total processed:     {total}")
    print(f"Fetched and saved:   {fetched}")
    print(f"Failed:              {failed}")


if __name__ == "__main__":
    main()
