"""MkDocs hook: generates a static markdown listing of all calendar events.

The calendar page (index.md) is rendered client-side via JS (XHR -> manifest.json
-> *.json), so events are invisible to AI agents and to the MkDocs search index.

This hook writes community/calendar/events.md from the same JSON sources (via
buildtools/generate_calendar_events.py) so that:

  1. MkDocs indexes the events page -> searchable via search_index.json
  2. generate-llms-full.py picks up events.md -> events appear in llms-full.txt
  3. generate-llms.py links to it -> agents can read upcoming events from llms.txt

Runs on_pre_build so the generated page exists before MkDocs scans the docs dir.
"""

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "buildtools"))

from generate_calendar_events import generate  # noqa: E402


def on_pre_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    result = generate(docs_dir)
    if result:
        events = __import__("generate_calendar_events", fromlist=["load_events"]).load_events(
            os.path.join(docs_dir, "community", "calendar")
        )
        print(f"  [calendar] Generated events.md with {len(events)} events")
