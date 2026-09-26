# Basic data retrieval

## Ask for the fields you need

A course catalogue has four rows:

| course_id | title | instructor_id |
|---:|---|---:|
| 101 | AI Foundations | 7 |
| 102 | Git Basics | 8 |
| 103 | Data Basics | 7 |
| 104 | Python Basics | 8 |

Each row represents one course. Two courses can have the same instructor ID without being the same course. The previous lesson defined the table `course_catalogue`; this lesson retrieves information from it. **Data retrieval** means asking a database to return values you need, without changing the stored rows.

To ask for a course's ID and title:

```sql
SELECT course_id, title
FROM course_catalogue;
```

Read it as: “Select these result columns from this source table.” `SELECT` introduces the output fields; `FROM` names the **source table** whose rows supply the values. The text between `SELECT` and `FROM` is the **select list**. Here it contains two **selected columns**, `course_id` and `title`. The query produces two output columns and four result rows; `instructor_id` still exists in the table even though it is not selected.

In the displays below, rows appear in ID order for readability. In the runnable lab, queries add `ORDER BY course_id` (or another explicit order) to make the printed output repeatable. Without a sorting request, a database does not promise that the rows will arrive in the order shown. Sorting is taught in a later lesson.

## Follow a row into the result

Trace source row 101: `(101, 'AI Foundations', 7)`. The select list takes its `course_id` value 101 and `title` value `AI Foundations`, so the output row is `(101, 'AI Foundations')`. Do the same for each source row:

| Output course_id | Output title |
|---:|---|
| 101 | AI Foundations |
| 102 | Git Basics |
| 103 | Data Basics |
| 104 | Python Basics |

This is a **result set**, not another stored table. The source has three columns; this result has two. Changing the select list changes the shape of the result, not the shape of the source table.

**Controlled prediction:**

```sql
SELECT title, course_id
FROM course_catalogue
ORDER BY course_id;
```

The output headings now read `title`, `course_id`, and the first row is `('AI Foundations', 101)`. The source row did not change. The order of expressions in a select list controls the order of result columns. The `ORDER BY` line orders **rows** and is separate from the select-list order of **columns**.

## Select named columns or every column

`*` means **all-column selection** in a select list:

```sql
SELECT *
FROM course_catalogue
ORDER BY course_id;
```

For the displayed table, its result headings are `course_id`, `title`, `instructor_id`, and the first row is `(101, 'AI Foundations', 7)`. Compare:

| Select list | Output columns for this table | First output row |
|---|---|---|
| `course_id, title` | `course_id`, `title` | `(101, 'AI Foundations')` |
| `title, course_id` | `title`, `course_id` | `('AI Foundations', 101)` |
| `*` | `course_id`, `title`, `instructor_id` | `(101, 'AI Foundations', 7)` |

`*` is useful when inspecting an unfamiliar small table. In an application that expects a particular result shape, name the required columns explicitly: adding a new stored column can change the output of `SELECT *`, and pulling unwanted columns can expose or transfer more data than needed. `*` does **not** mean “all tables,” “all database rows,” or “make a copy”; the `FROM` source and any other clauses determine what the query reads. It also does not create a new table.

## Give a short name to the source table

A **table alias** is a temporary name for a table within one query. Use `AS`:

```sql
SELECT c.course_id, c.title
FROM course_catalogue AS c
ORDER BY c.course_id;
```

`c` refers to `course_catalogue` in this statement. `c.title` means the `title` column from that source. The result still has four rows and two columns named `course_id`, `title`. The stored table is **still** named `course_catalogue`; the alias is not a `RENAME` operation. It becomes especially helpful when a later query reads from two tables that both have a column named `course_id`.

This query is incorrect:

```sql
SELECT c.title
FROM course_catalogue;
```

There is no `AS c`, so SQLite cannot resolve the qualifier `c` and reports an error. Repair it by adding `AS c` after `course_catalogue`, or write the unqualified `title` while using only this one source table. In some SQL products `AS` may be optional for a table alias, but writing it explicitly helps beginners locate the temporary name.

## Name the output columns for their consumer

A **column alias** changes a result-column heading for one query:

```sql
SELECT c.course_id AS id, c.title AS course
FROM course_catalogue AS c
ORDER BY c.course_id;
```

The result headings are `id` and `course`; its first row is `(101, 'AI Foundations')`. The source column names remain `course_id` and `title`. Distinguish the two uses of `AS`:

| Location | Example | Temporary name for |
|---|---|---|
| After a source table in `FROM` | `course_catalogue AS c` | The source table in this query |
| After a selected expression | `c.title AS course` | The corresponding result column |

An alias is not the stored data. Changing `AS course` to `AS label` changes a heading without changing the value `AI Foundations` or the table schema. If another application expects a result key named `course`, changing the alias may require changing that application's code; a local alias is temporary, but its output name can still matter to consumers.

## Why can a result contain duplicates?

The four source rows have different `course_id` values. Now select only their `instructor_id` values:

```sql
SELECT instructor_id
FROM course_catalogue
ORDER BY course_id;
```

The four one-column result rows are `(7,)`, `(8,)`, `(7,)`, `(8,)`. The first and third *result rows* are duplicates, even though the underlying course rows are different. A **duplicate result** is a repeated complete output row, judged by the columns you selected. Selecting fewer columns can make distinct source rows look identical in the result.

SQL normally retains these duplicate result rows. To ask for one row per different output value, use `DISTINCT` immediately after `SELECT`:

```sql
SELECT DISTINCT instructor_id
FROM course_catalogue
ORDER BY instructor_id;
```

The **distinct result** has two rows: `(7,)` and `(8,)`. This did **not** remove either course from the source table. It removed repeated *output rows* for this query only. If your task is “show every course and its instructor,” do not use `DISTINCT` to hide course rows. If your task is “list instructor IDs represented in the catalogue,” the shorter result is appropriate.

### `DISTINCT` compares the whole selected row

Try selecting two columns:

```sql
SELECT DISTINCT instructor_id, title
FROM course_catalogue
ORDER BY instructor_id, title;
```

The result still has **four** rows:

| instructor_id | title |
|---:|---|
| 7 | AI Foundations |
| 7 | Data Basics |
| 8 | Git Basics |
| 8 | Python Basics |

The ID 7 repeats, but the **pair** `(instructor_id, title)` does not. `DISTINCT` applies to the entire select list, not only to the first column written after it. Compare a four-row query with a two-row query before deciding which one answers your question. If a stored table later gains another course taught by 7, `SELECT DISTINCT instructor_id` can still return two IDs while the catalogue contains five courses.

## Guided lab: compare query shapes

Download the [basic data retrieval lab](QAI.02.01.11_Basic_Data_Retrieval_Lab.zip), unzip it, and run both files from that folder:

```sh
python retrieval.py
python check_retrieval.py
```

Use `python3` if needed. Python's standard `sqlite3` module creates the four-row sample table in memory. `retrieval.py` executes several read queries and prints their result headings and selected values. Its expected output is:

```text
Selected headings: course_id, title
Selected first row: (101, 'AI Foundations')
All-column headings: course_id, title, instructor_id
Alias headings: id, course
Repeated instructor values: [7, 8, 7, 8]
Distinct instructor values: [7, 8]
Distinct instructor-title pairs: 4
Source rows unchanged: True
```

The Python `cursor.description` names the output columns; `fetchall()` obtains the result rows. These are *client-side* operations, not SQL keywords. The setup `CREATE TABLE` and `INSERT` operations create private sample data so you can focus on retrieval. The final comparison checks that the retrieval queries did not change any source row.

**Trace before running:** predict why `instructor_id` produces four rows but `DISTINCT instructor_id` produces two. Then change only the first read query in a copy of `retrieval.py` from `SELECT course_id, title` to `SELECT title, course_id`. Predict `Selected headings: title, course_id` and `Selected first row: ('AI Foundations', 101)`. Run it and compare.

**Deliberate failure:** in another copy, use `SELECT course_name FROM course_catalogue;`. SQLite reports `no such column: course_name`. Inspect the table definition and use the existing `title` column. A `no such table` error points instead to a wrong `FROM` name or a missing setup. `DISTINCT` cannot repair a misspelled column or table; diagnose the failed identifier first.

## Build a compact teacher directory

An enrolment page needs each instructor ID represented in the catalogue once, under the result heading `teacher_id`. Create a read-only query that returns exactly `(7,)` and `(8,)` in that order. Use a table alias, a column alias, and `DISTINCT`. Predict the headings and row count before running it.

**Reference SQL:**

```sql
SELECT DISTINCT c.instructor_id AS teacher_id
FROM course_catalogue AS c
ORDER BY teacher_id;
```

**Reference Python**, after `connection = make_connection()` and with the supplied `result()` helper:

```python
headings, rows = result(
    connection,
    "SELECT DISTINCT c.instructor_id AS teacher_id "
    "FROM course_catalogue AS c ORDER BY teacher_id;",
)
assert headings == ["teacher_id"]
assert rows == [(7,), (8,)]
print(headings, rows)
```

The supplied program's `teacher_directory()` is the same solved feature. Attempt your query first, then compare with it. To check that this is a **directory**, add one more course taught by instructor 7 in a new in-memory setup and run it again: the result should still contain one row for 7 and one for 8. The number of courses can change without changing the number of represented instructor IDs. This is a bounded preview, not a table of instructor names; resolving IDs to instructor records requires a later join lesson.

**Independent variation:** make a two-column course label list with headings `id`, `label`, sorted by `course_id`. Predict all four rows. One valid solution is:

```sql
SELECT c.course_id AS id, c.title AS label
FROM course_catalogue AS c
ORDER BY c.course_id;
```

Its first row is `(101, 'AI Foundations')`, last row is `(104, 'Python Basics')`, and it has four rows. Preserve your own initial attempt, result, and any repair before consulting this solution. The output is for a learner-facing catalogue; it does not rename either source column.

## Choose the query that matches the question

| Question | Suitable query shape | Why |
|---|---|---|
| “What is the title of every course?” | `SELECT title FROM course_catalogue` | One output row per source course |
| “Which instructor IDs appear?” | `SELECT DISTINCT instructor_id FROM course_catalogue` | Repeated output IDs are removed |
| “Which instructor teaches each titled course?” | `SELECT instructor_id, title FROM course_catalogue` | The pairing is the needed fact; a repeated ID is expected |
| “Give the UI stable ID and display label.” | `SELECT course_id AS id, title AS label FROM course_catalogue` | Explicit result names and columns for the consumer |

In the lab, add `ORDER BY` when asserting the sequence of rows. Without it, judge the values and row counts rather than assuming a displayed order. An empty source table still gives a defined output shape with zero rows; a query that returns no rows is not necessarily an error.

## Check your understanding

1. Which clause tells the database the source table? Which part tells it what the result contains?
2. What are the headings and first row for `SELECT title, instructor_id FROM course_catalogue ORDER BY course_id;`?
3. Does `SELECT *` mean all rows from every table in the database?
4. Does `AS c` rename `course_catalogue` on disk? Does `AS label` rename `title` in its schema?
5. Why do four unique course rows produce duplicate rows when only `instructor_id` is selected?
6. Why does `SELECT DISTINCT instructor_id, title` return four rows, while `SELECT DISTINCT instructor_id` returns two?
7. What must you add if a test expects the returned rows in a particular order?

**Answers and reasoning**

1. `FROM` names the source table; the select list after `SELECT` defines the output columns.
2. Headings: `title`, `instructor_id`. First row: `('AI Foundations', 7)`.
3. No. In this query `*` expands to the columns of the `FROM` source. It does not select every table.
4. No to both. The table alias and result-column alias last for this query; the stored names stay the same.
5. Two distinct courses can refer to the same instructor; once only that ID is projected, those output rows are equal.
6. `DISTINCT` compares the whole selected result row. All four `(instructor_id, title)` pairs differ; only two distinct instructor IDs exist.
7. Specify an order, for example with `ORDER BY course_id`; an unsorted query does not promise a stable row sequence.

## Remember and retain

- `SELECT` gives the output list; `FROM` gives its source. The selected columns and their order determine the result shape.
- `SELECT *` expands to the available source columns; explicit fields keep a stable, intentional output.
- `AS` can name a source table or a result column for this query. It does not modify the stored schema.
- Repeated result rows can come from different source rows. `DISTINCT` removes duplicates across **all selected columns**, for this output only.
- Without `ORDER BY`, do not infer row order from a sample display.
- Keep evidence of your predicted and actual headings, the four-versus-two-row comparison, the corrected identifier error, and the teacher directory plus your independent two-column list.

## Further reading

- [SQLite: SELECT result columns, FROM sources, DISTINCT, and ordering](https://www.sqlite.org/lang_select.html)
- [Python: using SQLite cursors](https://docs.python.org/3/library/sqlite3.html)
