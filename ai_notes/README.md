# QElight AI lessons

The master TOC is `index.html`. Each lesson is a separate Markdown file in
`notes/`, displayed at `lesson.html?id=QAI.01.07`.

## Publish a new lesson

1. Add a file named `QAI.xx.yy_Descriptive_Name_Notes.md` directly inside
   `ai/notes/`. Its ID must match a section heading in `ai/index.html`.
2. Put any accompanying files inside `ai/notes/QAI.xx.yy_resources/` (with
   exactly the same ID). Subfolders are allowed. Link to particular resources
   in the Markdown using their relative paths, or let the reader list them in
   its **Practice resources** section.
3. Commit the Markdown file and resource folder. GitHub Pages rebuilds
   `ai/files.json` from the files in `ai/notes/`; the TOC and lesson reader use
   that list automatically. No JSON or script edit is needed for subsequent
   lessons. The first publication must include `catalog.js` and `files.json`.

For example:

```text
ai/notes/QAI.02.01.01_Data_and_Data_System_Basics_Notes.md
ai/notes/QAI.02.01.01_resources/example.ipynb
```

The TOC displays **Read lesson** only for note IDs it already contains. All
files in a resource folder are public, so upload only material intended for
learners. Markdown links resolve relative to their note file. Existing ZIP
practice projects may stay beside their notes and continue to work.

The automatic list depends on GitHub Pages' Jekyll build. A plain local HTTP
server serves the unprocessed `files.json` template and cannot preview the
automatic list; use a Jekyll preview or the published site. The bundled
Markdown renderer is Marked 17.0.5; its license is in `vendor/`.
