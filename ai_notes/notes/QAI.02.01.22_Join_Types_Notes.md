# Join types

## Choose which unmatched rows to keep

The previous lesson joined courses to instructors by matching their `instructor_id` values. Continue with these source tables:

| Course ID | Course title | Instructor key |
|---:|---|---:|
| 101 | AI Foundations | 7 |
| 102 | Git Basics | 8 |
| 103 | Data Basics | 7 |
| 104 | Python Basics | 8 |
| 105 | SQL Basics | 42 |

| Instructor ID | Instructor name |
|---:|---|
| 7 | Asha |
| 8 | Ben |
| 9 | Cora |

Course 105 has no matching instructor because ID 42 does not occur in `instructors`. Cora, ID 9, has no matching course. The join condition for all the two-table examples below is `c.instructor_id = i.instructor_id`, where `c` names the course table on the left and `i` names the instructor table on the right. A **join type** determines which matched or unmatched source rows the result retains.

| Join type | Matched pairs | Unmatched course 105 | Unmatched instructor 9 |
|---|---|---|---|
| `INNER JOIN` | Keep | Omit | Omit |
| `LEFT JOIN` | Keep | Keep | Omit |
| `RIGHT JOIN` | Keep | Omit | Keep |
| `FULL OUTER JOIN` | Keep | Keep | Keep |

The source rows are not deleted by a join. A missing field in a joined result can simply mean that no row on the other side matched.

## Inner join: matched pairs only

An **inner join** returns rows whose keys satisfy the `ON` condition on both sides:

```sql
SELECT c.course_id, c.title, i.instructor_id, i.instructor_name
FROM course_catalogue AS c
INNER JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
ORDER BY c.course_id;
```

The result has **four** rows: `(101, 'AI Foundations', 7, 'Asha')`, `(102, 'Git Basics', 8, 'Ben')`, `(103, 'Data Basics', 7, 'Asha')`, and `(104, 'Python Basics', 8, 'Ben')`. Course 105 and instructor 9 are unmatched, so neither appears. In this SQLite lab, plain `JOIN` gives the same matching result as `INNER JOIN`.

## Left outer join: keep every course

A **left outer join**, written `LEFT JOIN` or `LEFT OUTER JOIN`, preserves rows from the table written **before** the join:

```sql
SELECT c.course_id, c.title, i.instructor_id, i.instructor_name
FROM course_catalogue AS c
LEFT JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
ORDER BY c.course_id;
```

The four matched rows stay as above. A fifth row appears: `(105, 'SQL Basics', NULL, NULL)`. The instructor-side fields are SQL `NULL` because no instructor row with key 42 was joined. These are **missing joined values**. The course's own stored key is still 42; it is not erased. Cora is not included because this join preserves courses on the left, not unreferenced instructor rows on the right.

To check the stored key explicitly, select `c.instructor_id AS course_instructor_id` too. The unmatched course's result would then show `course_instructor_id = 42` beside `i.instructor_id = NULL`. That distinction matters: the course references an unavailable instructor record; it did not have a missing instructor key.

## Right outer join: keep every instructor

A **right outer join**, written `RIGHT JOIN` or `RIGHT OUTER JOIN`, preserves rows from the table written **after** the join:

```sql
SELECT c.course_id, c.title, i.instructor_id, i.instructor_name
FROM course_catalogue AS c
RIGHT JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
ORDER BY COALESCE(c.course_id, 1000 + i.instructor_id);
```

The four matched rows stay. Cora adds `(NULL, NULL, 9, 'Cora')`: there is no course to supply `course_id` or `title`. Course 105 is omitted because the left side is not preserved. The `COALESCE` expression in `ORDER BY` supplies a stable position for Cora's row when the course ID is missing; it does not replace a stored course ID. Right and full outer joins require SQLite **3.39.0 or newer**. Check your Python SQLite runtime with `python -c "import sqlite3; print(sqlite3.sqlite_version)"` if the lab reports an unsupported join.

You can often express the *preserve-instructors* intent by making `instructors` the left table of a `LEFT JOIN`, but the `RIGHT JOIN` spelling here makes the right-side preservation rule visible.

## Full outer join: keep both unmatched sides

A **full outer join** keeps every matched pair and every unmatched row from either table:

```sql
SELECT c.course_id, c.title, i.instructor_id, i.instructor_name
FROM course_catalogue AS c
FULL OUTER JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
ORDER BY COALESCE(c.course_id, 1000 + i.instructor_id);
```

The result contains **six** rows: the four matched course rows, `(105, 'SQL Basics', NULL, NULL)` for the unmatched course, and `(NULL, NULL, 9, 'Cora')` for the unmatched instructor. The output is one combined view. A full join does not create an instructor for 42 or a course for 9; the unavailable side is represented with `NULL` values.

| Output case | Course ID | Course's instructor key | Joined instructor ID | Joined instructor name |
|---|---:|---:|---:|---|
| Course 105 with no instructor match | 105 | 42 | `NULL` | `NULL` |
| Cora with no course match | `NULL` | `NULL` | 9 | Cora |

The table above includes `c.instructor_id`, which you can add to the `SELECT` list when tracing a full join. It is important to qualify the two different `instructor_id` fields. In this lab, `instructors.instructor_name` is declared `NOT NULL`, so a missing joined name signals a missing instructor row. If a right-side field were itself nullable, a `NULL` value in that one field would not always prove that the entire row failed to match; test a non-null key such as `i.instructor_id` to audit unmatched rows.

## Cross join: form every combination

A **cross join**, written `CROSS JOIN`, pairs every left-table row with every right-table row without requiring a matching-key condition:

```sql
SELECT COUNT(*) AS pair_count
FROM course_catalogue AS c
CROSS JOIN instructors AS i;
```

There are five courses and three instructors, so the count is **5 × 3 = 15**. Course 101 pairs with Asha, Ben, *and* Cora in this result. This is useful only when you actually need combinations; it does not mean all three instructors teach course 101. A missing join condition in a matching query can create similarly excessive pairs. A cross join's output grows as the product of the source row counts, so calculate that size before applying it to larger tables.

## Self join: compare rows within one table

A **self join** gives the same table two different aliases so each row can be compared with another row from that table. Find distinct pairs of courses taught by the same instructor:

```sql
SELECT a.course_id AS first_course_id,
       b.course_id AS second_course_id,
       a.instructor_id
FROM course_catalogue AS a
JOIN course_catalogue AS b
  ON a.instructor_id = b.instructor_id
 AND a.course_id < b.course_id
ORDER BY a.course_id, b.course_id;
```

The pairs are `(101, 103, 7)` and `(102, 104, 8)`. The aliases `a` and `b` represent two roles of the same source table in this query. `a.course_id < b.course_id` avoids pairing a course with itself and avoids listing the same pair in both directions. Course 105 has no second course with instructor key 42, so it belongs to no output pair. A self join does not require a second stored copy of the table.

## Join multiplicity: one row can produce several result rows

Now consider a small `course_tags` table:

| course_id | tag |
|---:|---|
| 101 | starter |
| 101 | featured |
| 102 | starter |
| 104 | starter |

Course 101 matches **two tag rows**. This is **join multiplicity**: a single course row can participate in several joined pairs.

```sql
SELECT c.course_id, c.title, t.tag
FROM course_catalogue AS c
JOIN course_tags AS t ON c.course_id = t.course_id
ORDER BY c.course_id, t.tag;
```

The output is `(101, 'AI Foundations', 'featured')`, `(101, 'AI Foundations', 'starter')`, `(102, 'Git Basics', 'starter')`, and `(104, 'Python Basics', 'starter')`. The two course-101 rows are distinct when `tag` is shown. If you select only `c.course_id, c.title`, the two course-101 output rows look **identical**: a **duplicate joined row** in the displayed result. The source course table still has just one course 101. Do not automatically remove duplicates with `DISTINCT` until you know whether multiple matching tags or another relationship is the reason. Courses 103 and 105 have no tag and are absent from this ordinary matching join.

## `ON` and `WHERE` do different jobs for an outer join

The `ON` condition states which rows match. In a `LEFT JOIN`, the left row is still kept when no right row satisfies it. A `WHERE` condition then filters the produced result. Compare these two queries:

```sql
-- Keep all five courses; only show Asha if she satisfies the ON condition.
SELECT c.course_id, i.instructor_name
FROM course_catalogue AS c
LEFT JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
 AND i.instructor_name = 'Asha'
ORDER BY c.course_id;
```

This returns five course rows. Names are Asha for 101 and 103, and `NULL` for 102, 104, and 105. Ben's courses were retained as left rows but did not match the *restricted* `ON` condition.

```sql
-- Keep only the joined rows whose output name is Asha.
SELECT c.course_id, i.instructor_name
FROM course_catalogue AS c
LEFT JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
WHERE i.instructor_name = 'Asha'
ORDER BY c.course_id;
```

This returns only `(101, 'Asha')` and `(103, 'Asha')`. The `WHERE` test removes rows whose joined name is Ben or `NULL`, including the unmatched course 105. Moving a right-table test from `ON` to `WHERE` can therefore change which left rows survive. State whether your intent is to change the matching rule or to filter the final output.

## Guided lab: predict, run, vary, repair

Download the [join types lab](QAI.02.01.22_Join_Types_Lab.zip), unzip it, and run from its folder:

```sh
python join_types.py
python check_join_types.py
```

Use `python3` if needed. The standard-library `sqlite3` module creates three in-memory tables. The lab requires an SQLite runtime with `RIGHT` and `FULL OUTER JOIN` support (version 3.39.0 or later). It prints:

```text
Inner: [(101, 'AI Foundations', 7, 'Asha'), (102, 'Git Basics', 8, 'Ben'), (103, 'Data Basics', 7, 'Asha'), (104, 'Python Basics', 8, 'Ben')]
Left: [(101, 'AI Foundations', 7, 'Asha'), (102, 'Git Basics', 8, 'Ben'), (103, 'Data Basics', 7, 'Asha'), (104, 'Python Basics', 8, 'Ben'), (105, 'SQL Basics', None, None)]
Right: [(101, 'AI Foundations', 7, 'Asha'), (102, 'Git Basics', 8, 'Ben'), (103, 'Data Basics', 7, 'Asha'), (104, 'Python Basics', 8, 'Ben'), (None, None, 9, 'Cora')]
Full: [(101, 'AI Foundations', 7, 'Asha'), (102, 'Git Basics', 8, 'Ben'), (103, 'Data Basics', 7, 'Asha'), (104, 'Python Basics', 8, 'Ben'), (105, 'SQL Basics', None, None), (None, None, 9, 'Cora')]
Cross count: 15
Tag rows: [(101, 'AI Foundations', 'featured'), (101, 'AI Foundations', 'starter'), (102, 'Git Basics', 'starter'), (104, 'Python Basics', 'starter')]
Self pairs: [(101, 103, 7), (102, 104, 8)]
Unmatched audit: [(105, 'SQL Basics', 42, None, None), (None, None, None, 9, 'Cora')]
Stored tables unchanged: True
```

**Controlled variation:** change `join_rows(db, 'inner')` to `join_rows(db, 'left')` in a copy and predict the added course-105 row with missing joined instructor values. Compare `right` and `full` as well. In your own query, move `i.instructor_name = 'Asha'` between `ON` and `WHERE` as shown above; predict five rows versus two. Restore the original queries after recording what changed.

**Reproduce and repair a logic error:** select only `c.course_id, c.title` from the course-tags join. Course 101 appears twice even though it exists once in the source. Select `t.tag` too and trace the two matching tag rows. If the intended report truly needs one row per course, decide how tags should be combined or which one is wanted before changing the SQL; simply erasing a duplicate-looking row can hide a real one-to-many relationship. The checker validates the four join types, the 15-way combination count, two self-join pairs, the tag multiplicity, and an audit of unmatched rows. Compare your own changed query output separately.

## Mini-project: audit unmatched records on both sides

An editor needs one report that lists **courses without an instructor record** and **instructors without a course**. Return the course ID, title, course's instructor key, matched instructor ID, and instructor name. Expect exactly two rows: course **105** refers to key **42** without an instructor match; instructor **9**, Cora, has no course. This is a good use of a full outer join followed by a test for a missing key on either side.

**Reference solution:**

```sql
SELECT c.course_id, c.title, c.instructor_id AS course_instructor_id,
       i.instructor_id AS matched_instructor_id, i.instructor_name
FROM course_catalogue AS c
FULL OUTER JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
WHERE c.course_id IS NULL OR i.instructor_id IS NULL
ORDER BY COALESCE(c.course_id, 1000 + i.instructor_id);
```

The result is `(105, 'SQL Basics', 42, NULL, NULL)` and `(NULL, NULL, NULL, 9, 'Cora')`. `c.course_id` and `i.instructor_id` are non-null keys in their actual source rows, so a missing key in a full-join result reveals an absent source-side match. The `WHERE` clause removes the four complete matched pairs and keeps both unmatched cases. The lab's `unmatched_audit()` implements this query. As an acceptance check, a left-join query with `WHERE i.instructor_id IS NULL` alone finds course 105 but cannot include Cora because the left join does not retain unmatched right rows.

**Independent variation:** use a self join to list **pairs of distinct courses taught by the same instructor**, returning first ID, second ID, and their shared instructor ID. Order the two IDs ascending within a pair and order output by the first ID. Predict the two expected rows before inspecting the reference:

```sql
SELECT a.course_id AS first_course_id,
       b.course_id AS second_course_id,
       a.instructor_id
FROM course_catalogue AS a
JOIN course_catalogue AS b
  ON a.instructor_id = b.instructor_id
 AND a.course_id < b.course_id
ORDER BY a.course_id, b.course_id;
```

Expected result: `(101, 103, 7)` and `(102, 104, 8)`. Course 105 has no partner with key 42. The lab's `same_instructor_pairs()` is a reference after your attempt. If a course pairs with itself, check for a missing strict `<` condition. If each pair appears in both directions, check whether you used `<>` instead of `<`. Save the original prediction, actual result, repaired query if needed, and one explanation of an excluded pair.

## Diagnose a join-type mistake

| Symptom | Likely cause | Repair |
|---|---|---|
| Course 105 is missing from a course-inclusive report | Used `INNER JOIN` or preserved the instructors side | Use `LEFT JOIN` with courses on the left; inspect its unmatched row |
| Cora is missing from a two-sided audit | Used `LEFT JOIN` from courses only | Use a full outer join and test for missing keys on either side |
| Unmatched course disappears after adding a condition on instructor name | Filter on the right table was placed in `WHERE` | Decide whether the test belongs in `ON` or `WHERE`; trace the resulting `NULL` row |
| Output grows to 15 pairs | Used `CROSS JOIN` or lost the matching condition | State the relationship and compare source counts |
| Course 101 appears twice after joining tags | Two tag rows match the same course | Include the tag to expose multiplicity before deciding how to report it |
| A course pairs with itself or appears in mirrored self-join pairs | No strict order between the two aliases | Add `a.course_id < b.course_id` when each unordered pair is wanted once |
| `RIGHT` or `FULL` is rejected as unsupported | SQLite runtime is older than 3.39.0 | Inspect `sqlite3.sqlite_version` in the running Python installation and use a supported version for this lab |

## Check your understanding

1. Which join types retain course 105? Which retain Cora?
2. What values fill instructor-side columns for course 105 in a `LEFT JOIN`?
3. Why does a cross join of five courses and three instructors have 15 rows?
4. What prevents the self join from pairing course 101 with itself and listing both `(101, 103)` and `(103, 101)`?
5. Why can a joined result show course 101 twice although the course table has just one such row?
6. Why does `WHERE i.instructor_name = 'Asha'` after a left join remove course 105?
7. Why does the unmatched audit test key columns with `IS NULL` rather than assuming that a nullable description implies no match?

**Answers and reasoning**

1. `LEFT JOIN` and `FULL OUTER JOIN` retain 105. `RIGHT JOIN` and `FULL OUTER JOIN` retain Cora.
2. SQL `NULL` for the unavailable right-side instructor ID and name; course 105's own instructor key remains 42.
3. Every course pairs with every instructor: 5 × 3 = 15, without testing an instructor relationship.
4. `a.course_id < b.course_id` requires two different IDs in one chosen order.
5. It matches both `starter` and `featured` tag rows. Selecting only course fields hides the distinguishing tag while keeping both result rows.
6. Course 105 has no joined instructor name, so that `WHERE` condition is not true for its output row.
7. The selected source keys are non-null in this lab; a missing joined key indicates no counterpart. A descriptive column may itself be null in another design.

## Remember and retain

- `INNER JOIN` keeps matched pairs; `LEFT JOIN` keeps left rows; `RIGHT JOIN` keeps right rows; `FULL OUTER JOIN` keeps both sides. Unmatched fields from the absent side are `NULL`.
- `CROSS JOIN` forms every pair. A self join compares two roles of one table. One-to-many matches can yield repeated visible rows without duplicate source rows.
- For outer joins, `ON` changes which pairs match and `WHERE` filters the joined result. Moving a condition between them can change retained rows.
- Verify the actual SQLite version when using `RIGHT` and `FULL OUTER JOIN`, and keep the matched, unmatched, and multiplicity traces to explain the result.
- Retain the unmatched audit, `ON` versus `WHERE` comparison, duplicate-tag diagnosis, and self-join pair query for later practice.

## Further reading

- [SQLite: SELECT and join semantics](https://www.sqlite.org/lang_select.html)
- [SQLite: release notes for RIGHT and FULL OUTER JOIN](https://www.sqlite.org/releaselog/3_39_0.html)
- [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)
