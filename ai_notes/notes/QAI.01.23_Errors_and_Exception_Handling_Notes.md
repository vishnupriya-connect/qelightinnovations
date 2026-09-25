# QAI.01.23 — Errors and Exception Handling

> QAI.01.22 Functions → **QAI.01.23 Errors and exception handling** → QAI.01.24 Debugging and testing

## 1. Destination: reject bad input and expose real bugs

In `text_utils.py` you assumed every question was text, every course title existed, and the character limit was sensible. Real inputs can violate those assumptions. A well-behaved application distinguishes:

1. a learner's correctable input problem, such as an empty question;
2. an invalid record or configuration that should be repaired;
3. a programming bug that the developer must investigate.

You will read a traceback, narrow a failure to its cause, add explicit validation, raise a meaningful exception, and catch only the anticipated errors at the user-facing boundary. The runnable mini-project `text_utils_checked.py` returns or prints predictable outcomes without echoing private question content in an error.

## 2. Bug, syntax error, runtime error, logical error

A **bug** is unintended program behaviour. Three useful classes:

| Kind | When it appears | Example | What you do |
|---|---|---|---|
| **syntax error** | Python cannot parse the source | missing colon after `if` | inspect indicated line and nearby syntax |
| **runtime error** | Python started executing but an operation fails | `int("abc")` | inspect value, operation, and exception type |
| **logical error** | code runs but result is wrong | rejecting length 80 when rule allows it | compare actual result with an explicit expected result |

You can inspect a syntax error safely by compiling **sample text** without executing it:

```python
broken_source = "if True print('ready')"   # missing colon
try:
    compile(broken_source, "<demo>", "exec")
except SyntaxError as error:
    print(type(error).__name__)           # SyntaxError
    print(error.lineno)                    # 1
```

A runtime failure:

```python
try:
    int("not a number")
except ValueError as error:
    print(type(error).__name__)           # ValueError
```

**Logical failure:** `if len(clean) >= 80: reject` is syntactically correct and runs, but if the declared rule is “allow 80, reject 81,” the boundary is wrong. A test of exactly 80 characters reveals the bug. Exception handling cannot detect every logical error.

## 3. Exception, type, message, location, traceback

An **exception** is a Python signal that an operation cannot continue normally. Its **exception type** identifies the category, such as `KeyError`, `TypeError`, `ValueError`, or `IndexError`. Its **error message** provides details; its **traceback** shows the sequence of calls that led to it.

For a **fictional** example:

```python
def title_of(record):
    return record["title"]

# title_of({"code": "QAI.01.23"})  # KeyError: 'title' if uncommented
```

An uncaught run ends with a traceback resembling:

```text
Traceback (most recent call last):
  File "...", line ..., in <module>
    title_of({"code": "QAI.01.23"})
  File "...", line ..., in title_of
    return record["title"]
KeyError: 'title'
```

Read **bottom upward for the immediate symptom**: `KeyError: 'title'` says a lookup requested a missing key. The line in `title_of` is the **error location** where it failed; the caller line shows how it was reached. The cause could be that a required title is absent upstream, rather than an error in bracket syntax. File paths and line numbers depend on your own file.

**Debug sequence:** reproduce with the smallest input → read type and last traceback line → find the failing line → inspect the values and required contract → correct the cause → rerun the same example. A traceback can contain paths or values; handle it as development information, not content to paste unfiltered into a public response.

## 4. `try` / `except`: recover only when you know how

`try` encloses an operation that might raise an expected exception. `except` runs only if that exception occurs:

```python
raw_limit = "80"
try:
    limit = int(raw_limit)
except ValueError:
    print("Enter an integer limit.")
else:
    print("Accepted limit:", limit)
```

```text
Accepted limit: 80
```

Change `raw_limit` to `"many"`: the conversion raises `ValueError`, so the message is `Enter an integer limit.` The handler is narrow: it catches an invalid numeric string. It does not conceal unrelated failures elsewhere in the program.

**Do not write** `except: pass` or `except Exception: return "OK"` to make a broken program look successful. A broad catch may hide bugs, data problems, or unexpected security-relevant failures. If you cannot recover, let the failure reach a properly configured application boundary while keeping private data out of user-facing output.

## 5. `else` and `finally` in an exception block

An exception block can use `else` and `finally`. The `else` body runs if the `try` body completes without an exception; `finally` runs whether an exception occurred or not:

```python
raw = "3"
try:
    count = int(raw)
except ValueError:
    print("Invalid count")
else:
    print("Converted:", count)
finally:
    print("Conversion attempt finished")
```

```text
Converted: 3
Conversion attempt finished
```

With `raw = "three"`, output becomes `Invalid count` followed by `Conversion attempt finished`. Use `finally` for necessary cleanup work such as closing a resource when no better context-manager abstraction applies. **Do not return from `finally`** as a general error-handling pattern: it can replace a prior result or suppress an exception. For files, a `with` block in QAI.01.28 normally handles closing more safely.

## 6. Raise an exception to enforce a contract

**Raise exception** means deliberately signal an invalid operation with `raise`. For example, a configured character limit must be a positive integer:

```python
def check_limit(limit):
    if type(limit) is not int or limit < 1:
        raise ValueError("character limit must be a positive integer")
    return limit

print(check_limit(80))                # 80
# check_limit(0)                      # ValueError if uncommented
```

The explicit type test rejects `True` even though Python treats `bool` as a subtype of `int`. This is one defensible rule for a numeric configuration value; write your policy before choosing validation. The exception message describes the violated condition without revealing a student's question or any secret.

**No exception is required for every user mistake:** an expected empty question might instead return a structured status such as `("EMPTY", "")`. In this node's project, a custom exception represents rejected input at a clean boundary. The important decision is that the calling code can **distinguish** accepted, rejected, and unexpectedly broken processing.

## 7. Custom exception and safe messages

A **custom exception** is your own exception type. Subclass a suitable built-in to communicate its meaning:

```python
class InvalidQuestionError(ValueError):
    """Question input violates the stated preparation contract."""


def require_question(raw):
    if not isinstance(raw, str):
        raise InvalidQuestionError("question must be text")
    clean = raw.strip()
    if clean == "":
        raise InvalidQuestionError("question is empty")
    return clean

print(require_question(" Explain AI "))  # Explain AI
```

The exception type tells a caller it is a known validation failure. The messages say **what needs correction** but do not include the supplied text. Avoid `raise ... (f"bad question: {raw}")` when `raw` might contain personal data or secrets. In production, record useful non-sensitive context such as a controlled error category and internal request identifier; keep full traceback details in protected developer diagnostics when appropriate.

An unexpected exception such as `AttributeError` due to a newly introduced coding bug should not be mislabeled `InvalidQuestionError` just to make the service continue. Catch only the category that the boundary knows how to handle.

## 8. Assertion and `assert`: a check for expectations

An **assertion** checks an expectation used by developers or tests:

```python
status = "READY"
assert status in {"READY", "EMPTY", "TOO_LONG"}
print("Expectation holds")
# assert 2 + 2 == 5              # AssertionError if uncommented
```

An `assert` whose expression is false raises `AssertionError`. It is useful in tests like those in QAI.01.22. **Do not use `assert` to validate untrusted inputs in a running application:** Python's optimised mode (`python -O`) can omit assert statements. Use an explicit `if` and raise a deliberate exception or return an error outcome. Tests, coverage, and regression design are expanded in QAI.01.24.

## 9. Defensive programming with clear failure boundaries

**Defensive programming** checks assumptions at the boundary where information enters and avoids turning bad data into misleading good-looking output. For the course utility:

- State the input contract: lesson record, required title, string question, positive integer limit.
- Validate these before `split`, `strip`, `len`, or formatting relies on them.
- Return a result or raise a well-defined validation exception; do not silently make up a course title.
- Catch a known exception where you can present a safe response; let unexpected bugs remain visible to protected diagnostics.
- Do not display raw learner questions or API keys in error messages, logs, or screenshots.
- Test normal, missing, wrong-type, and boundary cases; run the same failing input after a fix.

This is a **local** reliability step, not a claim that one Python file is a fully monitored production service. Structured logging, service monitoring, and wider incident procedures come later in the operations section.

## 10. Guided mini-project: `text_utils_checked.py`

Create this new file in `qai-path-lab/code-lab/`. It develops QAI.01.22's result construction with explicit input validation. It raises `InvalidQuestionError` for expected rejected inputs, catches it only at the display boundary, and leaves other errors visible.

```python
# text_utils_checked.py
class InvalidQuestionError(ValueError):
    """Known invalid lesson/question input with a safe error message."""


def prepare_request(lesson, raw_question, max_characters=80):
    """Return 'Course: <title> | Question: <clean>' for valid inputs.

    Reject invalid lesson/title/question/limit without echoing raw input.
    The limit counts Python string positions, not AI model tokens.
    """
    if not isinstance(lesson, dict):
        raise InvalidQuestionError("course record must be a dictionary")
    if "title" not in lesson or not isinstance(lesson["title"], str):
        raise InvalidQuestionError("course title is missing or invalid")
    title = lesson["title"].strip()
    if title == "":
        raise InvalidQuestionError("course title is missing or invalid")
    if not isinstance(raw_question, str):
        raise InvalidQuestionError("question must be text")
    if type(max_characters) is not int or max_characters < 1:
        raise InvalidQuestionError("character limit must be a positive integer")
    clean = " ".join(raw_question.split())
    if clean == "":
        raise InvalidQuestionError("question is empty")
    if len(clean) > max_characters:
        raise InvalidQuestionError("question exceeds character limit")
    return f"Course: {title} | Question: {clean}"


lesson = {"title": "GenAI"}
inputs = ["  Explain   AI  ", "   ", 42, "A" * 81]
for number, raw in enumerate(inputs, start=1):
    try:
        prepared = prepare_request(lesson, raw)
    except InvalidQuestionError as error:
        print(f"Request {number}: REJECT ({error})")
    else:
        print(f"Request {number}: READY ({prepared})")

# Normal, exactly at boundary, invalid and privacy-preserving error paths.
assert prepare_request(lesson, " A " * 1) == "Course: GenAI | Question: A"
assert prepare_request(lesson, "A" * 80) == (
    "Course: GenAI | Question: " + "A" * 80
)
for record, raw, limit, expected in [
    ({}, "Explain AI", 80, "course title is missing or invalid"),
    (lesson, "   ", 80, "question is empty"),
    (lesson, 42, 80, "question must be text"),
    (lesson, "A" * 81, 80, "question exceeds character limit"),
    (lesson, "Explain AI", 0, "character limit must be a positive integer"),
]:
    try:
        prepare_request(record, raw, max_characters=limit)
    except InvalidQuestionError as error:
        assert str(error) == expected
    else:
        raise AssertionError(f"expected rejection: {expected}")
assert lesson == {"title": "GenAI"}  # source record unchanged
print("Checks passed: 8")
```

Run with `py .\text_utils_checked.py` in Windows PowerShell (or the previously verified `python` command) or `python3 text_utils_checked.py` in Bash/Zsh.

**Expected output:**

```text
Request 1: READY (Course: GenAI | Question: Explain AI)
Request 2: REJECT (question is empty)
Request 3: REJECT (question must be text)
Request 4: REJECT (question exceeds character limit)
Checks passed: 8
```

**Trace of request 3:** `raw` is integer 42 → explicit type test is false → raise `InvalidQuestionError("question must be text")` → the matching `except` prints a safe rejection → later requests are still processed. The exception's message omits the actual question value.

**One limit of the demonstration:** the success output deliberately includes the cleaned question because it is a sample display. A real application's output and logs may need stricter handling for private learner text. The rejection messages themselves avoid echoing raw input.

### Controlled failure and repair

1. Change `lesson` to `{}`. All four requests produce `REJECT (course title is missing or invalid)`. The final assertion `lesson == {"title": "GenAI"}` fails because this change also alters the test fixture; restore the demo record before the full check run.
2. Change the fourth input to `"A" * 80`. Its result becomes `READY`. The separate assertion for 81 characters still confirms rejection.
3. In a **disposable copy only**, remove `isinstance(raw_question, str)` validation and use input 42. Calling `raw_question.split()` raises unexpected `AttributeError`, which the boundary's narrow `except InvalidQuestionError` does **not** catch. Restore the validation. The error identifies a missing precondition, not a reason to catch every exception.
4. Change a user-facing message to include `raw_question` and imagine it contains a private note. Undo that change: controlled category messages are enough to explain rejection without exposing the input.

## 11. Debug record: one failure investigated

Keep this format in `debug_log.md` or next to your notes; use fictional inputs:

| Field | Filled example |
|---|---|
| Observed result | request with integer question raised `AttributeError` in a disposable copy |
| Expected result | controlled “question must be text” rejection |
| Smallest reproducer | `prepare_request({"title": "GenAI"}, 42)` |
| Failing operation | `raw_question.split()` on an integer |
| Root cause | missing question-type validation before string operation |
| Fix | check `isinstance(raw_question, str)` and raise `InvalidQuestionError` |
| Regression check | same input now yields category message; normal text still prepares successfully |
| Privacy check | rejection does not include raw question or secrets |

**Important:** unlike the sample table, do not put real private learner text into a shared debug record. Keep enough information for diagnosis (type, failing operation, controlled identifier) and restrict any necessary detailed diagnostics.

## 12. Independent micro-lab with full solution

**Task:** write `required_course_code(record)`. A valid record is a dictionary with a nonblank string `"code"`. Return the trimmed code. For a missing key, non-string code, or blank string, raise a custom `InvalidCourseCode(ValueError)` with the fixed message `"course code is missing or invalid"`. At the call site, print one safe success or rejection line for each of three records: valid, missing, and blank. Do not print entire bad records.

**Complete solution:**

```python
class InvalidCourseCode(ValueError):
    """Course code failed an explicit input requirement."""


def required_course_code(record):
    """Return trimmed code; reject absent, wrong-type, or blank code."""
    if not isinstance(record, dict):
        raise InvalidCourseCode("course code is missing or invalid")
    if "code" not in record or not isinstance(record["code"], str):
        raise InvalidCourseCode("course code is missing or invalid")
    clean = record["code"].strip()
    if clean == "":
        raise InvalidCourseCode("course code is missing or invalid")
    return clean


records = [{"code": " QAI.01.23 "}, {}, {"code": "   "}]
for position, record in enumerate(records, start=1):
    try:
        code = required_course_code(record)
    except InvalidCourseCode as error:
        print(f"Record {position}: REJECT ({error})")
    else:
        print(f"Record {position}: READY ({code})")

assert required_course_code({"code": " AI "}) == "AI"
for bad in [{}, {"code": " "}, {"code": 42}, []]:
    try:
        required_course_code(bad)
    except InvalidCourseCode as error:
        assert str(error) == "course code is missing or invalid"
    else:
        raise AssertionError("expected an invalid-code exception")
print("Exercise checks passed: 5")
```

**Expected output:**

```text
Record 1: READY (QAI.01.23)
Record 2: REJECT (course code is missing or invalid)
Record 3: REJECT (course code is missing or invalid)
Exercise checks passed: 5
```

**Reasoning:** type and key checks occur before `.strip()`. The error message names a correctable category and never exposes a supplied record. The caller catches the custom type it can recover from. A different unexpected failure remains available for debugging.

## 13. What to remember and retain

- Syntax errors prevent parsing; runtime errors occur during execution; logical errors produce a wrong result without necessarily raising.
- Exception type and traceback help locate a failure; reproduce with the smallest safe input and identify the violated assumption.
- `try` encloses risky work; `except` handles a specific expected exception; `else` handles successful completion; `finally` handles work that must run after the attempt.
- `raise` signals a violated contract; a custom exception names a known error category.
- `assert` is for developer/test expectations, not untrusted-input validation; optimised Python may omit it.
- Defensive checks preserve useful error categories and keep personal data and secrets out of error messages.
- Save `text_utils_checked.py`, its successful output, the controlled wrong-type failure and repair, the filled debug record, and the exercise code. Explain to another learner why a blanket `except: pass` would be harmful here.

**Next:** QAI.01.24 uses reproducible tests, debugger steps, and regression cases to turn these fixes into lasting evidence.

---

**Node contract (S90):** `C | L3→L4 | H2–H3 | E3–E5 | A2–A4 | P0–P1`. All eighteen S86 error-handling items are addressed through a working mini-project, boundary checks, a minimal reproducer, a debug record, and a solved exercise. Actual learner evidence needs a local run and documented diagnosis; later L4 service operations are not established by this lesson alone.
