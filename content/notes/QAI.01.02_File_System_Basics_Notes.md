# QAI.01.02 — File-System Basics

> **Position in the QElight AI path**  
> `QAI.01.01 Computer and software basics` → **`QAI.01.02 File-system basics`** → `QAI.01.03 File-system actions` → terminal, Git, Python projects

## 1. Why the file system matters

Every AI/GenAI project is made of files:

- Python code;
- notebooks;
- documents and datasets;
- configuration;
- generated outputs;
- tests;
- logs;
- project documentation.

The **file system** is the organised structure used by an operating system to store and locate these files.

```text
Storage
  └─ folders/directories
       └─ files and subfolders
            └─ code, data, notebooks, configuration, outputs
```

## 2. File

- **File:** a named unit of stored information.
- A file can contain text, code, image data, audio, video, table data, settings, or other content.

### Examples in an AI project

| File | Likely content |
|---|---|
| `lesson_notes.md` | Markdown learning notes |
| `demo.ipynb` | notebook text/code/output structure |
| `app.py` | Python program |
| `students.csv` | table-like dataset |
| `config.json` | settings/configuration |
| `README.md` | project instructions |

## 3. Folder and directory

- **Folder:** a container that organises files and other folders.
- **Directory:** technical name for a folder.

The words *folder* and *directory* usually mean the same thing in ordinary development work.

### Example project structure

```text
qelight-course-assistant/
├─ notebooks/
│  └─ rag_demo.ipynb
├─ src/
│  └─ app.py
├─ data/
│  └─ sample_notes.csv
├─ config/
│  └─ settings.json
├─ outputs/
│  └─ answer_example.txt
└─ README.md
```

Each folder gives files a clear role. Good organisation reduces confusion as projects grow.

## 4. File name

- **File name:** the human-readable name used to identify a file.
- Good file names tell you what the file is without opening it.

### Good naming habits

- use meaningful words: `retrieval_demo.ipynb`, not `new_final2.ipynb`;
- use one consistent style: `lowercase_with_underscores` or `kebab-case`;
- include version/date only when it helps: `evaluation_2026_09_23.md`;
- avoid unclear spaces/special characters when files will be used in code/terminal commands;
- do not put secrets or personal data in file names.

## 5. File extension and file type

- **File extension:** the ending after the final dot in a file name.
- **File type:** the kind of content/format a file uses.

| File name | Extension | Typical type/purpose |
|---|---|---|
| `app.py` | `.py` | Python source code |
| `analysis.ipynb` | `.ipynb` | Jupyter notebook |
| `notes.md` | `.md` | Markdown text |
| `data.csv` | `.csv` | comma-separated table data |
| `settings.json` | `.json` | structured configuration/data |
| `image.png` | `.png` | image |
| `requirements.txt` | `.txt` | plain text dependency list |

### Important caution

Changing an extension does not reliably convert the file’s content.

```text
renaming image.png to image.txt
does not turn the image into readable text.
```

The extension helps software choose how to open/use the file; the actual internal content must match the expected type.

## 6. File path

- **File path:** the address that tells the operating system where a file or folder is located.
- A path is made of folder names and, usually, a final file name.

### Example

```text
qelight-course-assistant/notebooks/rag_demo.ipynb
```

This means:

```text
inside qelight-course-assistant
  inside notebooks
    find rag_demo.ipynb
```

## 7. Path separator

- **Path separator:** character used to separate folder names in a path.

| Environment | Common path separator |
|---|---|
| Windows | backslash `\` |
| Linux/macOS | forward slash `/` |
| many programming/web contexts | forward slash `/` is commonly accepted/used |

### Example

```text
Windows-style: C:\Users\Priya\qelight\app.py
Linux/macOS-style: /home/priya/qelight/app.py
```

Do not memorise a particular personal path. Understand the pattern: a path begins from some location and names each folder on the way to the file.

## 8. Absolute path

- **Absolute path:** complete path beginning from the top/root of a file-system location.
- It identifies a location without depending on where you are currently working.

### Examples

```text
Windows: C:\Users\Priya\qelight\data\sample_notes.csv
Linux/macOS: /home/priya/qelight/data/sample_notes.csv
```

### Use

- useful when exact location is needed;
- useful for troubleshooting;
- can be less portable because another computer/user may have a different location.

## 9. Relative path

- **Relative path:** path described from the current working directory rather than from the root.

### Example project location

```text
Current working directory: qelight-course-assistant/

Relative path to notebook: notebooks/rag_demo.ipynb
Relative path to data: data/sample_notes.csv
```

### Why relative paths are useful

If the project folder is moved to another computer but its internal structure stays the same, relative paths can continue to work.

| Absolute path | Relative path |
|---|---|
| exact machine-specific address | location relative to current folder |
| `C:\Users\...\data\file.csv` | `data/file.csv` |
| good for identifying a precise local place | good for portable project structure |

## 10. Current working directory

- **Current working directory (CWD):** the folder a program/terminal currently treats as its starting location.
- Relative paths are resolved from the current working directory.

### Example

```text
Current working directory: qelight-course-assistant/
Code asks for: data/sample_notes.csv

Resolved location:
qelight-course-assistant/data/sample_notes.csv
```

### Common failure

```text
FileNotFoundError: data/sample_notes.csv
```

This may mean the file exists but the current working directory is not the folder you thought it was. Do not immediately assume the dataset is missing.

## 11. Parent directory

- **Parent directory:** the folder immediately containing the current file/folder.
- Think of it as one level upward in the folder hierarchy.

### Example

```text
qelight-course-assistant/
└─ notebooks/
   └─ rag_demo.ipynb

Parent directory of rag_demo.ipynb: notebooks/
Parent directory of notebooks/: qelight-course-assistant/
```

The common relative-path symbol `..` means “parent directory” in many programming and terminal contexts. Detailed usage comes in the terminal section.

## 12. Home directory

- **Home directory:** the main personal folder assigned to a user account by the operating system.
- It often contains your documents, downloads, project folders, settings, and user-level files.

### Why it matters

- personal projects are often stored inside or below the home directory;
- many tools use the home directory for user-specific configuration;
- paths differ between user accounts, so project code should avoid hard-coding another person’s home path.

## 13. Hidden file

- **Hidden file:** file/folder normally not shown in ordinary file views unless hidden items are enabled. Hiding rules differ by operating system: a leading dot commonly hides a name in Unix-like tools; on Windows a file may be hidden by a file attribute or a viewer setting. A dot-prefixed name such as `.env` is a *common example of configuration naming*, not proof that Windows has hidden or protected that file.
- Many hidden files store configuration or tool metadata.

### Examples

| Example | Typical purpose |
|---|---|
| `.gitignore` | tells Git which files not to track |
| `.env` | local environment configuration/secrets; must not be shared if real secrets exist |
| `.venv` | local Python environment folder |
| `.config` | tool/user configuration on some systems |

### Important rule

Hidden does **not** mean secure. A hidden secret file still needs correct permissions and must not be shared or put into shared version history.

## 14. File permissions

- **File permission:** rule that controls who can access or change a file/folder.
- Common permission categories:
  - **read permission:** view file content/list folder content;
  - **write permission:** change/delete/create file content;
  - **execute permission:** run a program/script or enter/use a directory, depending on the operating system.

### Example

| Situation | Needed permission |
|---|---|
| open a dataset | read |
| update `app.py` | write |
| run an executable script on a Unix-like system | execute |
| create output file inside `outputs/` | write on the folder |

### Safety meaning

Permissions limit accidental or unauthorised access. Do not change permissions blindly to “make it work.” First understand what is being accessed and why.

**File versus folder permissions:** opening a file requires permission to read its content and permission to reach its containing folder. Creating a file requires appropriate rights on the containing folder, even if the new file does not exist yet. On Unix-like systems, a directory's execute/search permission is related to entering/traversing it; on Windows the detailed permissions are expressed differently. “I can see a filename” does not by itself prove “I can open, edit, or execute it.”

## 15. One complete project-path example

```text
qelight-course-assistant/
├─ README.md
├─ notebooks/
│  └─ prototype.ipynb
├─ src/
│  └─ app.py
├─ data/
│  ├─ sample/
│  │  └─ course_notes.csv
│  └─ private/                 ← access-controlled; not shared publicly
├─ config/
│  └─ settings.json
├─ outputs/
│  └─ demo_answer.txt
├─ .gitignore                  ← hidden file
└─ .env                        ← hidden secret/config file; never commit real secrets
```

From `qelight-course-assistant/`:

| Need | Relative path |
|---|---|
| run app code | `src/app.py` |
| open prototype notebook | `notebooks/prototype.ipynb` |
| load sample notes | `data/sample/course_notes.csv` |
| read configuration | `config/settings.json` |
| save demonstration output | `outputs/demo_answer.txt` |

## 16. Practical observation

On your own computer, without deleting or moving anything, identify:

- one folder containing project/learning material;
- one file and its extension;
- the parent folder of that file;
- whether the shown location is an absolute path or relative path;
- one hidden file/folder, if hidden items are displayed;
- whether you have read/write permission for a file you own.

Then describe it in this form:

```text
File:
File type/extension:
Parent directory:
Absolute path or relative path shown:
Current working directory (if using a notebook/editor):
```

## 17. Solved path-resolution lab

Assume the current working directory is:

```text
C:\QElight\genai-labs\week-01
```

| Expression | Resolved meaning | Why |
|---|---|---|
| `notes\intro.md` | `C:\QElight\genai-labs\week-01\notes\intro.md` | relative path starts at current directory |
| `..\shared\rubric.md` | `C:\QElight\genai-labs\shared\rubric.md` | `..` moves up one folder first |
| `C:\QElight\data\sample.csv` | same exact path | absolute path already starts from drive/root location |
| `outputs` | folder named `outputs` inside `week-01` | a name without a leading root/drive is relative |

### Debugging rule for “file not found”

1. Read the exact path named in the error.
2. Identify whether it is absolute or relative.
3. If relative, identify the current working directory.
4. Combine them mentally or on paper.
5. Check spelling, extension, and whether the intended file is actually there.

Do not solve a path error by copying the same file into random folders. First understand where the program is looking.

### One subtle rule: notebook file location is not always the working directory

A file manager may display `project/notebooks/prototype.ipynb` while the running notebook uses `project/` as its current working directory, or vice versa. Relative paths follow the **running program's current working directory**, not necessarily the folder containing its `.ipynb` or `.py` file. When a real run cannot find `data/sample.csv`, identify the working directory used by that run before rewriting paths.

## 18. Guided file-tree lab — paths that you can actually inspect

This lab is deliberately small and takes place only inside a new disposable folder you control. Use your graphical file manager and plain-text editor. No terminal or Python syntax is required yet. Do not use a real institute or client folder.

### 18.1 Create the practice tree

1. Pick a personal learning location where you are permitted to create files. Make a new folder named `qai-path-lab` and confirm that you are inside it.
2. Inside it, create `notes`, `data`, and `outputs` folders. These actions will be studied formally in QAI.01.03; here they only supply a controlled tree for understanding paths.
3. In a plain-text editor type `Fictional note for path practice.`. In the editor's Save window, **navigate into** your `notes` folder and save with the file name `intro.md`. Confirm the visible name ends in `.md`; if your file manager hides extensions, inspect its file properties rather than guessing.
4. Type `week,attendance` on the first line and `1,20` on the second line of another plain-text file. In the Save window **navigate into** `data` and save with the file name `sample.csv`. This is **fictional sample data**.
5. Open both files once. Do not move or delete anything outside `qai-path-lab`.

**Expected tree:**

```text
qai-path-lab/
├─ notes/
│  └─ intro.md
├─ data/
│  └─ sample.csv
└─ outputs/
```

**Check a common mistake:** some editors add `.txt` automatically when saving text. If you see `intro.md.txt` or `sample.csv.txt`, the actual file name and type are not the intended ones. Inspect the full filename, then correct it *within the practice folder*; changing an extension alone does not transform arbitrary file content, though these two files already contain plain text.

### 18.2 Resolve paths from two working directories

**Starting folder A:** `qai-path-lab/`.

| Expression | Expected location | Exists after §18.1? |
|---|---|---|
| `notes/intro.md` | `qai-path-lab/notes/intro.md` | yes |
| `data/sample.csv` | `qai-path-lab/data/sample.csv` | yes |
| `outputs/summary.txt` | `qai-path-lab/outputs/summary.txt` | no; folder exists, file has not been created |

**Starting folder B:** `qai-path-lab/notes/`.

| Expression | Expected location | Exists after §18.1? |
|---|---|---|
| `intro.md` | `qai-path-lab/notes/intro.md` | yes |
| `data/sample.csv` | `qai-path-lab/notes/data/sample.csv` | no |
| `../data/sample.csv` | `qai-path-lab/data/sample.csv` | yes |

**Interpretation:** The `data/sample.csv` expression did not change, but the starting folder did; that changes its resolved address. In a graphical file manager, move to folder B, go up to its parent, then enter `data` to confirm where the real file lives. On Windows the on-disk path is usually shown with backslashes (`..\data\sample.csv`); on Linux/macOS with forward slashes (`../data/sample.csv`). These are examples of path notation, not commands to run.

### 18.3 Diagnose an observed failure without copying files at random

Imagine your code or editor tries `data/sample.csv` while its working directory is folder B (`qai-path-lab/notes/`). It reports “file not found.”

1. **Prediction:** the program tried `qai-path-lab/notes/data/sample.csv`.
2. **Inspect:** `data` is next to `notes`, not inside it; the predicted location does not exist.
3. **Correction:** either use `../data/sample.csv` while keeping folder B, or start the run from folder A and keep `data/sample.csv`.
4. **Check:** the corrected path points to the one existing file. Record your chosen starting folder and resolved location.

**Variation to solve before reading:** If the current folder is `qai-path-lab/data/`, where does `../notes/intro.md` point, and does it exist? **Answer:** `..` moves to `qai-path-lab/`, then `notes/intro.md`; yes, it exists if §18.1 was completed as specified.

**Permission variation:** If the target file exists but the application says “permission denied,” do not label it “file not found.” Check whose folder it is, whether the application is authorised to read it, and the exact error; use your own practice file if you need a safe reading test. Changing broad system permissions is not the fix for this lesson.

### 18.4 Evidence and move-ahead condition

Keep a small record with (a) your observed practice tree, (b) the full actual names/extensions, (c) the starting folder and resolved destination for each row of §18.2, (d) the missing-file cause and correction, and (e) one permission case explanation. Mark the lab **pending execution** if you only read the expected tables. You are ready for QAI.01.03 when you can locate the same file from two different starting folders and explain a failed path without guessing.

## 19. What to remember

- File = stored information; folder/directory = container that organises files.
- File name identifies a file; extension suggests its format/type.
- Path is a file/folder address; separator differs across operating systems.
- Absolute path begins from root; relative path begins from current working directory.
- Current working directory determines how relative paths are resolved.
- Parent directory is one level up; home directory is the user’s main folder.
- Hidden files often hold configuration; hidden is not the same as secure.
- Permissions control read/write/execute access. Do not change them blindly.
- Good project structure makes code, data, configuration, outputs, and secrets easier to manage safely.

## 20. Next connection

Next: `QAI.01.03 — File-system actions`. You will learn the operations performed on files/folders: create, list, view, copy, move, rename, search, overwrite, append, delete, and restore—along with the safety rules for each.
