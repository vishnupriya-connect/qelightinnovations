# Row filtering

## Ask for some rows, not every row

The same course catalogue contains four rows:

| course_id | title | instructor_id | duration_minutes | lesson_count |
|---:|---|---:|---:|---:|
| 101 | AI Foundations | 7 | 95 | 4 |
| 102 | Git Basics | 8 | 50 | 3 |
| 103 | Data Basics | 7 | 80 | 4 |
| 104 | Python Basics | 8 | 65 | 3 |

The last lesson chose which **columns** to return. A **row filter** decides which **rows** qualify. Add a `WHERE` clause after the `FROM` source:

```sql
SELECT course_id, title, duration_minutes
FROM course_catalogue
WHERE duration_minutes >= 80
ORDER BY course_id;
```

`duration_minutes >= 80` is a **filter condition**. It asks whether a row's duration is at least 80 minutes. The result has course IDs **101** and **103**. Rows 102 and 104 are still stored; this `SELECT` does not delete or modify them. `ORDER BY course_id` simply makes the example's output order stable; sorting is covered later.

For each source row, the database checks the condition. A row is included when the `WHERE` expression is true. A false result excludes it. A condition involving a missing SQL `NULL` value can be unknown; that also does not include the row. This lesson's duration and instructor fields have no missing values, so the worked traces are ordinary true/false cases. Explicit missing-value conditions are taught next.

## Trace each comparison against a boundary

A **comparison condition** tests a relationship between two values. In `duration_minutes >= 80`, the left value comes from the current row; the right value is the fixed boundary 80. The six common comparisons give different outputs with the same source data:

| Condition in `WHERE` | Name | Course IDs returned | Why |
|---|---|---|---|
| `duration_minutes = 80` | **Equality condition** | 103 | Exactly 80 |
| `duration_minutes <> 80` | **Inequality condition** | 101, 102, 104 | All except 80 |
| `duration_minutes > 80` | **Greater-than condition** | 101 | Strictly above 80 |
| `duration_minutes < 80` | **Less-than condition** | 102, 104 | Strictly below 80 |
| `duration_minutes >= 80` | **Greater-than-or-equal condition** | 101, 103 | 80 is included |
| `duration_minutes <= 80` | **Less-than-or-equal condition** | 102, 103, 104 | 80 is included |

In SQL, `=` tests equality; it is not Python's `==`. `<>` is a widely used spelling for “not equal”; SQLite also accepts `!=`, but use one form consistently for this lab. The boundary row 103 is the best check for confusing `>` with `>=` or `<` with `<=`.

**Worked trace for row 103:** its duration is 80, so `80 > 80` is false while `80 >= 80` is true. For row 102, `50 < 80` is true and `50 = 80` is false. A query that returns **zero rows**, such as `WHERE duration_minutes > 200`, is a valid empty result, not necessarily a syntax error.

Text values are written as SQL text literals with single quotes:

```sql
SELECT course_id
FROM course_catalogue
WHERE title = 'Git Basics';
```

The result is course 102. Without the quotes, `Git Basics` would not be treated as one text value. When a value comes from an external user or program input, use a bound parameter rather than inserting that value directly into SQL text; the runnable lab includes a parameter example.

## Combine conditions with `AND`

A **logical condition** joins or changes other conditions. `AND` requires both sides to be true for a row:

```sql
SELECT course_id, title
FROM course_catalogue
WHERE instructor_id = 7 AND duration_minutes >= 80
ORDER BY course_id;
```

The result is **101, 103**. Check each row rather than guessing from the English description:

| Course | Instructor is 7? | Duration is at least 80? | Both (`AND`)? |
|---:|---|---|---|
| 101 | True | True | Include |
| 102 | False | False | Exclude |
| 103 | True | True | Include |
| 104 | False | False | Exclude |

For a controlled boundary change, replace 80 with 81. Course 103's duration is exactly 80, so it no longer qualifies. The result becomes **101**. The change filters the output; it does not rewrite course 103.

## Combine alternatives with `OR`

`OR` includes a row if **at least one** condition is true:

```sql
SELECT course_id
FROM course_catalogue
WHERE instructor_id = 8 OR duration_minutes > 90
ORDER BY course_id;
```

The result is **101, 102, 104**. Row 101 qualifies because 95 is above 90. Rows 102 and 104 qualify because their instructor is 8. Row 103 matches neither condition. `OR` does not add a second copy of a row that happens to satisfy both sides; this query examines the source row once and either includes it or excludes it. The earlier `DISTINCT` lesson concerned duplicates among *different* source rows after selecting columns.

## Negate a condition with `NOT`

`NOT` reverses an ordinary true/false condition:

```sql
SELECT course_id
FROM course_catalogue
WHERE NOT (instructor_id = 8)
ORDER BY course_id;
```

The result is **101, 103**. Parentheses make clear what is being negated: “not assigned to instructor 8.” For this table with non-null instructor IDs, `instructor_id <> 8` gives the same two rows. Do not assume this equivalence for a nullable field without checking SQL's unknown result: `NOT` of an unknown comparison remains unknown rather than automatically selecting the row.

## Group a condition to express the actual rule

In SQL, `AND` normally binds more tightly than `OR`. Compare these two queries:

```sql
-- Git Basics, or an instructor-7 course at least 90 minutes long.
SELECT course_id FROM course_catalogue
WHERE title = 'Git Basics' OR instructor_id = 7 AND duration_minutes >= 90
ORDER BY course_id;
```

```sql
-- At least 90 minutes long, and either Git Basics or an instructor-7 course.
SELECT course_id FROM course_catalogue
WHERE (title = 'Git Basics' OR instructor_id = 7) AND duration_minutes >= 90
ORDER BY course_id;
```

The first returns **101, 102**. It reads as `title = 'Git Basics' OR (instructor_id = 7 AND duration_minutes >= 90)`. Row 102 passes the Git alternative even though it lasts only 50 minutes. The second returns **101**. It requires *every* selected row to reach 90 minutes, so row 102 fails.

| Row | Is Git Basics? | Instructor 7? | At least 90? | Ungrouped first query | Grouped second query |
|---:|---|---|---|---|---|
| 101 | No | Yes | Yes | Include | Include |
| 102 | Yes | No | No | Include | Exclude |
| 103 | No | Yes | No | Exclude | Exclude |
| 104 | No | No | No | Exclude | Exclude |

This is **condition grouping**: parentheses define which logical parts belong together. A **parenthesised condition** such as `(title = 'Git Basics' OR instructor_id = 7)` is evaluated as a unit before applying the surrounding `AND`. Parentheses here group truth conditions; they do not change stored rows. Even when the default precedence would give the intended result, writing parentheses can make a long rule easier to review.

## Guided lab: predict, run, and repair

Download the [row filtering lab](QAI.02.01.13_Row_Filtering_Lab.zip), unzip it, and run both programs from its folder:

```sh
python row_filter.py
python check_row_filter.py
```

Use `python3` if that is your working command. Python's standard `sqlite3` module builds the four-row catalogue in memory. No external database is needed. The first program prints:

```text
At least 80: [101, 103]
Exactly 80: [103]
Below 80: [102, 104]
Instructor 7 AND at least 80: [101, 103]
Instructor 8 OR over 90: [101, 102, 104]
NOT instructor 8: [101, 103]
Ungrouped: [101, 102]
Grouped: [101]
Stored rows unchanged: True
```

The checker tests all six comparison operators at the boundary, a changed threshold, the three logical operators, both grouping interpretations, an empty result, a solved project, and an independent variation. It also compares the stored source rows before and after the read queries.

**Controlled change:** in a copy of `row_filter.py`, change the call `long_by_instructor(db, 80, 7)` to `long_by_instructor(db, 81, 7)`. Predict that the corresponding output becomes `[101]`. Run it, inspect course 103's 80-minute boundary, and record your predicted and actual results. The helper passes the values with `?` parameter markers; they stand for data values, not for column or table names.

**Reproduce a logic error:** take the grouped `WHERE` condition above, remove only its grouping parentheses, and predict that Git Basics reappears. Trace row 102 to explain why. Restore the parentheses if the desired rule requires every selected course to reach 90 minutes. This is a *logical error*: both statements can run, but they answer different questions.

## Mini-project: long courses with one exception

A catalogue view must show courses taught by instructor 7 that last at least 80 minutes, **plus Git Basics as an explicit exception**. In this four-row dataset, the expected IDs are **101, 102, 103**. Row 104 is instructor 8 and is not the named exception. Build a `SELECT course_id, title` query that implements this rule and keeps the ID order.

**Reference solution:**

```sql
SELECT course_id, title
FROM course_catalogue
WHERE (instructor_id = 7 AND duration_minutes >= 80)
   OR title = 'Git Basics'
ORDER BY course_id;
```

Expected rows: `(101, 'AI Foundations')`, `(102, 'Git Basics')`, `(103, 'Data Basics')`. The lab's `long_or_exception()` supplies the same reference rule for ID output only. A useful acceptance check is that removing the exception removes course 102 while retaining 101 and 103. If you accidentally write `instructor_id = 7 AND (duration_minutes >= 80 OR title = 'Git Basics')`, course 102 is excluded because its instructor is 8: the exception no longer operates independently.

**Independent variation:** show courses taught by instructor 8 that are shorter than 80 minutes, plus course 103 as an exception. Expected IDs: **102, 103, 104**. Attempt it before reading this reference:

```sql
SELECT course_id
FROM course_catalogue
WHERE (instructor_id = 8 AND duration_minutes < 80)
   OR course_id = 103
ORDER BY course_id;
```

To keep evidence, record the rule in ordinary language, your initial query, the predicted IDs, the observed IDs, and one explanation of why an excluded row fails. The checker validates the reference variation, but running it does not prove that your own query is correct; compare your independent statement with the expected rows and fix any mismatch.

## Diagnose common filtering faults

| Symptom | Cause to inspect | Repair |
|---|---|---|
| Duration 80 is missing unexpectedly | Used `>` instead of `>=` | Test the boundary row 103 and choose strict or inclusive comparison deliberately |
| Git Basics appears when every result should be at least 90 | `OR` alternative escaped the duration condition | Group the alternatives before `AND duration_minutes >= 90` |
| Git Basics is missing from an exception report | The exception was placed inside an instructor-7 `AND` group | Put the separate exception on the other side of `OR` |
| `no such column` error | Misspelled field or unquoted intended text literal | Inspect schema; quote `'Git Basics'` as text |
| Query returns zero rows | Conditions might be too restrictive, or zero matches are correct | Trace all four rows; compare boundary and expected rule before changing syntax |
| A nullable comparison behaves unexpectedly | SQL can produce unknown, which `WHERE` excludes | Inspect missing values and use an explicit missing-value policy; next lesson covers null conditions |

When building a larger filter, first state the inclusion rule in one sentence, group its parts with parentheses, then test normal, boundary, and deliberately excluded rows. Do not use a filter as a substitute for access control: a read query's output is only one part of an application's data-permission design.

## Check your understanding

1. Does `WHERE duration_minutes >= 80` delete courses 102 and 104?
2. Which IDs satisfy `duration_minutes > 80`? Which satisfy `>= 80`?
3. Why does `instructor_id = 8 OR duration_minutes > 90` include course 101?
4. Why does `NOT (instructor_id = 8)` exclude courses 102 and 104 here?
5. For row 102, why do the grouped and ungrouped 90-minute queries disagree?
6. If `WHERE duration_minutes > 200` produces no rows, what has been established?

**Answers and reasoning**

1. No. It selects rows 101 and 103 for this result; stored data stays intact.
2. Strict `>` returns 101; inclusive `>=` returns 101 and 103 because 103 is exactly 80.
3. Its duration is 95, so one `OR` alternative is true even though its instructor is 7.
4. Their instructor is 8; negating that true comparison gives false for those rows.
5. It satisfies the Git alternative but is only 50 minutes. Ungrouped `OR` includes it; grouped `AND duration_minutes >= 90` excludes it.
6. No current row satisfies that condition. It does not by itself prove a syntax failure or remove source data.

## Remember and retain

- `WHERE` evaluates a condition for each source row; true rows are included, while false and unknown rows are not.
- `=`, `<>`, `>`, `<`, `>=`, and `<=` answer different questions at a boundary; test the equal-to-boundary row.
- `AND` requires both; `OR` allows either; `NOT` negates a condition, subject to SQL's unknown value for missing data.
- `AND` binds more tightly than `OR`; parenthesise the intended rule and trace rows that distinguish competing interpretations.
- A filter changes the query result, not stored rows. Retain the six comparison predictions, grouping trace, corrected failure, mini-project, and independent variation before continuing.

## Further reading

- [SQLite: SELECT and WHERE clause](https://www.sqlite.org/lang_select.html)
- [SQLite: comparison and logical expressions](https://www.sqlite.org/lang_expr.html)
- [Python: supplying values to SQLite queries](https://docs.python.org/3/library/sqlite3.html)
