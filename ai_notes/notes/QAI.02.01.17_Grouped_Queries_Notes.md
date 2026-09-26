# Grouped queries

## From one catalogue summary to several summaries

The previous lesson used aggregate functions to produce one summary over all selected courses. Here is the same catalogue:

| course_id | title | instructor_id | duration_minutes | lesson_count | practice_minutes |
|---:|---|---:|---:|---:|---:|
| 101 | AI Foundations | 7 | 95 | 4 | 20 |
| 102 | Git Basics | 8 | 50 | 3 | `NULL` |
| 103 | Data Basics | 7 | 80 | 4 | 30 |
| 104 | Python Basics | 8 | 65 | 3 | `NULL` |

Suppose we want a separate summary for *each instructor* without writing one query for instructor 7 and another for instructor 8. A **group** is the set of rows that share a chosen value. `instructor_id` is the **grouping column**: rows 101 and 103 belong to instructor 7's group; rows 102 and 104 belong to instructor 8's group.

```sql
SELECT instructor_id,
       COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration,
       AVG(duration_minutes) AS average_duration
FROM course_catalogue
GROUP BY instructor_id
ORDER BY instructor_id;
```

This **grouped query** returns one row per instructor:

| instructor_id | course_count | total_duration | average_duration |
|---:|---:|---:|---:|
| 7 | 2 | 175 | 87.5 |
| 8 | 2 | 115 | 57.5 |

`GROUP BY instructor_id` assigns each source row to its instructor's group. `COUNT`, `SUM`, and `AVG` then run **per group**. For instructor 7, 95 + 80 = 175 and 175 ÷ 2 = 87.5. For instructor 8, 50 + 65 = 115 and 115 ÷ 2 = 57.5. The output contains two summary rows, not the four original course rows. `ORDER BY instructor_id` fixes the display order of those two summaries; grouping by itself does not promise result order.

The grouping column appears in the output so a reader knows which summary belongs to which instructor. Do not add a plain `title` to this `SELECT` and assume it lists all titles or consistently identifies a representative title. Titles differ within each instructor group. SQLite can accept a non-grouped, non-aggregated column here and choose a value from a group, but that does not answer the intended per-course question and is not portable SQL. Select the grouping column and aggregates for a dependable summary.

## Trace an aggregate inside each group

An **aggregate per group** only sees rows assigned to that group. Missing values still follow the aggregate rules from the last lesson:

```sql
SELECT instructor_id,
       COUNT(*) AS course_count,
       COUNT(practice_minutes) AS recorded_count,
       SUM(practice_minutes) AS recorded_total
FROM course_catalogue
GROUP BY instructor_id
ORDER BY instructor_id;
```

The result is `(7, 2, 2, 50)` and `(8, 2, 0, NULL)`. Instructor 8 has two courses but no recorded practice estimate. `COUNT(*)` counts both rows; `COUNT(practice_minutes)` counts neither; `SUM(practice_minutes)` is `NULL` because it receives no present values. The Python lab displays that SQL `NULL` as `None`. A group is still present when its measured field is entirely missing: grouping uses `instructor_id`, not `practice_minutes`.

You can group by a different column to answer a different question. `GROUP BY lesson_count` gives one group for 3-lesson courses (102, 104) and one group for 4-lesson courses (101, 103). In this small dataset those groups happen to have the same memberships as the instructor groups but different names and a different reason for membership. A future course could break that coincidence. Always say which column defines the group.

## `WHERE` is a row filter before grouping

`WHERE` chooses individual source rows **before** they are divided into groups. Here we retain courses that last at least 65 minutes:

```sql
SELECT instructor_id,
       COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration
FROM course_catalogue
WHERE duration_minutes >= 65
GROUP BY instructor_id
ORDER BY instructor_id;
```

| Stage | Instructor 7 | Instructor 8 |
|---|---|---|
| Original rows | 101 (95), 103 (80) | 102 (50), 104 (65) |
| Pass `WHERE duration_minutes >= 65` | 101, 103 | 104 only |
| Grouped output `(id, count, sum)` | `(7, 2, 175)` | `(8, 1, 65)` |

Course 102 fails the **row filter**, so it contributes to no group. Course 104 passes exactly at the boundary. If you raise the minimum from 65 to 80, the remaining rows are 101 and 103, both in instructor 7's group; there is **no output row for instructor 8**. With `WHERE duration_minutes > 200`, no source row survives and this grouped query returns **zero group rows**. This differs from an ungrouped aggregate query, which can return one summary row with a zero count over an empty input.

## `HAVING` is a group filter after grouping

A **group filter** decides which completed groups may appear. Use `HAVING` for a rule involving an aggregate computed for each group:

```sql
SELECT instructor_id,
       COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration
FROM course_catalogue
GROUP BY instructor_id
HAVING SUM(duration_minutes) >= 150
ORDER BY instructor_id;
```

Both groups first form from all four rows. Instructor 7's total is 175 and passes; instructor 8's total is 115 and fails. The output is only `(7, 2, 175)`. **Instructor 8's rows were not removed before computing the 115**; the *completed group* was then excluded from this result. At a threshold of 115, both groups pass because `>=` includes the boundary.

`WHERE duration_minutes >= 150` would ask whether each **course** lasts at least 150 minutes, which no row does. That is not a replacement for `HAVING SUM(duration_minutes) >= 150`. An aggregate such as `SUM(duration_minutes)` needs the group of rows to exist before it can be tested as a group total. This is why the two filters occupy different places in the query:

```sql
SELECT grouping_column, aggregate_expression
FROM table_name
WHERE condition_on_individual_rows
GROUP BY grouping_column
HAVING condition_on_a_group
ORDER BY grouping_column;
```

`WHERE` appears before `GROUP BY`; `HAVING` appears after `GROUP BY`. `ORDER BY` sorts the surviving summary rows. In this lesson, put individual-row conditions in `WHERE` and aggregate thresholds in `HAVING` so the intended stage is clear.

## Combine the two filters without mixing their meanings

This query first excludes courses shorter than 60, then retains only instructors with at least two surviving courses:

```sql
SELECT instructor_id, COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration
FROM course_catalogue
WHERE duration_minutes >= 60
GROUP BY instructor_id
HAVING COUNT(*) >= 2
ORDER BY instructor_id;
```

The surviving individual rows are **101, 103, 104**. Instructor 7 has two such rows and total 175; instructor 8 has one such row and total 65. The final output is `(7, 2, 175)`. The count in `HAVING` is a count **after** the row filter. If the row-filter boundary changes from 60 to 50, course 102 returns, so both instructors have two rows and pass `HAVING COUNT(*) >= 2`. If instead the group threshold changes to `COUNT(*) >= 3` with the row boundary still 60, no group passes. These controlled changes tell you which stage caused an output change.

## Guided lab: predict, run, vary, repair

Download the [grouped queries lab](QAI.02.01.17_Grouped_Queries_Lab.zip), unzip it, and run from its folder:

```sh
python grouped_queries.py
python check_grouped_queries.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module creates a private in-memory catalogue. The first program prints:

```text
Per instructor: [(7, 2, 175, 87.5, 2), (8, 2, 115, 57.5, 0)]
Rows at least 65, then group: [(7, 2, 175), (8, 1, 65)]
Groups totalling at least 150: [(7, 2, 175)]
Project report: [(7, 2, 175, 87.5, 2)]
Lesson-count variation: [(4, 2, 175, 87.5)]
Stored rows unchanged: True
```

Before running, identify the IDs in each group. Then change `group_after_row_filter(db, 65)` to `group_after_row_filter(db, 80)` in a copy of the program and predict that instructor 8 disappears. Change `group_filter(db, 150)` to `group_filter(db, 115)` and predict that instructor 8 reappears at the inclusive total boundary. Restore the calls after recording results. The numbers use `?` placeholders in the lab query because they are data values.

**Reproduce a logic failure:** an editor asks for instructors whose combined courses last at least 150 minutes. Try the incorrect row rule `WHERE duration_minutes >= 150 GROUP BY instructor_id`; it returns no groups. The two individual durations 95 and 80 never meet 150 alone. Repair it to `GROUP BY instructor_id HAVING SUM(duration_minutes) >= 150` and verify instructor 7's total of 175 appears. Another easy failure is to leave out `GROUP BY` and return one total over the entire catalogue, 290, instead of one total per instructor. The checker validates row and group boundaries, the project, the separate lesson-count grouping, missing values, an empty group result, and unchanged source data. Compare your own query to the expected rows as well.

## Mini-project: instructors with multiple qualifying courses

For a planning report, consider only courses lasting **at least 60 minutes**. For each instructor, return their ID, count of qualifying courses, total duration, average duration, and number of courses with a recorded practice estimate. Show only instructors with **at least two qualifying courses**, ordered by instructor ID.

Trace the data before writing the query: courses 101 (95), 103 (80), and 104 (65) pass the row filter. Instructor 7 has two rows, total 175, average 87.5, and two recorded practice estimates. Instructor 8 has just course 104, so it fails the group threshold. Expected one-row result: `(7, 2, 175, 87.5, 2)`.

**Reference solution:**

```sql
SELECT instructor_id,
       COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration,
       AVG(duration_minutes) AS average_duration,
       COUNT(practice_minutes) AS recorded_practice_count
FROM course_catalogue
WHERE duration_minutes >= 60
GROUP BY instructor_id
HAVING COUNT(*) >= 2
ORDER BY instructor_id;
```

The lab's `project_report()` runs the same query with bound thresholds. To test it, change only the row minimum to 50: instructor 8 now has courses 102 and 104 and joins the output as `(8, 2, 115, 57.5, 0)`. Change only the required group count to 3 while keeping the 60-minute minimum: the result becomes empty. Each change has a row-level or group-level explanation.

**Independent variation:** instead of grouping by instructor, group the four courses by their **lesson count**. Return the lesson count, number of courses, total duration, and average duration. Keep only groups whose average duration is **at least 70 minutes** and order by lesson count. Predict which group survives before reading this reference:

```sql
SELECT lesson_count,
       COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_duration,
       AVG(duration_minutes) AS average_duration
FROM course_catalogue
GROUP BY lesson_count
HAVING AVG(duration_minutes) >= 70
ORDER BY lesson_count;
```

Expected row: `(4, 2, 175, 87.5)`. The three-lesson courses have durations 50 and 65, averaging 57.5, so that group is filtered out. The lab's `lesson_count_variation()` is a supplied reference after your own attempt. As an additional check, change the `HAVING` boundary to 55 and predict both groups in order: `(3, 2, 115, 57.5)` then `(4, 2, 175, 87.5)`. Save your draft query, predicted result, observed result, and one explanation of a rejected group.

## Diagnose a grouped query

| Symptom | What to inspect | Repair |
|---|---|---|
| One summary row when you expected one per instructor | Missing `GROUP BY instructor_id` | Group by the value that defines separate summaries |
| A group has a lower count than expected | `WHERE` removed source rows before grouping | Trace the source IDs that pass the row condition |
| An instructor's entire summary disappears | `HAVING` rejected the completed group or no rows survived `WHERE` | Inspect each stage and its threshold; compare 115 and 175 |
| A row-level comparison is used to test a group total | `WHERE duration_minutes >= 150` tests single courses | Test `SUM(duration_minutes)` in `HAVING` after grouping |
| A title appears alongside a group total | `title` is neither grouped nor aggregated | Remove the bare title; use a separate row query if a specific course is needed |
| Practice count is zero although the group has courses | `COUNT(practice_minutes)` excludes missing estimates | Also display `COUNT(*)` and inspect the nullable field |

## Check your understanding

1. Which course IDs belong to the instructor-7 and instructor-8 groups?
2. What is the difference between `WHERE` and `HAVING` in these examples?
3. With `WHERE duration_minutes >= 65`, why does instructor 8's grouped count become 1?
4. With no `WHERE`, which instructor survives `HAVING SUM(duration_minutes) >= 150`, and why?
5. Why does `WHERE duration_minutes >= 150` not answer the same question?
6. What rows result from the mini-project when the row minimum is changed from 60 to 50?
7. Why is a plain `title` beside `GROUP BY instructor_id` unsafe as a group description?

**Answers and reasoning**

1. Instructor 7 has **101, 103**; instructor 8 has **102, 104**.
2. `WHERE` decides which individual rows enter any group; `HAVING` decides which completed groups appear.
3. Course 102 lasts 50 and is filtered out, while course 104 lasts exactly 65 and remains.
4. Instructor **7**, because its 95 + 80 = 175 meets 150; instructor 8's 50 + 65 = 115 does not.
5. No single course lasts 150 minutes. It removes all rows before any instructor total can be calculated.
6. Both groups: `(7, 2, 175, 87.5, 2)` and `(8, 2, 115, 57.5, 0)`.
7. Each instructor has multiple titles. A non-grouped, non-aggregated title does not identify all courses or a guaranteed representative course.

## Remember and retain

- `GROUP BY` assigns rows with the same grouping-column value to a group, yielding one aggregate result row for each surviving group.
- `WHERE` is a row filter before grouping. `HAVING` is a group filter after grouping and can test aggregate values such as `COUNT(*)` or `SUM(duration_minutes)`.
- Read a grouped query by listing rows that pass `WHERE`, building each group, calculating its aggregates, applying `HAVING`, then sorting the surviving summary rows.
- Do not treat a bare title as a reliable label for an instructor group. Choose grouping columns and aggregates that match the question.
- Keep your row trace, two boundary changes, corrected 150-minute query, mini-project report, and lesson-count variation for later review.

## Further reading

- [SQLite: SELECT, grouping, and HAVING](https://www.sqlite.org/lang_select.html)
- [SQLite: aggregate functions](https://www.sqlite.org/lang_aggfunc.html)
- [Python: sqlite3 bound parameters](https://docs.python.org/3/library/sqlite3.html)
