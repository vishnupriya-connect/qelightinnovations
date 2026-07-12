from pathlib import Path
import json

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

NOTES_DIR = ROOT / "notes"

OUTPUT_FILE = ROOT / "data" / "notes.json"

# -------------------------------------------------------
# Scan Notes Folder
# -------------------------------------------------------

notes = []

for file in sorted(NOTES_DIR.rglob("*.md")):

    relative_file = file.relative_to(ROOT).as_posix()

    relative_folder = file.parent.relative_to(NOTES_DIR).as_posix()

    notes.append({

        "title": file.stem,

        "path": relative_file,

        "folder": relative_folder

    })

# -------------------------------------------------------
# Write JSON
# -------------------------------------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        notes,
        f,
        indent=4,
        ensure_ascii=False
    )

# -------------------------------------------------------
# Console Output
# -------------------------------------------------------

print()

print("=" * 60)

print(f"Found {len(notes)} markdown files")

print(f"Generated")

print(f"    {OUTPUT_FILE}")

print("=" * 60)

print()

for note in notes:

    print(f"{note['folder']}")

    print(f"    {note['title']}")

    print()