# Join foundations

## Why combine two tables?

The course catalogue stores an instructor ID rather than repeating an instructor's name on every course. A separate `instructors` table stores the names. To display each course beside its instructor's name, a query must connect the tables.

**Course catalogue**

| course_id | title | instructor_id | duration_minutes |
|---:|---|---:|---:|
| 101 | AI Foundations | 7 | 95 |
| 102 | Git Basics | 8 | 50 |
| 103 | Data Basics | 7 | 80 |
| 104 | Python Basics | 8 | 65 |
| 105 | SQL Basics | 42 | 70 |

**Instructors**

| instructor_id | instructor_name |
|---:|---|
| 7 | Asha |
| 8 | Ben |
| 9 | Cora |

In this teaching dataset, course 105 deliberately has instructor ID **42**, which has no instructor row. Instructor 9, Cora, has no course. These rows let us observe what happens when a counterpart is missing. The small lab does not enforce a foreign-key constraint; in a system that requires every course to refer to an existing instructor, that rule would be defined and checked separately.

A **join** combines information from rows of two tables using a stated relationship. The **joined result** is a query output made from values of matching rows; it does not merge the stored tables into a new permanent table.

```sql
SELECT c.course_id, c.title, i.instructor_name
FROM course_catalogue AS c
JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
ORDER BY c.course_id;
```

Expected output:

| course_id | title | instructor_name |
|---:|---|---|
| 101 | AI Foundations | Asha |
| 102 | Git Basics | Ben |
| 103 | Data Basics | Asha |
| 104 | Python Basics | Ben |

The expression after `ON` is the **join condition**. The `instructor_id` values on both sides are the **join keys**. For course 101, `7 = 7` is true, so its title is paired with Asha's name. Course 103 also has key 7 and pairs with Asha. For course 102 and course 104, key 8 pairs with Ben. This result has four rows because four course rows find an instructor match. `ORDER BY c.course_id` makes the displayed order predictable.

## Trace a match and an unmatched row

Look up the values on each side before reasoning about the result:

| Course | Course's instructor key | Available instructor key | Match in this query? | Joined name |
|---:|---:|---:|---|---|
| 101 | 7 | 7 | Yes | Asha |
| 102 | 8 | 8 | Yes | Ben |
| 103 | 7 | 7 | Yes | Asha |
| 104 | 8 | 8 | Yes | Ben |
| 105 | 42 | No row with 42 | No | No joined row |

A **matching row** is a source row that finds a counterpart satisfying the `ON` condition. An **unmatched row** has no qualifying counterpart. With the ordinary `JOIN` used above, unmatched course 105 does not appear. Instructor 9 is also unmatched and does not appear. Both source rows **still exist** in their own tables. The next lesson compares join types that handle unmatched rows in different ways; for this lesson, trace the keys and understand why the displayed four-row result differs from the five-row source catalogue.

The **left table** in the statement is the one before `JOIN`, `course_catalogue`. The **right table** is the one after `JOIN`, `instructors`. These words describe positions in the SQL statement; they do not by themselves mean one table has priority in an ordinary matching join. The distinction will matter when a later lesson keeps unmatched rows from a chosen side.

## Name the correct relationship

The join condition must express the actual relationship between tables. This is wrong:

```sql
SELECT c.course_id, i.instructor_name
FROM course_catalogue AS c
JOIN instructors AS i
  ON c.course_id = i.instructor_id;
```

The `course_id` values are 101–105, while instructor IDs are 7, 8, and 9. The query runs but returns **zero rows**. The numbers have different meanings even though both are IDs. A valid join condition is a rule from the data model: `c.instructor_id = i.instructor_id`. Inspect the relevant source columns and a known pair, such as course 101 to instructor 7, before trusting a joined output.

In SQLite, leaving the `ON` condition out of this `JOIN` permits **every course to pair with every instructor**. Five course rows × three instructor rows produce **15** result rows, including false associations such as course 101 with Ben and Cora. This is not a lookup of actual instructors. The lab checks the 15-row count to make a missing condition observable. Other SQL systems can handle an omitted condition differently; always write the intended relationship explicitly.

## Use table aliases and qualified column names

`AS c` and `AS i` are **table aliases in a join**: short names for the two tables within this query. A **qualified column name** includes its source, such as `c.course_id` or `i.instructor_name`. It lets a reader see which table supplies each value. The join condition uses both qualified names, `c.instructor_id = i.instructor_id`.

Both tables contain a column named `instructor_id`. This statement has an **ambiguous column name**:

```sql
SELECT instructor_id
FROM course_catalogue AS c
JOIN instructors AS i
  ON c.instructor_id = i.instructor_id;
```

SQLite reports an ambiguity error because `instructor_id` could refer to either table. Qualify it as `c.instructor_id` or `i.instructor_id` according to the question. For matched pairs their values happen to be equal, but you still need to identify the source in SQL.

There is a different issue when you *deliberately select both* columns:

```sql
SELECT c.instructor_id, i.instructor_id
FROM course_catalogue AS c
JOIN instructors AS i ON c.instructor_id = i.instructor_id
ORDER BY c.course_id;
```

This query is valid, but its output has a **duplicate column name**: two result fields both labelled `instructor_id`. The values for the four matches are `(7, 7)`, `(8, 8)`, `(7, 7)`, and `(8, 8)`. Duplicate output labels can confuse a reader or code that looks up a field by name. Give each field a distinct output alias:

```sql
SELECT c.instructor_id AS course_instructor_id,
       i.instructor_id AS matched_instructor_id
FROM course_catalogue AS c
JOIN instructors AS i ON c.instructor_id = i.instructor_id
ORDER BY c.course_id;
```

The `AS` after a table name defines a **table alias** for qualifying references; the `AS` after a selected expression defines an **output column alias**. These solve related but different naming problems. The lab checks the ambiguity error, the duplicate output labels, and the repaired output labels.

## Filter the joined rows

First connect matching rows with `ON`, then use `WHERE` to select the joined rows that satisfy another rule:

```sql
SELECT c.course_id, c.title, i.instructor_name, c.duration_minutes
FROM course_catalogue AS c
JOIN instructors AS i ON c.instructor_id = i.instructor_id
WHERE c.duration_minutes >= 65
ORDER BY c.course_id;
```

The result is `(101, 'AI Foundations', 'Asha', 95)`, `(103, 'Data Basics', 'Asha', 80)`, and `(104, 'Python Basics', 'Ben', 65)`. Course 102 has a matching instructor but fails the duration filter at 50. Course 105 meets the duration filter at 70 but has **no matching instructor**, so it is absent for a different reason. Distinguish the two stages when debugging a missing result:

| Course | Instructor match? | Duration at least 65? | In final joined result? |
|---:|---|---|---|
| 101 | Yes | Yes | Yes |
| 102 | Yes | No | No |
| 103 | Yes | Yes | Yes |
| 104 | Yes | Yes, exactly 65 | Yes |
| 105 | No | Yes | No |

**Controlled variation:** change the duration boundary from 65 to 70. Course 104 at 65 leaves the result; 101 and 103 stay. Course 105 still does not appear because changing `WHERE` cannot create an instructor row with key 42. The expected IDs are **101, 103**.

## Guided lab: predict, run, diagnose

Download the [join foundations lab](QAI.02.01.21_Join_Foundations_Lab.zip), unzip it, and run from its folder:

```sh
python join_foundations.py
python check_join_foundations.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module creates the two tables in memory. The first program prints:

```text
Matched courses: [(101, 'AI Foundations', 'Asha'), (102, 'Git Basics', 'Ben'), (103, 'Data Basics', 'Asha'), (104, 'Python Basics', 'Ben')]
Project, at least 65: [(101, 'AI Foundations', 'Asha', 95), (103, 'Data Basics', 'Asha', 80), (104, 'Python Basics', 'Ben', 65)]
Independent variation: [(102, 'Git Basics', 'Ben'), (104, 'Python Basics', 'Ben')]
Course 105's key: (105, 42)
Instructor 9: (9, 'Cora')
Both tables unchanged: True
```

Predict the four matches and the two unmatched source rows before running. Then change `project_rows(db)` in a copy of the script to `project_rows(db, 70)` and check for IDs 101 and 103. Restore the original call afterward; the function binds the threshold using `?`.

**Reproduce and repair two errors:** replace `c.instructor_id` with `c.course_id` on the left of the `ON` equality. It runs but returns no matches; verify a known course and restore the actual join key. Then try the unqualified `SELECT instructor_id` example and observe the ambiguity error; repair it by choosing a table alias and checking the selected output field. A third experiment is to omit the `ON` condition on a fresh lab query and count 15 false combinations, then restore it. The checker covers these failures, output name collisions, the project, the independent variation, and unchanged source rows. Its passing result verifies the supplied queries; run your own edited statement and compare its rows too.

## Mini-project: longer courses with instructor names

Produce a report of matching courses lasting **at least 65 minutes**, showing course ID, title, instructor name, and duration in course-ID order. The expected three rows are:

| course_id | title | instructor_name | duration_minutes |
|---:|---|---|---:|
| 101 | AI Foundations | Asha | 95 |
| 103 | Data Basics | Asha | 80 |
| 104 | Python Basics | Ben | 65 |

**Reference solution:**

```sql
SELECT c.course_id, c.title, i.instructor_name, c.duration_minutes
FROM course_catalogue AS c
JOIN instructors AS i
  ON c.instructor_id = i.instructor_id
WHERE c.duration_minutes >= 65
ORDER BY c.course_id;
```

The lab's `project_rows()` runs this query. For acceptance, check 104 at the exact boundary, 102 as a matched course below the boundary, and 105 as a long course without an instructor match. A result of four or five rows needs a careful examination of the relationship and filter; a result of zero rows can indicate the wrong join key.

**Independent variation:** return the course ID, title, and instructor name for **Basics** courses taught by instructor **8**, ordered by course ID. Write the query yourself, using both the relationship in `ON` and the two selection conditions in `WHERE`. The expected rows are `(102, 'Git Basics', 'Ben')` and `(104, 'Python Basics', 'Ben')`.

```sql
SELECT c.course_id, c.title, i.instructor_name
FROM course_catalogue AS c
JOIN instructors AS i ON c.instructor_id = i.instructor_id
WHERE i.instructor_id = 8 AND c.title LIKE '%Basics'
ORDER BY c.course_id;
```

The lab's `independent_variation()` is the reference to inspect after your own attempt. Course 103 has a Basics title but belongs to instructor 7; course 101 belongs to instructor 7 and is not a Basics title; course 105 has no matched instructor 42. Keep the relationship you chose, your prediction, your output, and one explanation of a rejected course. The same pattern can answer questions about other instructor IDs by changing the bound value in the lab function.

## Diagnose a missing or excessive joined result

| Symptom | Possible cause | Check and repair |
|---|---|---|
| Zero matches though a known relationship exists | Wrong join keys, such as course ID compared with instructor ID | Check the meanings and values of each key; use `c.instructor_id = i.instructor_id` |
| 15 rows instead of four | Omitted `ON`, so every course pairs with every instructor in this SQLite lab | Add the relationship condition and inspect known pairs |
| Course 105 absent | Instructor key 42 has no right-table match | Inspect both source tables; the next lesson explores how join types handle unmatched rows |
| Course 102 absent only in the long-course report | Duration 50 fails `WHERE c.duration_minutes >= 65` | Inspect its match and its filter separately |
| `ambiguous column name: instructor_id` | Both tables have a column with that name | Qualify with `c.` or `i.` |
| Two output columns are both labelled `instructor_id` | Selected both qualified fields without distinct output labels | Use `AS course_instructor_id` and `AS matched_instructor_id` |

## Check your understanding

1. Which column pair is the join key relationship between the two tables?
2. What is the left table, and what is the right table in the main query?
3. Why do courses 101 and 103 both display Asha?
4. Why is course 105 missing from the four-row joined result? Has it been deleted?
5. What happens in this SQLite example if you leave out `ON`?
6. Why does unqualified `instructor_id` cause an error, whereas `c.instructor_id` works?
7. What is the difference between an ambiguous input column name and duplicate output column names?

**Answers and reasoning**

1. `course_catalogue.instructor_id = instructors.instructor_id`; with aliases, `c.instructor_id = i.instructor_id`.
2. `course_catalogue` is to the left of `JOIN`; `instructors` is to the right.
3. Both courses carry instructor key 7, which matches Asha's row.
4. Its key 42 matches no instructor row. It remains stored in `course_catalogue`.
5. Five courses each pair with three instructors, yielding **15** combinations, many of them false associations.
6. Both tables supply an `instructor_id` field; `c.` identifies the course-table field.
7. An ambiguous input name cannot be resolved to one source and errors. Selecting both explicitly is valid, but the result may have the same output label twice; use distinct aliases.

## Remember and retain

- A join combines matching source rows in a query result. The `ON` condition states which keys represent the relationship.
- An ordinary matching `JOIN` shows four matched courses here; unmatched course 105 and instructor 9 remain in their tables but do not appear in that result.
- Table aliases such as `c` and `i` make qualified names clear. Qualify shared field names and give duplicate output fields distinct aliases.
- Trace a missing result through the relationship first, then through any `WHERE` condition. A wrong or missing relationship can produce zero or excessive rows.
- Retain the source-key trace, wrong-key repair, ambiguous-name repair, changed threshold, mini-project report, and independent variation for later practice.

## Further reading

- [SQLite: SELECT and joins](https://www.sqlite.org/lang_select.html)
- [SQLite: SQL expression and column references](https://www.sqlite.org/lang_expr.html)
- [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)
