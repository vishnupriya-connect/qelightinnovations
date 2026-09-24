# QAI.01.03 — File-System Actions

> **Position in the QElight AI path**  
> `QAI.01.02 File-system basics` → **`QAI.01.03 File-system actions`** → `QAI.01.04 Terminal and shell basics`

## 1. Core idea

File-system actions change or inspect the project materials stored on a computer.

```text
Inspect first → identify exact target → choose action → verify result
```

This order matters because some actions are reversible and some can destroy or replace work.

## 2. Safety levels of common actions

| Action | Main effect | Risk level | Good habit |
|---|---|---|---|
| list/view/search | inspect only | low | confirm location/content |
| create/copy | add a new item | low–medium | use meaningful name/location |
| move/rename | change location/name | medium | confirm paths/references after move |
| overwrite | replace existing content | high | preview/backup/check target |
| delete | remove content | high | verify exact target; prefer recoverable deletion |
| restore | recover earlier/deleted content | depends | confirm correct version/source |

## 3. Create folder and create file

- **Create folder:** make a new directory to organise files.
- **Create file:** make a new stored item, often empty at first, then add content.

### Example project start

```text
qelight-rag-demo/
├─ notebooks/
├─ data/
├─ src/
├─ outputs/
└─ README.md
```

### Good practice

- create folders based on purpose, not random convenience;
- do not create duplicate folders such as `final`, `final2`, `final_new` unless a clear reason exists;
- create a README early so the project purpose and setup are not lost.

## 4. List folder contents

- **List folder contents:** display the files and folders directly inside a directory.
- It answers: *What is here now?*

### Why it matters

Before loading a dataset, running a script, copying files, or deleting output, list the target folder and verify its contents.

```text
Question: “Why cannot my notebook find `data.csv`?”
First check: list the expected data folder.
```

## 5. View file content

- **View file content:** inspect what a file contains without intentionally changing it.
- Examples: read a Markdown note, inspect a JSON configuration file, preview a CSV dataset, open a Python script.

### View before using

- inspect a configuration before changing settings;
- inspect an AI-generated script before executing it;
- inspect a dataset header before analysing it;
- inspect a `.env`-like configuration file without exposing secrets in screenshots/logs.

## 6. Open and close file

- **Open file:** load a file into an application/editor/viewer for reading or editing.
- **Close file:** release the application’s active use of that file.

### Why closing matters

- unsaved changes can be lost;
- some programs lock a file while it is open;
- another program may be unable to replace/move the file until it is closed;
- closing/reopening can show whether saved changes actually reached storage.

## 7. Copy file and copy folder

- **Copy file:** create another file with the same content while keeping the original.
- **Copy folder:** create another folder and duplicate its contents/subfolders.

### Example

```text
Original: data/raw/course_notes.csv
Copy:     data/backup/course_notes_before_cleaning.csv
```

### Use copy when

- keeping a backup before a risky transformation;
- preparing a safe sample dataset;
- creating a template/project starting point;
- separating raw data from processed data.

### Copy is not version control

Copies help short-term safety. Git/version control later provides a stronger history of code changes. For important data, use a clear versioning/backup process too.

## 8. Move file and move folder

- **Move file:** change a file’s location; it no longer remains at the old path.
- **Move folder:** change a folder’s location with its contents.

### Example

```text
Before: downloads/course_notes.csv
After:  qelight-rag-demo/data/raw/course_notes.csv
```

### Common effect of moving

Any code/notebook/configuration that refers to the old path can fail until updated.

```text
Old reference: downloads/course_notes.csv
New location:  data/raw/course_notes.csv
```

**Rule:** after a move, verify both the new location and any path references in the project.

## 9. Rename file and rename folder

- **Rename file/folder:** change its name while keeping it in the same location.

### Example

```text
Bad:  final_final.ipynb
Better: rag_retrieval_baseline.ipynb
```

### Rename safely

- use a name that says purpose, not emotion/time pressure;
- keep file extension correct;
- check links/imports/configuration that use the old name;
- avoid changing case only (for example `App.py` to `app.py`) when working across different operating systems, because behaviour can differ.

## 10. Delete file and delete folder

- **Delete file:** remove a file from its location.
- **Delete folder:** remove a folder; depending on method, its contents may also be removed.

### Why deletion is high risk

Some delete actions move content to a recycle bin/trash; others permanently remove it. A folder delete can affect many nested files.

### Safe deletion protocol

```text
1. Identify the exact absolute/relative target path.
2. List/inspect it.
3. Confirm it is not a parent/project/data folder by mistake.
4. Check whether it contains needed work or secrets.
5. Prefer moving to recycle bin/trash or making a backup when practical.
6. Delete only the confirmed target.
7. Verify result and know recovery path.
```

### Never use broad or uncertain targets

- do not delete a folder merely because its name looks similar;
- do not use wildcard/bulk deletion until you understand exactly what it matches;
- do not delete raw data, logs, model outputs, or configuration before deciding whether they are needed for reproducibility/audit;
- do not let AI-generated deletion code run without inspection and safe testing.

## 11. Restore file

- **Restore file:** recover a deleted file, an earlier version, or a backup copy.
- Restore source may be recycle bin/trash, version history, cloud backup, Git, database backup, or manual copy.

### Restore is possible only if a recovery source exists

| Recovery source | What it can restore |
|---|---|
| recycle bin/trash | recently deleted local item, if not permanently removed |
| backup copy | copied snapshot |
| cloud/version history | earlier stored version, if enabled |
| Git | tracked code/document versions |
| database backup | data state captured in backup |

Good recovery begins before deletion: keep meaningful backups and version history.

## 12. Search file name and search text in file

- **Search file name:** find files/folders based on their name/location.
- **Search text in file:** find a word/phrase inside file content.

### Examples

| Need | Search type |
|---|---|
| find `app.py` | file-name search |
| find where `API_KEY` is mentioned | text-in-file search |
| find all `README.md` files | file-name search |
| find old path `data/old.csv` in code | text-in-file search |

### Practical use

After renaming/moving a file, search project text for the old name/path. This finds code and documentation that need updating.

## 13. Overwrite file

- **Overwrite file:** write new content into an existing file, replacing its previous content.
- Overwrite can happen intentionally or accidentally when saving, copying, downloading, exporting, or generating output with the same file name.

### Example

```text
Existing: outputs/summary.txt
New program saves another result to: outputs/summary.txt

Result: earlier summary content may be replaced.
```

### Before overwriting

- inspect the existing file;
- decide whether to replace, append, or save a new version;
- use meaningful dated/versioned output names if history matters;
- back up or use version control for important work;
- confirm that the target is within the intended project/output folder.

## 14. Append to file

- **Append to file:** add new content to the end of an existing file without removing its current content.

### Example

```text
Existing log file:
Run 1 completed

Append:
Run 2 completed

Result:
Run 1 completed
Run 2 completed
```

### Use append for

- logs;
- experiment history;
- incremental report entries;
- collected results where earlier entries must remain.

### Caution

Appending repeatedly can create duplicate, unstructured, or sensitive logs. Define format, retention, and access rules.

## 15. Action comparison

| Action | Original remains at old place? | New content/location created? | Can destroy old content? |
|---|---:|---:|---:|
| copy | yes | yes | normally no, unless you replace an existing destination |
| move | no | yes, at new path | not normally, but references may break |
| rename | no old name | yes, new name at same location | not content itself, but references may break |
| overwrite | file remains by name | new content replaces old content | yes |
| append | yes | same file gains extra content | not old content, but can create bad/duplicate state |
| delete | no | no | yes; recovery may be unavailable |
| restore | recovery source preserved | recovered file/version | may overwrite current version if chosen carelessly |

## 16. Worked project example: safe dataset preparation

### Starting structure

```text
project/
└─ data/
   └─ raw/
      └─ course_notes.csv
```

### Intended work

Create cleaned data for an experiment without changing original source data.

### Safe action sequence

```text
1. View/list `data/raw/` and confirm course_notes.csv exists.
2. Copy the raw file or read it into a program.
3. Save cleaned result under a new path:
   data/processed/course_notes_cleaned_v1.csv
4. Keep raw data unchanged.
5. Record which raw version created which processed version.
6. If a result is wrong, delete only the confirmed processed output—not raw source data.
```

This pattern supports reproducible ML/GenAI work.

## 17. Guided file actions: an AI project practice area

**Practice boundary:** work only inside the disposable `qai-path-lab` folder created in `QAI.01.02`. The files represent a tiny course-assistant project. They are practice data, not a real student's documents. Use a file explorer and a plain-text editor. Commands come in `QAI.01.04`.

### 17.1 Prepare and inspect

If the earlier practice folder is unavailable, create this exact structure. An empty `outputs/` folder is intentional.

```text
qai-path-lab/
├─ notes/
│  └─ intro.md            contents: Fictional note for path practice.
├─ data/
│  └─ sample.csv          contents: topic,hours   (first line)
│                        orientation,1 (second line)
└─ outputs/
```

Here, `.md` denotes a Markdown text note and `.csv` denotes table-like text with comma-separated fields. Open both files, read their content, close them, then list each folder in the explorer. **Check:** the three folder names and two file names match; you have not changed either file.

### 17.2 Create, open, close, view, and append

1. In `outputs/`, create the plain-text file `action_log.txt`. Write `Run 1: created` and save.
2. Close the editor, reopen that file, and read the line. If it is missing, check where you saved the file before repeating the action.
3. At the **end** of the existing text, add a new line `Run 2: checked`; save and close. Reopen and inspect.

**Expected file content after step 3:**

```text
Run 1: created
Run 2: checked
```

Both lines present means you **appended**. If only `Run 2: checked` remains, you replaced the first line and must repair it now.

### 17.3 Copy, rename, and move a file

1. Copy `notes/intro.md` into `outputs/`. Name the new copy `outputs/intro_copy.md` without replacing an existing file.
2. Inspect **both** files: the first line in each should read `Fictional note for path practice.`. `notes/intro.md` must still exist.
3. Rename `outputs/intro_copy.md` to `outputs/intro_archive.md`. The former name should disappear from `outputs/`.
4. Move `outputs/intro_archive.md` into `data/`. The result is `data/intro_archive.md`; it must no longer appear in `outputs/`.

**Interpretation:** after copying, two separate files exist. Renaming or moving changes the path; neither makes the original note disappear. A program reading the old `outputs/intro_archive.md` path now needs an updated path.

### 17.4 Copy, move, and rename a folder

1. Copy the **entire** `notes/` folder into `outputs/`. If the explorer names it `notes`, rename only that copied folder to `notes_copy`. Result: `outputs/notes_copy/intro.md`.
2. Verify the original `notes/intro.md` still exists and the copied `outputs/notes_copy/intro.md` contains the same line.
3. Move the copied folder into `data/`: `data/notes_copy/intro.md`. Confirm its former place in `outputs/` is empty.
4. Rename the moved folder to `data/notes_archive/`. Verify `data/notes_archive/intro.md` exists.

**Pause on a replace/merge prompt:** the proposed destination already contains something. Cancel, inspect both folders, and choose a distinct name. Never replace an existing folder just to finish the practice.

### 17.5 Search by name and search by content

- Search **within `qai-path-lab`** for file name `intro_archive.md`. Expected: `data/intro_archive.md`.
- Search the **contents** of files in the practice folder for `Fictional note for path practice.`. Expected matches in `notes/intro.md`, `data/intro_archive.md`, and `data/notes_archive/intro.md`.
- Some file explorers search names only or skip text in certain locations. If content search yields no matches, open the three known files and use the editor's text-search feature in each; record that your explorer's content search was unavailable.

**Why both searches?** File-name search tells you *which file* has a particular name; content search tells you *which files mention a phrase or an old project path*.

### 17.6 Deliberate overwrite with a backup

1. Inspect `outputs/action_log.txt`: it must have the two lines in §17.2.
2. Copy it to `outputs/action_log_before_replace.txt`. Open the copy and verify it has **both** lines.
3. Open the original `outputs/action_log.txt`. Replace **its complete contents** with `Run 3: replaced`. Save, close, and reopen it.
4. Check that `outputs/action_log.txt` has only the replacement line and `outputs/action_log_before_replace.txt` still has both earlier lines. This is an intentional **overwrite** of a disposable file, with a recoverable earlier copy.

If a save or paste operation asks whether to replace a different file, stop and inspect its full location and contents before proceeding.

### 17.7 Delete and restore only disposable items

1. Create `outputs/delete_me/throwaway.txt` containing `Disposable practice item`.
2. Confirm the exact folder `qai-path-lab/outputs/delete_me/` and its one file; then use a **recoverable** delete that explicitly sends the folder to the recycle bin/trash.
3. Verify `outputs/delete_me/` has disappeared. In recycle bin/trash, find that **exact** deleted folder and restore it. Reopen `outputs/delete_me/throwaway.txt` and read its line.
4. For the separate **delete-file** action, send `outputs/delete_me/throwaway.txt` to recycle bin/trash, verify it is missing, restore the exact file, and verify the line again.

**If your location or operating system does not offer a recoverable delete, skip the deletion steps.** Keep the practice item. Recovery is not guaranteed, and permanent delete is unnecessary here. If restoration reports that a same-named item already exists, stop and inspect both copies; do not overwrite either blindly.

### 17.8 Expected state after the guided actions

If every optional recycle-bin step was available and successful, the practice area should now look like this:

```text
qai-path-lab/
├─ notes/
│  └─ intro.md
├─ data/
│  ├─ sample.csv
│  ├─ intro_archive.md
│  └─ notes_archive/
│     └─ intro.md
└─ outputs/
   ├─ action_log.txt                Run 3: replaced
   ├─ action_log_before_replace.txt Run 1 and Run 2
   └─ delete_me/
      └─ throwaway.txt              Disposable practice item
```

**Evidence record, completed example:**

| Action | Before | After | Check |
|---|---|---|---|
| copy file | `notes/intro.md` only | plus `data/intro_archive.md` after move | original still opens |
| copy folder | `notes/` only | plus `data/notes_archive/` after move | both `intro.md` files open |
| append | log has Run 1 | log has Run 1 and Run 2 | read both lines |
| overwrite | log has Run 1 and Run 2; backup made | log has Run 3; backup retains Run 1 and Run 2 | open both files |
| delete and restore | throwaway item exists | item temporarily missing, then restored | open restored item |

The table records *observable results*, not just clicks. If your search or restore was unavailable, note that explicitly instead of claiming it worked.

## 18. Independent variation with a worked solution

**Task:** take the disposable `data/sample.csv` as raw data for a small AI exercise. Make a copy in `outputs/`, move the copy into `notes/`, rename it `sample_checked.csv`, and add the line `file actions,1` **only to that copy**. Keep the raw source intact. Write down the final location of each file and its content.

**Worked solution:**

1. Open `data/sample.csv`; verify its two original lines: `topic,hours` and `orientation,1`.
2. Copy it to `outputs/sample_backup.csv`; verify both locations now exist.
3. Move the copy to `notes/sample_backup.csv`; confirm it no longer exists in `outputs/`.
4. Rename the moved copy to `notes/sample_checked.csv`; confirm its old name is gone.
5. Open `notes/sample_checked.csv`; add `file actions,1` on a **new final line**, save and reopen it.
6. Reopen `data/sample.csv` and verify it still has only the two original lines.

**Expected result:**

```text
data/sample.csv:
topic,hours
orientation,1

notes/sample_checked.csv:
topic,hours
orientation,1
file actions,1
```

In a real ML or GenAI project, this same habit separates original input data from the edited data used for an experiment.

## 19. Troubleshooting these actions

| Symptom | Likely cause | Next check/action |
|---|---|---|
| file appears missing after save | saved to another folder or different extension | inspect the editor's saved path; search for the full file name; check for `.txt` added to `.md` |
| copied file not where expected | pasted into current folder instead of intended folder | list both source and destination; move only the verified practice copy |
| moved file no longer opens through old link | old path is stale | identify new path; update the reference |
| old line disappears after editing | overwritten instead of appended | open backup; recover earlier line and save with correct two lines |
| file will not move or rename | open in another application, or access denied | save and close editor; verify permissions and destination; avoid privileged changes |
| search shows no content match | name-only search or unsupported text indexing | open known files and search text inside the editor |
| restore cannot find the item | deletion skipped trash or history unavailable | stop; use an existing practice backup if available; never promise recovery |

## 20. What to remember

- Inspect before changing: list folder, view file, confirm path.
- Copy preserves original; move changes location; rename changes name.
- Overwrite replaces old content; append adds to old content.
- Delete can be permanent; restore needs a recovery source.
- Search by name to locate files; search text to locate content/references.
- After move/rename, update code, notebooks, configuration, and documentation that use old paths.
- Keep raw data separate from processed data; protect reproducibility and recovery.
- Never execute unknown AI-generated code that changes/deletes files without reading, testing, and confirming the target.

## 21. Next connection

Next: `QAI.01.04 — Terminal and shell basics`. You will perform these same file-system actions through typed commands, which makes work repeatable, automatable, and useful for Python/Git/deployment workflows.
