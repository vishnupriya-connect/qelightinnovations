# Aggregate functions

## Turn several rows into a summary

Continue with the course catalogue. The new `practice_minutes` field is an optional estimate of practice time; `NULL` means no estimate has been recorded:

| course_id | title | instructor_id | duration_minutes | lesson_count | topic_note | practice_minutes |
|---:|---|---:|---:|---:|---|---:|
| 101 | AI Foundations | 7 | 95 | 4 | intro | 20 |
| 102 | Git Basics | 8 | 50 | 3 | `NULL` | `NULL` |
| 103 | Data Basics | 7 | 80 | 4 | tables | 30 |
| 104 | Python Basics | 8 | 65 | 3 | `NULL` | `NULL` |

An **aggregate function** computes a summary from values across multiple rows. **Aggregation** is the act of reducing those rows to a summary. For example, `SUM(duration_minutes)` combines 95, 50, 80, and 65 into **290**. That **aggregate result** answers a question about the selected rows rather than returning each course separately.

```sql
SELECT COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_minutes
FROM course_catalogue;
```

The result is one row: `(4, 290)`. `AS` gives useful names to the output fields. Without a `GROUP BY` clause, all rows that pass `WHERE` form one input group for the aggregate. A **grouped value** such as the sum is one value computed from that group of rows. The next lesson will show how to produce separate summaries for several groups. Here we deliberately calculate one summary over the entire catalogue or over one filtered subset. Do not put a plain `title` next to `COUNT(*)` and expect the result to list four titles: that would confuse a single summary row with individual source rows, and SQLite's handling of such a bare column is not a portable way to identify a course.

## Count all rows, present values, and distinct values

`COUNT` has three useful forms:

```sql
SELECT COUNT(*) AS all_courses,
       COUNT(topic_note) AS courses_with_notes,
       COUNT(DISTINCT instructor_id) AS different_instructors
FROM course_catalogue;
```

Expected one-row result: `(4, 2, 2)`.

| Expression | What it counts here | Result |
|---|---|---:|
| `COUNT(*)` | **All rows**, including those with missing fields | 4 |
| `COUNT(topic_note)` | Rows whose `topic_note` is **non-null** | 2 |
| `COUNT(DISTINCT instructor_id)` | Different non-null instructor IDs: 7 and 8 | 2 |

These are different questions. Course 102 still contributes to `COUNT(*)`, though its `topic_note` is missing. `COUNT(topic_note)` ignores its missing note. `DISTINCT` eliminates repeated values before `COUNT`: instructor 7 occurs twice but is counted once. If you instead use `COUNT(DISTINCT duration_minutes)`, the result is **4** because all four durations differ. `COUNT(DISTINCT topic_note)` is **2** here (`intro`, `tables`); it does not count the two `NULL` entries as another note value.

For this catalogue, `COUNT(*) - COUNT(topic_note)` is **2**, the number of rows with missing notes. This subtraction works because every source row is counted once by `COUNT(*)` while only nonmissing notes are counted by `COUNT(topic_note)`. If you need the actual missing rows, query them with `WHERE topic_note IS NULL` as in the preceding lesson.

## Add, average, and find extremes

The other common aggregate functions operate on a numeric column in these examples:

```sql
SELECT SUM(duration_minutes) AS total_minutes,
       AVG(duration_minutes) AS average_minutes,
       MIN(duration_minutes) AS shortest_minutes,
       MAX(duration_minutes) AS longest_minutes
FROM course_catalogue;
```

The result is `(290, 72.5, 50, 95)`:

| Function | Trace over the four durations | Result |
|---|---|---:|
| `SUM` | 95 + 50 + 80 + 65 | 290 |
| `AVG` | 290 ÷ 4 non-null durations | 72.5 |
| `MIN` | Smallest duration | 50 |
| `MAX` | Largest duration | 95 |

`MIN(duration_minutes)` gives the smallest **duration**, not the ID or title of the course with that duration. Likewise `MAX` gives the largest value, not an entire row. If the question is “which course is longest?”, use a sorted row query such as `SELECT course_id, title, duration_minutes FROM course_catalogue ORDER BY duration_minutes DESC, course_id ASC LIMIT 1`. That produces course 101 and explicitly handles which row wins a tie. `AVG` can return a fractional result even when each stored duration is an integer.

## What happens to missing numeric values?

Look at `practice_minutes`: 20 and 30 are present; two other rows have SQL `NULL`. For `COUNT(column)`, `SUM`, `AVG`, `MIN`, and `MAX`, the missing inputs are ignored when the function receives values from this column:

```sql
SELECT COUNT(*) AS courses,
       COUNT(practice_minutes) AS courses_with_estimate,
       SUM(practice_minutes) AS estimated_total,
       AVG(practice_minutes) AS estimated_average,
       MIN(practice_minutes) AS smallest_estimate,
       MAX(practice_minutes) AS largest_estimate
FROM course_catalogue;
```

The result is `(4, 2, 50, 25.0, 20, 30)`.

| Row | Practice estimate | Included in `COUNT(*)`? | Included in `COUNT(practice_minutes)` and the numeric calculation? |
|---:|---:|---|---|
| 101 | 20 | Yes | Yes |
| 102 | `NULL` | Yes | No |
| 103 | 30 | Yes | Yes |
| 104 | `NULL` | Yes | No |

This is **null in aggregation**: the aggregate over the recorded estimates uses **two** numbers. The average is `(20 + 30) ÷ 2 = 25`, not `50 ÷ 4 = 12.5`. A missing estimate does not mean zero minutes. If your question truly requires missing estimates to be treated as zero, first state and justify that rule; it would answer a *different* question. Keep the count of recorded estimates next to their average so a reader can see its denominator.

**Controlled change:** if a real estimate of `0` is recorded for course 102, it is no longer missing: `COUNT(practice_minutes)` becomes 3, the sum stays 50, and `AVG(practice_minutes)` becomes approximately 16.67. A recorded zero affects the denominator; an unknown estimate does not. This is a prediction to test in a separate copy of the lab data, then restore the original row.

## Filter before summarising

A `WHERE` clause selects the rows that feed the aggregate. It does not turn them into multiple output rows:

```sql
SELECT COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_minutes,
       AVG(duration_minutes) AS average_minutes
FROM course_catalogue
WHERE instructor_id = 7;
```

Courses 101 and 103 pass the filter, so the one-row result is `(2, 175, 87.5)`. The trace is `95 + 80 = 175`, then `175 ÷ 2 = 87.5`. Instructor 8 would produce `(2, 115, 57.5)` using courses 102 and 104. A fixed `WHERE instructor_id = 7` is a single-subset summary. Asking for instructor 7 and 8 summaries *side by side as separate rows* requires grouping, covered next.

An important distinction is **no matching rows** versus **matching rows whose measured value is always missing**:

| Input to the aggregate | `COUNT(*)` | `COUNT(practice_minutes)` | `SUM(practice_minutes)` | `AVG(practice_minutes)` |
|---|---:|---:|---|---|
| All four courses | 4 | 2 | 50 | 25.0 |
| Instructor 8: courses 102 and 104, both estimates missing | 2 | 0 | `NULL` | `NULL` |
| Courses over 200 minutes: no rows | 0 | 0 | `NULL` | `NULL` |

For an aggregate query without `GROUP BY`, SQLite still returns **one summary row** when `WHERE` matches no rows. `COUNT(*)` and `COUNT(column)` are 0; `SUM`, `AVG`, `MIN`, and `MAX` on that empty input are `NULL`. Do not call `SUM`'s `NULL` a measured total of zero. In the instructor-8 case, rows exist, but neither provides a practice estimate. In a no-match case such as `WHERE duration_minutes > 200`, there are no rows at all. The two counts distinguish those situations. A filtered aggregate does not remove or update rows in the table.

## Guided lab: predict, run, vary, repair

Download the [aggregate functions lab](QAI.02.01.16_Aggregate_Functions_Lab.zip), unzip it, and run both programs from its folder:

```sh
python aggregate_functions.py
python check_aggregate_functions.py
```

Use `python3` if needed. The lab uses the standard-library `sqlite3` module and an in-memory table. The first program prints:

```text
Catalogue: (4, 2, 2, 290, 72.5, 50, 95)
Practice: (4, 2, 50, 25.0, 20, 30)
Range project: (3, 10, 65.0, 2, 1, 30)
Instructor 7: (2, 175, 87.5, 80, 95, 2, 50)
Instructor 8: (2, 115, 57.5, 50, 65, 0, None)
No matching rows: (0, None, None, None, None)
Stored rows unchanged: True
```

Python displays a SQL `NULL` as `None` in a fetched result. Before running, predict the denominator of `AVG(practice_minutes)`, then inspect the first two summary lines. Change `range_report(db)` in `main()` to `range_report(db, 51, 79)`. Only course 104 qualifies, so predict `(1, 3, 65.0, 1, 0, None)` before running. Restore the original call afterward. The function binds the two boundaries using `?` placeholders.

**Reproduce a plausible mistake:** manually divide `SUM(practice_minutes)` by `COUNT(*)` and get `50 ÷ 4 = 12.5`. Compare it to SQL's `AVG(practice_minutes) = 25.0`; check the two rows with missing values. Repair your explanation to use the count of **present numeric estimates**, `COUNT(practice_minutes) = 2`. Test the all-null instructor-8 subset too: its sum and average are `NULL`, not zero, while the total row count is 2. The checker covers distinct counts, normal numeric results, missing values, an empty input, both range boundaries, and the independent variation. It validates the supplied functions; run and compare your own query separately.

## Mini-project: a short-course summary

An editor wants one report for courses lasting **50 through 80 minutes inclusive**. Return the number of courses, total lessons, average duration, number of different instructors, count of courses with recorded practice estimates, and sum of those recorded practice estimates. Work out the rows before writing SQL: courses **102, 103, 104** qualify. They have 3 + 4 + 3 = **10** lessons and 50 + 80 + 65 = **195** duration minutes; `195 ÷ 3 = 65`. Instructors 8 and 7 give **2** distinct IDs. Only course 103 records practice minutes, **30**. The expected summary is `(3, 10, 65.0, 2, 1, 30)`.

**Reference solution:**

```sql
SELECT COUNT(*) AS course_count,
       SUM(lesson_count) AS lesson_total,
       AVG(duration_minutes) AS average_duration,
       COUNT(DISTINCT instructor_id) AS instructor_count,
       COUNT(practice_minutes) AS recorded_practice_count,
       SUM(practice_minutes) AS recorded_practice_total
FROM course_catalogue
WHERE duration_minutes BETWEEN 50 AND 80;
```

The lab's `range_report()` runs this query with bound range values. A useful acceptance check is changing the range to 51 through 79. Only course 104 remains: course 102 at 50 and course 103 at 80 have been excluded. With course 104's estimate missing, the report's last two values are `0` and `NULL`, respectively. If you expected the project to return three rows, revisit what an ungrouped aggregate query returns: it is one summary over the three qualifying rows.

**Independent variation:** create one summary for instructor 7's courses. Return, in order: row count; total, average, minimum, and maximum duration; count of present practice estimates; sum of practice estimates. Predict the values before inspecting this reference:

```sql
SELECT COUNT(*), SUM(duration_minutes), AVG(duration_minutes),
       MIN(duration_minutes), MAX(duration_minutes),
       COUNT(practice_minutes), SUM(practice_minutes)
FROM course_catalogue
WHERE instructor_id = 7;
```

Expected result: `(2, 175, 87.5, 80, 95, 2, 50)`. The two courses are 101 and 103. Both have recorded practice estimates; 20 + 30 = 50. The lab's `instructor_report(db, 7)` gives the same reference row. As a diagnostic extension, run the same rule for instructor 8 and explain why it returns `(2, 115, 57.5, 50, 65, 0, None)`. Preserve your prediction, query, observed result, and one corrected mistake if needed.

## Diagnose common aggregate faults

| Symptom | Cause to check | Repair |
|---|---|---|
| Row count unexpectedly low | `COUNT(nullable_column)` counts present values, not all rows | Use `COUNT(*)` for rows; keep both counts if missingness matters |
| Unique instructor count is 4 | Counted rows rather than distinct values | Use `COUNT(DISTINCT instructor_id)`; trace IDs 7, 8, 7, 8 |
| Practice average appears too low | Divided sum by all four rows and treated unknown estimates as zero | Compare `COUNT(practice_minutes)` with `COUNT(*)`; use `AVG(practice_minutes)` for the recorded estimates |
| Sum or average is `NULL` while rows exist | Every value in the measured column is missing | Check `COUNT(*)` and `COUNT(column)` together; report missing data faithfully |
| A maximum value is mistaken for a whole course | `MAX(column)` returns a value, not the full row | Retrieve a sorted row with `ORDER BY ... DESC LIMIT 1` if a course is needed |
| Summary after a `WHERE` filter differs | Wrong rows entered the calculation or a boundary was excluded | List qualifying IDs first, then calculate the aggregate by hand |

## Check your understanding

1. What does `COUNT(*)` report here, and why does `COUNT(topic_note)` differ?
2. Why is `COUNT(DISTINCT instructor_id)` 2?
3. What are `SUM(duration_minutes)`, `AVG(duration_minutes)`, `MIN(duration_minutes)`, and `MAX(duration_minutes)` for the full catalogue?
4. Why is `AVG(practice_minutes)` 25 instead of 12.5?
5. What does `SUM(practice_minutes)` return for instructor 8, whose two courses lack estimates?
6. Does an ungrouped aggregate query with a `WHERE` condition matching no rows return zero rows or one summary row in SQLite?
7. Why does `MAX(duration_minutes)` alone not identify the longest course's title?

**Answers and reasoning**

1. `COUNT(*)` is **4** because it counts all four rows; `COUNT(topic_note)` is **2** because two notes are `NULL`.
2. The nonmissing instructor IDs are 7, 8, 7, 8; removing duplicates leaves 7 and 8.
3. Total **290**, average **72.5**, minimum **50**, maximum **95**.
4. Only estimates 20 and 30 are present; SQL divides their sum 50 by **2** recorded values.
5. SQL `NULL`, displayed as `None` by Python; there are no non-null practice values to sum for that subset.
6. **One summary row**: `COUNT(*)` is 0 and the other numeric aggregates have `NULL` results for empty input.
7. It returns only the maximum numeric value. A row query sorted by duration with a tie breaker returns the associated course information.

## Remember and retain

- An aggregate function condenses selected rows into a grouped value; without `GROUP BY`, this lesson returns one summary row.
- `COUNT(*)` counts rows, `COUNT(column)` counts present values, and `COUNT(DISTINCT column)` counts different present values.
- `SUM`, `AVG`, `MIN`, and `MAX` summarise their input values; SQL `NULL` inputs are ignored here. Check the count used for an average.
- With no numeric inputs, `SUM`, `AVG`, `MIN`, and `MAX` return `NULL`; `COUNT` returns 0. A filtered aggregate may still have one result row even when no source row matches.
- Retain the counts trace, the repaired average-denominator explanation, the changed-boundary result, the mini-project query, and your instructor variation.

## Further reading

- [SQLite: built-in aggregate functions](https://www.sqlite.org/lang_aggfunc.html)
- [SQLite: aggregate SELECT queries](https://www.sqlite.org/lang_select.html)
- [Python: SQLite parameter substitution](https://docs.python.org/3/library/sqlite3.html)
