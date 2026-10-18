# SQL language basics

## From a data question to a result

Suppose a course catalogue contains the following rows in a table called `courses`:

| course_id | course_title | instructor_id |
|---:|---|---:|
| 101 | AI Foundations | 7 |
| 102 | Git Basics | 8 |
| 103 | Data Basics | 9 |

You want to see course IDs and titles. In ordinary language: “From the courses table, show each course ID and title.” In **SQL** (Structured Query Language), write:

```sql
SELECT course_id, course_title
FROM courses;
```

The **query result** is a two-column set of three rows:

| course_id | course_title |
|---:|---|
| 101 | AI Foundations |
| 102 | Git Basics |
| 103 | Data Basics |

SQL is a language for communicating with a relational database. It describes which data or operation you want; the database system parses the text, checks names and syntax, and carries out the request. The example asks for information and does not change the stored rows. Other SQL statements can create structures or change data; we will study those operations separately.

**A helpful mental model:** the stored table is the source; the SQL statement is the instruction; executing it produces either a result or an error. A result is not a copy of the database: selecting two columns does not remove the third stored column.

## Recognise the parts of one statement

```sql
-- Show the course labels without changing the table.
SELECT course_id, course_title AS label
FROM courses;
```

| Part | Meaning here | How to recognise it |
|---|---|---|
| `SELECT`, `FROM`, `AS` | **SQL keywords**: words with a defined job in this statement | The database interprets them as language instructions |
| `courses`, `course_id`, `course_title`, `label` | **SQL identifiers**: names of the table, columns, and a result-column alias | They identify an object or output name; `label` is only the output heading |
| `course_title` | **SQL expression**: the column value read for each source row | The database evaluates it for each selected row |
| `AS label` | Output alias: gives that result column a heading | Does not change the stored column name |
| `SELECT course_id, course_title AS label` | A **SQL clause** that specifies result columns | Begins with `SELECT` |
| `FROM courses` | A **SQL clause** that identifies the source table | Begins with `FROM` |
| `-- Show ...` | A **SQL comment** for a human reader | Begins with `--` and ends at the line break |
| `;` | **Statement terminator** | Marks the end of the SQL statement in scripts and interactive shells |

A **SQL statement** is a complete request, such as the whole `SELECT ... FROM ...;`. A **SQL query** asks for data. This complete `SELECT` is both a statement and a query; a query can also appear inside a larger statement. `FROM courses` by itself is only a clause, not a complete statement. SQL keywords are conventionally capitalised for readability; `SELECT` and `select` are both recognised by SQLite. Identifier spelling still matters: `course_title` is a different name from `course_name`.

The columns between `SELECT` and `FROM` form a select list. A column name on that list is one simple expression. `AS label` names the output column; it does not rename `course_title` in the stored table. Later lessons expand selection, filtering, joins, grouping, and aliases. Here, focus on reading the structure of a statement and predicting its result.

### Identifier versus literal

An **SQL literal** is a fixed value written in the statement. Compare:

```sql
SELECT course_title, 'course' AS item_type, 1 AS example_count
FROM courses;
```

`course_title` is an identifier: it reads each row's column value. `'course'` is a text literal: it gives the same text in every result row. `1` is a numeric literal. `item_type` and `example_count` are identifiers used as output headings. This query returns three columns and three rows; the first row is `AI Foundations | course | 1`.

| Written form | Category | Meaning |
|---|---|---|
| `course_title` | Identifier | Look up the named column in the source row |
| `'course_title'` | Text literal | Use the exact text `course_title` in every result row |
| `1` | Numeric literal | Use the number one |
| `'1'` | Text literal | Use the character `1` as text |

Use single quotes for **text values** in these examples. Do not put a column name in single quotes when you intend to read that column. Some SQL systems have ways to quote identifiers, but those differ by database; simple names such as `course_title` avoid that issue here. A literal is still part of SQL text: when a value comes from a user or program input, use a bound parameter instead of joining that input into the SQL string. The lab demonstrates this distinction.

### Expressions can compute a result

An **expression** produces a value. A column reference, a literal, or a calculation may be an expression:

```sql
SELECT course_id, course_id + 1000 AS display_id
FROM courses;
```

The first output row is `101 | 1101`; the last is `103 | 1103`. The calculation appears only in the result. The stored `course_id` values remain 101, 102, and 103.

## Comments and statement boundaries

Use `--` for a comment up to the end of that line, or `/* ... */` for a block comment:

```sql
/* Read two fields for a catalogue preview. */
SELECT course_id,  -- stable course identifier
       course_title
FROM courses;
```

Both comment forms are ignored when SQLite interprets the statement. A comment is for explanation and must not hide required code accidentally. This code is wrong for the intended query:

```sql
SELECT course_id -- , course_title FROM courses;
```

The rest of that line is a comment, so the statement has no `FROM courses`; in SQLite it then tries to use `course_id` without a table and reports an error. Put the next SQL part on a new line or move the comment to its own line. `#` is accepted for certain whole-line comments in the SQLite command-line program, but it is **not** the portable SQL comment form; use `--` or `/* ... */` in SQL files.

The semicolon ends a statement when a SQL script contains several statements. The SQLite interactive shell waits for it to know the command is complete. Python's `sqlite3.Connection.execute()` can execute one complete statement without a final semicolon, but including one in a saved SQL statement is clear and generally reusable. A semicolon inside a quoted text literal is data, not a statement boundary.

## What is in a query result?

For `SELECT course_id, course_title FROM courses;`, SQLite produces a **result set**: result columns named `course_id` and `course_title`, with one **result row** for each matching source row. A **result column** is a named position in that output. It can be a stored column (`course_id`), an expression (`course_id + 1000`), or a fixed literal (`'course'`). A query can produce an empty result set; that still has defined result columns but zero rows.

Do not rely on the displayed row order unless the statement specifies an order. The tables above show the sample rows in ID order to make the example readable; SQL does not promise that order without `ORDER BY`. Sorting is taught later. Also, seeing a result does not prove the source table has changed: this lesson's `SELECT` statements read without modifying it.

**Query execution** means sending the statement to a database connection, having the database parse and run it, then reading either the returned rows or an error. A client program can show the same result in a grid, tuples, or another display. The display format is not the database table itself.

## Guided lab: execute, predict, inspect

Download [SQL language basics lab](QAI.02.01.09_SQL_Language_Basics_Lab.zip), unzip it, and run from its folder:

```sh
python sql_language_basics.py
python check_sql_language_basics.py
```

Use `python3` if that is your working command. No server or extra Python package is required: Python's standard `sqlite3` module builds a temporary database in memory. The lab creates the sample `courses` table and inserts the three displayed rows as setup. The exercise here concerns *reading statements and results*; the table creation and inserts prepare a safe sample and are taught in detail in later lessons.

Expected first-program output:

```text
Columns: course_id, course_title
Rows: (101, 'AI Foundations'), (102, 'Git Basics'), (103, 'Data Basics')
Literal first row: ('AI Foundations', 'course', 1)
Expression first row: (101, 1101)
Before/after stored rows equal: True
```

The Python client asks SQLite to execute SQL and reads the result columns from `cursor.description` and rows from `cursor.fetchall()`. It adds `ORDER BY course_id` *only to keep the printed example reproducible*; a later lesson teaches sorting. The `Before/after` check verifies that the three reads did not change the sample table. The checker then confirms the expected outputs, a controlled change, and a recoverable error.

Read this fragment of the lab before running it:

```python
cursor = connection.execute(
    "SELECT course_id, course_title FROM courses ORDER BY course_id;"
)
column_names = [item[0] for item in cursor.description]
rows = cursor.fetchall()
```

`connection` is the database connection. `execute()` asks SQLite to run **one** SQL statement. `cursor` holds access to the result; `description` describes its output columns, and `fetchall()` obtains its rows. These are Python client operations, not SQL keywords. Running a query is different from *fetching* its result for display.

### Controlled change

Copy the lab file. In the select list, replace `course_title` with `instructor_id`; keep the table and ordering unchanged. Before running, write the expected column names and first and last rows. Your prediction should be:

```text
Columns: course_id, instructor_id
First row: (101, 7)
Last row: (103, 9)
```

Only change the **first query** in your copied demonstration, then run it. The other printed examples remain the same. Explain why changing a selected column changes the output shape but does not alter any stored row.

### Fix a deliberate error

In another copy, use `course_name` instead of `course_title` in the first query. SQLite reports `no such column: course_name`. Inspect the table's actual column names and repair the identifier to `course_title`. The lesson lab's checker includes a similar expected failure and verifies that correcting the name recovers the intended row. If the error is instead `no such table: courses`, inspect the `FROM` identifier and confirm that the setup ran on the **same connection**. Do not mask unexpected errors with `except: pass`.

## Apply the syntax to one useful task

A teaching page needs a stable catalogue preview containing a course identifier, a readable label, and the fixed text `course`. Build a query with exactly these three result columns, in this order:

| Output heading | Source of value |
|---|---|
| `course_id` | Column from the current row |
| `label` | The current row's `course_title` |
| `item_type` | Text literal `'course'` |

Start with the three-row in-memory `courses` table. The output should contain three rows; its first row is `(101, 'AI Foundations', 'course')`. Record the names and rows, and check that the table still has three original rows afterwards. This is a small catalogue-preview feature: a consumer can use `course_id` to identify a course and show `label` to a learner. It is limited to one table and read-only output.

**Reference query:**

```sql
SELECT course_id, course_title AS label, 'course' AS item_type
FROM courses
ORDER BY course_id;
```

**Reference Python (inside the lab, after `connection = make_connection()`):**

```python
before = connection.execute(
    "SELECT course_id, course_title, instructor_id "
    "FROM courses ORDER BY course_id;"
).fetchall()

cursor = connection.execute(
    "SELECT course_id, course_title AS label, 'course' AS item_type "
    "FROM courses ORDER BY course_id;"
)
names = [column[0] for column in cursor.description]
rows = cursor.fetchall()

after = connection.execute(
    "SELECT course_id, course_title, instructor_id "
    "FROM courses ORDER BY course_id;"
).fetchall()

assert names == ["course_id", "label", "item_type"]
assert rows == [
    (101, "AI Foundations", "course"),
    (102, "Git Basics", "course"),
    (103, "Data Basics", "course"),
]
assert before == after
print(names)
print(rows)
```

The `ORDER BY` clause makes the test's row sequence predictable; it does not form part of this lesson's core vocabulary. If your result heading is `course_title` instead of `label`, check `AS label`. If each row contains the text `course_title` instead of the actual title, remove the single quotes around the **column identifier**. If the query fails, run the simplest working `SELECT course_id FROM courses;`, then add one expression at a time.

For an independent variation after the guided task, produce `course_id`, a computed `display_id` equal to `course_id + 1000`, and `item_type`. Predict all rows before running. The expected IDs are 1101, 1102, and 1103; the item type remains `course`. Verify that the stored IDs remain 101, 102, and 103. The lab checker provides a reference for comparing your result once you have attempted it.

## Avoid three common misunderstandings

| Symptom | Likely cause | Diagnosis and repair |
|---|---|---|
| Every output row says `course_title` | Wrote `'course_title'`, a literal | Use `course_title` without single quotes to read the column |
| `no such column: course_name` | Identifier differs from the real schema | Read the table definition and use the actual `course_title` name |
| Results appear in an unexpected order | The statement does not request any order | Ask for order explicitly when order matters; do not infer it from sample output |

A fourth mistake is building SQL by inserting unchecked text into a query. In Python, `connection.execute("SELECT ? AS supplied;", (value,))` safely binds a **value** as data; `?` is a parameter marker, not an identifier. For example, supplying `"AI'; DROP TABLE courses; --"` through `?` returns that entire string as one value and leaves the table alone. Parameter markers cannot stand for a table or column name. Do not concatenate user input into SQL to choose a value. Data modification and secure query construction receive deeper treatment later.

## Check your understanding

1. In `SELECT course_title, 'course_title' FROM courses;`, what differs between the two output columns?
2. Which is a whole statement: `FROM courses` or `SELECT course_id FROM courses;`?
3. For `SELECT course_id + 1000 AS display_id FROM courses;`, what is the first output value? Does it change the stored ID?
4. Why should a test not assume three result rows arrive in ID order without requesting that order?
5. What would be the result column names for `SELECT course_title AS label, 1 AS unit FROM courses;`?
6. How does a Python program get the actual rows after calling `execute()` for a `SELECT`?

**Answers and reasoning**

1. The unquoted identifier reads each row's title; the quoted text literal repeats the text `course_title` in every row.
2. `SELECT course_id FROM courses;` is a complete statement; `FROM courses` is only a clause.
3. `1101`; a computed output is read-only here, so stored `course_id` remains 101.
4. SQL does not promise result row order without a sorting request; a current display order may change.
5. `label` and `unit`; `AS` names the output headings.
6. Use the returned cursor's fetching method, for example `cursor.fetchall()`. `cursor.description` supplies output-column metadata.

## Remember and retain

- SQL gives a database a structured instruction. A query asks for data; a `SELECT` query is one kind of SQL statement.
- Keywords supply the language structure, identifiers name things, and literals supply fixed values.
- Expressions produce values; clauses are parts of a complete statement; comments explain it to human readers.
- A semicolon marks a statement boundary in a script or interactive shell.
- A result set contains result columns and zero or more result rows; a displayed result does not change the stored table.
- Predict result headings, row values, and whether storage changes before running a statement. Check those predictions against actual output and investigate mismatches.

Keep your executed query, predicted and actual result, one corrected error, and the independent `display_id` variation together as a small reproducible record. You can proceed when you can identify every part of an unfamiliar basic statement, run and modify it, explain its output, and correct a wrong identifier without copying the reference query.

## Further reading

- [SQLite: SQL language syntax](https://www.sqlite.org/lang.html)
- [SQLite: SELECT statements](https://www.sqlite.org/lang_select.html)
- [SQLite: SQL comments](https://www.sqlite.org/lang_comment.html)
- [SQLite: command-line shell and statement terminators](https://www.sqlite.org/cli.html)
