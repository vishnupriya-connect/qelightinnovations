# QAI.01.12 — Comparison and Boolean Logic

> `QAI.01.11 Arithmetic operations` → **`QAI.01.12 Comparison and Boolean logic`** → `QAI.01.13 String basics`

## 1. Destination: turn a calculated value into a decision

The course assistant can count source documents. Now it must answer: “Is the count within the permitted range?” and “Has the material been approved?” **Comparison** produces yes/no results; **Boolean logic** combines those results. This is how a program decides whether a task is ready for its next step.

You will predict comparisons and complete truth tables, run safe boundary tests, show when Python skips part of an expression, and debug mistakes that can approve an invalid value. The code uses fictional counts and flags inside `qai-path-lab/code-lab/`. Conditional `if` branches and richer input validation are studied later; you can learn and test the expressions here without building a whole application.

## 2. Comparison operators produce Boolean results

A **comparison operator** asks about the relationship between two values. A **Boolean result** is `True` or `False`. A **Boolean expression** is an expression evaluated for a yes/no result.

```python
document_count = 3
print(document_count == 3)  # True
print(document_count != 3)  # False
print(document_count > 2)   # True
print(document_count < 2)   # False
print(document_count >= 3)  # True
print(document_count <= 3)  # True
```

| Operator | Name | Read `count OP 3` as | Result when count is 3 |
|---|---|---|---|
 `==` | equality | equal to 3? | `True` |
 `!=` | inequality | different from 3? | `False` |
 `>` | greater than | more than 3? | `False` |
 `<` | less than | fewer than 3? | `False` |
 `>=` | greater than or equal | at least 3? | `True` |
 `<=` | less than or equal | at most 3? | `True` |

**Boundary language:** “At least three” includes 3, so use `>= 3`; “more than three” excludes 3, so use `> 3`. “At most five” includes 5. Always test the equality boundary, not just values far away from it.

**Assignment versus comparison:** `count = 3` assigns a value to a name; `count == 3` checks equality and produces a Boolean. Mixing them changes a program's meaning. `==` asks about **value equality**; `is` asks whether two references identify the **same object**, as studied in `QAI.01.09`. Use `is None` to check for the special absent value, and `==` for ordinary value equality.

## 3. The types being compared matter

```python
print(3 == "3")  # False: number and text do not compare equal
print(3 < 5)     # True: comparable numbers
```

`3 < "5"` raises `TypeError` in Python 3: a numerical order is not defined between an integer and this string. Do not “fix” it by automatically converting every identifier or title into a number; first establish what the input represents.

An equality result alone does not prove values have identical types. For example, `True == 1` is `True` in Python because `bool` is related to the numeric type `int`. To validate an actual yes/no flag, inspect its type and intended meaning, not just an equality comparison with 1. This note uses real Boolean values `True` and `False` for approval flags.

## 4. Truth value and logical operators

A **truth value** is how Python interprets a value when a yes/no answer is needed. A `bool` value already gives that answer. Some other values are false-like (`0`, `""`, `None`, an empty list); nonempty text such as `"False"` is true-like. You saw these distinctions in `QAI.01.08`.

A **logical operator** combines or reverses yes/no interpretations:

- `and`: both conditions must be true.
- `or`: at least one condition must be true.
- `not`: reverse the truth value.

```python
enough_documents = True
approved = False
print(enough_documents and approved)  # False
print(enough_documents or approved)   # True
print(not approved)                    # True
```

For a course assistant, “enough **and** approved” means both requirements. “Enough **or** approved” accepts either one; that would be a mistake if both requirements are mandatory. Translate the requirement into plain words before choosing the operator.

## 5. Build the truth tables once, then use them

A **truth table** lists every possible combination of Boolean inputs and the resulting output.

| A | B | `A and B` | `A or B` |
|---|---|---|---|
 `False` | `False` | `False` | `False` |
 `False` | `True` | `False` | `True` |
 `True` | `False` | `False` | `True` |
 `True` | `True` | `True` | `True` |

| A | `not A` |
|---|---|
 `False` | `True` |
 `True` | `False` |

**How to remember:** `and` is true only in the last row, when **both** inputs are true. `or` is false only in the first row, when **neither** input is true. `not` reverses a Boolean. Use the table to check the four approval cases instead of relying on a vague everyday reading of “or.”

## 6. Compose a real rule, then check its boundaries

Suppose a fictional exercise needs at least 1 source document, permits at most 5, and requires approval:

```python
document_count = 5
approved = True
valid_count = 1 <= document_count <= 5
ready = valid_count and approved
print("Valid count:", valid_count)  # True
print("Ready:", ready)              # True
```

`1 <= document_count <= 5` is Python's **chained comparison**: the count must be at least 1 **and** at most 5. With a simple variable, it expresses the same condition as `(1 <= document_count) and (document_count <= 5)`. The count at either boundary is accepted.

| document_count | approved | valid count? | ready? | Why? |
|---:|---|---|---|---|
 0 | `True` | `False` | `False` | below minimum |
 1 | `True` | `True` | `True` | lower boundary included |
 5 | `True` | `True` | `True` | upper boundary included |
 6 | `True` | `False` | `False` | above maximum |
 3 | `False` | `True` | `False` | approval missing |

**Worked bug:** `valid_count or approved` with count 6 and `approved = True` produces `True`. That rule lets approval excuse an invalid count. The stated requirement says both checks are mandatory, so it needs `and`.

## 7. Precedence and parentheses: state your rule visibly

For these operators, comparison groups before `not`, `not` before `and`, and `and` before `or`. Parentheses make the intended policy readable:

```python
print(not 3 == 4)                  # True; read as not (3 == 4)
print((True or False) and False)   # False
print(True or (False and False))   # True
```

Without parentheses, `True or False and False` is `True` because `and` groups first. If the intended rule is “either A or B, and additionally C,” write `(A or B) and C`. Avoid using a memorised precedence list as a substitute for stating the requirement in words.

## 8. Short-circuit evaluation: when the right side is skipped

**Short-circuit evaluation** means Python may decide the logical result from the left operand and **not evaluate** the right operand.

- `False and ...` cannot make both sides true, so the right side is skipped.
- `True or ...` is already true, so the right side is skipped.
- `True and ...` needs the right side; `False or ...` needs the right side.

The following expressions prove the skipping using an operation that would fail if reached. `1 / 0` by itself raises `ZeroDivisionError`:

```python
print(False and (1 / 0))  # False: division skipped
print(True or (1 / 0))    # True: division skipped
```

Do **not** run `True and (1 / 0)` in your main lab expecting a Boolean: it evaluates the division and raises `ZeroDivisionError`. This difference tells you precisely which operand Python needed.

### Safe numerical guard

```python
divisor = 0
enough_per_group = (divisor != 0) and (12 / divisor >= 3)
print(enough_per_group)  # False; no division occurred
```

If `divisor` becomes 2, the left check is true; 12 / 2 is 6, which is at least 3, so the result is `True`. If `divisor` becomes 6, 12 / 6 is 2, so it is `False`. **Order matters:** put the protection check on the left. `(12 / divisor >= 3) and (divisor != 0)` would attempt division before checking zero.

This is a small instructional guard for a numerical value. In a larger program, input types, domain rules, and errors still require explicit validation; a single short-circuit expression does not validate everything.

## 9. One precise caveat: `and` and `or` can return an operand

When the inputs are actual Boolean values, the examples above return `True` or `False`. With other values, Python's `and`/`or` return one of the values evaluated, **not necessarily a `bool`**:

```python
print("" or "Untitled")  # Untitled (string)
print(0 and (1 / 0))    # 0 (integer; right side skipped)
print(not "")           # True (not always returns a Boolean)
```

This explains why an expression such as `count == 1 or 2` is wrong for “count is 1 or 2.” When the first comparison is false, `or` returns the truthy integer 2:

```python
count = 5
print(count == 1 or 2)               # 2, not False
print((count == 1) or (count == 2))  # False
```

For this lesson's policy checks, write a complete comparison on **each side** of `or`, or use the simpler chained comparison when testing a range. Python's [Boolean operations reference](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not) describes the short-circuit and operand-return behavior.

## 10. Guided lab: a document readiness check

Create `logic_lab.py` in `qai-path-lab/code-lab/`. Predict the output before running:

```python
# Fictional course document checks; no files or services are accessed.
document_count = 5
approved = True
minimum = 1
maximum = 5

valid_count = minimum <= document_count <= maximum
ready = valid_count and approved
needs_review = not approved

print("Valid count:", valid_count)
print("Approved:", approved)
print("Ready:", ready)
print("Needs review:", needs_review)

divisor = 0
safe_group = (divisor != 0) and (12 / divisor >= 3)
print("Safe group:", safe_group)
```

**Expected output:**

```text
Valid count: True
Approved: True
Ready: True
Needs review: False
Safe group: False
```

Run from `code-lab`: `py .\logic_lab.py` in Windows PowerShell, using `python` if that is your verified interpreter; `python3 logic_lab.py` in Bash/Zsh.

**Controlled variation, one change at a time:** set `document_count` to 0, 1, 6 and predict `Ready`: False, True, False while approval remains true. Restore count 5, then change only `approved` to `False`: `Ready` becomes False and `Needs review` becomes True. Restore it; change `divisor` to 2 and then 6: `Safe group` becomes True and then False. These runs are your **boundary tests**; record each prediction beside its observed output.

## 11. Debug the rule, not just the syntax

| Mistake | Observed effect | Correction |
|---|---|---|
 `valid_count or approved` used for two mandatory checks | count 6 with approval True passes | use `valid_count and approved` |
 `document_count > 1` for “at least 1” | count 1 wrongly rejected | use `>= 1` |
 `count == 1 or 2` | count 5 produces truthy integer 2 | write `count == 1 or count == 2` |
 guard written after division | denominator zero raises before check | evaluate `divisor != 0` first, with `and` |
 `approved = "False"` | nonempty string is truthy | use Boolean `False`; validate received text before using it |
 `3 < "5"` | `TypeError` | establish the intended type and validate conversion if appropriate |

**Debug sequence:** restate the policy in plain English, identify each Boolean expression, evaluate its boundary values, compare with a truth-table row, then run the corrected code. A syntactically valid condition can still enforce the wrong policy.

## 12. Independent exercise with complete solution

**Task:** a fictional lesson needs at least 2 documents, permits at most 5, and requires instructor approval. Write `lesson_gate.py` to print `Allowed: True/False`. Separately, protect the calculation `18 / group_size >= 3` from a zero group size. Predict the outcome for (documents, approval, group size): (2, True, 0), (5, True, 3), (6, True, 3), and (3, False, 3). Change inputs for each run; do not change the rule.

**Worked solution:**

```python
documents = 2
approved = True
group_size = 0

count_ok = 2 <= documents <= 5
allowed = count_ok and approved
group_ok = (group_size != 0) and (18 / group_size >= 3)

print("Allowed:", allowed)
print("Group sufficient:", group_ok)
```

| documents | approved | group_size | Allowed | Group sufficient | Reason |
|---:|---|---:|---|---|---|
 2 | `True` | 0 | `True` | `False` | lower count boundary allowed; division skipped |
 5 | `True` | 3 | `True` | `True` | upper boundary allowed; 18 / 3 = 6 |
 6 | `True` | 3 | `False` | `True` | document count above 5, separate grouping calculation still works |
 3 | `False` | 3 | `False` | `True` | missing approval; grouping calculation still works |

Two displayed checks answer **different** questions. `Allowed` depends on document count and approval; `Group sufficient` depends on group size. If the product later requires **both** before proceeding, a future branch would combine those Boolean results with `and`. This separation makes it easier to test each rule independently.

## 13. Evidence and recall

Keep `logic_lab.py`, `lesson_gate.py`, and `expression_trace.md` with the completed `and/or/not` truth tables, the five boundary cases from `10, the four independently tested cases from `12, one short-circuit prediction and observation, and one repaired logic mistake from `11. The notes should distinguish **predicted** from **observed** results.

**Remember:** comparisons yield Booleans; `==` checks equality while `=` assigns; `and` requires both, `or` at least one, and `not` reverses; boundary words (“at least,” “at most”) determine whether equality is included; short-circuit can skip the right side; `and/or` with non-Boolean operands can return an operand rather than a Boolean.

## 14. Next connection

`QAI.01.13 — String basics` studies the text in course titles, user questions, document names, and prompts: characters, quotes, length, indexes, and slices.
