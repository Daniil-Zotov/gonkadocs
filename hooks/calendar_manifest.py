"""MkDocs hook: generates manifest.json for calendar events.

Scans docs/community/calendar/ for all *.json files (excluding manifest.json
itself) and writes a manifest list so the calendar template can discover and
load all event files dynamically.
"""

import json
import os
from glob import glob


def on_post_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    calendar_dir = os.path.join(docs_dir, "community", "calendar")

    if not os.path.isdir(calendar_dir):
        return

    json_files = sorted(
        f for f in glob(os.path.join(calendar_dir, "*.json"))
        if os.path.basename(f) != "manifest.json"
    )

    manifest = {
        "sources": [os.path.basename(f) for f in json_files],
    }

    manifest_path = os.path.join(calendar_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)

    print(f"  [calendar] Generated manifest.json with {len(json_files)} sources")
