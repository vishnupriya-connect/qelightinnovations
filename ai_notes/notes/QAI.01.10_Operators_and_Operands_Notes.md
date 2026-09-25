# QAI.01.10 — Operators and Operands

> `QAI.01.09 Objects, references, aliases, and copies` → **`QAI.01.10 Operators and operands`** → `QAI.01.11 Arithmetic operations`

## 1. What you will be able to do

A course assistant calculates time for an orientation and several practice rounds. A wrong grouping of the same values can give a plausible-looking but incorrect answer. This lesson teaches you to identify **operators** and **operands**, predict what an expression produces, read the order of evaluation, and use parentheses to express the intended calculation.

You have already used `+`, `=`, `==`, and `is` in earlier nodes. Here we study the general structure of expressions. The complete catalogue of arithmetic and comparison operations follows in `QAI.01.11–.12`. Work in the disposable `qai-path-lab/code-lab/` folder.

## 2. Operands, operators, expressions, and results

```python
2 + 3
```

| Part | Term | Meaning |
|---|---|---|
 `2` | operand | value the operation acts on |
 `+` | operator | symbol specifying the operation |
 `3` | operand | other value the operation acts on |
 `2 + 3` | expression | code that produces a value |
 `5` | expression result | value produced by evaluating the expression |

**Evaluate** means determine the resulting value. A variable can be an operand: in `documents + new_documents`, Python looks up the values under both names, then applies `+`. The type of each operand matters: `2 + 3` gives numerical 5, while `"2" + "3"` gives string `"23"`. The symbol alone does not tell you the whole result.

The **result is not automatically printed in a saved script**:

```python
2 + 3
print(2 + 3)
```

When this file runs, it displays only `5` from `print`. The first expression is evaluated, but the script has no instruction to show its result. At the interactive `>>>` prompt, Python may show the value of a standalone expression; keep that environment distinction from `QAI.01.06`.

## 3. Unary and binary operators

A **unary operator** works with one operand. A **binary operator** works with two:

```python
print(-3)       # -3: unary - applied to 3
print(7 - 3)    # 4: binary - between 7 and 3
print(+3)       # 3: unary + applied to 3
```

The same printed symbol `-` can have two roles. In `-3` it indicates the negative of one number; in `7 - 3` it indicates subtraction of the second number from the first. Later `not` will be another unary operator, acting on a yes/no interpretation. Learn its complete rules in the Boolean logic node.

**Trace before running:** count the operands near the operator and say the operation aloud. “Negative three” uses one operand; “seven minus three” uses two.

## 4. Expressions can be nested

An expression can contain smaller **nested expressions**:

```python
print((2 + 3) * 4)  # 20
```

First, inner `2 + 3` produces 5. Then outer `5 * 4` produces 20. `*` denotes multiplication. The outer `print(...)` displays the resulting value; those outer parentheses belong to the function call. The inner `(2 + 3)` are **grouping parentheses** used to control calculation. They have different purposes even though both use the same characters.

**Worked trace:**

| Step | Smaller expression | Result |
|---|---|---:|
 1 | `2 + 3` | 5 |
 2 | `5 * 4` | 20 |
 3 | `print(20)` | shows `20` |

Do not read nested code as one opaque line. Identify the innermost part, calculate it, substitute its result, then continue.

## 5. Precedence: which operation groups first?

**Operator precedence** is Python's set of rules for grouping operations when you have not supplied parentheses. In these basic arithmetic examples, multiplication groups before addition:

```python
print(2 + 3 * 4)    # 14
print((2 + 3) * 4)  # 20
```

For the first expression, the multiplication `3 * 4` produces 12, then `2 + 12` produces 14. Parentheses change the intended grouping of the second expression: `2 + 3` produces 5 before multiplication, giving 20.

**Misconception guard:** “Python always reads left to right” is too simple. The unparenthesised expression `2 + 3 * 4` has `+` on the left, yet multiplication groups first. Also, grouping rules and the detailed order in which subexpressions run are related but not identical; when side effects matter later, inspect evaluation order separately.

### Use meaning, not just a memorised rule

For a course assistant:

- orientation: 10 minutes;
- practice: 3 rounds of 4 minutes.

The intended total is 10 minutes plus `3 * 4` minutes = **22 minutes**:

```python
orientation_minutes = 10
practice_rounds = 3
minutes_per_round = 4
total_minutes = orientation_minutes + practice_rounds * minutes_per_round
print(total_minutes)  # 22
```

Writing `(orientation_minutes + practice_rounds) * minutes_per_round` would give 52, but it would also combine minutes and a count of rounds before multiplying. The output looks numeric, yet the expression is conceptually wrong. State the calculation in words and units before writing code.

## 6. Parentheses express the intended grouping

**Parentheses** are a way to make grouping visible. Compare:

```python
print(10 + 3 * 4)      # 22
print((10 + 3) * 4)    # 52
print(10 + (3 * 4))    # 22
```

| Expression | First calculated group | Final result |
|---|---|---:|
 `10 + 3 * 4` | `3 * 4 = 12` | 22 |
 `(10 + 3) * 4` | `10 + 3 = 13` | 52 |
 `10 + (3 * 4)` | `3 * 4 = 12` | 22 |

Even when grouping parentheses do not change the answer, they can help the next reader see the intended structure. Avoid a wall of unnecessary parentheses; use them where a rule is easy to misread or where the business meaning requires a particular group.

**Nested grouping:** `((2 + 3) * 4) + 1` gives 21. Trace: 2 + 3 = 5; 5 * 4 = 20; 20 + 1 = 21. The outermost pair around `(2 + 3) * 4` groups the intermediate result; it is not a command by itself.

## 7. Associativity: when operators share a level

**Operator associativity** gives a default grouping when operators of the same relevant precedence appear in sequence. In the following subtraction expression, grouping proceeds left to right:

```python
print(10 - 3 - 2)       # 5, because (10 - 3) - 2 = 5
print(10 - (3 - 2))     # 9
```

Associativity and precedence answer different questions:

- **Precedence:** which kinds of operators group before others? In `2 + 3 * 4`, `*` groups before `+`.
- **Associativity:** with operators at a common precedence level, how do they group by default? `10 - 3 - 2` groups as `(10 - 3) - 2`.

Not every operator associates the same way. `**` means exponentiation (“raise to a power”): `2 ** 3` means 2 cubed, or 8. A chain of exponentiation groups from the right:

```python
print(2 ** 3 ** 2)      # 512: 2 ** (3 ** 2)
print((2 ** 3) ** 2)    # 64
```

This is a preview of arithmetic operations in `QAI.01.11`; you do not need to memorise the full precedence table here. When a calculation is consequential or not obvious, write the grouping explicitly and verify it with a small example.

## 8. Unary signs and grouping: one subtle check

Do not assume a visible minus sign always means “make the whole calculation negative before doing anything else”:

```python
print(-2 ** 2)      # -4
print((-2) ** 2)    # 4
```

In the first line, the power `2 ** 2` produces 4 and the unary minus makes it -4. In the second, parentheses make negative two the operand of exponentiation, so (-2) times (-2) gives 4. This is another reason to group the intended number explicitly. Exponentiation and signed values receive fuller practice in `QAI.01.11`.

## 9. Guided lab: predict, execute, and change one group

Create `operators_operands.py` inside `qai-path-lab/code-lab/`:

```python
# Fictional timings; no actual course timetable is changed.
orientation_minutes = 10
practice_rounds = 3
minutes_per_round = 4

practice_minutes = practice_rounds * minutes_per_round
correct_total = orientation_minutes + practice_minutes
wrong_grouping = (orientation_minutes + practice_rounds) * minutes_per_round

print("Practice minutes:", practice_minutes)
print("Intended total:", correct_total)
print("Wrong grouping:", wrong_grouping)
print("Same value?", correct_total == wrong_grouping)
```

`==` asks whether two values compare equal, as introduced in `QAI.01.09`. Predict the four output lines:

```text
Practice minutes: 12
Intended total: 22
Wrong grouping: 52
Same value? False
```

Run from `code-lab` using `py .\operators_operands.py` in Windows PowerShell or `python3 operators_operands.py` in Bash/Zsh. Use your verified `python` command instead of `py` if appropriate.

**Controlled variation:** change only `practice_rounds = 3` to `practice_rounds = 2`. Before running, predict practice minutes 8; intended total 18; wrongly grouped total 48; equality `False`. Run, compare, and restore the original value if needed.

**Explain the mechanism:** `practice_rounds` and `minutes_per_round` are the two operands of `*`; their product is an operand of `+` with `orientation_minutes`. The grouping in `wrong_grouping` instead combines orientation minutes with the number of rounds before multiplying.

## 10. Common mistakes and exact repairs

| Observation | Cause | Repair |
|---|---|---|
 `2 + 3 * 4` prints 14 when 20 was expected | multiplication grouped first | write `(2 + 3) * 4` if that matches the actual task |
 `10 - 3 - 2` prints 5 when 9 was expected | left associativity | write `10 - (3 - 2)` if subtracting the difference is intended |
 `"2" + "3"` prints `23` instead of 5 | operands are text | convert justified numeric input first; check the types |
 `2 + "3"` raises `TypeError` | incompatible operand types for this addition | decide numerical addition or text construction explicitly |
 `print((2 + 3) * 4` fails before output | unclosed function-call parenthesis | close the missing `)` and rerun |
 `total = 2 + 3` displays nothing | assignment does not print | add `print(total)` to a saved script |

**Debug sequence:** write the expected calculation in words; label operands and operators; put parentheses around intended groups; identify types; predict one small numerical case; run and compare.

## 11. Independent exercise with full solution

**Task:** a fictional lesson has 5 minutes of setup, followed by 4 rounds of 6 minutes. Save `expression_lab.py` that prints (1) practice minutes, (2) total minutes, and (3) whether `5 + 4 * 6` equals `(5 + 4) * 6`. Name the operators and operands in the total calculation; predict all outputs before running. Then change rounds to 2 and predict the first two outputs.

**Worked solution:**

```python
setup_minutes = 5
rounds = 4
minutes_per_round = 6

practice_minutes = rounds * minutes_per_round
total_minutes = setup_minutes + practice_minutes
same_grouping = (setup_minutes + rounds * minutes_per_round) == (
    (setup_minutes + rounds) * minutes_per_round
)

print("Practice:", practice_minutes)
print("Total:", total_minutes)
print("Same grouping?", same_grouping)
```

**Expected original result:** `Practice: 24`; `Total: 29`; `Same grouping? False`, because the alternative grouping gives `(5 + 4) * 6 = 54`. Multiplication operates on `rounds` and `minutes_per_round`; addition operates on `setup_minutes` and the computed practice minutes; equality compares the two totals.

**When `rounds = 2`:** practice = 2 * 6 = 12 and total = 5 + 12 = 17. The alternative grouping becomes (5 + 2) * 6 = 42, so the comparison remains `False`. A correct explanation says *why* the numbers differ, not just what printed.

## 12. Evidence and recall

Keep `operators_operands.py` and `expression_lab.py` in `code-lab`. Add `expression_trace.md` with the initial and changed predictions, actual outputs, one line-by-line trace of `10 + 3 * 4`, and a brief explanation of the wrong grouping's unit mismatch.

**Remember:** operands are values being used; operators specify operations; an expression produces a result; unary operators use one operand and binary operators two; precedence controls mixed kinds of operations, associativity controls default grouping at one level, and parentheses state your intended grouping explicitly.

## 13. Next connection

`QAI.01.11 — Arithmetic operations` gives the complete basic arithmetic toolkit: addition, subtraction, multiplication, division, floor division, remainders, powers, signs, and rounding.
