# QAI.01.24 — Debugging and Testing

> QAI.01.23 Errors and exception handling → **QAI.01.24 Debugging and testing** → QAI.01.25 Modules and imports

## 1. Destination: prove a fix stays fixed

A course-question function may work for `"Explain AI"` yet fail for a blank question, an absent title, or exactly 80 characters. **Debugging** means finding the cause of an observed mismatch and correcting it. **Testing** means checking specified inputs against specified results so future changes do not quietly reintroduce the mistake.

Your P1 result here is a runnable `test_text_utils.py` test suite for the function developed in QAI.01.23, plus a short expected-versus-actual and fix record. You will intentionally introduce one boundary bug in a disposable copy, see a test fail, and restore the correct comparison. Do this with fictional input only.

## 2. Test, test case, input, expected output, actual output

A **test** compares behaviour with a requirement. A **test case** specifies:

- **test input:** what is supplied;
- **expected output:** the result the requirement calls for;
- **actual output:** what the program produced;
- **decision:** pass when they agree, investigate when they differ.

For the rule “allow a cleaned question of at most 80 characters”:

| Test input | Expected output | Actual output from correct function | Decision |
|---|---|---|---|
| `" Explain AI "` | formatted `Explain AI` | formatted `Explain AI` | pass |
| `"A" * 80` | accepted | accepted | pass |
| `"A" * 81` | rejected as too long | rejected as too long | pass |
| `"   "` | rejected as empty | rejected as empty | pass |

The difference between lengths 80 and 81 tests the exact **boundary**. If the 80-character input is rejected, a likely defect is `>= 80` where the requirement says `> 80`. A passing normal example alone does not test the boundary.

## 3. Debugging by a small reproducible case

Suppose the earlier `prepare_request` rejects `"A" * 80` after you edit its threshold. Reproduce with the smallest clear input that shows the failure:

```python
def accepted_length(clean, limit=80):
    return len(clean) <= limit

print(accepted_length("A" * 80))    # True
print(accepted_length("A" * 81))    # False
```

**Reasoning:** 80 must pass and 81 must fail. Inspect the comparison in the full function. If it currently says `if len(clean) >= max_characters:`, change `>=` to `>`, rerun **the same failing input**, and rerun the rest of the test suite. This is a **logical error**: code executes without an exception but contradicts the stated rule.

Do not “fix” the expected result to match the broken code unless the underlying requirement has actually changed. Retain a test for the discovered defect: that is a **regression test**.

## 4. Debug output and print debugging

**Debug output** is temporary information that helps locate where a result diverges. **Print debugging** inserts temporary `print` statements:

```python
raw = "  AI  "
clean = " ".join(raw.split())
limit = 80
print("debug raw type:", type(raw).__name__)   # str
print("debug cleaned length:", len(clean))     # 2
print("debug over limit:", len(clean) > limit) # False
```

Print *type, length, controlled status, and branch choice*, not the raw question when it might contain private student text or a secret. Remove or control debug prints after diagnosis; a production error response should not expose internal implementation details.

A debugger is often better than adding many prints because you can pause and inspect state without editing every code path.

## 5. Breakpoint and debugger: pause at the decision

A **debugger** is a tool that pauses a program and lets you inspect its execution. A **breakpoint** identifies where to pause. With a local Python file open in VS Code:

1. Put a breakpoint on the line `if len(clean) > max_characters:` in `text_utils_checked.py`.
2. Run a local demonstration under the Python debugger using fictional `"A" * 80` input.
3. When paused, **inspect variable** values: `len(clean)` and `max_characters`.
4. **Watch expression:** enter `len(clean) > max_characters`; expected value at length 80 is `False`.
5. Move one instruction at a time and record which branch executes.

In VS Code's Python debugger, **Step Into** (typically F11) enters a called function; **Step Over** (typically F10) executes a call without entering its body; **Step Out** (typically Shift+F11) finishes the current function and returns to its caller. Key bindings can differ; use the visible debugger controls if yours do. For a call from a test:

- Step Into `prepare_request(...)` to see validation and cleaning.
- Step Over `len(clean)` when you only need its returned number.
- Step Out to return from `prepare_request` to the test call.

The Python built-in `breakpoint()` can also pause into a configured debugger in a local run, but a breakpoint left in a shared or automated script can interrupt execution. Use local controlled examples; remove breakpoints and accidental sensitive watch expressions before sharing output.

## 6. Unit test and edge case

A **unit test** checks one small unit of behaviour—in this lesson, the question-preparation function—with controlled inputs and outcomes. An **edge case** is an input at a boundary or an unusual but allowed condition. Useful cases for this contract:

- normal: surrounding/repeated spaces produce one-line cleaned text;
- boundary: exactly 80 accepted, 81 rejected;
- invalid: no title, wrong question type, nonpositive limit;
- privacy: error message does not contain raw private text;
- mutation: source dictionary remains unchanged.

Unit tests reduce uncertainty about this function. They do not prove security, model correctness, integration with a live API, or production availability.

## 7. Make the two runnable project files

Place these files together in `qai-path-lab/code-lab/`. The first contains the callable function from QAI.01.23 **without demonstration code running on import**. The second imports it for tests. **Import** here means making the definitions in one Python file usable from another; QAI.01.25 explains that mechanism in depth. `unittest` is a testing library included with Python, so this exercise needs no extra package.

### File 1: `text_utils_checked.py`

```python
# text_utils_checked.py
class InvalidQuestionError(ValueError):
    """Known invalid course/question input with a safe error message."""


def prepare_request(lesson, raw_question, max_characters=80):
    """Return a formatted course request, or raise InvalidQuestionError."""
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
```

### File 2: `test_text_utils.py`

```python
# test_text_utils.py
import unittest
from text_utils_checked import InvalidQuestionError, prepare_request


class PrepareRequestTests(unittest.TestCase):
    def test_normalisation_and_format(self):
        actual = prepare_request({"title": " GenAI "}, "  Explain   AI \n")
        self.assertEqual(actual, "Course: GenAI | Question: Explain AI")

    def test_exactly_at_limit_is_accepted(self):
        actual = prepare_request({"title": "GenAI"}, "A" * 80)
        self.assertEqual(actual, "Course: GenAI | Question: " + "A" * 80)

    def test_one_over_limit_is_rejected(self):
        with self.assertRaisesRegex(InvalidQuestionError, "exceeds character limit"):
            prepare_request({"title": "GenAI"}, "A" * 81)

    def test_empty_question_is_rejected(self):
        with self.assertRaisesRegex(InvalidQuestionError, "question is empty"):
            prepare_request({"title": "GenAI"}, "   ")

    def test_required_title_is_rejected_if_absent(self):
        with self.assertRaisesRegex(InvalidQuestionError, "title is missing or invalid"):
            prepare_request({}, "Explain AI")

    def test_wrong_question_type_is_rejected(self):
        with self.assertRaisesRegex(InvalidQuestionError, "question must be text"):
            prepare_request({"title": "GenAI"}, 42)

    def test_error_does_not_echo_private_input(self):
        # Fictional marker only; never put an actual private value in a test.
        marker = "fictional-private-marker" * 10
        with self.assertRaises(InvalidQuestionError) as caught:
            prepare_request({"title": "GenAI"}, marker, max_characters=5)
        self.assertNotIn(marker, str(caught.exception))
        self.assertEqual(str(caught.exception), "question exceeds character limit")

    def test_source_record_is_unchanged(self):
        lesson = {"title": " GenAI "}
        prepare_request(lesson, "Explain AI")
        self.assertEqual(lesson, {"title": " GenAI "})


if __name__ == "__main__":
    unittest.main()
```

Run from the folder containing both files:

- Windows PowerShell: `py -m unittest -v test_text_utils` (or use the verified `python` interpreter).
- Bash/Zsh: `python3 -m unittest -v test_text_utils`.

Expected result: **8 tests run, all OK**. The runner prints each test name; exact timing and file paths depend on the machine. The `if __name__ == "__main__":` guard also lets you run the test file directly without automatically running it on import; this guard is explained fully in QAI.01.25.

**Why this is not merely duplicating the function:** tests are chosen from *requirements* and failure history: whitespace normalisation, the 80/81 boundary, missing required data, wrong type, privacy of rejection, and no mutation of the caller's record. Changing a function implementation should still leave these observable contracts intact.

## 8. Controlled defect → failing test → repair

Make a disposable copy of `text_utils_checked.py` or save a reversible edit. Replace just `if len(clean) > max_characters:` with `if len(clean) >= max_characters:`. Rerun the suite:

- `test_exactly_at_limit_is_accepted` fails, because length 80 now raises `InvalidQuestionError` instead of returning the formatted request.
- `test_one_over_limit_is_rejected` still passes, so a single “long input rejected” test alone would not expose this bug.
- Restore `>` and rerun. All eight tests should pass again.

This is a **regression test**: keep the length-80 case in the suite after the repair. If the real requirement later changes to reject length 80, update the documented contract and affected tests together, and review the reason.

## 9. Expected-versus-actual investigation record

Use a short table after reproducing a bug. Here is a complete example with fictional input:

| Field | Record |
|---|---|
| Test input | course title `GenAI`, question `"A" * 80`, limit 80 |
| Expected output | formatted request; exactly 80 allowed |
| Actual output (deliberately broken `>=` variant) | `InvalidQuestionError: question exceeds character limit` |
| Failing condition | `len(clean) >= max_characters` evaluated `80 >= 80` → `True` |
| Root cause | threshold operator disagreed with documented rule |
| Fix | change `>=` to `>` |
| Regression test | `test_exactly_at_limit_is_accepted` |
| Post-fix result | 8 tests OK, including the 81 rejection |
| Privacy check | no real learner text placed in shared report |

Keep this as `debug_log.md` or next to the note for your project evidence. A test failure tells you **where a mismatch is observed**, not automatically the root cause; the trace and controlled edit establish the cause.

## 10. Independent task with full solution

**Task:** a course score of 70 or higher receives `"PASS"`; a smaller nonnegative score receives `"REVIEW"`; a negative score is invalid. Write `score_status(score)` and a small `unittest` suite covering 69, 70, 71, and -1. Then describe which test would catch an accidental `score > 70` threshold.

**Complete runnable solution** (save separately as `test_score_status.py`):

```python
import unittest


def score_status(score):
    """Return PASS/REVIEW for nonnegative integer score; reject invalid data."""
    if type(score) is not int or score < 0:
        raise ValueError("score must be a nonnegative integer")
    if score >= 70:
        return "PASS"
    return "REVIEW"


class ScoreStatusTests(unittest.TestCase):
    def test_below_boundary(self):
        self.assertEqual(score_status(69), "REVIEW")

    def test_at_boundary(self):
        self.assertEqual(score_status(70), "PASS")

    def test_above_boundary(self):
        self.assertEqual(score_status(71), "PASS")

    def test_negative_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonnegative integer"):
            score_status(-1)


if __name__ == "__main__":
    unittest.main()
```

Run with `py -m unittest -v test_score_status` on Windows or `python3 -m unittest -v test_score_status` in Bash/Zsh. **Expected:** 4 tests, OK. An accidental `score > 70` makes `test_at_boundary` fail because score 70 would return `REVIEW`. This is a fictional programming exercise, not a rule for evaluating actual student competence.

## 11. Where L4 practice begins

Before using this code in a real application, decide:

- how failed requests are identified without storing raw personal questions in routine logs;
- which validation failures the user can correct and which indicate a faulty integration;
- how a failure is reported without a stack trace, secret, or private payload in the user response;
- who owns regression tests and checks they run during code changes;
- what additional integration, security, load, and monitoring tests the deployment requires.

These are operational responsibilities to practise in later projects. The eight local unit tests are evidence for their **specified contracts**, not proof of end-to-end reliability.

## 12. What to remember and retain

- Debugging: reproduce → isolate → inspect state → correct cause → rerun failing case and wider suite.
- A test case needs input, **expected** output, and observed **actual** output; a passing run without an expectation is weak evidence.
- Edge cases include boundaries, missing input, wrong types, and empty input.
- Unit tests check one small behaviour; a regression test preserves a fix against later changes.
- A breakpoint pauses code; step into enters a call, step over executes without entering, step out returns; inspect variables and watch expressions at the decision point.
- Keep both runnable files, the eight-test success result, a deliberate failing-boundary result followed by a repaired run, the expected-versus-actual debug record, and the four-test exercise solution. Use fictional data in all shared artifacts.

**Next:** QAI.01.25 teaches how Python finds the module you imported and how to keep reusable functions separate from runnable demonstration code.

---

**Node contract (S90):** `C | L3→L4 | H2–H3 | E3–E5 | A2–A5 | P0–P1`. All eighteen S86 debugging/testing topics are covered with a runnable test suite, controlled regression, debugger walkthrough, expected-versus-actual record, and complete solved task. Learner evidence requires executing the suite, observing the deliberate failure, and retaining the repair record.
