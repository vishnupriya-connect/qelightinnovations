# Views and reusable queries

## Give a useful query a lasting name

A course catalogue holds the rows below. The `active` value is 1 for a current course and 0 for an archived course.

| course_id | title | duration_minutes | active |
|---:|---|---:|---:|
| 101 | AI Foundations | 95 | 1 |
| 102 | Git Basics | 50 | 1 |
| 103 | Data Basics | 80 | 1 |
| 104 | Python Basics | 65 | 1 |
| 105 | SQL Basics | 70 | 1 |
| 106 | Archived Basics | 120 | 0 |

Suppose the same “active courses lasting at least 70 minutes” rule is needed in several reports. We can write its `SELECT` each time, but repeated copies are easy to change inconsistently. A **view** gives the query a reusable name:

```sql
CREATE VIEW learning_courses (course_id, title, duration_minutes) AS
SELECT course_id, title, duration_minutes
FROM courses
WHERE active = 1 AND duration_minutes >= 70;
```

`CREATE VIEW` stores the **view definition**, the named `SELECT`. It does not store another permanent copy of these result rows. Reading the view runs its query against the underlying table's current data. The name can then be used in the `FROM` clause much like a table name:

```sql
SELECT course_id, title, duration_minutes
FROM learning_courses
ORDER BY course_id;
```

The initial output is `(101, 'AI Foundations', 95)`, `(103, 'Data Basics', 80)`, and `(105, 'SQL Basics', 70)`. Course 104 is too short at 65 minutes; course 106 fails the `active = 1` condition despite lasting 120 minutes. Both conditions must hold. A view is a **query abstraction**: its reader asks for the named set without rewriting the filter, while its definition remains available for inspection.

| Object | What its name represents here | Lifetime of the name | Are result rows stored by that object? |
|---|---|---|---|
| Base table `courses` | Stored course records | Until dropped | Yes |
| CTE `long_courses` introduced with `WITH` | An intermediate query in one statement | That statement | Not necessarily; SQLite chooses how to evaluate it |
| View `learning_courses` | A saved `SELECT` definition | Until dropped | No permanent result copy |
| Snapshot table `learning_snapshot` | Copied query result at a point in time | Until changed or dropped | Yes |

The **reusable query** is the rule encoded in the view definition, not a frozen list of its current rows. A CTE is useful for naming a step within one statement. A view is useful when several statements need the same named rule.

## A virtual table mental model, with a SQLite distinction

People sometimes describe a view as a **virtual table**: you can read it with `SELECT ... FROM learning_courses` and see rows and columns, although those rows are derived from a query rather than stored as the view's own data. This is a mental model for the ordinary `CREATE VIEW` above.

SQLite also has a *different* feature literally named `CREATE VIRTUAL TABLE`, which uses a registered module to connect SQL to a storage or computation engine. The view in this lesson is **not** a SQLite `CREATE VIRTUAL TABLE`. When reading SQLite documentation or error messages, keep the two terms separate.

In SQLite, ordinary views are read-only: `UPDATE learning_courses ...` raises an error. To change a course's duration in this example, update `courses`, the base table. SQLite can also use `INSTEAD OF` triggers for certain view-write behavior; this lab uses no such triggers.

## Watch a view follow source data

Suppose course 104 is revised from 65 to 85 minutes:

```sql
UPDATE courses
SET duration_minutes = 85
WHERE course_id = 104;
```

Running the same `SELECT` from `learning_courses` now gives IDs **101, 103, 104, 105**, with durations **95, 80, 85, 70**. We did not recreate the view. Its rule stayed the same; the underlying row changed. The archived course 106 remains absent.

A second reusable report can ask for the count and total duration:

```sql
SELECT COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_minutes
FROM learning_courses;
```

Initially the result is `(3, 245)` because `95 + 80 + 70 = 245`. After updating course 104, it is `(4, 330)` because `95 + 80 + 85 + 70 = 330`. Both statements read the same named rule. The outer query may select fewer columns, aggregate, join, or sort the view result as needed. Put `ORDER BY` in a consuming query when output order matters; do not assume the view's rows arrive in a particular order.

The named columns in `CREATE VIEW learning_courses (course_id, title, duration_minutes)` make the exposed fields explicit. If that list is omitted, use clear `AS` aliases for derived output fields. Avoid depending on automatically generated names.

## Inspect, replace, and drop a definition in SQLite

To inspect the saved definition in SQLite:

```sql
SELECT sql
FROM sqlite_schema
WHERE type = 'view' AND name = 'learning_courses';
```

The returned `CREATE VIEW` text includes the original `duration_minutes >= 70` condition. Suppose the team now defines a learning course as at least **80** minutes. SQLite does not provide `CREATE OR REPLACE VIEW`; drop the old view and create a new definition:

```sql
DROP VIEW learning_courses;

CREATE VIEW learning_courses (course_id, title, duration_minutes) AS
SELECT course_id, title, duration_minutes
FROM courses
WHERE active = 1 AND duration_minutes >= 80;
```

The lab makes this change *after* course 104 has become 85 minutes. The new view contains **101, 103, 104**; course 105 at 70 minutes no longer qualifies. The count and total are `(3, 260)`. Both the changed source row and the changed rule matter. If you changed only one, predict a different result before running the query.

Dropping a view removes its name and definition, not the underlying course records:

```sql
DROP VIEW IF EXISTS learning_courses;
SELECT COUNT(*) FROM courses;  -- still 6
```

`IF EXISTS` prevents an error if that view name is already absent; it does not make other failures disappear. A later `SELECT ... FROM learning_courses` fails because the view name is gone. A fresh `SELECT` from `courses` still works. Before changing a shared view, check the queries that depend on its name and column layout; keep the exposed column names and meanings stable if those consumers rely on them. In a real migration, coordinate the drop and recreation so readers do not encounter a missing or incompatible definition.

## Compare a live view with a stored result

A **materialized view** is a stored result of a query that can later be refreshed; PostgreSQL, for example, provides `CREATE MATERIALIZED VIEW` and `REFRESH MATERIALIZED VIEW`. SQLite does **not** provide those commands. We can demonstrate the *stored-result idea* in SQLite with an ordinary table:

```sql
CREATE TABLE learning_snapshot AS
SELECT course_id, title, duration_minutes
FROM learning_courses;
```

This is an ordinary snapshot table, **not** a native SQLite materialized view. It copies the three rows that qualified at creation: 101, 103, 105. Now update course 104 to 85 minutes. The live view contains four rows, including 104, while `learning_snapshot` still contains its original three rows. A reader needs to know **when a snapshot was refreshed**, or the answer may be stale.

After changing the view rule to 80 minutes, this small lab refreshes the snapshot explicitly:

```sql
DELETE FROM learning_snapshot;
INSERT INTO learning_snapshot (course_id, title, duration_minutes)
SELECT course_id, title, duration_minutes
FROM learning_courses;
```

The refreshed snapshot now has 101, 103, 104. This two-statement refresh is a teaching demonstration. In a shared application, plan for readers, failures, and a consistent refresh boundary; do not assume a plain `DELETE` followed later by an `INSERT` is invisible to other readers. A snapshot trades automatic freshness for stored results and a refresh responsibility. Also, `AS MATERIALIZED` on a SQLite CTE is an execution hint for a *statement*, not a lasting materialized view.

## Guided lab: predict, run, change, repair

Download the [views and reusable queries lab](QAI.02.01.26_Views_and_Reusable_Queries_Lab.zip), unzip it, and run these commands from its folder:

```sh
python views_queries.py
python check_views_queries.py
```

Use `python3` if needed. Python's built-in `sqlite3` creates an in-memory database each run. No server or package installation is needed. The first program prints:

```text
Initial view: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80), (105, 'SQL Basics', 70)]
Initial report: (3, 245)
After source update, view: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80), (104, 'Python Basics', 85), (105, 'SQL Basics', 70)]
After source update, snapshot: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80), (105, 'SQL Basics', 70)]
Updated report: (4, 330)
After definition change: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80), (104, 'Python Basics', 85)]
Independent short-course view: [(102, 'Git Basics')]
After explicit snapshot refresh: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80), (104, 'Python Basics', 85)]
Base table row count after drop: 6
```

**Trace first.** Write the qualifying IDs for the initial rule and the archived exception. Calculate the total minutes. Follow 104 through the update, then follow 105 through the definition change. Before running the checker, explain why the snapshot does not follow either change until refresh.

**Controlled variation.** In a copy, update course 104 to **75** instead of 85. Predict: the original 70-minute view includes 104 and reports `(4, 320)`; after changing the view boundary to 80, 104 is excluded and the view contains only 101 and 103 with report `(2, 175)`. Restore 85 before using the included checker, which checks the supplied scenario.

**Reproduce and repair a failure.** Try a second `CREATE VIEW learning_courses ...` without dropping the existing one. SQLite rejects the duplicate name. Repair by checking the intended new definition, dropping the view, and recreating it with the new threshold as in `replace_learning_view()`. Then inspect `sqlite_schema` and query the new view. The checker also attempts a direct `UPDATE` on the ordinary view and confirms the base rows did not change; make a legitimate source update through `courses` instead.

## Mini-project: a reusable course report

Build a report used by both a course list page and a planning summary. The shared rule is: **active courses with duration at least 70 minutes**. The list page needs ID, title, and duration sorted by ID. The summary needs count and total minutes. Once course 104 changes to 85 minutes, both consumers must reflect the source change without editing two separate filter expressions.

**Reference solution:**

```sql
CREATE VIEW learning_courses (course_id, title, duration_minutes) AS
SELECT course_id, title, duration_minutes
FROM courses
WHERE active = 1 AND duration_minutes >= 70;

SELECT course_id, title, duration_minutes
FROM learning_courses ORDER BY course_id;

SELECT COUNT(*) AS course_count,
       SUM(duration_minutes) AS total_minutes
FROM learning_courses;
```

Initially, the list IDs are **101, 103, 105**, and the summary is `(3, 245)`. Update course 104's base-table duration to 85, rerun both consuming queries, and get IDs **101, 103, 104, 105** and `(4, 330)`. Explain why course 106 cannot appear merely because it is long. The lab's `learning_rows()` and `report()` show both consumers. Save the two outputs, your predicted change, the view definition, and a short explanation of its source dependency.

**Independent variation:** create a `short_courses` view returning only ID and title for **active courses shorter than 70 minutes**, sorted by ID when read. Before the update, the expected IDs are **102 and 104**. After course 104 becomes 85 minutes, the expected result is only `(102, 'Git Basics')`; archived 106 is still excluded. Try it before looking at the reference:

```sql
CREATE VIEW short_courses (course_id, title) AS
SELECT course_id, title
FROM courses
WHERE active = 1 AND duration_minutes < 70;

SELECT course_id, title FROM short_courses ORDER BY course_id;
```

The lab's `short_course_view()` runs the reference after the 104 update. If 104 remains in your output, check whether your view reads the updated `courses` table. If 106 appears, check the active condition. Keep your initial prediction, SQL, actual output, and correction.

## Diagnose a mismatch

| Symptom | Check | Repair |
|---|---|---|
| Course 106 appears | View has only a duration condition | Add `active = 1` to the definition |
| Course 104 does not enter after the source update | Updated a snapshot or queried the wrong name | Update `courses`; read the live view again |
| `CREATE VIEW` says the name already exists | Old definition still exists | Review dependents, drop the old view, create the intended definition |
| Direct `UPDATE` on the view fails | SQLite ordinary views are read-only | Update the base table, then query the view |
| Course 105 remains after the boundary changes to 80 | Old 70-minute definition still in use | Inspect `sqlite_schema`; recreate the view with 80 |
| Snapshot disagrees with current view | Snapshot was copied earlier | Refresh intentionally, then recheck; state its freshness |
| Query fails after `DROP VIEW` | Its view name was removed | Recreate the view, or read the base table for a different question |

## Check your understanding

1. What does `CREATE VIEW` save, and how is that different from the rows in `learning_snapshot`?
2. Which three courses initially appear, and why is course 106 absent?
3. Why does course 104 appear in the view after changing a base row from 65 to 85?
4. What are the count and total immediately after that update, before changing the view definition?
5. After changing the boundary to 80, which IDs remain and what happens to course 105?
6. What is the difference between an ordinary SQLite view and the SQLite feature called a virtual table?
7. Why can the snapshot be stale, and does the lab create a native materialized view?
8. What happens to the base table when you drop the view?

**Answers and reasoning**

1. A view saves a named `SELECT` rule; `learning_snapshot` stores copied result rows.
2. **101, 103, 105**. Course 106 is archived (`active = 0`), despite its long duration.
3. The same saved filter evaluates current source data; 104 now meets both conditions.
4. **Four courses, 330 minutes** (`95 + 80 + 85 + 70`).
5. **101, 103, 104** remain. Course 105's 70 minutes no longer meet the 80-minute boundary.
6. A view is a saved `SELECT`; `CREATE VIRTUAL TABLE` is a distinct SQLite module-based feature.
7. Its rows are stored until refreshed. The lab creates a normal table as a demonstration, not a native materialized view.
8. Its six course records remain; only the view name and definition are removed.

## Remember and retain

- A view names a reusable query. Its output changes when its source data changes, even if the definition does not.
- A view definition can also change; distinguish changing **data** from changing the **rule**.
- SQLite replaces a view through drop and create; inspect dependencies and the exposed columns before changing a shared definition.
- An ordinary view, a SQLite virtual table, a one-statement CTE, and a stored snapshot have different mechanisms and lifetimes.
- Keep your initial and updated list, two summary totals, replacement output, snapshot trace, and independent short-course result for later review.

## Further reading

- [SQLite: CREATE VIEW](https://www.sqlite.org/lang_createview.html)
- [SQLite: DROP VIEW](https://www.sqlite.org/lang_dropview.html)
- [SQLite: CREATE VIRTUAL TABLE](https://www.sqlite.org/lang_createvtab.html)
- [PostgreSQL: materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html)
