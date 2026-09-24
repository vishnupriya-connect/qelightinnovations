"""Build the lesson index from the TOC and the Markdown files.

Run from anywhere: python3 ai/scripts/build_lessons.py
"""

import json
import re
from pathlib import Path

AI = Path(__file__).resolve().parents[1]
html = (AI / "index.html").read_text(encoding="utf-8")
source = re.search(r'<script id="toc-source" type="text/plain">(.*?)</script>', html, re.S)
if source is None:
    raise SystemExit("Cannot find the embedded TOC")

headings = {}
for line in source.group(1).splitlines():
    match = re.match(r"^#{3,6}\s+(QAI\.\d+(?:\.\d+)+)\s+[—–-]\s+(.+)$", line)
    if match:
        if match[1] in headings:
            raise SystemExit(f"Duplicate TOC ID: {match[1]}")
        headings[match[1]] = match[2].strip()

manifest = AI / "lessons.json"
existing = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
lessons = {}
for path in sorted((AI / "notes").glob("*.md")):
    code = path.name.split("_", 1)[0]
    if code not in headings:
        raise SystemExit(f"No matching TOC heading: {path.name}")
    if code in lessons:
        raise SystemExit(f"Duplicate note ID: {code}")
    if not path.read_text(encoding="utf-8").startswith(f"# {code}"):
        raise SystemExit(f"Note title does not match ID: {path.name}")
    lessons[code] = {
        "title": headings[code],
        "note": "notes/" + path.name,
        "resources": existing.get(code, {}).get("resources", []),
    }

# Keep the learning order from the TOC, not filename sorting.
ordered = {code: lessons[code] for code in headings if code in lessons}
manifest.write_text(
    json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Indexed {len(ordered)} lessons; {len(headings) - len(ordered)} TOC sections await notes")
