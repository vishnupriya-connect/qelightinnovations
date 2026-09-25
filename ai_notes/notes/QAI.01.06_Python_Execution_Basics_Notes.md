# QAI.01.06 — Python Execution Basics

> `QAI.01.05 Program and code basics` → **`QAI.01.06 Python execution basics`** → `QAI.01.07 Values and variables`

## 1. What changes in this lesson

In `QAI.01.05`, you read and saved a Python code file. Now you will find the **Python interpreter**, confirm which installation actually runs, execute a saved `.py` file, use Python's interactive mode, and diagnose three different failure types.

**Outcome:** when somebody says “the program does not work,” you can first determine whether Python itself was found, whether Python understood the file, or whether an instruction failed while running. You will use the disposable `qai-path-lab/code-lab/` folder from the previous lesson. If it is absent, create it before the practice.

## 2. The dependency chain

```text
Your terminal command → Python interpreter → code in a .py file → actions/output → termination
```

| Term | Meaning here | Concrete example |
|---|---|---|
| Python | the programming language whose rules the code follows | `print("Hello")` is Python code |
| Python interpreter | the program that reads and executes Python code | the program launched by `py` or `python3` |
| Python installation | Python interpreter and related files placed on a computer | a working Python 3 installation |
| Python version | the release of the interpreter being used | output beginning with `Python 3` |
| Python script | saved Python instructions meant to be run as a file | `hello_qelight.py` |
| `.py` file | text file with the conventional Python source suffix | `code-lab/hello_qelight.py` |

**Mental model:** a text editor creates the instructions; the interpreter performs them. A terminal launches the interpreter. These are different tools. If Python is not installed, saving `hello.py` still works, but running it through Python cannot work yet.

One computer may have **more than one** Python interpreter. “Python is installed” does not tell you which one a command launches. For reproducible AI work, record its version and path alongside the observed program result.

## 3. Check first, then install only if needed

### 3.1 Windows PowerShell

Open PowerShell. Start by seeing what command is available:

```powershell
Get-Command py, python -ErrorAction SilentlyContinue | Select-Object Name, Source
```

An empty result means neither name was found by this shell. The `py` and `python` commands may point to different launcher arrangements, so test the one you intend to use. The [official Windows setup guide](https://docs.python.org/3/using/windows.html) explains the Python install manager and earlier launcher arrangements. Commands and availability can vary.

```powershell
py --version
py -c "import sys; print(sys.executable)"
```

**Expected:** a line beginning with `Python 3` and then the absolute path to the interpreter executable. `-c` asks Python to run the short code that follows instead of reading a script file. `import sys` makes Python's own runtime information available; `sys.executable` identifies the running interpreter. You do not need to master imports yet.

If `py` is unavailable but `python` works, substitute `python` in *both* commands and all subsequent Windows examples. On the current Python install manager, the first attempt to launch Python when no runtime is installed may offer or start installing a runtime; review the prompt and its source before continuing.

**Inspect path:** compare the displayed executable location with what you intended to use. A command that starts a store alias, a different Python installation, or a project environment can lead to different results even if it prints `Python 3`.

### 3.2 macOS/Linux Bash or Zsh

```bash
command -v python3
python3 --version
python3 -c 'import sys; print(sys.executable)'
```

**Expected:** `command -v` names an available command path; Python reports a version beginning with `Python 3`; the final command prints the actual interpreter's absolute path. If `python3` is absent, follow the installation instructions appropriate to your operating system; do not assume the unversioned `python` command points to Python 3. The [Python interpreter guide](https://docs.python.org/3/tutorial/interpreter.html) documents launching the interpreter and running files.

### 3.3 If Python 3 is missing

- On **Windows or macOS**, use the official [Python downloads page](https://www.python.org/downloads/) and the [official Windows setup guide](https://docs.python.org/3/using/windows.html) where relevant. Choose a supported Python 3 release offered for your system. The Windows guide describes the current install manager and how to start Python after installation.
- On **Linux**, use the supported package method for your particular distribution, or its official instructions. Package commands differ by distribution; confirm the resulting `python3 --version` and `sys.executable` rather than assuming success.
- If you use a **managed classroom or office computer** where installation is blocked, run the read-and-trace steps now; arrange an approved Python environment with the trainer before attempting installation.

After installing, open a **new terminal** and rerun the checks above. Do not modify operating system paths at random to make a command appear. The path, version, and working shell are part of your `python_readiness.md` record in §11.

## 4. Interactive interpreter: run one expression at a time

**Interactive interpreter:** Python session that accepts a piece of code, executes it, displays the result when appropriate, then waits for the next piece. Start it in your terminal:

```powershell
py
```

or:

```bash
python3
```

You should see a Python banner and the `>>>` prompt. The terminal shell prompt and Python's `>>>` prompt are different: at `>>>`, you type Python **code**, not shell commands such as `cd` or `Get-ChildItem`.

```python
>>> 2 + 3
5
>>> print("AI practice")
AI practice
>>> exit()
```

**Type only the expressions or statements following each `>>>`.** The `5` and `AI practice` lines are expected results, not commands to type. `2 + 3` is an expression, so interactive Python shows its value. `print(...)` displays the text through a statement. `exit()` closes this interactive session and returns control to your terminal shell; it does not delete any file.

If you see `...` instead of a fresh `>>>`, Python is waiting for a continuation, often because a parenthesis or quote was left open. Complete it or cancel the unfinished entry (Ctrl+C), then retry a simple expression.

## 5. Execute a saved Python script

First create `hello_qelight.py` inside `qai-path-lab/code-lab/` using a **plain-text** or code editor. Save these exact lines:

```python
# Fictional learner example.
print("QElight course assistant")
print("Ready for AI practice")
```

Open a terminal and change into the **real absolute path** to your `code-lab` folder. Example paths below are placeholders, not locations guaranteed to exist:

```powershell
# Windows PowerShell: replace example path with your actual code-lab location
Set-Location -LiteralPath 'C:\Users\Priya\qai-path-lab\code-lab'
Get-Location
Get-ChildItem -Name
py .\hello_qelight.py
```

```bash
# macOS/Linux: replace example path with your actual code-lab location
cd '/home/learner/qai-path-lab/code-lab'
pwd
ls
python3 hello_qelight.py
```

**Expected:** before running, the listing includes `hello_qelight.py`. Running it prints:

```text
QElight course assistant
Ready for AI practice
```

The **script path** is the argument supplied to Python. Python reads that file and executes it. The command from the wrong working directory cannot find the same relative script path. You can also pass the **absolute file path** to the interpreter from a different directory.

**Controlled change:** edit only `Ready for AI practice` to `Ready for GenAI practice`, save, and run again. The second line should change; the first should stay. If the old line remains, inspect the editor's save state and the exact file path passed to the interpreter.

## 6. Three failure locations: diagnose in order

Use this sequence to decide where to investigate:

```text
Could the shell start Python?
  no → interpreter/command problem
  yes → Could Python read the file's syntax?
          no → syntax/indentation problem
          yes → Did an instruction fail while running?
                  yes → runtime error
                  no → normal completion or intended early termination
```

### 6.1 Interpreter or command problem

Try running `py --version` on Windows or `python3 --version` on macOS/Linux. If the shell says the command is **not found/not recognized**, it has not launched the intended Python interpreter. Inspect command spelling, operating system, and installation; install/configure Python through an appropriate official route before debugging your script.

If Python prints a working version but says it **cannot open** `hello_qelight.py`, then Python started successfully: inspect your current directory, file name, extension, and path. A missing **script** is different from a missing **interpreter**.

### 6.2 Syntax error: Python cannot read the instruction

In a *new, disposable* file named `broken_syntax.py`, deliberately save:

```python
print("Before error")
print("Second line"
```

Run `py .\broken_syntax.py` or `python3 broken_syntax.py`. **Expected:** a `SyntaxError` mentioning the line with the unclosed parenthesis; `Before error` does **not** appear. Python must parse this file before executing its statements. The wording of the error can vary by Python version. Correct the file by adding `)` to the end of the second line and rerun; both printed lines should then appear.

An indentation error is also a failure to form a valid Python code block. The indented `if` demonstration in `QAI.01.05` shows a safe example.

### 6.3 Runtime error: Python starts, then an instruction fails

In another *new, disposable* file named `broken_runtime.py`, save:

```python
print("Before calculation")
print(1 / 0)
print("After calculation")
```

Run it. **Expected:** `Before calculation` appears, then a `ZeroDivisionError` and a **traceback**. A traceback names where an error happened, including the file and line number. `After calculation` does **not** appear. Python could read the syntax and began executing; the division itself failed.

**Repair:** change `print(1 / 0)` to `print(1 / 2)`, save, rerun. Expected lines: `Before calculation`, `0.5`, `After calculation`. Do not fix a runtime failure by reinstalling Python when the traceback already identifies the failing instruction.

### 6.4 Read the error report precisely

| Observation | Meaning | First next action |
|---|---|---|
| command name not recognized | shell did not find a suitable Python launcher | verify installed command and operating system |
| `can't open file` | Python launched, but script path failed | check folder, exact name, `.py` extension |
| `SyntaxError` / `IndentationError` | file cannot be read as valid code | inspect reported line and neighbouring punctuation/indentation |
| `ZeroDivisionError` after first line printed | execution started, then failed | inspect arithmetic on reported line |
| correct output but wrong version/path | another interpreter was launched | inspect `sys.executable`, version, and launch command |

**Debug record example:** “Expected three lines; saw the first line plus `ZeroDivisionError` from line 2; corrected divisor from 0 to 2; reran and saw all three lines.” This is more useful than “Python broken.”

## 7. Normal completion and intentional termination

**Program termination** means the current program stops running and returns control to the caller. A script normally stops after its last statement completes. A program can also stop because an unhandled error occurred or because it deliberately requested an early exit.

To see both normal and intentional termination, create a new disposable `finish_status.py`:

```python
import sys

print("Finished the practice step")
sys.exit(0)
print("Never reached")
```

`sys` is a Python module that exposes interpreter functions. `sys.exit(0)` requests termination with status **0**; the final line is not reached. Run the file, then inspect its status **immediately**, before another command:

```powershell
py .\finish_status.py
$LASTEXITCODE
```

```bash
python3 finish_status.py
echo $?
```

**Expected:** `Finished the practice step`, then exit status `0`. Change `sys.exit(0)` to `sys.exit(3)` and rerun. The displayed sentence is still the same, but status becomes `3`. This demonstrates why visible text alone cannot prove success. `0` is the conventional success status; nonzero values indicate other results, and their exact meaning depends on the program. An unhandled error also ends a program unsuccessfully but produces a traceback; the controlled `sys.exit(3)` does not need a traceback.

`$LASTEXITCODE` in PowerShell tracks the latest **external program**; PowerShell's built-in commands have their own success reporting. In Bash/Zsh, `$?` changes after each subsequent command. This is why the status command appears immediately after Python.

## 8. Reuse the previous lesson's code files

Now revisit the `QAI.01.05` files inside the same `code-lab` folder:

| File | Command from `code-lab` on Windows | What to expect |
|---|---|---|
| `hello.py` | `py .\hello.py` | welcome and topic lines |
| `course_card.py` | `py .\course_card.py` | waits for a fictional name; prints its course card |
| `topic_arg.py` | `py .\topic_arg.py GenAI` | prints `Today: GenAI` |

On macOS/Linux substitute `python3 filename.py` and use `/` in paths. Enter a fictional name for interactive input. The `GenAI` value after the last script's filename is a **program argument**; without it that demonstration produces the `IndexError` explained in `QAI.01.05`.

**Interpretation:** a Python interactive session, a saved `.py` script, keyboard input after a script starts, and an argument in the launching command are related but distinct ways of using the same interpreter.

## 9. Independent micro-lab with worked solution

**Task:** without changing any earlier files, create `readiness_step.py` in `code-lab`. It must print `Python ready`, then `Step 2`. Run it, record your interpreter version and path, deliberately introduce an invalid missing parenthesis into a *copy* named `readiness_broken.py`, identify the error type, then repair the copy. Keep the original intact.

**Worked source for the original:**

```python
print("Python ready")
print("Step 2")
```

**Worked action sequence, Windows:**

```powershell
# From code-lab; confirm the new names do not exist before creating them
Get-Location
Get-ChildItem -Name
py --version
py -c "import sys; print(sys.executable)"
py .\readiness_step.py
Copy-Item -LiteralPath .\readiness_step.py -Destination .\readiness_broken.py
```

Open **only** `readiness_broken.py` in the editor; remove the final `)` from its second line; save. Run `py .\readiness_broken.py`. **Expected:** `SyntaxError`; the first print in that file does not run. Restore the `)` and rerun. **Expected:** both lines display; `readiness_step.py` has remained unchanged throughout. On macOS/Linux use `python3` instead of `py`, `cp readiness_step.py readiness_broken.py` for the copy, and `pwd`/`ls` for navigation/listing.

**Result record template, with a solved example of observations:**

| Check | Example observation to record |
|---|---|
| launch command | `py .\readiness_step.py` on Windows |
| Python version | the actual `Python 3.x.y` printed on *your* machine |
| interpreter path | the actual absolute path printed by `sys.executable` |
| working folder | actual path ending in `code-lab` |
| good script output | `Python ready`, followed by `Step 2` |
| bad copy | `SyntaxError`, second line with a missing `)` |
| after repair | both lines display; original copy still intact |

Write your **actual** version and path. `3.x.y` is a placeholder, not a claim about the software installed on your computer.

## 10. Troubleshooting without losing the thread

| Symptom | Test | Safe correction |
|---|---|---|
| `py` missing on Windows | `Get-Command py, python -ErrorAction SilentlyContinue` | use working `python` or follow official installation guide |
| `python3` missing on macOS/Linux | `command -v python3` | follow your OS's supported installation method |
| script missing | print working directory and list files | change to `code-lab` or use exact absolute script path |
| `hello.py.txt` exists instead of `.py` | show full file extensions in explorer | rename this disposable file to `.py` |
| edited code seems ignored | compare editor's open path with executed script path | save and run the same file |
| Python version/path unexpected | inspect `--version` and `sys.executable` using the same command | choose and consistently use the intended interpreter |
| `>>>` appears while you try shell commands | you are inside interactive Python | type `exit()` to return to shell |
| `...` appears after unfinished input | interpreter awaits continuation | close the quote/parenthesis or use Ctrl+C |
| syntax error before any prints | source could not be parsed | check punctuation and indentation near reported line |
| first print works, then traceback | execution began and later failed | inspect final traceback line and its indicated source line |

**Boundary:** project-specific virtual environments and package installation come later in the Python working environment sequence. At this node, be able to identify the interpreter/version/path and execute a standard-library-only script without modifying system settings blindly.

## 11. Keep one reproducible readiness record

Create `python_readiness.md` in `code-lab` and fill in the **observed**, not imagined, results:

```md
# Python readiness

- System and shell: [for example, Windows PowerShell]
- Working folder: [actual absolute path]
- Launch command: [py or python or python3]
- Python version: [actual output]
- Interpreter path: [actual sys.executable output]
- Interactive check: [2 + 3 -> 5, if performed]
- Script: hello_qelight.py
- Script result: [the two displayed lines]
- Syntax failure: [reported error, source line, fix]
- Runtime failure: [reported error, source line, fix]
- Status check: [finish_status.py exit 0 and exit 3, if performed]
```

The exact local version and path will vary. The finished file and small scripts are your **evidence** that you can repeat the steps. If the interpreter is unavailable on a managed device, record that obstacle and complete the execution evidence after an approved environment is provided.

## 12. What to remember

- Source text in `.py` needs an interpreter to run; the editor and terminal have different jobs.
- Check version **and** actual interpreter path, particularly when multiple Python installations exist.
- Interactive `>>>` accepts Python code; a terminal shell accepts launch/navigation commands.
- The current directory determines which relative script path Python receives.
- “Python command not found,” “script cannot be opened,” `SyntaxError`, and a runtime exception identify different failure points.
- A script can end normally, through an error, or by an explicit exit; check result and exit status when needed.
- Debug using the observed command, path, line number, full error, one correction, and a rerun.

## 13. Next connection

`QAI.01.07 — Values and variables`: the small examples used fixed text, input, and named values. Next you will learn exactly how Python stores, names, evaluates, and changes those values.
