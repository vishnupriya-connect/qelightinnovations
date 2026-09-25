# QAI.01.22 — Functions

> QAI.01.21 Repetition and loops → **QAI.01.22 Functions** → QAI.01.23 Errors and exception handling

## 1. Destination: reuse question validation without hidden state

QAI.01.20 decided what to do with one course question; QAI.01.21 repeated that decision for a list. Now you will put the repeatable steps in named functions so the caller can supply inputs, receive results, and check them. Your P1 mini-project is `text_utils.py`: a small course-question utility with a demo and assertions that check its results.

One function should have a clear job. In this lesson, question cleaning, question validation, request construction, and printing results each have distinct purposes. Full error and test tooling follows in QAI.01.23–01.24; here you will establish runnable, checked behaviour.

## 2. Function, definition, name, and call

A **function** is a named, reusable block of code. A **function definition** begins with `def` and gives a **function name**. A **function call** uses its name followed by parentheses:

```python
def course_greeting():
    return "Welcome to GenAI"

print(course_greeting())             # Welcome to GenAI
print(course_greeting())             # Welcome to GenAI
```

`def course_greeting():` defines the function; `course_greeting()` calls it. The indented body runs when the call occurs, not merely when Python reads the definition. A function defined but never called produces no output by itself.

**Mental model:** the caller sends input → the function performs its stated work → `return` sends a result back. Sometimes a function intentionally produces an outside effect instead; that difference matters below.

## 3. Parameter and argument; positional and keyword calls

A **parameter** is the input name written in the definition. An **argument** is the actual value passed in a call:

```python
def lesson_label(code, title):
    return f"{code}: {title}"

print(lesson_label("QAI.01.22", "Functions"))
print(lesson_label(title="Functions", code="QAI.01.22"))
```

```text
QAI.01.22: Functions
QAI.01.22: Functions
```

`code` and `title` are parameters. `"QAI.01.22"` and `"Functions"` are arguments. The first call uses **positional arguments**; order determines their destination. The second uses **keyword arguments**; names determine their destination, so their written order may differ.

`lesson_label("Functions", "QAI.01.22")` still runs but produces `Functions: QAI.01.22`, a **logical error**. Clear parameter names and keyword calls help avoid such swaps. An unknown keyword (such as `label="Functions"` here) raises `TypeError`.

## 4. Required, optional, and default arguments

A **required argument** must be supplied by a caller when its parameter has no default. An **optional argument** may be omitted because its parameter has a **default**:

```python
def format_lesson(title, level="Beginner"):
    return f"{title} [{level}]"

print(format_lesson("Functions"))                    # Functions [Beginner]
print(format_lesson("Functions", "Advanced"))        # Functions [Advanced]
print(format_lesson("Functions", level="Intermediate"))  # Functions [Intermediate]
```

`title` is required; `level` defaults to `"Beginner"`. `format_lesson()` raises `TypeError` because its required title is missing. A standard signature puts required positional parameters before parameters with defaults.

**Avoid a mutable default:** `def add_item(item, items=[]): ...` can retain the **same list** between calls because that default object is created when the definition runs. Here is a safe fresh-list pattern when that behaviour is needed:

```python
def added_item(item, items=None):
    if items is None:
        items = []
    result = items.copy()
    result.append(item)
    return result

print(added_item("ML"))              # ['ML']
print(added_item("GenAI"))           # ['GenAI'], not ['ML', 'GenAI']
```

`None` here means “no list supplied”; `items.copy()` avoids modifying a supplied list. Use identity check `is None` when testing for this sentinel, because `[]` is an intentionally supplied empty list.

## 5. Return value versus no return value

A **return value** is what a call gives back to the caller. `return` ends the current call immediately and supplies that value:

```python
def cleaned_question(raw):
    return " ".join(raw.split())

result = cleaned_question("  Explain  GenAI ")
print(result)                        # Explain GenAI
```

Printing inside a function is not returning:

```python
def print_question(raw):
    print(" ".join(raw.split()))

result = print_question("  Explain  GenAI ")
print("Returned:", result)
```

```text
Explain GenAI
Returned: None
```

The first line comes from `print_question`. A function with **no explicit return value** finishes and returns `None`. Use `return` when other code must use the result, and print at a clear user-facing boundary. This distinction is central for reusable code and tests.

**Early return** expresses a rejection clearly:

```python
def question_status(raw):
    clean = raw.strip()
    if clean == "":
        return "EMPTY"
    return "READY"

print(question_status("   "))        # EMPTY
print(question_status(" Explain "))  # READY
```

Only one return runs per call. The second return runs when the early rejection did not occur.

## 6. Local variable, global variable, and scope

A **local variable** is bound inside a function call. Its **scope** is where its name is usable. A **global variable** here means a name defined at module level, outside the function:

```python
course = "GenAI"                     # global name

def describe(title):
    label = f"{course}: {title}"     # local label; reads global course
    return label

print(describe("Functions"))         # GenAI: Functions
# print(label)                       # NameError: local label is not defined here
```

The function can read `course`, but now its result depends on a value that was **not passed to it**. Such hidden dependence makes isolated testing and reuse harder. Give the needed value as an argument:

```python
def describe(course_name, title):
    label = f"{course_name}: {title}"
    return label

print(describe("GenAI", "Functions")) # GenAI: Functions
print(describe("ML", "Functions"))    # ML: Functions
```

Assignment to a local name also does not change a separate global name with the same spelling:

```python
title = "Original"
def build_title():
    title = "New"
    return title

print(build_title())                 # New
print(title)                         # Original
```

Names and mutable objects are different issues: a function can mutate a **list object passed as an argument** with `append` even though the parameter name is local. If the caller must retain an unchanged list, make a new one and document the choice.

## 7. Signature and docstring

A **function signature** gives its name and input parameters, including defaults. For `def prepare_question(raw, max_characters=80):`, `raw` is required and `max_characters` has a default.

A **docstring** is a string literal immediately inside a function body that describes its contract. State the accepted inputs, result, and important limits rather than repeat the code word for word:

```python
def prepare_question(raw, max_characters=80):
    """Return (status, cleaned_text) for a string question.

    status is READY, EMPTY, or TOO_LONG. Spaces are collapsed to one.
    max_characters counts Python string positions, not model tokens.
    """
    clean = " ".join(raw.split())
    if clean == "":
        return ("EMPTY", "")
    if len(clean) > max_characters:
        return ("TOO_LONG", clean)
    return ("READY", clean)

print(prepare_question("  Explain   AI  "))      # ('READY', 'Explain AI')
print(prepare_question("   "))                   # ('EMPTY', '')
```

Every branch returns a two-item tuple: the caller can unpack `status, clean` predictably. The docstring explicitly assumes `raw` is a string; rejecting other types at the boundary is addressed more fully in QAI.01.23–01.24. A docstring does not itself enforce its statements—tests and code must agree with it.

## 8. Reusable function, pure function, side effect

A **reusable function** can be called with different inputs without rewriting its body. A **pure function** returns an outcome determined by its explicit inputs and does not change external state. `prepare_question` is pure for the given string and integer inputs.

A **side effect** changes something outside a function's return value—printing, editing a passed list, writing a file, or making a network request are examples:

```python
def make_label(code):
    return f"Course {code}"          # result; no printing

def show_label(code):
    print(f"Course {code}")          # side effect: displayed output

print(make_label("QAI.01.22"))       # Course QAI.01.22
show_label("QAI.01.22")              # Course QAI.01.22
```

Printing can be exactly what a display function is meant to do; side effects are not automatically bad. They should be intentional and visible in the function's purpose. A pure validation function is easier to call from a notebook, tests, or a later API because it returns data instead of deciding when to print.

**Mutation example:**

```python
def add_in_place(items, new_item):
    items.append(new_item)            # changes the caller's list

path = ["Python"]
add_in_place(path, "ML")
print(path)                           # ['Python', 'ML']
```

Compare with `added_item` in Section 4, which returns a new list. Choose based on the required ownership and make it clear in the name and documentation.

## 9. Recursion, recursive call, base case

**Recursion** is a function calling itself. A **recursive call** works on a smaller version of the original problem. A **base case** stops further calls:

```python
def countdown(number):
    if number <= 0:                    # base case
        return ["Done"]
    return [number] + countdown(number - 1)  # recursive call

print(countdown(3))                   # [3, 2, 1, 'Done']
print(countdown(0))                   # ['Done']
```

Trace `countdown(3)`: it constructs `[3] + countdown(2)` → `[3, 2] + countdown(1)` → `[3, 2, 1] + countdown(0)` → base case `["Done"]`. If the number did not decrease, the base case might never be reached; Python eventually raises a recursion-depth error rather than finish.

For simple counting and long sequences, a loop is usually clearer and avoids recursion-depth limits. Recursion is useful when a problem naturally breaks into similar smaller problems, such as nested structures, provided that termination and input size are controlled.

## 10. Mini-project: `text_utils.py`

Create `text_utils.py` in `qai-path-lab/code-lab/`. It has three reusable functions plus a display section and simple **assertions**. An assertion checks that a condition is true; if false, Python raises `AssertionError`. QAI.01.23–01.24 teach when assertions and full tests are appropriate.

**Input contract:** `lesson` is a dictionary with a required nonblank string `"title"`; each question is a string; `max_characters` is a nonnegative integer. This first project validates the title and question content but assumes those input types. It does not send questions to an AI model.

```python
# text_utils.py
def clean_question(raw):
    """Return one-line text with surrounding and repeated whitespace removed."""
    return " ".join(raw.split())


def classify_question(raw, max_characters=80):
    """Return (status, cleaned_text) for a string question.

    Status is READY, EMPTY, or TOO_LONG.
    max_characters measures Python string positions, not model tokens.
    """
    clean = clean_question(raw)
    if clean == "":
        return ("EMPTY", "")
    if len(clean) > max_characters:
        return ("TOO_LONG", clean)
    return ("READY", clean)


def prepare_requests(lesson, raw_questions, max_characters=80):
    """Return one (status, display) result per question without editing inputs.

    A missing/blank course title rejects every question.
    The caller supplies a dictionary lesson and a list of string questions.
    """
    results = []
    for raw in raw_questions:
        if "title" not in lesson or lesson["title"].strip() == "":
            results.append(("MISSING_TITLE", "REJECT: missing course title"))
            continue
        status, clean = classify_question(raw, max_characters=max_characters)
        if status == "READY":
            results.append((status, f"{lesson['title']} | {clean}"))
        elif status == "EMPTY":
            results.append((status, "REJECT: empty question"))
        else:
            results.append((status, "REJECT: question exceeds character limit"))
    return results


lesson = {"title": "GenAI"}
raw_questions = ["  Explain   AI  ", "   ", "A" * 81]
results = prepare_requests(lesson, raw_questions)
for status, display in results:
    print(f"{status}: {display}")

# Deterministic checks: normal, empty, length boundary, missing title, no mutation.
assert clean_question("  Explain   AI  ") == "Explain AI"
assert classify_question("   ") == ("EMPTY", "")
assert classify_question("A" * 80) == ("READY", "A" * 80)
assert classify_question("A" * 81) == ("TOO_LONG", "A" * 81)
assert prepare_requests({}, ["Explain AI"]) == [
    ("MISSING_TITLE", "REJECT: missing course title")
]
assert raw_questions == ["  Explain   AI  ", "   ", "A" * 81]
assert lesson == {"title": "GenAI"}
print("Checks passed: 7")
```

Run from `code-lab` with `py .\text_utils.py` in Windows PowerShell (or the verified `python` command), or `python3 text_utils.py` in Bash/Zsh.

**Expected output:**

```text
READY: GenAI | Explain AI
EMPTY: REJECT: empty question
TOO_LONG: REJECT: question exceeds character limit
Checks passed: 7
```

**How to read the data flow:** `raw_questions` → each `raw` enters `prepare_requests` → `classify_question` calls `clean_question` → a two-item status result comes back → the outer function builds one display result per input → the caller prints. Validating the title within the loop makes the behaviour explicit for each question, though an application could check a course record once before processing a large batch.

### Controlled change and debug

1. Change only `raw_questions` to `["Explain GenAI"]`. Predict one `READY` line. The final assertion about `raw_questions` will now **fail** because it checks the original sample list. When experimenting, restore the original inputs before running the complete checks, or update that input-specific assertion to the new expected value. Do not remove an assertion just to suppress a real mismatch.
2. Keep the original questions, change `lesson` to `{}`, and predict three `MISSING_TITLE` lines. The check for `lesson == {"title": "GenAI"}` will also fail by design until you restore the fixture. Restore it and rerun.
3. Change `max_characters=80` to `max_characters=10` only in the call to `prepare_requests`. The first cleaned question `"Explain AI"` has 10 characters and remains READY; 81 A characters remain TOO_LONG. The explicit boundary checks for `classify_question` still use its own default of 80.

**Meaningful tests:** an assertion succeeding means these specified examples agree with the current code. It does not prove every possible input works. Add a blank-title, exactly-at-limit, and wrong-type case in QAI.01.23–01.24; define a clear error policy before accepting arbitrary external data.

## 11. Independent exercise and full solution

**Task:** create a reusable function `visible_label(title, prefix="Lesson")`. It must strip surrounding spaces from `title`, return `"MISSING TITLE"` when the stripped title is empty, otherwise return `"<prefix>: <title>"`. Call once positionally using only a title and once with the `prefix` keyword set to `"Topic"`. Show that the supplied title variable remains unchanged; check normal, blank, and custom-prefix outputs.

**Complete solution:**

```python
def visible_label(title, prefix="Lesson"):
    """Return a display label for nonblank string title without changing it."""
    clean = title.strip()
    if clean == "":
        return "MISSING TITLE"
    return f"{prefix}: {clean}"

original = "  Functions  "
print(visible_label(original))
print(visible_label(original, prefix="Topic"))
print(visible_label("   "))
print(repr(original))

assert visible_label(" AI ") == "Lesson: AI"
assert visible_label("   ") == "MISSING TITLE"
assert visible_label(" ML ", prefix="Topic") == "Topic: ML"
assert original == "  Functions  "
print("Exercise checks passed: 4")
```

**Expected output:**

```text
Lesson: Functions
Topic: Functions
MISSING TITLE
'  Functions  '
Exercise checks passed: 4
```

**Reasoning:** `title` is a required parameter; `prefix` is optional with a default. `title.strip()` creates a new string and leaves `original` intact. Both branches return a string; printing and checking happen at the caller, which makes the function reusable.

## 12. Diagnose function problems

| Observation | Cause | Repair |
|---|---|---|
| caller receives `None` after a printed answer | function printed but did not return | `return` a value if caller needs it |
| `NameError` for a local name outside function | local scope ends at function boundary | use the return value |
| function works only with one global course title | hidden global dependence | accept course as a parameter |
| output changes after another call unexpectedly | shared mutable default or shared mutable input | use `None` sentinel and choose copy/mutation deliberately |
| arguments appear in wrong fields | positional order was swapped | inspect signature; use keyword arguments for clarity |
| call raises `TypeError` for missing argument | required parameter was not supplied | supply it or define a justified default |
| recursion never reaches result | missing base case or no progress toward it | establish base case and decreasing measure before call |
| `assert` reports a failure after changing a fixture | old expected input no longer matches changed demo | compare actual and intended requirement; restore or update fixture deliberately |
| printed output “looks right” but other code cannot reuse it | function mixes computation with display | return data and print at the caller boundary |

**Debug routine:** write the function's signature, call arguments, local variable values, each return path, and any side effects. Run normal, blank, and boundary inputs. Identify whether a failure belongs to the function, the caller's data, or the expected result.

## 13. What to remember and retain

- `def` names reusable work; a call supplies arguments for parameters.
- Positional arguments follow parameter order; keyword arguments name their destination.
- Required parameters need an argument; defaults make a parameter optional; avoid shared mutable defaults.
- `return` gives a result to the caller; printing alone returns `None`.
- Local names live within a function; make needed outside values explicit parameters rather than hidden globals.
- Signature and docstring state the expected call and result; tests verify representative cases.
- Pure functions with explicit inputs simplify reuse; side effects must be intentional.
- Recursion needs a base case and progress toward it; use simpler loops when they fit.
- Retain `text_utils.py`, successful run output, a deliberate failing-assertion observation from one controlled variation, and the exercise solution. For the P1 mini-project, write a short README-style record: how to run; accepted input shape; status outputs; one limitation (the input types are assumed); and which boundary tests passed.

**Next:** QAI.01.23 shows how to read errors and handle genuinely recoverable failures. QAI.01.24 turns the example assertions into more systematic tests.

---

**Node contract (S90):** `C | L3 | H1–H3 | E2–E5 | A1–A4 | P0–P1`. All twenty-five S86 function topics are covered with worked calls, a runnable P1 mini-project, concrete checks, controlled failures, and a complete independent solution. Learner evidence requires running, varying, and recording results; the written code itself is a reference solution.
