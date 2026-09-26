# Sorting and limiting results

## Which row comes first?

Continue with the four-course catalogue:

| course_id | title | instructor_id | duration_minutes | lesson_count | topic_note |
|---:|---|---:|---:|---:|---|
| 101 | AI Foundations | 7 | 95 | 4 | intro |
| 102 | Git Basics | 8 | 50 | 3 | `NULL` |
| 103 | Data Basics | 7 | 80 | 4 | tables |
| 104 | Python Basics | 8 | 65 | 3 | `NULL` |

Earlier lessons used `ORDER BY course_id` to display answers predictably. **Result order** is the order in which the query returns rows. A table's display or insertion order does not guarantee a query's output order. Without `ORDER BY`, even if four IDs appear in the same sequence during one run, do not rely on that sequence for the next query. Sorting affects the query result, not the stored rows.

## Choose a sort column and direction

Add `ORDER BY` after `FROM` and any `WHERE` clause:

```sql
SELECT course_id, title, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes ASC;
```

`duration_minutes` is the **sort column**. `ASC` means **ascending order**, from the smaller duration to the larger duration:

| Position | course_id | duration_minutes |
|---:|---:|---:|
| 1 | 102 | 50 |
| 2 | 104 | 65 |
| 3 | 103 | 80 |
| 4 | 101 | 95 |

The result IDs are **102, 104, 103, 101**. For a simple SQLite `SELECT`, `ORDER BY duration_minutes` has the same ascending direction by default; write `ASC` when it helps a reader see the rule. The direction applies to this column, not to the ID shown alongside it.

Use `DESC` for **descending order**, from the larger duration to the smaller duration:

```sql
SELECT course_id, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes DESC;
```

The IDs become **101, 103, 104, 102**. Changing `ASC` to `DESC` changes the order of the result; no duration value changes. The title is another possible sort column: `ORDER BY title ASC` gives **101, 103, 102, 104** in this catalogue (`AI`, `Data`, `Git`, `Python`). Text sorting can depend on database collation and configuration, so examples use ordinary ASCII titles. The query can also sort by a column you did not display: `SELECT course_id, title ... ORDER BY duration_minutes DESC` still returns the IDs in descending duration order.

| Requested order | SQL after `FROM course_catalogue` | Result IDs |
|---|---|---|
| Shortest to longest | `ORDER BY duration_minutes ASC` | 102, 104, 103, 101 |
| Longest to shortest | `ORDER BY duration_minutes DESC` | 101, 103, 104, 102 |
| Title A to Z | `ORDER BY title ASC` | 101, 103, 102, 104 |

## Break ties with another key

Two courses share instructor 7, and two share instructor 8. If you sort only by `instructor_id ASC`, you know that both instructor-7 rows precede both instructor-8 rows, but you have not specified which row comes first *within* either tied group. A visible order in a particular run is not a guarantee for tied rows.

List sort keys from most important to next most important:

```sql
SELECT course_id, instructor_id, title
FROM course_catalogue
ORDER BY instructor_id ASC, title ASC, course_id ASC;
```

`instructor_id` is the **primary sort key**: group rows by instructor, 7 before 8. `title` is the **secondary sort key**: order names inside each instructor group. `course_id` is a final, unique tie breaker if an instructor has two identically named courses. In this data, the resulting IDs are **101, 103, 102, 104**.

| Instructor group | Titles sorted A to Z within the group | IDs |
|---:|---|---|
| 7 | AI Foundations, Data Basics | 101, 103 |
| 8 | Git Basics, Python Basics | 102, 104 |

The key directions can differ. `ORDER BY instructor_id ASC, title DESC, course_id ASC` yields **103, 101, 104, 102**. The first group is still instructor 7, but within that group `Data` comes before `AI`; within instructor 8, `Python` comes before `Git`. For a numeric tie example, `ORDER BY lesson_count DESC, duration_minutes ASC, course_id ASC` yields **103, 101, 102, 104**: first the 4-lesson pair, shorter duration first, then the 3-lesson pair, shorter duration first. If *all* listed sort keys tie, relative order is still unspecified; add a unique key when consistent ordering matters.

## Keep only the first few sorted rows

`LIMIT` restricts how many result rows are returned. Put it **after** `ORDER BY`:

```sql
SELECT course_id, title, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 1;
```

The **top result** by duration is `(101, 'AI Foundations', 95)`. Here “top” refers to the chosen sorting rule. `ORDER BY duration_minutes ASC, course_id ASC LIMIT 1` instead returns `(102, 'Git Basics', 50)`, the shortest course. A **first result** likewise means the row at position 1 in *your specified order*: `ORDER BY course_id ASC LIMIT 1` returns course **101**. `LIMIT 1` alone does not define which row is first. Add a complete `ORDER BY` when the identity of that row matters.

To display the first two longest courses:

```sql
SELECT course_id, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 2;
```

The rows are `(101, 95)` and `(103, 80)`. `LIMIT` changes the number of returned rows; it does not delete the other courses. If fewer rows qualify than the limit allows, SQLite returns the rows that exist.

## Skip earlier rows with an offset

Use `OFFSET` with `LIMIT` to skip a number of rows from the sorted result:

```sql
SELECT course_id, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 2 OFFSET 2;
```

The full sorted IDs are **101, 103, 104, 102**. `OFFSET 2` skips IDs 101 and 103; `LIMIT 2` returns the next two, **104, 102**. An **offset** is a count of skipped rows, not a course ID and not a page number. `OFFSET 0` skips nothing. With `LIMIT 2 OFFSET 4`, all four rows are skipped and the result is empty.

| Offset | Rows skipped | Next two IDs |
|---:|---|---|
| 0 | None | 101, 103 |
| 1 | 101 | 103, 104 |
| 2 | 101, 103 | 104, 102 |
| 4 | All four | None |

Notice that `OFFSET 1` for a second two-row page is an error in the *page calculation*: it repeats 103 from page 1. The SQL is valid but the intended page is wrong.

## Build pages from one consistent ordering

**Pagination** divides a result into numbered pages. For page size 2, the first page starts at offset 0 and the second at offset 2. In general:

```text
offset = (page_number - 1) × page_size
```

The page number here starts at 1. With page size 2, page 3 starts at offset 4 and is empty in this four-row dataset. The query has the same `ORDER BY` and `LIMIT` for each page; only `OFFSET` changes:

```sql
SELECT course_id, title
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 2 OFFSET 0;  -- page 1
```

```sql
SELECT course_id, title
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 2 OFFSET 2;  -- page 2
```

Expected page 1 is **101, 103**; page 2 is **104, 102**. `course_id ASC` breaks a future tie in duration because each course ID is unique. Without a complete sort, pages can overlap or omit rows if equal sort values change relative order. Even with a complete sort, separate page requests can shift if rows are inserted, removed, or edited between requests. In this lab, the dataset stays unchanged while the two pages are read. For a changing large dataset, page numbering alone does not promise a fixed snapshot, and deep offsets can be expensive; these concerns matter when building an actual feed or catalogue service.

You can combine `WHERE` with sorting and paging: the filter chooses eligible rows; the sort orders those rows; the limit and offset select a slice of that ordered result. Write the clauses in that order in SQL: `WHERE ... ORDER BY ... LIMIT ... OFFSET ...`.

## Guided lab: predict, run, change, diagnose

Download the [sorting and limiting lab](QAI.02.01.15_Sorting_and_Limiting_Lab.zip), unzip it, and run from that folder:

```sh
python sorting_limiting.py
python check_sorting_limiting.py
```

Use `python3` if that is your installed command. Both programs use Python's standard-library `sqlite3` and create an in-memory catalogue. The first program prints:

```text
Title ascending: [101, 103, 102, 104]
Duration ascending: [102, 104, 103, 101]
Duration descending: [101, 103, 104, 102]
Instructor, then title: [101, 103, 102, 104]
First by course ID: [101]
Top by duration: [101]
Duration page 1: [101, 103]
Duration page 2: [104, 102]
Project page: [(104, 'Python Basics')]
Stored rows unchanged: True
```

**Controlled change:** in a copy of `sorting_limiting.py`, change `duration_page(db, 2, 2)` to `duration_page(db, 2, 1)`. Calculate `(2 - 1) × 1 = 1`, predict `[103]`, and run it. Restore the original call. Then change `title ASC` to `title DESC` inside the instructor ordering in `main()`; predict `[103, 101, 104, 102]` before running. The helper `duration_page()` binds the page size and offset using `?` placeholders; sort column names and `ASC`/`DESC` are fixed SQL text, not parameters that can be bound as values.

**Reproduce and repair a logical error:** get two-row page 2 with `LIMIT 2 OFFSET 1`. The query runs, but the output is `[103, 104]`, repeating course 103 from page 1. Compute the correct offset from page number and page size, repair it to `OFFSET 2`, and verify `[104, 102]`. The checker tests both offset choices, changed page sizes, an empty page, order directions, tied keys, the mini-project, and unchanged stored data. It checks supplied reference queries; compare your own edited query separately.

## Mini-project: second missing-note Basics course

An editor wants Basics courses that lack topic notes, sorted by title A to Z. Show the **second** matching course, with its ID and title. The filter leaves Git Basics and Python Basics. Title order puts Git first and Python second. With a page size of one row, the second page skips one row. Expected output is `(104, 'Python Basics')`.

Attempt your own query before reading the worked solution:

```sql
SELECT course_id, title
FROM course_catalogue
WHERE title LIKE '%Basics'
  AND topic_note IS NULL
ORDER BY title ASC, course_id ASC
LIMIT 1 OFFSET 1;
```

`course_id` is a final unique tie breaker. `project_page()` in the lab runs this rule with the pattern, limit, and offset bound to parameters. For an acceptance check, change just `OFFSET 1` to `OFFSET 0`: you should get `(102, 'Git Basics')`. If the second query still returns 104, inspect the filter and ordering before trusting the page number.

**Independent variation:** show page 2 of **all four courses** ordered by longest duration first, with **two courses per page**. Predict the skipped rows and write the query yourself. Then compare with this reference:

```sql
SELECT course_id, duration_minutes
FROM course_catalogue
ORDER BY duration_minutes DESC, course_id ASC
LIMIT 2 OFFSET 2;
```

The expected rows are `(104, 65)` and `(102, 50)`. In the lab, `duration_page(db, 2, 2)` returns their IDs `[104, 102]`. Record your query, expected rows, actual rows, why page 1 does not reappear, and the correction if the two pages overlap. For a further test, add another course with the *same* duration as an existing course and predict how `course_id ASC` places the tied rows before checking the pages again.

## Find the source of a wrong result

| Symptom | Inspect | Repair |
|---|---|---|
| Rows seem to arrive in unpredictable order | No `ORDER BY`, or equal keys with no tie breaker | Specify the actual ranking column and enough tie breakers |
| Shortest course appears when you wanted the longest | Used `ASC` rather than `DESC` | Reverse the duration direction; check rows 101 (95) and 102 (50) |
| Correct instructor groups, wrong order inside each group | Only the primary sort key was specified | Add a secondary sort key such as `title ASC` |
| Two pages share a row | Used `OFFSET 1` for a second page of size 2 | Recalculate `(page_number - 1) × page_size` |
| “Top” row changes after rewriting the order | The ranking rule itself changed | State what “top” means and sort on that measure before `LIMIT 1` |
| Filtered result is empty | Filter might remove all rows, or offset might skip all matches | Run the filter without `LIMIT` to count and inspect the sorted eligible rows |

## Check your understanding

1. Why should you not rely on the rows appearing in ID order when `ORDER BY` is absent?
2. What IDs does `ORDER BY duration_minutes DESC` produce in this table?
3. Why is `ORDER BY instructor_id ASC` insufficient for a predictable order among the two instructor-7 courses?
4. What is the difference between a primary sort key and a secondary sort key?
5. Which row is returned by `ORDER BY duration_minutes ASC LIMIT 1`? Is that the longest course?
6. With page size 2, what offset starts page 2, and what IDs appear there under descending duration?
7. What can change between two page requests even if the sorting rule is complete?

**Answers and reasoning**

1. Without an ordering clause, the database does not promise a particular result order. An observed ID sequence can be incidental.
2. **101, 103, 104, 102**, corresponding to durations 95, 80, 65, and 50.
3. Both rows have the same instructor ID, so the listed key cannot distinguish their order. Add a second key such as title and ideally a unique final key.
4. The primary key ranks or groups rows first; the secondary key decides the order when primary values tie.
5. Course **102** is first at 50 minutes. It is the shortest, not the longest; `DESC` would put the longest first.
6. Offset **2** skips page 1's IDs 101 and 103. Page 2 contains **104, 102**.
7. If rows are added, removed, or changed between requests, later pages can shift despite a consistent sort rule.

## Remember and retain

- `ORDER BY` defines result order; `ASC` runs low to high and `DESC` high to low for this numeric field.
- Add a secondary sort key for ties, plus a unique final key if the exact order matters.
- `LIMIT` takes the first N sorted rows; `OFFSET` skips earlier sorted rows. Neither changes the table.
- Page offset is `(page_number - 1) × page_size` for pages numbered from 1.
- Keep a record of your predicted order, changed direction, wrong offset and repair, project query, and independent page query so you can reconstruct the rule later.

## Further reading

- [SQLite: SELECT, ORDER BY, and LIMIT](https://www.sqlite.org/lang_select.html)
- [SQLite: row values and pagination tradeoffs](https://www.sqlite.org/rowvalue.html)
- [Python: sqlite3 placeholders](https://docs.python.org/3/library/sqlite3.html)
