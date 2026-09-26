# Data insertion

## Add a new row to a table

The earlier lessons read from a four-course catalogue. **Data insertion** adds a **new row** to a table. It changes the stored data, so check both the input and the result. Our example table has these columns:

| Column | Rule | Meaning |
|---|---|---|
| `course_id` | `INTEGER PRIMARY KEY` | Unique course ID |
| `title` | `TEXT NOT NULL` | Required title |
| `instructor_id` | `INTEGER NOT NULL` | Required instructor ID |
| `duration_minutes` | `INTEGER NOT NULL` | Required duration |
| `lesson_count` | `INTEGER NOT NULL` | Required lesson count |
| `topic_note` | Nullable text | May be missing |
| `practice_minutes` | Nullable integer | May be missing |
| `status` | `TEXT NOT NULL DEFAULT 'draft'` | Uses `draft` when omitted |

The starting rows are courses 101–104. Their status is `published`. `NOT NULL` means a column cannot contain a SQL `NULL`; a default supplies a value when a column is omitted from an insert. The examples use a private in-memory SQLite database so you can run them without modifying any real catalogue.

The basic statement begins with `INSERT INTO` followed by the target table:

```sql
INSERT INTO course_catalogue
    (course_id, title, instructor_id, duration_minutes, lesson_count)
VALUES
    (105, 'SQL Basics', 7, 70, 3);
```

`INSERT` names the operation; `INTO course_catalogue` identifies where the row goes. The **column list** names the fields supplied. The **value list** after `VALUES` has one value for each named column **in the same order**. This is a **single-row insert**. Course 105 is added with title SQL Basics, instructor 7, duration 70, and three lessons.

Query the new row to see what the table stored:

```sql
SELECT course_id, title, topic_note, practice_minutes, status
FROM course_catalogue
WHERE course_id = 105;
```

Expected: `(105, 'SQL Basics', NULL, NULL, 'draft')`. The two optional fields were omitted, so they are `NULL`. The omitted `status` column uses its declared default, `draft`. The four earlier rows remain present. An insert without a column list would need a value for **every** table column in table order in SQLite; naming columns is easier to review and allows optional or defaulted fields to be omitted.

When values originate in a program, bind them as data rather than constructing a SQL string from user input:

```python
db.execute(
    """INSERT INTO course_catalogue
       (course_id, title, instructor_id, duration_minutes, lesson_count)
       VALUES (?, ?, ?, ?, ?)""",
    (105, "SQL Basics", 7, 70, 3),
)
db.commit()
```

Each `?` stands for one value, and five supplied values match five named columns. The lab commits successful changes and uses a new in-memory database on each run. If your own application uses a file database, a successful insert can persist there; choose the intended database before executing a write.

## Add several rows in one statement

A **multi-row insert** can put several value lists after one `VALUES` keyword:

```sql
INSERT INTO course_catalogue
    (course_id, title, instructor_id, duration_minutes, lesson_count)
VALUES
    (106, 'Query Practice', 8, 45, 2),
    (107, 'Data Visuals', 9, 60, 3);
```

Both new rows use the same column list. Each parenthesised value list maps left to right to the five named columns. Courses 106 and 107 receive `NULL` for `topic_note` and `practice_minutes` and the default `draft` status. Check both IDs rather than assuming the insert did what you intended:

```sql
SELECT course_id, title, status
FROM course_catalogue
WHERE course_id IN (106, 107)
ORDER BY course_id;
```

Expected rows are `(106, 'Query Practice', 'draft')` and `(107, 'Data Visuals', 'draft')`. Python's `executemany()` can also bind several sets of values to the same SQL statement; that is a Python interface for repeated executions. The SQL statement shown here demonstrates multiple row value lists directly.

| Added ID | Title | Instructor | Duration | Lessons | Status |
|---:|---|---:|---:|---:|---|
| 105 | SQL Basics | 7 | 70 | 3 | draft |
| 106 | Query Practice | 8 | 45 | 2 | draft |
| 107 | Data Visuals | 9 | 60 | 3 | draft |

## Copy selected rows with `INSERT ... SELECT`

The source of inserted values can be a query instead of literal `VALUES`. The lab also has a `long_course_archive` table with columns `course_id`, `title`, and `duration_minutes`. To copy courses lasting at least 80 minutes:

```sql
INSERT INTO long_course_archive (course_id, title, duration_minutes)
SELECT course_id, title, duration_minutes
FROM course_catalogue
WHERE duration_minutes >= 80;
```

This is an **insert from query**. The `SELECT` produces three values per qualifying source row, in the same order as the three target columns. Courses 101 (95 minutes) and 103 (80 minutes) qualify. The archive then contains `(101, 'AI Foundations', 95)` and `(103, 'Data Basics', 80)`. The source catalogue still contains its seven rows. `INSERT ... SELECT` copies selected values into new rows in the destination; it does not move or remove the source rows.

**Controlled variation:** if you change the range to `duration_minutes >= 70` *on a fresh database before copying*, course 105 joins 101 and 103 in the archive. If you change the threshold to 96, no source row qualifies and the archive stays empty. The `SELECT` output must have the same number of fields as the target column list. Re-running the same copy into an archive that already has IDs 101 and 103 attempts to insert duplicate primary keys and is rejected; start from a fresh lab connection for each variation. Inspect the actual destination rows and source count after each run.

## Required values, omitted values, and defaults

Omitting a column has different results depending on the table's definition:

| Kind of column | Omitted in an insert | Example |
|---|---|---|
| Required `NOT NULL` without a default | Insert fails | Omitted `title` |
| Nullable without an explicit default | Gets SQL `NULL` | Omitted `topic_note` |
| Declared with a default | Gets that default | Omitted `status` becomes `draft` |

This query tries to add a row without its required title:

```sql
INSERT INTO course_catalogue
    (course_id, instructor_id, duration_minutes, lesson_count)
VALUES
    (109, 7, 60, 3);
```

SQLite rejects it with a `NOT NULL constraint failed` error. Course 109 is **not added**. The fix is to provide a genuine title in the column and value lists, then verify that the row exists. Explicitly supplying `NULL` for `status` is also different from *omitting* `status`: the declared default applies when the column is omitted, while an explicit `NULL` violates this `NOT NULL` column. A unique `course_id` matters too; reusing 105 would collide with an existing primary key.

For a table where every field can be generated or defaulted, SQLite also supports **default value insertion** with `DEFAULT VALUES`. The lab's `review_queue` table has an automatically assigned integer primary key, a `state` default of `pending`, and an `attempts` default of 0:

```sql
INSERT INTO review_queue DEFAULT VALUES;
```

On the fresh lab database this inserts `(1, 'pending', 0)`. It creates **one** row from defaults. It cannot make a valid row in our `course_catalogue`, because that table requires a real title, instructor ID, duration, and lesson count with no defaults for them. `DEFAULT VALUES` is a separate whole-row form, while omission from a regular column list lets selected fields receive defaults.

## Guided lab: predict, run, verify, repair

Download the [data insertion lab](QAI.02.01.19_Data_Insertion_Lab.zip), unzip it, and run both programs from its folder:

```sh
python data_insertion.py
python check_data_insertion.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module creates three in-memory tables. The first program prints:

```text
After three new courses: [(105, 'SQL Basics', None, None, 'draft'), (106, 'Query Practice', None, None, 'draft'), (107, 'Data Visuals', None, None, 'draft')]
Archive: [(101, 'AI Foundations', 95), (103, 'Data Basics', 80)]
Default queue row: [(1, 'pending', 0)]
Independent row: (108, 'Linux Basics', None, None, 'published')
Original four retained: True
```

`None` in the Python output represents SQL `NULL`. Before running, predict the number of rows in the catalogue after the first and second inserts (5, then 7), the archive IDs, and which fields get `NULL` or defaults. After running, use the printed rows and the checker to confirm. The checker also intentionally tries an insert with a missing required title and verifies that it was rejected without adding course 109.

**Reproduce and repair a failure:** in a fresh copy of the lab, try the missing-title SQL above in a `try`/`except sqlite3.IntegrityError` block (the checker shows this pattern). Verify that ID 109 is absent. Add `title` to the column list and a real title to the corresponding value position, run the repaired insert, and check that ID 109 now exists. Do not read an error message alone as proof of the table's final state; query it afterward. Make each variation on a fresh database or use an unused ID so earlier inserts do not affect the result.

## Mini-project: extend the catalogue and make an archive

Starting from the four original courses, add **SQL Basics** as course 105 (instructor 7, 70 minutes, 3 lessons) and add **Query Practice** and **Data Visuals** as courses 106 and 107 with the values in the table above. Let the optional fields be missing and the status default to `draft`. Then populate a separate three-column archive with all catalogue courses lasting at least 80 minutes. Finally, report the IDs and statuses of the three new catalogue rows and all archive rows.

**Expected evidence:** the new rows are `(105, 'draft')`, `(106, 'draft')`, and `(107, 'draft')`; the archive contains **101** and **103**. The source catalogue contains **7** rows after these inserts. Course 105 at 70 does not meet the archive boundary; course 103 at exactly 80 does.

**Reference solution:**

```sql
INSERT INTO course_catalogue
    (course_id, title, instructor_id, duration_minutes, lesson_count)
VALUES (105, 'SQL Basics', 7, 70, 3);

INSERT INTO course_catalogue
    (course_id, title, instructor_id, duration_minutes, lesson_count)
VALUES (106, 'Query Practice', 8, 45, 2),
       (107, 'Data Visuals', 9, 60, 3);

INSERT INTO long_course_archive (course_id, title, duration_minutes)
SELECT course_id, title, duration_minutes
FROM course_catalogue
WHERE duration_minutes >= 80;

SELECT course_id, status FROM course_catalogue
WHERE course_id BETWEEN 105 AND 107 ORDER BY course_id;

SELECT course_id, title, duration_minutes FROM long_course_archive
ORDER BY course_id;
```

The lab's `add_one()`, `add_two()`, and `copy_long_courses()` are the reference steps. Check both tables after the operations. If the archive includes 105, inspect the threshold. If a new status is `NULL` instead of `draft`, inspect the table declaration and whether you omitted the column or supplied an explicit value.

**Independent variation:** on the same fresh lab after the mini-project, insert course **108, Linux Basics**, instructor **9**, duration **55**, and **2** lessons. Set `status` explicitly to `published`, but omit both optional note and practice fields. Before opening the reference function, write the `INSERT` yourself and predict its row. The expected selected values are `(108, 'Linux Basics', NULL, NULL, 'published')` for ID, title, note, practice, and status. The explicit `published` value wins over the default `draft`; the archive still has only 101 and 103 because the earlier copy did not select course 108 and the new duration is below 80.

```sql
INSERT INTO course_catalogue
    (course_id, title, instructor_id, duration_minutes, lesson_count, status)
VALUES (108, 'Linux Basics', 9, 55, 2, 'published');
```

The lab's `independent_variation()` is a reference to inspect *after* your attempt. Keep your statement, predicted row, actual selected row, and a brief explanation of one field supplied explicitly and one field filled by omission. The checker validates the supplied reference function, not any query you wrote separately.

## Diagnose insertion faults

| Symptom | Likely cause | Repair |
|---|---|---|
| Values appear under the wrong columns | Column list and value order do not correspond | Map each value to its named column before executing |
| Wrong number of values error | A row has too many or too few values for the column list | Count names and values for every row in `VALUES`, or SELECT expressions in `INSERT ... SELECT` |
| `NOT NULL constraint failed` | Required field omitted or explicitly set to `NULL` | Supply a valid required value; verify no partial new row was added |
| Unique or primary-key constraint error | Attempted to reuse an ID, possibly by re-running a copy | Start with a fresh lab database or use a new ID; do not silently overwrite data |
| Optional field is `NULL` but status is `draft` | Different column definitions | Check which fields have a declared default and which simply allow missing values |
| Archive is empty or includes unexpected courses | Query's `WHERE` condition controls which source rows are copied | List qualifying source IDs first, then compare destination rows |

## Check your understanding

1. What do `INSERT INTO`, the column list, `VALUES`, and the value list each specify?
2. What happens to course 105's `topic_note`, `practice_minutes`, and `status` when those columns are omitted?
3. How many rows does the multi-row `VALUES` statement add? How would you verify?
4. Does `INSERT ... SELECT` remove rows from the source catalogue?
5. Why does the insert for course 109 without a title fail?
6. How is an omitted `status` different from an explicit SQL `NULL` for that column?
7. Why does `INSERT INTO review_queue DEFAULT VALUES` work but the same form cannot make a valid catalogue course?

**Answers and reasoning**

1. `INSERT INTO` names the destination; the column list fixes target fields and order; `VALUES` introduces literal data; a value list gives the corresponding values for one new row.
2. The two optional fields become SQL `NULL`; `status` becomes its declared default `draft`.
3. **Two** rows, IDs 106 and 107. Query the table for both IDs and check their selected fields.
4. No. It copies query results into the target and leaves the source rows present.
5. `title` is `NOT NULL` and has no default; omitting it cannot produce a valid row.
6. Omission activates the `draft` default. An explicit `NULL` violates `status`'s `NOT NULL` rule.
7. Every queue field can be generated or filled by defaults. Catalogue fields including title and instructor ID have no default and are required.

## Remember and retain

- `INSERT INTO table (columns...) VALUES (values...)` adds rows; keep the column and value positions aligned.
- One `VALUES` tuple adds one row; several tuples add multiple rows. `INSERT INTO ... SELECT ...` uses selected source values to create destination rows.
- Omitted nullable columns become `NULL` and omitted columns with declared defaults receive those defaults. Missing required values cause an error.
- `DEFAULT VALUES` makes one row only when all fields can be generated, defaulted, or nullable.
- Verify added IDs, actual stored fields, source retention, and rejected inserts. Retain your failed and corrected query, mini-project results, and independent variation.

## Further reading

- [SQLite: INSERT](https://www.sqlite.org/lang_insert.html)
- [SQLite: CREATE TABLE, defaults, and constraints](https://www.sqlite.org/lang_createtable.html)
- [Python: SQLite placeholders and transactions](https://docs.python.org/3/library/sqlite3.html)
