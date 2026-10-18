# SQL expressions and calculated columns

## Derive an answer without changing a stored value

The catalogue now records the duration and number of lessons for each course:

| course_id | title | duration_minutes | lesson_count |
|---:|---|---:|---:|
| 101 | AI Foundations | 95 | 4 |
| 102 | Git Basics | 50 | 3 |
| 103 | Data Basics | 80 | 4 |
| 104 | Python Basics | 65 | 3 |

An instructor asks, “What would the duration be if we added ten minutes to each course?” We can answer with an **expression** in a `SELECT` result:

```sql
SELECT course_id, duration_minutes,
       duration_minutes + 10 AS extended_minutes
FROM course_catalogue
ORDER BY course_id;
```

The result is:

| course_id | duration_minutes | extended_minutes |
|---:|---:|---:|
| 101 | 95 | 105 |
| 102 | 50 | 60 |
| 103 | 80 | 90 |
| 104 | 65 | 75 |

`extended_minutes` is a **calculated column**: an output value computed from each input row. It is not a stored column in `course_catalogue`. Re-running this query computes it again from the current stored values. If you want to change stored durations, that is a different operation taught later. The `ORDER BY` line is present only to make the example's row sequence reproducible; row sorting gets its own lesson.

## Break down an arithmetic expression

In `duration_minutes + 10`, `+` is a **SQL operator**: it tells the database which operation to perform. `duration_minutes` and `10` are its **SQL operands**: the values it operates on. For course 101 the column supplies 95, so the **arithmetic expression** becomes `95 + 10` and produces 105.

| Operator | Action on course 101 | Expression | Result |
|---|---|---|---:|
| `+` | **Addition** | `duration_minutes + 10` → `95 + 10` | 105 |
| `-` | **Subtraction** | `duration_minutes - 5` → `95 - 5` | 90 |
| `*` | **Multiplication** | `duration_minutes * 2` → `95 * 2` | 190 |
| `/` | **Division** | `duration_minutes / lesson_count` → `95 / 4` | 23 in SQLite with integer operands |
| `%` | **Remainder** | `duration_minutes % lesson_count` → `95 % 4` | 3 in SQLite with integer operands |

The last two results tell us that four whole groups of 23 minutes account for 92 minutes, with 3 minutes left to distribute: `4 × 23 + 3 = 95`. The query does not decide which lesson receives those three extra minutes. A remainder is what remains after whole-number division; it is **not** a percentage. `*` is SQL multiplication; `%` is remainder in this SQLite example.

### Division needs a data-type check

SQLite divides two integers using integer division when the inputs and result permit it:

```sql
SELECT 5 / 2 AS whole_result,
       5 / 2.0 AS fractional_result,
       5 % 2 AS leftover;
```

The result is `(2, 2.5, 1)`. The literal `2.0` is a real-number operand, so `5 / 2.0` gives a fractional result. Likewise, `duration_minutes * 1.0 / lesson_count` gives `23.75` for course 101. Do not silently assume the same integer-division rule in another database product; check its type and operator semantics. A fractional binary floating-point result is an approximation in general. For money or measurements requiring an exact specified precision, choose and validate a suitable representation rather than multiplying by `1.0` without thought.

For `1 / 0` and `1 % 0`, SQLite returns SQL `NULL`, meaning no numeric result is available; Python's SQLite client shows that value as `None`. Other database systems may report an error instead. A `NULL` result is not zero and should not be interpreted as a valid duration. If a row's `lesson_count` could be zero, validate or handle that case before relying on a per-lesson number. The lab tests the zero-divisor boundary without modifying a table.

## Predict operator precedence, then use parentheses

**Operator precedence** is the order in which operators are applied when an expression contains several of them. SQLite performs multiplication, division, and remainder before addition and subtraction in these examples. With course 101:

```sql
SELECT duration_minutes + 10 * lesson_count AS without_grouping,
       (duration_minutes + 10) * lesson_count AS with_grouping
FROM course_catalogue
ORDER BY course_id;
```

The first result row is `(135, 420)`:

- Without parentheses: `95 + (10 × 4) = 95 + 40 = 135`.
- With parentheses: `(95 + 10) × 4 = 105 × 4 = 420`.

`(duration_minutes + 10)` is a **parenthesised expression**. It makes addition happen before the multiplication outside it. The difference between 135 and 420 is large, so the grouped expression is not merely a formatting choice. Use parentheses where the intended calculation could be misread, and test with values that make two interpretations produce different results.

| course_id | `duration_minutes + 10 * lesson_count` | `(duration_minutes + 10) * lesson_count` |
|---:|---:|---:|
| 101 | 135 | 420 |
| 102 | 80 | 180 |
| 103 | 120 | 360 |
| 104 | 95 | 225 |

Both are legitimate SQL expressions but answer different questions. State what the numbers are meant to represent before deciding which expression is suitable. A duration of 420 minutes is not automatically a sensible change to the course; the example is for tracing evaluation order.

## Build a readable string expression

A **string expression** produces text. In SQLite, the **concatenation** operator `||` joins text fragments:

```sql
SELECT title || ' (' || course_id || ')' AS label
FROM course_catalogue
ORDER BY course_id;
```

Course 101 produces `AI Foundations (101)`. The first operand is the `title` column; `' ('` and `')'` are fixed text values. SQLite converts the integer course ID to text as part of this concatenation. A **calculated-column alias** (`AS label`) names the resulting output column; it does not add a stored `label` field. For a different database engine, check its text-concatenation syntax: for example, MySQL commonly uses `CONCAT(...)` instead of SQLite's `||` in its default SQL mode.

If any concatenated operand is SQL `NULL`, SQLite's `||` result is `NULL`. Do not assume a missing text field behaves like an empty string. Our sample `title` is `NOT NULL`; later data-cleaning lessons address missing values in more depth. The lab uses fixed column names and values so you can concentrate on the expression itself.

## A calculated catalogue preview

A teaching page needs four facts for each course: its stored duration, an extended-duration scenario, the minutes left after whole 30-minute blocks, and a readable label. A single `SELECT` can produce these alongside the stable ID and title:

```sql
SELECT course_id, title, duration_minutes,
       duration_minutes + 10 AS extended_minutes,
       duration_minutes % 30 AS leftover_minutes,
       title || ' (' || course_id || ')' AS label
FROM course_catalogue
ORDER BY course_id;
```

| course_id | title | duration_minutes | extended_minutes | leftover_minutes | label |
|---:|---|---:|---:|---:|---|
| 101 | AI Foundations | 95 | 105 | 5 | AI Foundations (101) |
| 102 | Git Basics | 50 | 60 | 20 | Git Basics (102) |
| 103 | Data Basics | 80 | 90 | 20 | Data Basics (103) |
| 104 | Python Basics | 65 | 75 | 5 | Python Basics (104) |

`leftover_minutes` here is `duration_minutes % 30`, so it describes the **original** duration, not `extended_minutes`. If the intended question is “What remains after extending each course by ten minutes?”, use `(duration_minutes + 10) % 30` instead. For course 101 that would be `105 % 30 = 15`. Naming a result clearly does not make a wrong formula correct; compare it with the question and trace at least one row.

## Guided lab: run, change, and inspect

Download the [calculated columns lab](QAI.02.01.12_Calculated_Columns_Lab.zip), unzip it, and run from its folder:

```sh
python calculated_columns.py
python check_calculated_columns.py
```

Use `python3` if that is your working command. Python's built-in `sqlite3` module creates the four sample rows in a new in-memory database. The first program prints:

```text
Arithmetic headings: course_id, plus_10, minus_5, twice, whole_per_lesson, leftover
Arithmetic first row: (101, 105, 90, 190, 23, 3)
Precedence first row: (135, 420)
Real division first row: 23.75
First text label: AI Foundations (101)
Divide by zero is NULL: True
Source durations unchanged: True
```

The Python client calls `execute()` to run a statement, reads `cursor.description` for headings, and calls `fetchall()` for rows. Those are Python operations, not extra SQL clauses. `SELECT` creates temporary output values; the `before` and `after` comparison checks that the stored IDs and durations stayed the same.

**Controlled modification:** copy `calculated_columns.py`. In its arithmetic query, change `duration_minutes + 10 AS plus_10` to `duration_minutes + 15 AS plus_15`. Predict the altered heading and first row: `plus_15` replaces `plus_10`, and course 101's row becomes `(101, 110, 90, 190, 23, 3)`. Keep the other expressions unchanged. If you change the number but leave `plus_10` as the heading, the value 110 is correct for the new expression but the output name is misleading. Repair both together.

**Controlled failure:** remove the parentheses from `(duration_minutes + 10) * lesson_count`. You will get 135 instead of 420 for course 101. Diagnose it by tracing `10 * 4` before adding 95; restore the parentheses and rerun. The checker also verifies `5 / 2`, `5 / 2.0`, and both zero-divisor operations so a plausible-looking integer result does not mask a wrong expectation.

## Independent practice: split time across lessons

For each course, produce `course_id`, `whole_minutes`, and `leftover_minutes`. `whole_minutes` should be the whole-number result of `duration_minutes / lesson_count`; `leftover_minutes` should be the remainder. Predict all four rows before consulting the reference:

| course_id | whole_minutes | leftover_minutes |
|---:|---:|---:|
| 101 | 23 | 3 |
| 102 | 16 | 2 |
| 103 | 20 | 0 |
| 104 | 21 | 2 |

**Reference query:**

```sql
SELECT course_id,
       duration_minutes / lesson_count AS whole_minutes,
       duration_minutes % lesson_count AS leftover_minutes
FROM course_catalogue
ORDER BY course_id;
```

**Reference Python**, with the lab's `make_connection()` and `query()` functions:

```python
connection = make_connection()
headings, rows = query(
    connection,
    "SELECT course_id, "
    "duration_minutes / lesson_count AS whole_minutes, "
    "duration_minutes % lesson_count AS leftover_minutes "
    "FROM course_catalogue ORDER BY course_id;",
)
assert headings == ["course_id", "whole_minutes", "leftover_minutes"]
assert rows == [(101, 23, 3), (102, 16, 2), (103, 20, 0), (104, 21, 2)]
connection.close()
```

The lab's `lesson_split()` supplies this solution for later comparison. Its checker verifies a useful relationship on *every* row: `whole_minutes * lesson_count + leftover_minutes == duration_minutes`. This relationship would expose a mistake if, for example, the divisor of the remainder calculation differed from the divisor of the division calculation. Keep an independent attempt and explain one row before checking the answer.

### One interpretation change

Suppose the report should show remaining minutes **after** each ten-minute extension, not before it. Replace `duration_minutes % 30` with `(duration_minutes + 10) % 30` and use an alias such as `extended_leftover_minutes`. Expected results for the four courses are 15, 0, 0, and 15. The source durations remain 95, 50, 80, and 65. Check the original question and the alias together when you modify a formula.

## Troubleshoot a surprising result

| Observation | Cause to inspect | Repair |
|---|---|---|
| `95 / 4` displays `23` rather than `23.75` | SQLite divided integer operands | Use an intentional real operand such as `95 * 1.0 / 4` if a fractional approximation answers the question |
| `95 + 10 * 4` gives `135`, not `420` | Multiplication has higher precedence | Use `(95 + 10) * 4` when that is the intended calculation |
| `1 / 0` appears as `None` in Python | SQLite returned SQL `NULL` | Treat zero divisors as invalid or missing for the chosen task, not as a numeric zero |
| Label is `NULL` unexpectedly | One SQLite `||` operand is `NULL` | Inspect the source and define an explicit missing-value policy before concatenation |
| Calculated heading is opaque or stale | An expression has no useful alias, or the alias no longer matches it | Supply/update `AS` with a meaningful result name |
| Projected value seems correct but answers the wrong question | Formula uses original instead of extended duration, or vice versa | Translate the user question into operands and check a hand-worked row |

Do not use floating-point results casually for exact money arithmetic. Do not assume another SQL engine will match SQLite on `/`, `%`, `||`, or division by zero; confirm the target dialect's behaviour before transferring a query.

## Check your understanding

1. In `duration_minutes + 10`, what are the operator and operands?
2. For course 102, what are `duration_minutes / lesson_count` and `duration_minutes % lesson_count` in this SQLite sample?
3. Why do `95 + 10 * 4` and `(95 + 10) * 4` differ?
4. What does `AS extended_minutes` change in the stored table?
5. What is the result of `title || ' (' || course_id || ')'` for course 104?
6. Why is `duration_minutes % 30` different from `(duration_minutes + 10) % 30` for course 101?
7. What does Python receive when SQLite evaluates `1 / 0` in a selected expression?

**Answers with reasoning**

1. `+` is the SQL operator; `duration_minutes` and `10` are its operands.
2. `50 / 3` gives the whole-number result 16; `50 % 3` gives remainder 2. `16 × 3 + 2 = 50`.
3. Multiplication precedes addition in the first expression (`135`); parentheses make addition happen first in the second (`420`).
4. It changes only the result-column heading. No stored column is created or updated.
5. `Python Basics (104)`.
6. The first computes `95 % 30 = 5`; the second computes `105 % 30 = 15`.
7. SQLite returns SQL `NULL`; the Python SQLite client represents it as `None`.

## Remember and retain

- A calculated column is a value in a query result. It does not update the source table.
- Operators act on operands; trace one row by substituting its actual column values.
- SQLite integer division and real-number division can differ; `%` is remainder, not percentage.
- Multiplication/division/remainder take precedence over addition/subtraction in these examples; parentheses express a deliberate grouping.
- A SQLite string expression can concatenate text with `||`; `AS` names the calculated output.
- Check zero divisors, missing values, type behaviour, and whether a formula answers the requested question. Keep your predicted and observed results, corrected failure, preview query, and lesson-split evidence.

## Further reading

- [SQLite: expressions, operators, and precedence](https://www.sqlite.org/lang_expr.html)
- [SQLite: numeric storage and conversions](https://www.sqlite.org/datatype3.html)
- [Python: SQLite database API](https://docs.python.org/3/library/sqlite3.html)
