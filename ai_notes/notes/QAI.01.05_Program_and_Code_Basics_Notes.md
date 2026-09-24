# QAI.01.05 — Program and Code Basics

> `QAI.01.04 Terminal and shell basics` → **`QAI.01.05 Program and code basics`** → `QAI.01.06 Python execution basics`

## 1. Destination of this lesson

A course assistant might greet a learner, ask for a topic, and display what to study. You could do that manually each time. A **program** records instructions so a computer can repeat the work. In this lesson, you will read a tiny program, predict its result, run it if Python is available, change one instruction, and correct two common mistakes.

You need only the file, folder, and terminal skills from `QAI.01.02–QAI.01.04`. Python installation and interpreter setup have their own lesson in `QAI.01.06`. If Python is not yet installed, perform the read-and-predict exercises now and run the exact files after that lesson.

**Safe practice area:** make a new `qai-path-lab/code-lab/` folder. Work only there, using made-up learner names. Never run a downloaded or AI-generated program before reading what it does with your files, network, and credentials.

## 2. From idea to observable result

```text
Human goal
  → instructions written as source code
  → saved code file
  → program runs
  → observable result or error
  → inspect and correct
```

| Term | Precise meaning | In our example |
|---|---|---|
| program | instructions intended to perform a task | greet a learner and display a topic |
| source code | human-readable instructions in a programming language | `print("Today: AI")` |
| code file | stored file containing source code | `hello.py` |
| run a program | ask a suitable program to execute the source instructions | run `hello.py` through Python |
| program output | information produced while the program runs | `Today: AI` on the screen |
| error | indication that something prevented intended work | incorrect spelling of `print` |

**Mental model:** a recipe is a written plan; preparing it is an action. A code file is a written plan; running it is an action. Editing the recipe does not prepare food, and merely saving a code file does not run it.

**Important distinction:** what a program *prints* is not the only possible result. A program could also create a file or change data. Always inspect the code and its actual effects.

## 3. Tools for writing code

- **Text editor:** application that edits plain text. Plain text is text without hidden document styling. A code file is plain text.
- **Code editor:** text editor with programming conveniences such as line numbers, syntax colouring, and indentation support.
- **Integrated development environment (IDE):** an application that brings code editing, running, and debugging tools together. **Debugging** means finding why actual behaviour differs from intended behaviour.

You can write this exercise using a basic text editor or a code editor such as VS Code. Save the file with the exact name `hello.py` inside `code-lab`. The `.py` ending identifies a Python source file. On Windows, make sure it did not become `hello.py.txt`; show file-name extensions in the file explorer if needed.

| Action | What you should observe |
|---|---|
| type instructions into a new editor tab | text exists in the editor, perhaps not yet as a file |
| save as `code-lab/hello.py` | file appears in that exact folder |
| close and reopen it | stored source code reappears |
| run it | program output or an error appears |

The last action requires a Python installation; the previous three do not. `QAI.01.06` teaches that installation and how to locate the interpreter.

## 4. The smallest useful program

Create `hello.py` with exactly these two lines:

```python
print("Welcome to the course assistant")
print("Today: AI")
```

Read before running:

- `print` asks Python to display a value.
- `(` and `)` surround the value given to `print`.
- Quotation marks mark the start and end of each piece of text.
- Each line is a **statement**: an instruction to perform an action.
- Python usually runs these statements from top to bottom.

**Prediction:** which line appears first? The welcome line, because its `print` statement comes first.

**Expected screen output:**

```text
Welcome to the course assistant
Today: AI
```

The code includes `print` and quotation marks; the output contains only the displayed text. **Source code and program output are different things.**

### Run it if Python is already installed

Open the terminal in the `code-lab` folder. First list the folder and check that `hello.py` exists. Then use the command appropriate for your system:

```powershell
# Windows PowerShell; from code-lab/
Get-Location
Get-ChildItem
py .\hello.py
```

```bash
# macOS/Linux Bash or Zsh; from code-lab/
pwd
ls
python3 hello.py
```

If `py` or `python3` is not found, or the output does not match, record the exact command and error. `QAI.01.06` covers finding and configuring the Python interpreter. Do not install an unknown tool just because a dialog offers one.

### Change one instruction; predict first

Replace only `AI` with `GenAI`, save, and run the **same saved file** again. Expected second line: `Today: GenAI`. If it still says `AI`, check whether you saved the edit and whether the terminal runs the same `hello.py` you opened.

## 5. Syntax, statement, and expression

**Syntax** means the rules for forming instructions that a programming language can read. Here are two deliberate mistakes:

```python
print("Welcome"
```

The closing `)` is missing. Python cannot read this correctly; it reports a **syntax error**. Compare punctuation with the working `print("Welcome")` and add the missing character.

```python
prnit("Welcome")
```

The word is misspelled. The punctuation is valid, but when Python runs it, it cannot find a known name `prnit`; it typically reports a **NameError**. Correct the name to `print`. A syntax error and a name error have different causes.

**Expression** means a piece of code that produces a value. The expression `2 + 3` produces `5`:

```python
print(2 + 3)
```

Here `2 + 3` is an expression; the whole `print(2 + 3)` line is a statement that displays the expression's result. Expected output: `5`. If you write `print("2 + 3")`, the characters inside quotes are ordinary text, so expected output is `2 + 3`. This difference matters whenever an AI application combines fixed text with computed results.

**Worked trace:**

| Code | First obtain a value | Display |
|---|---|---|
| `print(2 + 3)` | compute `5` | `5` |
| `print("2 + 3")` | keep literal text `2 + 3` | `2 + 3` |

## 6. Code block and indentation

Sometimes an action should happen only when a condition is satisfied. A **condition** is a statement that can be true or false. Here `3 >= 2` asks whether 3 is at least 2; it is true. `if` uses the result to decide whether to run an indented **code block**.

```python
if 3 >= 2:
    print("Ready to continue")
print("Check complete")
```

- `if 3 >= 2:` introduces the condition and ends with a colon `:`.
- The four spaces before the first `print` are **indentation**. They show that the statement belongs to the `if` block.
- The final `print` begins at the left edge; it runs after the block regardless of the condition.

**Expected output:**

```text
Ready to continue
Check complete
```

Now change only `3 >= 2` to `1 >= 2`. Predict: `Ready to continue` disappears because the condition is false; `Check complete` still appears. You are changing an input value inside the source code, not a live learner's data. Later lessons show better ways to supply values while running.

**Indentation mistake:**

```python
if 3 >= 2:
print("Ready to continue")
```

The instruction belonging to `if` must be indented. Python reports an **IndentationError**. Repair by placing four spaces before `print`. A text editor's tab may look like spaces but behave differently; use a consistent four-space indentation in these exercises.

## 7. Comments: notes for the human reader

A **comment** explains the source code to a person. Python ignores it as a command.

```python
# This example uses fictional course text.
print("Today: AI")  # This line displays the chosen label.
```

The first `#` starts a **single-line comment**. The second `#` starts a comment after a code statement. The expected output is only `Today: AI`: comment text is not printed.

When a note needs several lines, put `#` at the start of each line:

```python
# Tiny course-assistant example.
# No actual student records are used.
print("Ready")
```

Some languages provide a special **multiline comment** syntax. Python does **not** use triple-quoted strings (`"""..."""`) as a general comment mechanism: those are strings, which can serve as documentation in certain positions. Use consecutive `#` lines for ordinary explanatory comments here. Do not confuse a helpful comment with evidence that the code works; run and inspect the program.

## 8. Three different ways information reaches a program

You already saw text fixed in source code: `print("Today: AI")`. That text will stay the same until someone edits the file. A more useful program can receive information **when it runs**.

### 8.1 Interactive program input

`input(...)` displays a question, waits for someone to type text, and gives the typed text back to the program. A **variable** is a name for a stored value; `name` below holds the typed text. Variables are taught fully in `QAI.01.07`.

Save as `ask_name.py`:

```python
name = input("Learner name: ")
print("Hello,", name)
```

**Run:** `py .\ask_name.py` in PowerShell or `python3 ask_name.py` in Bash/Zsh. At the prompt, type the fictional name `Asha` and press Enter.

```text
Learner name: Asha
Hello, Asha
```

Here `Asha` is **program input**, and `Hello, Asha` is **program output**. The saved file does not permanently acquire the name `Asha`. Typing `Meera` on the next run changes the displayed greeting without changing the source code. Do not type real private details into a practice recording.

### 8.2 Program argument supplied in the command line

An **argument** here is a value placed after the code file's name in the terminal command. You saw command arguments in `QAI.01.04`; now the running Python program reads one. `sys` is a built-in Python module that provides access to command-line arguments. A **module** is reusable code imported with `import`. `sys.argv` holds the argument list: position `0` is usually the script name; position `1` is the first value after it. This way of identifying a value by its position is called **indexing**; details come later.

Save as `topic_arg.py`:

```python
import sys

topic = sys.argv[1]
print("Today:", topic)
```

**Run from `code-lab`:**

```powershell
py .\topic_arg.py GenAI
```

```bash
python3 topic_arg.py GenAI
```

**Expected output:** `Today: GenAI`. The source file still has no fixed topic name: `GenAI` was supplied for this run. If the argument is omitted, `sys.argv[1]` has no value and Python reports an **IndexError**. The immediate repair is to provide the missing topic; later you will learn to check for it and give a friendly error instead.

**Never pass passwords or API keys as practice arguments:** command lines may be visible in history or process listings. Secrets receive their own handling later in the course.

### 8.3 Separate the three cases

| Case | Where value comes from | Example | What changes on a new run? |
|---|---|---|---|
| fixed value | source code | `"AI"` in `hello.py` | same until file is edited |
| interactive input | typed after program starts | `Asha` after `Learner name:` | learner can type another name |
| program argument | terminal command before start | `GenAI` after `topic_arg.py` | caller can supply another topic |

This is the starting point for later AI applications: data arrives from a user, a file, or another system; the program reads it, processes it, and returns a result. The rest of the course will explain each mechanism at the required depth.

## 9. An operational debugging routine

When a program does something unexpected:

1. State what you expected in one sentence.
2. Record exactly what happened, including the complete error message.
3. Confirm your current directory and the exact code file you ran.
4. Inspect the file's saved text at the reported error line.
5. Change **one** relevant item; save and rerun.
6. Compare the new output with the prediction.

| Observation | What to check | Worked correction |
|---|---|---|
| `hello.py` cannot be found | current directory and file extension | enter `code-lab`; ensure saved name is `hello.py`, not `hello.py.txt` |
| `SyntaxError` for `print("Welcome"` | opening and closing punctuation | change to `print("Welcome")` |
| `NameError` for `prnit` | misspelled name | change to `print` |
| `IndentationError` after `if ...:` | spaces at beginning of block line | insert four spaces before nested `print` |
| `IndexError` in `topic_arg.py` | command omitted required argument | run with `GenAI` after the file name |
| output still shows old value | unsaved edit or wrong copy of file | save editor tab; display current folder and list the file |

An error is evidence about a specific failure, not a judgment of the learner. Do not respond by randomly installing packages, changing system settings, or deleting files.

## 10. Guided implementation: read, predict, run, change

Create a new file `course_card.py` in `code-lab`:

```python
# Fictional course card; no private learner data.
learner = input("Learner name: ")
print("Welcome,", learner)

if 2 + 1 >= 3:
    print("Preparation: ready")

print("Topic: GenAI")
```

**Before running, trace it:**

1. The comment is ignored.
2. The program waits for a fictional name and stores the typed text in `learner`.
3. The welcome line is displayed.
4. Expression `2 + 1` produces `3`; `3 >= 3` is true, so the indented readiness line is displayed.
5. The topic line is displayed regardless of the condition.

**Expected interaction when you type `Asha`:**

```text
Learner name: Asha
Welcome, Asha
Preparation: ready
Topic: GenAI
```

**Controlled variation:** change `2 + 1 >= 3` to `2 + 0 >= 3`. Prediction: the readiness line disappears; the welcome and topic lines still appear. Save and run to test your prediction. Restore the earlier condition afterwards if you want the original behaviour.

**Deliberate debugging variation:** remove the four spaces before `print("Preparation: ready")`, save, and try to run. Expected: an indentation error. Restore four spaces, save, and rerun. Do this only inside the disposable practice file.

## 11. Independent check with complete solution

**Task:** create `study_step.py` in `code-lab` so it asks for a fictional learner name, prints `Hello, <name>`, then prints `Step 1: inspect the input`. Include one meaningful comment. Predict the result for `Meera`, run if possible, then change only the step number to `2` and predict again.

**One complete solution:**

```python
# A tiny practice step; the learner name is fictional.
name = input("Learner name: ")
print("Hello,", name)
print("Step 1: inspect the input")
```

**Expected first interaction:**

```text
Learner name: Meera
Hello, Meera
Step 1: inspect the input
```

After changing only the last statement to `print("Step 2: inspect the input")`, the third displayed line becomes `Step 2: inspect the input`; the first two lines are unchanged. **Explanation:** only fixed text in the last statement changed; `name` still receives the value typed during the run. The comment remains invisible in output.

**Evidence:** retain the three saved code files `hello.py`, `course_card.py`, and `study_step.py`; record one prediction, one observed result, and one repaired error. `ask_name.py` and `topic_arg.py` are optional additional files. If Python is not installed yet, mark actual execution as pending and finish it in `QAI.01.06` rather than claiming a run occurred.

## 12. What to remember

- A program is executable instructions; source code is its readable form; a code file stores it.
- Saving code and running code are different actions.
- A statement performs an action; an expression produces a value.
- Python's `if` block uses a colon and indentation to group statements.
- A `#` comment explains code to readers; it does not appear in ordinary program output.
- Fixed source text, interactive input, and command-line arguments supply information in different ways.
- Check exact file, line, expected result, actual result, and one correction before rerunning.

## 13. Next connection

`QAI.01.06 — Python execution basics` explains the Python interpreter, installation, versions, interactive mode, running `.py` files, and how to distinguish syntax errors from errors that happen during execution.
