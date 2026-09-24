# QElight AI lessons

The master TOC is `index.html`. Keep one Markdown file per lesson in `notes/`;
the public reader is `lesson.html?id=QAI.00.01`. Only lessons present in
`lessons.json` get a **Read lesson** link in the TOC.

## Add a lesson

1. Place `QAI.xx.yy_Descriptive_Name_Notes.md` in `notes/`. Its first line must
   begin with `# QAI.xx.yy`, and that ID must have a heading in the TOC.
2. Run `python3 ai/scripts/build_lessons.py` from the repository root.
3. Commit the Markdown file and regenerated `lessons.json` together. Open the
   local site with `python3 -m http.server 8000` and visit
   `http://localhost:8000/ai/` to check the new lesson link. Opening the HTML
   directly via `file://` will block the lesson fetch in most browsers.

The script fails on a missing TOC heading, duplicate ID, or mismatched note ID.
Lessons stay in TOC order for **Previous** and **Next** navigation. A lesson ID
gets its own stable URL even when its display title changes.

For later assets, add an entry to that lesson's `resources` list in
`lessons.json`:

```json
{ "label": "Practice notebook", "url": "notebooks/QAI.01.06_Practice.ipynb" }
```

This also works for repository or project URLs. The build script retains
existing `resources` entries when regenerating the index.

The bundled Markdown renderer is Marked 17.0.5; its license is in `vendor/`.
