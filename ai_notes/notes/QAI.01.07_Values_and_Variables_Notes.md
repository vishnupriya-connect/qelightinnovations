# QAI.01.07 — Values and Variables

> `QAI.01.06 Python execution basics` → **`QAI.01.07 Values and variables`** → `QAI.01.08 Data types`

## 1. What you are building

A course assistant has to remember how many practice documents it has and display how many more can be added. A fixed message such as `print("Documents: 2")` cannot update itself when a document is added. **Variables** let a program use names for values that may change as it runs.

In this lesson, you will predict values line by line, write a short document-count program, change its input values, fix two naming mistakes, and verify actual output. Work in the disposable `qai-path-lab/code-lab/` folder from `QAI.01.05–.06`.

**Boundary:** here we learn names and assignment. What data types are and how Python objects can share references are covered in `QAI.01.08–.09`. We need not assume those mechanisms to trace today's small programs correctly.

## 2. First distinction: value, literal, and name

```python
document_count = 2
course_name = "GenAI"
```

| Part | What it is | Example |
|---|---|---|
| value | information Python works with | a count of 2; course text `GenAI` |
| literal | value written directly in source code | `2`, `"GenAI"` |
| variable | a name that currently refers to a value | `document_count`, `course_name` |

**Mental model:** a variable name acts like a label that Python uses to find the current value associated with that name. It is **not** a permanent inscription of the value and **not** necessarily a separate physical box holding its own copy. The details of Python objects and references come in `QAI.01.09`.

**Read the code aloud:** “Associate the name `document_count` with the value 2.” The name is not the count itself. If the value later changes to 3, the same name can refer to the new value.

Quotes matter:

```python
document_count = 2
print(document_count)
print("document_count")
```

**Expected output:**

```text
2
document_count
```

Without quotes, Python looks up the variable's value; inside quotes, the letters are fixed text. This distinction is essential when showing model names, counts, prompt text, and results in later AI programs.

## 3. Variable name and identifier

An **identifier** is a valid name used for something in Python. A **variable name** is an identifier you use to refer to a value. Python requires that it does not start with a digit, contain spaces, or use a reserved word such as `class`. For names in these lessons, use ordinary letters, digits **after** the first character, and underscores `_`; do not start with a digit. Names distinguish uppercase and lowercase letters.

| Name | Valid? | Why / better choice |
|---|---|---|
| `document_count` | yes | descriptive and easy to read |
| `course2` | yes | digit follows letters |
| `2courses` | no | begins with a digit; use `courses_2` |
| `course name` | no | space divides it; use `course_name` |
| `class` | no | Python reserves it for a language construct; use `class_name` |
| `DocumentCount` | yes | a different name from `document_count` |

Python also permits some other valid identifiers, but **clear English names with underscores** are the course convention. The underscore is part of the name, not a space. `document_count`, `Document_count`, and `DOCUMENT_COUNT` are three distinct identifiers.

**Naming convention** means a team-agreed style, not a runtime requirement. Use `lowercase_words_with_underscores` for ordinary variables, and choose a name that says what the value means: `document_count` tells more than `x`; `max_practice_documents` tells more than `m`. Avoid using a built-in name such as `print` for one of your own variables, because that can hide the useful built-in function.

## 4. Assignment: evaluate the right side, then associate the name

An **assignment** associates a name on the left with the value obtained from the right:

```python
document_count = 2
```

`=` is the **assignment operator**. It does **not** ask whether the two sides are mathematically equal. In the line above, it gives `document_count` the value `2` for later use. Python's comparison operator `==` asks whether two values are equal; comparison is covered more fully with conditions later.

The right side can also be an **expression** that must be evaluated first. An expression is code that produces a value:

```python
starting_documents = 2
added_documents = 1
document_count = starting_documents + added_documents
print(document_count)
```

**Trace before running:**

| Executed line | Right-side value | Names after the line |
|---|---:|---|
| `starting_documents = 2` | 2 | `starting_documents` → 2 |
| `added_documents = 1` | 1 | `starting_documents` → 2; `added_documents` → 1 |
| `document_count = starting_documents + added_documents` | 2 + 1 → 3 | previous names unchanged; `document_count` → 3 |
| `print(document_count)` | look up 3 | display `3`; names unchanged |

`print` displays the result; assignment alone does not automatically print it in a saved script. `QAI.01.06` showed that an expression typed at the interactive `>>>` prompt can show its value automatically; a normal `.py` script does not display the value of each expression just because that expression is written in the file.

## 5. Reassignment: the same name can refer to a new value

```python
document_count = 2
print(document_count)
document_count = 3
print(document_count)
```

**Expected output:** `2` on one line, `3` on the next. **Reassignment** means the name `document_count` is associated with a different value after the second assignment. The earlier print has already happened; a new assignment does not change past output.

This useful line is valid Python:

```python
document_count = document_count + 1
```

**Correct reading:** first evaluate the **old** `document_count + 1`; then assign the resulting value back to the name `document_count`. If the old value was 2, the new value is 3. In mathematical notation `x = x + 1` would be contradictory if `=` meant equality; in Python it is an instruction to update a name.

**Worked trace:**

```python
document_count = 2
document_count = document_count + 1
document_count = document_count + 1
print(document_count)
```

| Moment | `document_count` |
|---|---:|
| after first assignment | 2 |
| after first update | 3 |
| after second update | 4 |
| printed | 4 |

**Failure to predict:** if you try to update `document_count` before assigning it for the first time, Python cannot find the old value and reports a `NameError`. A value must be assigned before this form of update.

## 6. Evaluate an expression and display or print a value

**Evaluate** means find the value an expression produces. **Display** means make the result visible to a human. In saved programs, `print()` is the built-in function used here to print values to the terminal.

```python
starting_documents = 2
new_documents = 1
print("Documents:", starting_documents + new_documents)
```

The expression `starting_documents + new_documents` evaluates to `3`. `print()` displays the fixed label and the evaluated value. **Expected:** `Documents: 3`. A comma between the two items makes `print` place a space between them by default. `print()` with nothing inside prints an empty line; that is sometimes useful for formatting output, although no calculation occurs.

Contrast a calculation with fixed text:

```python
print(2 + 1)      # displays 3
print("2 + 1")    # displays the characters 2 + 1
```

The `#` portions are comments for readers and are not part of the output.

### A three-line AI example

```python
course_name = "GenAI"
document_count = 2
print("Course:", course_name)
print("Documents:", document_count)
```

**Expected:** `Course: GenAI` then `Documents: 2`. The name `document_count` represents a simple count in a course assistant; it does not claim that documents were actually downloaded, read, or indexed. Later lessons build those operations and check their results.

## 7. Constant convention: an intention, not enforcement

A **constant** is a value a programmer intends to keep unchanged for a particular program or calculation. Python programmers conventionally write the names of such values in `UPPERCASE_WITH_UNDERSCORES`:

```python
MAX_PRACTICE_DOCUMENTS = 5
document_count = 3
remaining_slots = MAX_PRACTICE_DOCUMENTS - document_count
print("Remaining slots:", remaining_slots)
```

**Expected output:** `Remaining slots: 2`. The uppercase name tells teammates, “treat this limit as fixed while the program runs.” Python **does not enforce** this naming convention:

```python
MAX_PRACTICE_DOCUMENTS = 5
MAX_PRACTICE_DOCUMENTS = 6
print(MAX_PRACTICE_DOCUMENTS)  # prints 6
```

This is legal Python, but changing a value promised as fixed can mislead others. If a limit must be configurable later, use an explicit configuration method and document it; uppercase alone is no protection.

## 8. Complete guided micro-lab: course assistant counts

Create `values_variables.py` inside your existing `qai-path-lab/code-lab/` folder. Copy the code exactly once, save, and **predict** each output line before running it:

```python
# Fictional course assistant: arithmetic only, no external files or API calls.
MAX_PRACTICE_DOCUMENTS = 5
course_name = "GenAI"
document_count = 2
new_documents = 1

print("Course:", course_name)
print("Before:", document_count)

document_count = document_count + new_documents
remaining_slots = MAX_PRACTICE_DOCUMENTS - document_count

print("After:", document_count)
print("Remaining slots:", remaining_slots)
```

**Trace of the values:**

| Step | `document_count` | `new_documents` | `remaining_slots` |
|---|---:|---:|---:|
| before update | 2 | 1 | not assigned yet |
| after `document_count = document_count + new_documents` | 3 | 1 | not assigned yet |
| after `remaining_slots = 5 - document_count` | 3 | 1 | 2 |

**Expected terminal output:**

```text
Course: GenAI
Before: 2
After: 3
Remaining slots: 2
```

Run from `code-lab` using the interpreter you verified in `QAI.01.06`:

```powershell
# Windows PowerShell
Get-Location
Get-ChildItem -Name
py .\values_variables.py
```

```bash
# macOS/Linux Bash or Zsh
pwd
ls
python3 values_variables.py
```

If your Windows interpreter command was `python`, use `python` in place of `py` consistently. The `Get-Location`/`pwd` step should show `code-lab`; the listing must contain `values_variables.py` before you run it.

### Change one input value and predict again

Change `new_documents = 1` to `new_documents = 2`; do **not** change any other line. Before running, predict: old count 2 + 2 new documents = 4; remaining slots 5 - 4 = 1. Save and run. **Expected:** `Before: 2`, `After: 4`, `Remaining slots: 1`. The course label stays `GenAI`.

Restore `new_documents = 1` afterward to recover the first worked result. This is a controlled test: one changed input should affect only outputs that depend on it.

## 9. Failure diagnosis in the same practice file

Do these on a **separate copy** named `values_variables_debug.py` so the good original remains available. Change one line at a time, run, diagnose, then repair it before the next case.

| Deliberate change | Expected symptom | Cause and exact repair |
|---|---|---|
| `print(document_cout)` | `NameError` naming `document_cout` | misspelled name; use `document_count` |
| `print("document_count")` in place of `print(document_count)` | prints the word rather than number | quotes made fixed text; remove quotes to look up the value |
| `document_count = document_count + 1` before its first assignment | `NameError` | no earlier value to use; assign a starting count first |
| `2documents = 2` | `SyntaxError` | invalid identifier begins with digit; use `documents_2` |
| `document_count == 3` instead of `document_count = 3` | count remains unchanged; in a saved script this comparison line prints nothing | `==` compares values; use `=` to assign |

**Important:** a Python line containing `document_count == 3` is a valid expression, so it may not produce an error at all. It simply fails to update the name. Silent wrong results require a prediction and a before/after print, not just the absence of a traceback.

**Debug method:** state the expected value, inspect the exact executed line, identify the name and operator, make one correction, save, rerun, and compare the output.

## 10. Independent exercise with full solution

**Task:** write `lesson_capacity.py` without looking at the solution first. A fictional GenAI lesson has capacity `8`. There are `3` enrolled learners and `2` new learners. Print four lines: the lesson name, the count before adding, the count after adding, and the available seats. Use a named uppercase capacity; do not type the final number of seats directly into `print()`.

**Worked solution:**

```python
# Fictional counts used only for variable practice.
LESSON_CAPACITY = 8
lesson_name = "GenAI foundations"
enrolled_learners = 3
new_learners = 2

print("Lesson:", lesson_name)
print("Before:", enrolled_learners)

enrolled_learners = enrolled_learners + new_learners
available_seats = LESSON_CAPACITY - enrolled_learners

print("After:", enrolled_learners)
print("Available seats:", available_seats)
```

**Expected output:**

```text
Lesson: GenAI foundations
Before: 3
After: 5
Available seats: 3
```

**Why the answer is 3:** evaluate old count `3` plus new count `2` to get `5`, then calculate capacity `8` minus current enrolment `5` to get `3`. `LESSON_CAPACITY` remains `8` throughout. If `new_learners` becomes `1`, the new count becomes `4` and available seats becomes `4`. That is the check that your expressions respond to input changes rather than printed fixed answers.

## 11. Evidence to keep before moving on

Save `values_variables.py` and `lesson_capacity.py` inside `code-lab`. Add a small `values_trace.md` with:

- the **initial** predicted and observed output for `values_variables.py`;
- the **modified** predicted and observed output when `new_documents = 2`;
- the `3 → 5 → 3` calculation for lesson enrolment and remaining capacity;
- one mistake from §9, its observed symptom, and the exact repair.

An output comment such as `# expected: After: 3` can be placed beside the relevant print in your own code file, but comments do not execute or prove the result; record what you actually observed too. If a learner has no working interpreter yet, mark execution **pending** and complete `QAI.01.06` first.

## 12. What to remember

- **Literal:** value written directly in code. **Variable:** name currently referring to a value.
- **Identifier:** valid name; use descriptive lowercase words joined by underscores for ordinary variables.
- Assignment `=` evaluates the right side first, then binds the left-side name to that result.
- Reassignment can change the value reached through the same name; earlier printed output stays as it was.
- An expression yields a value; in a saved script use `print()` when you want to show that value.
- Quoted `"document_count"` is text; unquoted `document_count` asks for the named value.
- `UPPERCASE_NAMES` conventionally mark intended constants; Python still permits reassignment.
- Trace names and values line by line; compare predicted output with the actual program result.

## 13. Next connection

`QAI.01.08 — Data types`: so far you have used counts and text. Next you will examine what kind of value each is, why operations differ by type, and what conversion is needed when user input arrives as text.
