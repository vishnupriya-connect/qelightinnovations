# Conditional SQL expressions

## Make a value from a condition

Use the same four-course catalogue. Two fields can be missing: `topic_note` and `practice_minutes`.

| course_id | title | duration_minutes | lesson_count | topic_note | practice_minutes |
|---:|---|---:|---:|---|---:|
| 101 | AI Foundations | 95 | 4 | intro | 20 |
| 102 | Git Basics | 50 | 3 | `NULL` | `NULL` |
| 103 | Data Basics | 80 | 4 | tables | 30 |
| 104 | Python Basics | 65 | 3 | `NULL` | `NULL` |

A **conditional expression** produces a value based on a test. In earlier lessons, `WHERE duration_minutes >= 80` decided whether a row appears at all. A conditional expression can keep every row and add a new *result value* instead. For example, call courses at least 80 minutes long “Extended,” courses from 60 through 79 “Standard,” and shorter courses “Short.” Those labels are **derived categories**: calculated from stored durations when the query runs, rather than stored in a new table column.

```sql
SELECT course_id, duration_minutes,
       CASE
           WHEN duration_minutes >= 80 THEN 'Extended'
           WHEN duration_minutes >= 60 THEN 'Standard'
           ELSE 'Short'
       END AS duration_band
FROM course_catalogue
ORDER BY course_id;
```

The result is:

| course_id | duration_minutes | duration_band |
|---:|---:|---|
| 101 | 95 | Extended |
| 102 | 50 | Short |
| 103 | 80 | Extended |
| 104 | 65 | Standard |

`CASE` starts the expression. Each `WHEN` supplies a condition. Its corresponding `THEN` supplies the **condition result** if that condition is true. `ELSE` supplies the fallback when no earlier condition is true. `END` closes the expression. `AS duration_band` gives the calculated output column a readable name. The query returns all four rows because no `WHERE` clause removes any. The source durations and missing notes stay unchanged.

## Trace the first true branch

For each row, SQL checks the `WHEN` conditions in order and uses the `THEN` value of the **first true** one:

| Course | `duration >= 80`? | If not, `duration >= 60`? | Result |
|---:|---|---|---|
| 101 (95) | Yes | Not needed | Extended |
| 102 (50) | No | No | Short from `ELSE` |
| 103 (80) | Yes, at boundary | Not needed | Extended |
| 104 (65) | No | Yes | Standard |

This is **category creation** by conditions. The categories do not overlap in the output because the first successful branch wins. The two conditions *can* both be true for a 95-minute course; testing the more specific `>= 80` first is what assigns “Extended.” If you reverse the two `WHEN` clauses, course 101 and course 103 satisfy `>= 60` first and are incorrectly labelled “Standard.” That query is valid SQL but implements a different rule. State the category boundaries before writing the branches and test rows at 50, 60, 80, and 95 when available.

**Controlled variation:** change the boundaries to `>= 81` for Extended and `>= 66` for Standard, keeping that order. Now 101 remains Extended, 103 at 80 becomes Standard, and 104 at 65 becomes Short. Course 102 stays Short. The output categories become **Extended, Short, Standard, Short** in ID order. Changing the boundary affects the calculated labels, not the stored durations.

`ELSE` is optional, but omission has a visible consequence:

```sql
SELECT course_id,
       CASE WHEN duration_minutes >= 80 THEN 'Extended' END AS duration_band
FROM course_catalogue
ORDER BY course_id;
```

Courses 101 and 103 receive `Extended`; courses 102 and 104 receive SQL `NULL` because no `WHEN` succeeds and there is no `ELSE`. If every row should have a label, include an appropriate `ELSE`. Do not confuse the resulting `NULL` label with a missing `duration_minutes` in the source: the sample durations are all present.

## Handle a missing value in a condition

A condition can explicitly test `NULL` using `IS NULL`:

```sql
SELECT course_id,
       CASE
           WHEN topic_note IS NULL THEN 'Needs note'
           ELSE 'Note present'
       END AS note_status
FROM course_catalogue
ORDER BY course_id;
```

The statuses are `(101, 'Note present')`, `(102, 'Needs note')`, `(103, 'Note present')`, and `(104, 'Needs note')`. A `CASE WHEN topic_note = NULL` would not find the missing notes: equality with SQL `NULL` is unknown, not true. Use `IS NULL` just as you would in a `WHERE` clause. When a `WHEN` condition is false or unknown, that branch is not selected; SQL tries the next branch or the `ELSE` value.

This use of `CASE` answers “what status label should each row show?” The earlier `WHERE topic_note IS NULL` instead answers “which rows have a missing note?” Choose the operation that matches the question.

## Choose a display fallback with `COALESCE`

For a simple **null replacement** in the query result, `COALESCE` returns the first argument that is not SQL `NULL`:

```sql
SELECT course_id,
       COALESCE(topic_note, 'Not recorded') AS displayed_note
FROM course_catalogue
ORDER BY course_id;
```

The displayed values in ID order are **intro**, **Not recorded**, **tables**, **Not recorded**. `COALESCE(topic_note, 'Not recorded')` retains each actual note when present and uses the provided text only for a missing note. This changes an output value, **not** the stored `topic_note`: `COUNT(topic_note)` still reports 2 present values after the read query.

With several possible values, `COALESCE(first, second, third)` picks the first non-null argument from left to right. For example, `COALESCE(NULL, NULL, 'Fallback')` returns `'Fallback'`; if all arguments are `NULL`, its result is `NULL`. For this two-value display case, the second argument is a label chosen by the query writer, not evidence that the topic note has actually been entered.

Be especially careful with numeric fallbacks:

```sql
SELECT course_id, COALESCE(practice_minutes, 0) AS displayed_practice_minutes
FROM course_catalogue
ORDER BY course_id;
```

The output is 20, 0, 30, 0. For courses 102 and 104, that zero is a **display choice**, not a measured practice estimate. The earlier aggregate `AVG(practice_minutes)` is 25 over the two recorded estimates; an average over `COALESCE(practice_minutes, 0)` would be 12.5 over four output values and would answer a different question. If missing data matters, keep it as `NULL` for calculations or show a clear “not recorded” label to readers. Also, `COALESCE` only replaces SQL `NULL`; an empty string `''` is a present value and remains empty.

| Need | Expression | Example result for course 102 |
|---|---|---|
| Exclude courses with missing notes | `WHERE topic_note IS NOT NULL` | Row excluded |
| Label whether a note exists | `CASE WHEN topic_note IS NULL THEN 'Needs note' ELSE 'Note present' END` | Needs note |
| Display readable text where note is missing | `COALESCE(topic_note, 'Not recorded')` | Not recorded |

## Guided lab: predict, run, change, repair

Download the [conditional expressions lab](QAI.02.01.18_Conditional_Expressions_Lab.zip), unzip it, and run both programs from its folder:

```sh
python conditional_expressions.py
python check_conditional_expressions.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module builds the four rows in memory. The first program prints:

```text
Duration categories: [(101, 'Extended'), (102, 'Short'), (103, 'Extended'), (104, 'Standard')]
Displayed notes: [(101, 'intro'), (102, 'Not recorded'), (103, 'tables'), (104, 'Not recorded')]
Basics project: [(102, 'Git Basics', 'Short', 'Needs note'), (103, 'Data Basics', 'Extended', 'tables'), (104, 'Python Basics', 'Standard', 'Needs note')]
Independent variation: [(101, 'Less practice', 'intro'), (102, 'Unestimated', 'Needs note'), (103, 'More practice', 'tables'), (104, 'Unestimated', 'Needs note')]
Stored rows unchanged: True
```

First predict the four duration categories. Change `duration_categories(db)` to `duration_categories(db, 81, 66)` in a copy of the lab. Before running, predict which boundary rows change. Restore the original call afterward. The helper binds the two thresholds with `?` placeholders as data values.

**Reproduce and repair a logic failure:** in your own query, put `WHEN duration_minutes >= 60 THEN 'Standard'` before the `>= 80` branch. Observe that 101 and 103 become “Standard.” Trace course 103: 80 satisfies the first branch, so SQL never reaches the second. Move the `>= 80` branch first and check that 101 and 103 are Extended again. The checker also covers omitted `ELSE` producing `NULL`, several `COALESCE` arguments, the mini-project, the independent variation, and unchanged source rows. Its successful run checks supplied examples; run and assess your own edits too.

## Mini-project: a readable Basics catalogue view

Return ID, title, duration category, and a readable note for courses whose titles end in `Basics`, ordered by ID. Apply the category rules: **Extended** at 80 or above, **Standard** from 60 through 79, **Short** below 60. If a note is missing, display `Needs note`. Keep the actual stored note when it is present.

Before writing SQL, identify the rows: 102 (Git Basics, 50, missing note), 103 (Data Basics, 80, tables), and 104 (Python Basics, 65, missing note). Course 101 is not a Basics title. Expected result:

| course_id | title | duration_band | displayed_note |
|---:|---|---|---|
| 102 | Git Basics | Short | Needs note |
| 103 | Data Basics | Extended | tables |
| 104 | Python Basics | Standard | Needs note |

**Reference solution:**

```sql
SELECT course_id, title,
       CASE
           WHEN duration_minutes >= 80 THEN 'Extended'
           WHEN duration_minutes >= 60 THEN 'Standard'
           ELSE 'Short'
       END AS duration_band,
       COALESCE(topic_note, 'Needs note') AS displayed_note
FROM course_catalogue
WHERE title LIKE '%Basics'
ORDER BY course_id;
```

The lab's `project_view()` implements this reference. If you instead use `WHERE topic_note IS NOT NULL`, you remove courses 102 and 104, which the project requires to be shown with a fallback label. If you place `WHEN >= 60` first, Data Basics at 80 is mislabelled Standard. These two mistakes run successfully but fail the actual request.

**Independent variation:** show a practice category and a readable note for **all four courses**, ordered by ID. The practice rules are: missing estimate → `Unestimated`; recorded estimate at least 25 → `More practice`; other recorded estimate → `Less practice`. Use `COALESCE(topic_note, 'Needs note')` for the displayed note. Predict each row before looking at the reference:

```sql
SELECT course_id,
       CASE
           WHEN practice_minutes IS NULL THEN 'Unestimated'
           WHEN practice_minutes >= 25 THEN 'More practice'
           ELSE 'Less practice'
       END AS practice_category,
       COALESCE(topic_note, 'Needs note') AS displayed_note
FROM course_catalogue
ORDER BY course_id;
```

Expected rows are `(101, 'Less practice', 'intro')`, `(102, 'Unestimated', 'Needs note')`, `(103, 'More practice', 'tables')`, and `(104, 'Unestimated', 'Needs note')`. Course 103 meets the recorded estimate boundary at 30; course 101's 20 is lower; courses 102 and 104 have no estimate. The lab's `independent_variation()` is a reference after your own attempt. Save your draft query, predicted rows, actual rows, and one explanation of a missing-value branch. A useful further check is changing the `More practice` boundary from 25 to 30: course 103 remains in that category exactly at the boundary.

## Diagnose conditional output

| Symptom | What to inspect | Repair |
|---|---|---|
| A long course shows “Standard” | Broad `WHEN >= 60` appears before `WHEN >= 80` | Test the more specific high boundary first |
| Some categories unexpectedly show `NULL` | No `WHEN` matches and `ELSE` was omitted | Add the intended fallback branch |
| Missing notes show “Note present” | Used `topic_note = NULL` in a `WHEN` | Use `topic_note IS NULL` |
| A fallback seems to have edited source data | Confused calculated display field with stored field | Query the original `topic_note` and `COUNT(topic_note)` again |
| An average changes after adding zero fallbacks | Replaced unknown numeric estimates with zeros before calculating | Decide whether zeros represent real observations; keep missing values distinct when they do not |
| A row disappears instead of getting a label | Used `WHERE` to select rows rather than `CASE` or `COALESCE` to make a result value | Return the intended rows, then calculate the display value |

## Check your understanding

1. What do `CASE`, `WHEN`, `THEN`, `ELSE`, and `END` each do?
2. Which category does a duration of exactly 80 receive under the main rule? Which category does 65 receive?
3. Why does reversing the two `WHEN` branches label course 101 incorrectly?
4. What value does a `CASE` with no matching `WHEN` and no `ELSE` produce?
5. Does `COALESCE(topic_note, 'Not recorded')` edit the stored note?
6. Why can `AVG(COALESCE(practice_minutes, 0))` differ from `AVG(practice_minutes)`?
7. When do you need `WHERE`, and when is `CASE` a better match for the question?

**Answers and reasoning**

1. `CASE` begins the expression; `WHEN` tests a condition; its `THEN` supplies a value; `ELSE` supplies a fallback; `END` closes the expression.
2. Exactly 80 is **Extended**; 65 is **Standard** because it is below 80 but at least 60.
3. 95 satisfies the broad `>= 60` branch first, so SQL never reaches the Extended branch.
4. SQL `NULL` in the derived result.
5. No. The fallback appears in the query result; the original column is still `NULL` for courses 102 and 104.
6. The second ignores missing numeric values and averages 20 and 30 to get **25**; the first introduces two zero values and averages 20, 0, 30, 0 to get **12.5**.
7. `WHERE` chooses which rows to include; `CASE` computes a condition-based value for each returned row.

## Remember and retain

- `CASE WHEN condition THEN value ... ELSE fallback END` yields one result value for a row. The first true `WHEN` wins.
- Put higher overlapping thresholds before lower ones when building duration categories; test exact boundaries and an excluded example.
- `ELSE` provides a value if no branch matches; omitting it can yield SQL `NULL`.
- `COALESCE` selects the first non-null argument and can provide a readable fallback without altering storage. A fallback zero is not automatically a measured zero.
- Retain your category trace, reversed-branch failure and repair, boundary variation, mini-project query, and independent practice labels.

## Further reading

- [SQLite: CASE expressions](https://www.sqlite.org/lang_expr.html)
- [SQLite: COALESCE](https://www.sqlite.org/lang_corefunc.html)
- [Python: SQLite parameter substitution](https://docs.python.org/3/library/sqlite3.html)
