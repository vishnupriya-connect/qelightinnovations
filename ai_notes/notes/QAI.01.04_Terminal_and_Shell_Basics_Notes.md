# QAI.01.04 — Terminal and Shell Basics

> **Position in the QElight AI path**  
> `QAI.01.03 File-system actions` → **`QAI.01.04 Terminal and shell basics`** → `QAI.01.05 Program and code basics`

## 1. Why use a terminal?

A graphical interface lets you click folders, buttons, and windows. A terminal lets you give typed instructions to the computer.

```text
You type a command
        ↓
Shell interprets the command
        ↓
Operating system performs the requested action
        ↓
Terminal shows output, error, and result status
```

The terminal is important because Python, Git, package installation, data processing, application startup, cloud systems, and deployment all use command-line workflows.

## 2. Terminal, shell, and command line

### Terminal

- **Terminal:** an application/window where you type text commands and see their results.
- On Windows, examples include Windows Terminal and PowerShell windows.
- On Linux/macOS, examples include Terminal applications.

### Shell

- **Shell:** program inside the terminal that reads commands and asks the operating system to perform them.
- Common shells include PowerShell, Command Prompt, Bash, and Zsh.

### Command line

- **Command line:** text-based way of interacting with a computer by typing commands.

| Term | Main meaning |
|---|---|
| terminal | the interface/window |
| shell | interpreter that understands commands |
| command line | style of interaction using typed commands |

### Simple analogy

```text
Restaurant counter = terminal
Waiter who understands the order = shell
Spoken/written order style = command line
```

## 3. Prompt

- **Prompt:** text shown by a shell to indicate that it is ready for a command.
- It often includes the current folder or other context.

Example shape:

```text
PS C:\Users\Priya\qelight>
```

Do not type the prompt itself. Type after it.

## 4. Command, command name, argument, option, and flag

### Command

- **Command:** instruction typed into a shell.

### Command name

- **Command name:** the main action/program to run.

### Argument

- **Argument:** value supplied to a command, commonly a file name, folder path, or text value.

### Option

- **Option:** setting that changes how a command behaves.

### Flag

- **Flag:** option that turns a behaviour on/off or requests a specific mode.

### General shape

```text
command-name   argument   option/flag
```

### Example idea

```text
Get-ChildItem  data       -Recurse
```

| Part | Meaning |
|---|---|
| `Get-ChildItem` | command name: list items |
| `data` | argument: folder to inspect |
| `-Recurse` | option/flag: include nested folders |

Command syntax differs between shells. Always read the command help/documentation before using unfamiliar options, especially options that write, overwrite, or delete.

## 5. Command input and command output

- **Command input:** information supplied to a command.
- **Command output:** information produced by a command.

### Example

```text
Command: list files in the data folder
Input:   path to the data folder
Output:  names/details of files and subfolders
```

Command output can be text, tables, file content, a program result, an error message, or a new file created by the command.

## 6. Standard input, standard output, and standard error

Programs commonly use three basic communication channels.

| Channel | Meaning | Typical use |
|---|---|---|
| standard input (`stdin`) | input supplied to a program | user text, piped data, file content redirected to program |
| standard output (`stdout`) | normal result produced by program | list of files, calculated value, generated report |
| standard error (`stderr`) | error/diagnostic message | missing file, invalid command, permission error |

### Important distinction

An error message is not always “bad output.” It is a separate channel that helps you understand what failed.

Later, scripts and applications may write normal results to output files while recording errors in logs.

## 7. Exit status

- **Exit status:** small result code returned when a command/program finishes.
- In many environments, `0` means successful completion; a non-zero value usually indicates some failure/exception condition.

### Why it matters

Visible output can look normal while a later step failed. Automation/CI systems use exit status to decide whether to continue, stop, retry, or report failure.

For now, remember:

```text
Command finished ≠ command succeeded.
Check output/error and, when needed, exit status.
```

## 8. Command history

- **Command history:** record of commands previously typed in a shell session or saved history.

### Useful habits

- use arrow keys to review/reuse recent commands;
- inspect a previous command before running it again;
- do not assume an old command is safe in the current folder;
- do not copy commands containing secrets into notes/screenshots/history shared with others.

History saves time, but understanding comes before repetition.

## 9. Current directory and change directory

- **Current directory:** folder where the shell/program is currently operating.
- **Change directory:** switch the current directory to another folder.

### Core principle

```text
Relative paths are interpreted from the current directory.
```

### Windows PowerShell: safe orientation commands

```powershell
# Show current directory
Get-Location

# Change into a project folder
Set-Location C:\Users\Priya\qelight

# Short alias commonly used in PowerShell
cd C:\Users\Priya\qelight
```

Use your own real project path. Do not copy the example path as though it must exist on your computer.

### Cross-platform idea

| Goal | PowerShell | Bash/Zsh (Linux/macOS) |
|---|---|---|
| show current directory | `Get-Location` or `pwd` | `pwd` |
| change directory | `Set-Location path` or `cd path` | `cd path` |

## 10. List files

- **List files:** show items inside the current or specified folder.

### PowerShell

```powershell
# List current folder contents
Get-ChildItem

# Common short alias
ls

# List a specific folder
Get-ChildItem data
```

### Use before action

List a folder before loading a file, moving output, or running any command that changes files. It helps confirm the correct target.

## 11. Create directory

- **Create directory:** make a new folder from the command line.

### PowerShell

```powershell
# Create one folder in the current directory if it does not already exist
New-Item -ItemType Directory -Name outputs
```

Expected result: an `outputs` folder appears in the current directory.

Before creating a folder, confirm the current directory so it is created in the intended project, not somewhere else.

## 12. View content

- **View command:** display content without intentionally editing it.

### PowerShell

```powershell
# Show content of a text/Markdown/CSV-like file
Get-Content README.md
```

Use this to inspect a README, small configuration file, log, or text output. Do not print files containing real secrets/credentials into a shared terminal, recording, screenshot, or chat.

## 13. Search

- **Search command:** find file names or text inside files.

### PowerShell: search text in files

```powershell
# Find the text "old_data.csv" in Python files below src
Select-String -Path .\src\*.py -Pattern "old_data.csv"
```

### Why this matters

After renaming or moving a dataset/configuration file, search for its old path in code and notes. This prevents hidden broken references.

## 14. Copy and move

The underlying actions were explained in `QAI.01.03`. The terminal makes them repeatable.

### PowerShell: copy a file

```powershell
Copy-Item data\raw\notes.csv data\backup\notes_before_cleaning.csv
```

### PowerShell: move a file

```powershell
Move-Item downloads\notes.csv data\raw\notes.csv
```

### Safety rule

Before copying/moving:

1. confirm current directory;
2. list source and destination folders;
3. check whether destination already contains the same name;
4. know whether the command may overwrite/replace an item;
5. verify result after action.

Avoid deletion commands until you understand paths, options, and recovery.

## 15. Clear terminal

- **Clear terminal:** remove visible screen output to make the current session easier to read.
- It does not delete files or undo commands.

### PowerShell

```powershell
Clear-Host
```

Common short alias:

```powershell
cls
```

## 16. Guided PowerShell practice: an inspectable AI project folder

In the previous lesson you created the disposable `qai-path-lab` folder using a file explorer. Open that folder in the explorer and copy its **full path**. Type each line separately, check the expected result, and only then run the next. The example location below is illustrative: replace it with the actual path on *your* computer. Use PowerShell, not Command Prompt. If `terminal-lab` already exists, inspect it and choose another new folder name consistently throughout this lab.

### 16.1 Orient, enter, and create

```powershell
Get-Location
Set-Location -LiteralPath 'C:\Users\Priya\qai-path-lab'
Get-Location
Get-ChildItem
New-Item -ItemType Directory -Path .\terminal-lab
Set-Location -LiteralPath .\terminal-lab
Get-Location
Get-ChildItem
New-Item -ItemType Directory -Path .\notes
New-Item -ItemType Directory -Path .\archive
Get-ChildItem
```

**Expected:** your location now ends in `qai-path-lab\terminal-lab`; the first listing inside it is empty; the last listing shows two folders, `notes` and `archive`. `Set-Location` changes your shell's current directory, not the location of a file on disk. `.` denotes the current directory. If the example absolute path fails, stop and use the real folder path copied from the explorer; do not proceed from the wrong directory.

### 16.2 Write and view a disposable file

```powershell
Set-Content -LiteralPath .\notes\intro.txt -Value 'Course assistant: fictional note.'
Get-ChildItem -LiteralPath .\notes
Get-Content -LiteralPath .\notes\intro.txt
```

**Expected:** `notes/intro.txt` exists and contains one line, `Course assistant: fictional note.` `Set-Content` creates or **replaces** content at the named path; use it here only because `intro.txt` is new and disposable. `Get-Content` reads text without editing it. Do not display real credentials on a shared screen.

### 16.3 Copy, append, and move: compare the original and copy

```powershell
Copy-Item -LiteralPath .\notes\intro.txt -Destination .\archive\intro_copy.txt
Get-Content -LiteralPath .\archive\intro_copy.txt
Add-Content -LiteralPath .\archive\intro_copy.txt -Value 'Checked in terminal lab.'
Get-Content -LiteralPath .\notes\intro.txt
Get-Content -LiteralPath .\archive\intro_copy.txt
```

**Expected:** the source has one line; the copy has the original line followed by `Checked in terminal lab.` `Add-Content` appended only to the copy.

```powershell
New-Item -ItemType Directory -Path .\archive\saved
Move-Item -LiteralPath .\archive\intro_copy.txt -Destination .\archive\saved\intro_copy.txt
Get-ChildItem -LiteralPath .\archive
Get-ChildItem -LiteralPath .\archive\saved
Get-Content -LiteralPath .\archive\saved\intro_copy.txt
```

**Expected:** `archive` contains a `saved` folder; `saved` contains the two-line copy. The former `archive/intro_copy.txt` path is absent; `notes/intro.txt` remains. If a destination exists, inspect it first; do not force a replacement just to finish the lab.

### 16.4 Search filenames, then file contents

```powershell
Get-ChildItem -Path . -Recurse -File -Filter '*.txt'
Select-String -Path .\notes\*.txt,.\archive\saved\*.txt -Pattern 'Course assistant' -SimpleMatch
```

**Expected:** the first command lists two text file paths; the second finds the phrase inside **both** files. `-Recurse` means include nested folders; `-Filter` matches file **names**, while `Select-String` matches **content**. `-SimpleMatch` treats the pattern as literal text.

### 16.5 Help, history, error, and screen clearing

```powershell
Get-Help Get-ChildItem -Examples
Get-History
Get-Content -LiteralPath .\notes\missing.txt
$?
Get-Location
Get-ChildItem -LiteralPath .\notes
Get-Content -LiteralPath .\notes\intro.txt
Clear-Host
Get-ChildItem -Path . -Recurse
```

**Expected:** help shows usage examples; history shows recent commands for this session (details vary by shell). The deliberately missing file produces an error; `$?` checked **immediately** afterward normally shows `False`. The subsequent listing shows the real file name and the corrected `Get-Content` prints its line. After `Clear-Host`, earlier displayed text disappears, but both files and the current directory remain. Review commands recalled from history before pressing Enter; arguments can expose secrets in terminal history.

**Final tree to verify in the file explorer too:**

```text
qai-path-lab/
└─ terminal-lab/
   ├─ notes/
   │  └─ intro.txt                  one line
   └─ archive/
      └─ saved/
         └─ intro_copy.txt         two lines
```

## 17. Common failures and debugging order

| Symptom | Likely cause | First check |
|---|---|---|
| “path not found” | incorrect path/current directory | `Get-Location`; `Get-ChildItem` |
| “access denied” | insufficient permission or locked file | ownership/permissions; close competing application |
| command not recognised | wrong shell, missing program, spelling issue | command name, installation, shell documentation |
| unexpected file change | wrong source/destination/current directory | stop; list/inspect paths; restore from backup if needed |
| output is confusing | command uses options/aliases not understood | read help/docs; simplify command |

## 18. Core operational terminal skills

### Help, quoting, and safe selection

```powershell
# Read built-in help before using an unfamiliar command
Get-Help Copy-Item -Examples

# Quotes preserve a path containing spaces as one argument
Set-Location "C:\QElight\GenAI Labs"

# Inspect only Markdown files in the current folder
Get-ChildItem -Filter *.md
```

- **Wildcard:** a pattern such as `*.md`, meaning “all names ending in `.md`”.
- A wildcard can match more files than expected. List its matches before using it with any modifying command.
- Quoting is not decoration: without quotes, spaces can split one path into several arguments.

### Pipeline, redirection, and environment inspection

```powershell
# Pipeline: send output from the left command to the right command
Get-ChildItem | Where-Object { $_.Extension -eq ".md" }

# Save normal output; do this only inside a known safe project folder
Get-ChildItem -Name | Out-File -Encoding utf8 file-list.txt

# Inspect the value of a non-secret environment variable
$env:USERNAME

# Inspect the name of a variable without revealing secret values
Get-ChildItem Env: | Where-Object { $_.Name -eq "MODEL_PROVIDER_API_KEY" }
```

- **Pipeline:** connection where one command's output becomes the next command's input.
- **Redirection/output file:** save displayed result to a file. `Out-File` overwrites the named file; use a deliberately new output name unless replacement is intended.
- **Environment variable:** named setting supplied to a process; do not display or copy real secret values.

### Exit status and error diagnosis

For an **external program**, check `$LASTEXITCODE` *immediately* after the program. A value of `0` commonly signals success; a nonzero value indicates another outcome. PowerShell cmdlets are different: `$?` tells whether the immediately preceding PowerShell command succeeded; also read its visible error and verify the result. `$LASTEXITCODE` can retain an earlier external program's code after a PowerShell cmdlet, so it cannot verify that later cmdlet.

On Windows, this deliberate status demonstration changes no files:

```powershell
cmd /c exit 0
$LASTEXITCODE       # expected: 0
cmd /c exit 7
$LASTEXITCODE       # expected: 7, deliberately nonzero
```

For Bash/Zsh, `true; echo $?` produces `0` and `false; echo $?` produces a nonzero value. Each new command changes `$?`, so inspect it immediately.

### Bash/Zsh working equivalence

| Goal | PowerShell | Bash/Zsh |
|---|---|---|
| help/examples | `Get-Help Copy-Item -Examples` | `man cp` or `cp --help` |
| list Markdown files | `Get-ChildItem -Filter *.md` | `ls *.md` |
| set variable for current shell | `$name = "value"` | `name="value"` |
| read environment variable | `$env:NAME` | `echo "$NAME"` |
| save output to file | `command | Out-File file.txt` | `command > file.txt` |
| append output | `command | Add-Content file.txt` | `command >> file.txt` |
| last external exit code | `$LASTEXITCODE` | `echo $?` |

Learn one shell deeply: **PowerShell first** on Windows. Read Bash/Zsh commands well enough to adapt AI documentation. In the shell you actually use, read the next lab as complete practice, not merely a translation table. `Get-ChildItem | Select-Object Name, Length` is a PowerShell **pipeline**: the `|` passes result objects, each with named fields such as file name and byte length. In Bash/Zsh many pipelines pass text. Do not assume that commands sharing an alias, such as `ls`, share all behaviour.

### Bash/Zsh complete equivalent of the PowerShell lab

Use this sequence in Bash or Zsh on macOS/Linux. Begin from an existing disposable `qai-path-lab` folder; replace the example absolute path with its real path. If `terminal-lab` already exists, choose another new name consistently. Run **one line at a time** and compare the two-file final tree with §16.

```bash
pwd
cd '/home/learner/qai-path-lab'
pwd
ls
mkdir terminal-lab
cd terminal-lab
mkdir notes archive
pwd
ls
printf '%s\n' 'Course assistant: fictional note.' > notes/intro.txt
cat notes/intro.txt
cp notes/intro.txt archive/intro_copy.txt
printf '%s\n' 'Checked in terminal lab.' >> archive/intro_copy.txt
cat notes/intro.txt
cat archive/intro_copy.txt
mkdir archive/saved
mv archive/intro_copy.txt archive/saved/intro_copy.txt
find . -type f -name '*.txt'
grep -n -F 'Course assistant' notes/intro.txt archive/saved/intro_copy.txt
```

**Expected:** two `.txt` files, with one line in the original and two in the moved copy; the text search matches both. `printf` produces text. `>` writes or **replaces** its target; `>>` **appends**. Use `>` here only for the known new disposable file. `find` searches paths by name; `grep -F` searches file contents for a literal phrase; `-n` includes the line number.

Diagnose a harmless missing-file error:

```bash
cat notes/missing.txt
echo $?                   # immediately after failed cat: nonzero
pwd
ls notes
cat notes/intro.txt
```

The folder listing identifies the real name. `clear` clears the display without changing files. `man cp` shows local documentation on systems with manual pages. If an expected command or help system is unavailable, record which shell and system you opened and inspect local help rather than guessing a substitute.

### Independent practice, followed by a complete solution

**Task:** while inside `terminal-lab`, create `drafts/`; copy `notes/intro.txt` to `drafts/lesson.txt`; append `Draft checked.` to that copy; search for `Draft checked.` in the draft; verify that the original still has one line. Inspect first if these destination paths already exist. Do not overwrite an existing practice result.

**PowerShell solution:**

```powershell
Get-Location
Get-ChildItem -LiteralPath .\notes
New-Item -ItemType Directory -Path .\drafts
Copy-Item -LiteralPath .\notes\intro.txt -Destination .\drafts\lesson.txt
Add-Content -LiteralPath .\drafts\lesson.txt -Value 'Draft checked.'
Get-Content -LiteralPath .\notes\intro.txt
Get-Content -LiteralPath .\drafts\lesson.txt
Select-String -Path .\drafts\lesson.txt -Pattern 'Draft checked.' -SimpleMatch
```

**Bash/Zsh solution:**

```bash
pwd
ls notes
mkdir drafts
cp notes/intro.txt drafts/lesson.txt
printf '%s\n' 'Draft checked.' >> drafts/lesson.txt
cat notes/intro.txt
cat drafts/lesson.txt
grep -n -F 'Draft checked.' drafts/lesson.txt
```

**Expected answer:** the source contains only `Course assistant: fictional note.`; the draft contains that line followed by `Draft checked.`; the search reports the draft's second line. The copy made a separate file; append changed only that copy. After this task, the practice subtree contains **three** text files.

**Evidence record:** note your current directory, a source and destination listing, the exact search output, and one error plus its repair. If a result differs, stop at the first unexpected command, record the complete error and current directory, then inspect source and destination before retrying.

## 19. What to remember

- Terminal is the interface; shell interprets commands; command line is the typed interaction style.
- A command has a name, optional arguments, and options/flags.
- `stdin` supplies input; `stdout` shows normal output; `stderr` shows errors/diagnostics.
- Exit status helps automation decide whether a command succeeded.
- Current directory controls relative paths; always confirm it before an action.
- List and inspect before copy/move/create; verify after action.
- Clear terminal affects display only, not files.
- Never run unfamiliar, destructive, or secret-bearing commands without understanding target, effect, and recovery path.

## 20. Next connection

Next: `QAI.01.05 — Program and code basics`. You will move from giving existing commands to writing your own instructions as source code.
