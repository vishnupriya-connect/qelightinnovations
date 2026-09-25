# QAI.01.20 — Conditional Execution

> QAI.01.19 Sets → **QAI.01.20 Conditional execution** → QAI.01.21 Repetition and loops

## 1. Destination: decide what to do with a learner question

Your course assistant receives a question and a lesson record. Some questions contain only spaces. Some records lack a required title. Valid questions should proceed to the next step; invalid ones need a clear result. A **condition** lets the program choose an action based on the actual input rather than assume every input is valid.

You will build `validation_and_loop_lab.py` in two stages: this node supplies the **validation and branches**; QAI.01.21 adds looped processing and per-item tracing. You will run normal, empty, missing-field, and length-boundary cases. A “valid to proceed” result here says only that these basic checks passed; it does not prove that the question is safe or answerable by an AI model.

## 2. Condition and Boolean condition

A **condition** is a test whose outcome determines what runs. A **Boolean condition** produces `True` or `False`. You already used comparisons and `and`/`or`/`not` in QAI.01.12:

```python
question = "Explain GenAI"
print(len(question) > 0)                 # True
print(question == "")                    # False
print("GenAI" in question)               # True
```

For user text, whitespace alone is not a useful question. Clean it before testing emptiness:

```python
raw = "   "
clean = " ".join(raw.split())
print(repr(clean))                       # ''
print(clean == "")                       # True
```

Python also treats an empty string, empty list, empty dictionary, and zero as **falsey** in a condition. A nonempty string is **truthy**, even if it contains only spaces. `bool("   ")` is `True`; `bool("   ".strip())` is `False`. For important validation, a clear comparison such as `clean == ""` often communicates the exact requirement better than an implicit truth test.

## 3. Branch and conditional statement: `if`

A **branch** is one route through the program. A **conditional statement** executes a route according to a condition. The `if` statement runs its indented **true branch** only when its condition is true:

```python
question = "Explain GenAI"
if question != "":
    print("Question received")           # runs
print("Check finished")                  # runs regardless
```

```text
Question received
Check finished
```

Read it as “**if** the question is not empty, print the first line; then continue.” The colon `:` begins the branch; consistent indentation places a line *inside* it. A line aligned with `if` is outside the branch. Changing `question` to `""` skips the first print but still prints `Check finished`.

**Trace:**

| `question != ""` | Inside `if` runs? | After `if` runs? |
|---|---|---|
| `True` | yes | yes |
| `False` | no | yes |

If no action is given for false, the `if` simply skips its body. For two deliberately different outcomes, add `else`.

## 4. True branch and false branch: `if` / `else`

`else` runs the **false branch** when the related `if` condition is false:

```python
raw_question = "  "
clean = " ".join(raw_question.split())
if clean == "":
    print("Please enter a question.")
else:
    print("Ready:", clean)
```

```text
Please enter a question.
```

Exactly one of the two print branches runs in this example. Change `raw_question` to `"  Explain GenAI  "` and the output becomes `Ready: Explain GenAI`. The cleaning step and the branch serve different purposes: first determine the usable text; then decide what action follows.

## 5. Several mutually exclusive routes: `elif`

`elif` means “else if”: evaluate the next test only if earlier branches did not run. The first true branch in a single `if` / `elif` / `else` chain wins:

```python
clean = " ".join("  Explain GenAI  ".split())
if clean == "":
    print("Empty question")
elif len(clean) > 80:
    print("Too long")
else:
    print("Accepted:", clean)
```

```text
Accepted: Explain GenAI
```

**Boundary:** length 80 is accepted because the test is `> 80`; length 81 is rejected. Decide and record the limit before writing the code. A limit on Python string length is a local input rule, not a model-token limit.

**Order matters:** check a missing or malformed value before operations that assume it is valid. Do not put `len(value)` in an earlier branch if `value` might be `None` without an explicit policy for that case.

## 6. Boolean conditions and short-circuit behaviour

A condition may combine smaller tests with `and` / `or` / `not`. `and` stops at the first false result; `or` stops at the first true result:

```python
record = {"code": "QAI.01.20", "title": "Conditional execution"}
clean = "Explain branches"
if "title" in record and clean != "":
    print("Required title and question present")
```

```text
Required title and question present
```

Short-circuiting can prevent a missing-key lookup if the presence check is **first**:

```python
record = {"code": "QAI.01.20"}
print("title" in record and record["title"] != "")  # False; no KeyError
# print(record["title"] != "" and "title" in record)  # KeyError if run
```

Here the left test is false, so Python does not evaluate `record["title"]`. Do not depend on this trick in place of clear validation when a missing title must be reported distinctly.

`None`, an empty value, and a missing key can mean different things. For required input, check the field's presence and value explicitly; do not let `record.get("title")` collapse those states without a reason.

## 7. Nested condition: a decision inside a decision

A **nested condition** places another `if` inside the branch of the first. It is useful when the inner test makes sense only after an outer condition succeeds:

```python
record = {"title": "GenAI"}
question = "  Explain  "
if "title" in record:
    clean = " ".join(question.split())
    if clean == "":
        print("Title exists, but question is empty")
    else:
        print(f"Ask about {record['title']}: {clean}")
else:
    print("Course title is missing")
```

```text
Ask about GenAI: Explain
```

There are two decision levels: (1) is the title key present? (2) with that title present, is the cleaned question empty? Trace both before extending the code. Excessive nesting makes decisions harder to read; `elif` or later functions can make related checks clearer.

## 8. Conditional expression: choose a value in one line

A **conditional expression** is a Python expression that selects one of two **values**:

```python
clean = "Explain GenAI"
display = clean if clean != "" else "No question supplied"
print(display)                         # Explain GenAI
```

Read it as “use `clean` **if** it is not empty; **else** use the fallback string.” For `clean = ""`, `display` becomes `"No question supplied"`. This selects a value; it is not the same grammar as a multiline `if` statement. Use the multiline form when several steps, an error path, or an important reason need to be shown. Never use a fallback merely to hide missing **required** input.

## 9. Conditional return: outcome from a function

A **function** is a named reusable operation; `return` gives its result back to its caller. Full function design comes in QAI.01.22. Here is a narrow preview of a **conditional return**, where each branch returns a different result:

```python
def status_for(raw_question):
    clean = " ".join(raw_question.split())
    if clean == "":
        return "missing"
    return "ready"

print(status_for("   "))              # missing
print(status_for("Explain GenAI"))    # ready
```

`def status_for(raw_question):` creates a function whose input is referred to as `raw_question`. The caller passes a string inside parentheses. If the cleaned string is empty, `return "missing"` ends that call immediately; otherwise execution reaches `return "ready"`. **Returning** a result is different from printing it: the caller receives a value it can use.

Avoid a route that accidentally reaches the end without a return when callers expect a meaningful status; in that case Python returns `None`. A more complete function that checks types, return shapes, and tests comes in QAI.01.22–01.24.

## 10. Guided implementation: accept or reject a course question

Create `validation_and_loop_lab.py` in `qai-path-lab/code-lab/`. This is **stage 1** of the file; stage 2 adds the loop in QAI.01.21. For now change the two inputs and rerun for each test case.

```python
# validation_and_loop_lab.py — stage 1: one record, one question
lesson = {"code": "QAI.01.20", "title": "Conditional execution"}
raw_question = "  Explain   GenAI  "
clean = " ".join(raw_question.split())
max_characters = 80

if "title" not in lesson:
    result = "REJECT: missing course title"
elif lesson["title"].strip() == "":
    result = "REJECT: blank course title"
elif clean == "":
    result = "REJECT: empty question"
elif len(clean) > max_characters:
    result = "REJECT: question exceeds character limit"
else:
    result = f"READY: {lesson['title']} | {clean}"

print(result)
```

Run from `code-lab` with `py .\validation_and_loop_lab.py` in Windows PowerShell (or your verified `python` command), or `python3 validation_and_loop_lab.py` in Bash/Zsh.

**Expected output for supplied inputs:**

```text
READY: Conditional execution | Explain GenAI
```

**Why that branch:** `"title" in lesson` is true, the title is not blank, `clean` is `"Explain GenAI"`, and its length is at most 80. All rejection tests are false, so the `else` branch runs.

### Four controlled test cases

For each row, start from the original script, change only the inputs described, predict, run, and record the actual output:

| Change from original | Expected result | What it tests |
|---|---|---|
| none | `READY: Conditional execution \| Explain GenAI` | normal case |
| `raw_question = "   "` | `REJECT: empty question` | whitespace boundary |
| `lesson = {"code": "QAI.01.20"}` | `REJECT: missing course title` | required key absent; no `KeyError` |
| `lesson = {"code": "QAI.01.20", "title": "  "}` | `REJECT: blank course title` | present key, blank value |

**Character boundary:** with the original lesson, set `raw_question = "A" * 80`. The program prints `READY: Conditional execution | ` followed by exactly 80 A characters. With `"A" * 81`, it prints `REJECT: question exceeds character limit`. A question of 80 A characters is *allowed by this simple length rule*, not guaranteed to be meaningful or appropriate for the model.

**Current assumption:** `lesson["title"]` and `raw_question` are strings. If data may contain numbers, `None`, or a list, this script needs a type and schema check before calling `.strip()`/`.split()`. Errors, exception handling, and test design receive fuller treatment in QAI.01.23–01.24.

## 11. Diagnose branch failures

| Symptom | Likely cause | Fix |
|---|---|---|
| empty input is accepted | test ran on raw spaces rather than cleaned text | inspect `repr(clean)` and compare `clean == ""` |
| missing title raises `KeyError` | lookup occurred before presence check | put presence test first |
| long question accepted at the boundary | wrong `>` versus `>=` choice | write exact limit and test length 80 and 81 |
| both error and success messages print | separate `if` blocks were used for exclusive outcomes | use one `if`/`elif`/`else` chain |
| branch never runs | indentation is outside intended block or condition false | trace each Boolean value; align spaces deliberately |
| `if record.get("title"):` merges distinct cases | missing, `None`, and empty text are all falsey | separate key-presence and value checks |
| `print` inside function shows text but caller gets `None` | printing did not return a value | use `return` for a result used by caller |
| `.strip()` gives `AttributeError` | assumed text but received another type | validate type/schema before string operations |

**Debug sequence:** record the inputs; print `repr` of received and cleaned text; evaluate each condition in the same order as the code; note the first true branch; compare the actual message with the specified outcome. Re-test the normal case after fixing a boundary case.

## 12. Independent micro-lab with full solution

**Task:** a lesson record requires `"code"` and `"title"`. A cleaned question must be nonempty and at most 30 characters. Starting from `lesson = {"code": "QAI.01.20", "title": "Conditionals"}` and `raw = "  What is an if statement?  "`, print one result: `"REJECT: missing code"`, `"REJECT: missing title"`, `"REJECT: empty"`, `"REJECT: too long"`, or `"READY: <code> | <clean question>"`. Put the checks in a safe order. Test an empty question and a missing title separately.

**Full solution:**

```python
lesson = {"code": "QAI.01.20", "title": "Conditionals"}
raw = "  What is an if statement?  "
clean = " ".join(raw.split())

if "code" not in lesson:
    result = "REJECT: missing code"
elif "title" not in lesson:
    result = "REJECT: missing title"
elif clean == "":
    result = "REJECT: empty"
elif len(clean) > 30:
    result = "REJECT: too long"
else:
    result = f"READY: {lesson['code']} | {clean}"
print(result)
```

**Expected original output:**

```text
READY: QAI.01.20 | What is an if statement?
```

**Solved variations:** with `raw = "    "`, the output is `REJECT: empty`. With `lesson = {"code": "QAI.01.20"}` and the original `raw`, output is `REJECT: missing title`. If both title is missing *and* question is empty, the message is `REJECT: missing title` because that check occurs first. For a long-question test, `raw = "A" * 31` yields `REJECT: too long`. This exercise checks field **presence**; a blank string stored as a title is a separate validity rule you can add before `clean == ""`.

## 13. Remember and retain

- A Boolean **condition** decides which **branch** executes.
- `if` runs on true; `else` runs if the preceding tests are false; `elif` allows another exclusive test.
- Branch order matters. Check required keys before looking them up.
- A nested condition makes a second decision within an already chosen branch.
- A conditional expression chooses between values; a conditional return gives a function's outcome to its caller.
- Test the normal case, blank input, missing required field, and both sides of a numeric boundary.
- Keep `validation_and_loop_lab.py`, the test table with observed outputs, and one debug note describing any mismatch. In QAI.01.21 you will extend this same validation idea to a series of questions and trace loop behaviour.

**Next:** QAI.01.21 explains why repeating one decision across many items calls for a loop and how to guarantee that repetition terminates.

---

**Node contract (S90):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. All twelve S86 conditional topics receive an explanation, worked trace, runnable script, controlled boundary checks, and a complete solved micro-lab. Learner evidence requires actually running, changing, and explaining the cases.
