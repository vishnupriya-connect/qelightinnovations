# QAI.01.11 — Arithmetic Operations

> `QAI.01.10 Operators and operands` → **`QAI.01.11 Arithmetic operations`** → `QAI.01.12 Comparison and Boolean logic`

## 1. Destination: calculate and verify a course schedule

Suppose a course assistant must calculate total practice time, how many complete study blocks fit into a session, and how many minutes remain. You need more than a calculator-like list of symbols: you need to know which operation matches the question, what kind of result it gives, and how to test boundary cases.

By the end, you can predict and execute `+`, `-`, `*`, `/`, `//`, `%`, and `**`; explain positive, negative, and decimal results; calculate whole **quotients** and **remainders**; round a displayed value deliberately; and debug wrong types and division by zero. Work in the disposable `qai-path-lab/code-lab/` folder.

## 2. A number, an operation, and a result

An **arithmetic operator** asks Python to perform a calculation on numbers. An **operand** is a value it operates on. For `8 + 3`, 8 and 3 are operands; `+` is the operator; 11 is the expression result.

| Question | Python expression | Result | Meaning |
|---|---|---:|---|
 add 3 documents to 8 | `8 + 3` | 11 | total documents |
 remove 3 from 8 | `8 - 3` | 5 | documents remaining |
 3 rounds, 8 minutes each | `3 * 8` | 24 | total minutes |
 share 8 minutes among 2 tasks | `8 / 2` | 4.0 | minutes per task as a floating-point result |

The same `+` symbol can join strings instead of adding numbers. The type and intended meaning of each operand matter. From `QAI.01.08`, `"8" + "3"` produces `"83"`; it is not a count of 11.

## 3. Addition and subtraction

The **addition operator** `+` combines numerical quantities. The **subtraction operator** `-` finds a difference or removes an amount:

```python
source_documents = 8
added_documents = 3
print(source_documents + added_documents)  # 11
print(source_documents - added_documents)  # 5
```

Ask which direction the question goes: “current 8 plus 3 added” gives 11; “current 8 minus 3 removed” gives 5. Reversing subtraction changes the answer: `8 - 3` is 5, while `3 - 8` is -5.

A **positive number** is greater than zero, such as 5; `+5` explicitly shows a positive sign. A **negative number** is below zero, such as -5. Zero is neither positive nor negative. A leading `-` in `-5` acts as a unary sign, unlike subtraction with two operands. You can compute negative remaining capacity, but in a real scheduler that would mean you have overbooked, not that a negative number of seats physically exists.

## 4. Multiplication

The **multiplication operator** `*` combines a quantity and a number of groups:

```python
rounds = 3
minutes_per_round = 8
print(rounds * minutes_per_round)  # 24
```

Say the units aloud: `3 rounds × 8 minutes per round = 24 minutes`. Python will calculate `3 * 8` even if you accidentally supply unrelated quantities; correct units are your responsibility.

`2 * (3 + 4)` is 14 because grouping makes 3 + 4 equal 7 before multiplication. Without parentheses, `2 * 3 + 4` is 10. You already traced precedence and grouping in `QAI.01.10`.

## 5. Division `/`: a numerical quotient

The **division operator** `/` asks how much is in each equal share. Its answer is a **quotient**:

```python
print(8 / 2)      # 4.0
print(7 / 2)      # 3.5
print(type(8 / 2))  # <class 'float'>
```

Even `8 / 2` produces `4.0`, a float. A **decimal number** has a fractional representation such as 3.5. For 7 study minutes spread across 2 equal tasks, 3.5 minutes per task can make sense. For 7 indivisible documents placed in folders, fractional documents do not make sense; use whole-block division and a remainder instead.

**Do not divide by zero.** `7 / 0` raises `ZeroDivisionError` because Python cannot form a finite quotient. `7 // 0` and `7 % 0` also fail. The defect is the divisor, the value on the **right** of the operator.

## 6. Floor division `//`: complete blocks

The **floor-division operator** `//` gives a **floor quotient**: the exact numerical division result rounded **down toward negative infinity** to a whole-number level. With two integer operands its result is an integer:

```python
print(7 // 2)      # 3
print(type(7 // 2))  # <class 'int'>
```

Seven practice questions can fill three complete sets of two, leaving one question. For **nonnegative** counts, this looks like “discard the fractional part.” That description fails for negative values: `-7 / 2` is -3.5, and flooring down gives `-7 // 2 == -4`, not -3. When a float is an operand, `//` still floors the quotient but the result may have float type, such as `7.0 // 2 == 3.0`. Inspect type if it matters.

**Unit choice:** use `//` only when the question asks for completed equal-size blocks or another floor quotient. It is not a replacement for ordinary division when fractional results are meaningful.

## 7. Remainder `%`: what does not fill a block?

The **remainder operator** `%` finds what is left after floor division. The **remainder** is the part that does not make another full block:

```python
print(7 // 2)  # 3 complete groups
print(7 % 2)   # 1 left over
print(7 == (7 // 2) * 2 + (7 % 2))  # True
```

The final line verifies `dividend = floor quotient × divisor + remainder`. Here the **dividend** is the number being divided (7), and the **divisor** is the block size (2). For nonnegative integers with a positive divisor, the remainder lies between zero and one less than the divisor. A common use is wrapping around a fixed number of positions; that use appears when indexing and loops are studied.

### Negative inputs: calculate rather than guess

Flooring moves toward **negative infinity**, not toward zero. Python's remainder takes the sign of the divisor or is zero for these integer examples:

| Expression | Floor quotient | Remainder | Check |
|---|---:|---:|---|
 `7 // 3` and `7 % 3` | 2 | 1 | 7 = 2 × 3 + 1 |
 `-7 // 3` and `-7 % 3` | -3 | 2 | -7 = -3 × 3 + 2 |
 `7 // -3` and `7 % -3` | -3 | -2 | 7 = -3 × -3 + -2 |
 `-7 // -3` and `-7 % -3` | 2 | -1 | -7 = 2 × -3 + -1 |

For `-7 // 3`, the ordinary division result is about -2.33; floor down to -3. Then `-7 - (-3 × 3) = 2`. This is why `-7 % 3` is 2. Do not carry a “discard the decimal digits” rule from the positive case to negative values. Python's [expression reference](https://docs.python.org/3/reference/expressions.html) specifies floor division and modulo behavior.

## 8. Exponentiation `**`: repeated powers

The **exponentiation operator** `**` raises a base to a power:

```python
print(2 ** 3)      # 8 = 2 * 2 * 2
print(10 ** 2)     # 100
print((2 + 1) ** 2) # 9
```

`2 ** 3` means “2 raised to the power 3,” not “2 multiplied by 3.” For a tiny illustrative search space with two choices repeated across three independent positions, `2 ** 3` gives eight possible arrangements. Do not assume such a toy formula models a real language model's behaviour; it only illustrates arithmetic growth.

Precedence still matters: `-2 ** 2` gives -4 because it is grouped as `-(2 ** 2)`; `(-2) ** 2` gives 4. Chained powers group from the right, as shown in `QAI.01.10`.

## 9. Rounded values: presentation versus underlying result

A **rounded value** is a nearby value chosen for a requested level of display or calculation. Python's `round(number, digits)` can produce a value rounded to a specified number of decimal places:

```python
hours = 95 / 60
print(hours)           # 1.5833333333333333 on a typical Python installation
print(round(hours, 2)) # 1.58
```

`round(hours, 2)` returns a new rounded value; `hours` itself still refers to the earlier unrounded value unless you assign a new result. “Show 1.58 hours” is different from “95 minutes became exactly 1.58 hours.”

**Rounding is not the same as `int()` or `//`.** `int(2.9)` gives 2 by discarding its fractional part; `round(2.9)` gives 3; `2.9 // 1` gives 2.0. For halfway cases Python's built-in `round` chooses the nearest even result: `round(2.5) == 2` and `round(3.5) == 4`. Binary floating-point representation can also affect apparent decimal ties. Do not assume `round` implements every billing or grading policy; state the required policy and choose a method accordingly. See the [official `round` specification](https://docs.python.org/3/library/functions.html#round) and [floating-point explanation](https://docs.python.org/3/tutorial/floatingpoint.html).

## 10. Guided lab: course practice blocks

Create `arithmetic_operations.py` inside `qai-path-lab/code-lab/`:

```python
# Fictional lesson schedule: minutes are nonnegative whole numbers.
available_minutes = 95
minutes_per_block = 30

full_blocks = available_minutes // minutes_per_block
leftover_minutes = available_minutes % minutes_per_block
hours_exact = available_minutes / 60
hours_display = round(hours_exact, 2)

print("Whole blocks:", full_blocks)
print("Leftover minutes:", leftover_minutes)
print("Hours displayed:", hours_display)
print("Reconstructed minutes:", full_blocks * minutes_per_block + leftover_minutes)
```

**Predict first:** 95 minutes contain three complete 30-minute blocks; 90 minutes are used and 5 remain; 95 / 60 is approximately 1.5833 hours, displayed as 1.58. Expected output:

```text
Whole blocks: 3
Leftover minutes: 5
Hours displayed: 1.58
Reconstructed minutes: 95
```

The reconstruction is a quick consistency check. Run from `code-lab`: `py .\arithmetic_operations.py` in Windows PowerShell, using `python` if that was your verified interpreter; on macOS/Linux use `python3 arithmetic_operations.py`.

**Controlled variation:** change only `available_minutes = 95` to `available_minutes = 100`. Predict 3 complete blocks, 10 minutes left, `round(100 / 60, 2) == 1.67` hours displayed, and a reconstruction of 100. Save, run, compare, then restore the original value.

## 11. Safe failure experiment: zero divisor and wrong type

Run each in a **new disposable** file so the correct schedule script stays intact.

```python
print(7 / 0)  # raises ZeroDivisionError
```

The operation cannot return a valid numeric quotient; inspect the traceback. **Repair:** change the divisor to a known nonzero value, such as 2; `7 / 2` produces 3.5. In a real program, verify a received divisor is nonzero before calculation.

```python
entered_minutes = "95"
print(entered_minutes // 30)  # raises TypeError
```

`entered_minutes` is text. **Repair only if the text really represents a whole-number duration:** use `minutes = int(entered_minutes)`, then `print(minutes // 30)` to get 3. Invalid text needs the conversion handling you practised in `QAI.01.08`.

| Symptom | Likely cause | First check |
|---|---|---|
 `ZeroDivisionError` | divisor is zero | print or inspect the right operand before division |
 `TypeError` for `//` | input is text or another unsuitable type | inspect `repr(value)` and `type(value)` |
 unexpected negative `//` or `%` result | assumed truncation toward zero | calculate floor quotient, then reconstruct original using divisor and remainder |
 result `4.0` instead of `4` | used ordinary `/` | decide if fractional-capable result or complete blocks are intended |
 displayed 1.58 mistaken for exact hours | rounded for presentation | retain original minutes or unrounded value for later calculations |

## 12. Independent practice with complete solution

**Task:** a fictional workshop has 73 available minutes. Each complete practice block takes 12 minutes. Calculate complete blocks, leftover minutes, exact numerical hours, and hours rounded to two decimal places. Verify the block calculation by reconstructing 73. Then predict results if available time becomes -73 minutes with a positive 12-minute divisor. Negative time is a diagnostic exercise, **not** a usable schedule.

**Worked solution — `workshop_blocks.py`:**

```python
available_minutes = 73
block_minutes = 12

full_blocks = available_minutes // block_minutes
leftover = available_minutes % block_minutes
exact_hours = available_minutes / 60

print("Blocks:", full_blocks)
print("Leftover:", leftover)
print("Hours:", exact_hours)
print("Hours shown:", round(exact_hours, 2))
print("Reconstructed:", full_blocks * block_minutes + leftover)
```

**Expected:** 6 complete blocks, 1 minute left, `73 / 60 == 1.2166666666666666` on a typical Python installation, displayed hours 1.22, reconstructed 73. The exact printed floating-point digits may vary across implementations; the number is approximately 1.2167.

**Negative diagnostic:** `-73 // 12 == -7` and `-73 % 12 == 11`, because `-7 * 12 + 11 == -73`. A proposed rule “drop fractional digits” would predict -6 and is wrong here. A scheduler should separately reject a negative duration; this arithmetic diagnosis does not mean a negative schedule is valid.

## 13. Evidence and technical recall

Keep `arithmetic_operations.py`, `workshop_blocks.py`, and a short `arithmetic_trace.md` with predicted and actual outputs for 95 and 100 minutes, the worked 73-minute result, one `ZeroDivisionError` and repair, and the equation `-73 = (-7 × 12) + 11`.

**Remember:** `/` returns a fractional-capable quotient; `//` floors; `%` gives the compatible remainder; `**` raises to a power; `round` produces a rounded result according to its rules. For positive counts, `//` and `%` mean complete blocks and leftovers. For negative operands, verify with `dividend = quotient × divisor + remainder`. Always check type, units, divisor, and whether a rounded value is only for display.

## 14. Next connection

`QAI.01.12 — Comparison and Boolean logic` uses numerical results to answer yes/no questions: “Is there enough time?”, “Is this count valid?”, and “Should this branch run?”.
