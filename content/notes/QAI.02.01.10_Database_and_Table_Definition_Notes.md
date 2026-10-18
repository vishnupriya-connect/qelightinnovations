# Database and table definition

## Give each fact a place before entering data

The course catalogue from the previous lesson used three fields: `course_id`, `course_title`, and `instructor_id`. Where did that table and its fields come from? Someone defined the **database** to connect to and the **table schema**: the table name, its columns, their types, and their rules.

**Database creation** establishes a place to store tables. **Database selection** determines which database a connection or client uses for a statement. **Table creation** establishes a named row structure inside that database. **Table alteration** changes an existing table definition. **Table deletion** removes the table and its rows. **Database deletion** removes an entire database and its tables. These are different scopes of change.

The group of SQL commands that defines and changes database objects is often called **data definition language**, or **DDL**. Names such as `CREATE TABLE`, `ALTER TABLE`, and `DROP TABLE` describe actions on the schema. A successful change can affect applications that refer to the old names, so first predict which object and data the statement will affect.

This lesson uses a disposable SQLite database for the runnable exercises. MySQL and PostgreSQL examples explain common commands whose syntax SQLite does not use. Keep the product label next to a statement: sharing a SQL keyword does not make all dialects interchangeable.

## One task, two database workflows

Suppose you need a database for course records. In a **MySQL 8.4** client, this is a typical sequence:

```sql
CREATE DATABASE course_lab;
USE course_lab;
-- Later, only after deciding to remove the entire database:
DROP DATABASE course_lab;
```

`CREATE DATABASE` creates the named database. It does **not** automatically select it. `USE course_lab` selects it as the current database for that client session. `DROP DATABASE` removes the database and all its tables; it is far broader than dropping one table. These examples are for a MySQL client on an isolated, authorised practice server. **Do not run the final line against a database with wanted data.**

With **SQLite**, the common workflow is to open a database file and work through the resulting connection:

```python
import sqlite3

connection = sqlite3.connect("course_lab.db")
# Execute CREATE TABLE and other SQL through this connection.
connection.close()
```

Opening a filename with Python's `sqlite3.connect()` creates that database file if it does not exist. The filename selects the main database for that connection. SQLite does **not** accept MySQL's `CREATE DATABASE course_lab;`, `USE course_lab;`, or `DROP DATABASE course_lab;` statements. To remove this particular SQLite database in a local lab, close every connection, verify the exact disposable file, and remove that file with a file operation; do not confuse that with SQL `DROP TABLE`. File deletion is not a general substitute for server-based `DROP DATABASE`, and a real SQLite application may have related journal or WAL files and backup/recovery requirements.

| Intention | MySQL 8.4 | SQLite in this Python lab |
|---|---|---|
| Create database | `CREATE DATABASE course_lab;` | Open an absent database filename with `sqlite3.connect(path)` |
| Select database | `USE course_lab;` in a session | Open/use the connection to the chosen filename |
| Delete database | `DROP DATABASE course_lab;` | Close the lab connection; remove its verified disposable file |
| Create / alter / drop a table | SQL on the selected database | SQL executed on the open connection |

In PostgreSQL, `CREATE DATABASE` exists, but database selection is normally performed by **connecting** to the desired database; MySQL's `USE` is not the portable way to switch a PostgreSQL connection. These comparisons teach the concept of database scope without asking you to install three systems.

## Create a table and read its definition

With a connection to an empty SQLite database, run:

```sql
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_title TEXT NOT NULL,
    instructor_id INTEGER NOT NULL
);
```

`CREATE TABLE` gives a table a name. Inside the parentheses are **column definitions**. `INTEGER` and `TEXT` are types; `PRIMARY KEY` says which value identifies a course row; `NOT NULL` rejects a missing value in those columns. The preceding lessons introduced types and integrity rules. The statement defines a structure; it does not itself add three course rows.

To examine the definition in SQLite, use `PRAGMA table_info(courses);`, or let a Python client read its returned rows. For this table, the ordered column names are `course_id`, `course_title`, `instructor_id`. `PRAGMA` is a SQLite-specific inspection statement; other database systems use different inspection commands or system catalogues.

**Before running a definition statement, trace:** Which database connection? Which table name? Which columns? Does it create a new object, alter an old one, or delete anything? If the table already exists, a second plain `CREATE TABLE courses (...)` fails with an “already exists” error. `CREATE TABLE IF NOT EXISTS ...` suppresses that particular error but does **not** verify that the existing table has your expected schema. Inspect it before relying on it.

## Alter an existing table, one controlled change at a time

Start with three course rows from the previous lesson:

| course_id | course_title | instructor_id |
|---:|---|---:|
| 101 | AI Foundations | 7 |
| 102 | Git Basics | 8 |
| 103 | Data Basics | 9 |

An **`ALTER TABLE`** statement names the existing table and a requested schema change. The words after it specify *which kind* of change. The lab performs these four changes in order in SQLite:

```sql
ALTER TABLE courses
ADD COLUMN delivery_mode TEXT NOT NULL DEFAULT 'online';

ALTER TABLE courses
RENAME COLUMN course_title TO title;

ALTER TABLE courses
RENAME TO course_catalogue;

ALTER TABLE course_catalogue
DROP COLUMN delivery_mode;
```

1. **`ADD COLUMN`** appends `delivery_mode` to the schema. The `DEFAULT 'online'` supplies a value for the existing rows when they are read; it also gives future rows a default if they omit that column. Here the default is needed because the new column is `NOT NULL` and rows already exist. The database system's rules for adding constrained columns differ across products.
2. **`RENAME COLUMN`** changes the column's name to `title`. It does not rewrite the title text in the three rows. A query using `course_title` after this rename must be updated to use `title`.
3. **`RENAME TO`** changes the table name to `course_catalogue`. A query referring to `courses` now uses the wrong table name.
4. **`DROP COLUMN`** removes `delivery_mode` and its stored values. It does not remove the whole table. The other columns and three row facts remain in this simple example.

The column-name trace is:

| Stage | Columns, in order |
|---|---|
| Just created | `course_id`, `course_title`, `instructor_id` |
| After `ADD COLUMN` | `course_id`, `course_title`, `instructor_id`, `delivery_mode` |
| After both `RENAME` operations | `course_id`, `title`, `instructor_id`, `delivery_mode` |
| After `DROP COLUMN` | `course_id`, `title`, `instructor_id` |

The first record remains course 101, title “AI Foundations,” instructor 7. Column order is shown here so you can trace the lab, not as a reason to use unnamed values in future application code. Some columns cannot be dropped directly: for example, SQLite rejects dropping this table's primary-key `course_id`. Dependencies in indexes, views, triggers, keys, or other schema objects can also prevent a change or require a planned migration. Never treat `DROP COLUMN` as harmless simply because the table survives.

### `ALTER COLUMN` depends on the database product and version

**`ALTER COLUMN`** means a change to an *existing column's definition*, such as a type, default, or constraint. The exact operations and syntax differ. For example, PostgreSQL 18 can change a column's type with a form such as:

```sql
-- PostgreSQL 18 example; do not paste this into the SQLite lab.
ALTER TABLE courses
ALTER COLUMN course_title TYPE VARCHAR(200);
```

Type changes must be checked against existing values; a database may reject a conversion or need an explicit conversion rule. **SQLite 3.53.0 and later** supports `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` and `DROP NOT NULL`. Its direct `ALTER COLUMN` support here concerns that constraint; do **not** infer that SQLite supports the PostgreSQL `TYPE` form. Older SQLite versions reject even this `ALTER COLUMN` form. The lab prints your installed SQLite version's outcome: `NOT NULL enforced` on a supporting version, or `Unavailable in this SQLite version` otherwise. It does not ask you to install a newer version merely to finish the rest of the lab. More complex SQLite changes may require building a new table, copying validated data, and replacing the old structure under a planned migration.

**Prediction:** In a separate `drafts` table with a non-null title, adding a `NOT NULL` requirement on a supporting version makes a later insert of a null title fail. It does not alter the existing title string. Before requiring `NOT NULL` on real existing data, check for nulls; the operation may fail if they exist.

## Remove a table without confusing it with a database

In the lab, use a disposable table:

```sql
CREATE TABLE scratch (note TEXT);
DROP TABLE scratch;
```

**`DROP TABLE`** removes the entire named table and its rows. The query that checks for a table named `scratch` then finds none. The `course_catalogue` table remains, and the database file remains. `DROP TABLE IF EXISTS scratch;` avoids an error if the table is already absent; it does not protect against giving the *wrong existing table name*. For existing data that must survive, examine dependencies, keep a usable backup, and test the change on a copy first.

| Statement | Scope of removal |
|---|---|
| `DROP COLUMN delivery_mode` | That column and its values from an existing table |
| `DROP TABLE scratch` | The whole `scratch` table and all its rows |
| MySQL `DROP DATABASE course_lab` | The database and its tables |

**`RENAME` is different from `DROP`:** a rename preserves the object and changes how you refer to it; a drop removes an object. Either can break code that still uses the earlier name, so inspect and update dependent queries.

## Guided lab: build, change, inspect, and reconnect

Download the [database and table definition lab](QAI.02.01.10_Database_Table_Definition_Lab.zip). Unzip it and run both files from the unzipped folder:

```sh
python schema_lab.py
python check_schema_lab.py
```

Use `python3` if needed. The script needs SQLite 3.35.0 or newer for `DROP COLUMN`. Check the version with `python -c "import sqlite3; print(sqlite3.sqlite_version)"`. The lab creates a new file in a private temporary directory, closes its connections, and removes it when done. It does not touch a database you already have.

On SQLite 3.53.0 or later, the first program prints:

```text
Database file exists: True
Created columns: course_id, course_title, instructor_id
After ADD: course_id, course_title, instructor_id, delivery_mode
After RENAME: course_id, title, instructor_id, delivery_mode
After DROP COLUMN: course_id, title, instructor_id
Stored rows preserved: True
Scratch table exists after DROP TABLE: False
ALTER COLUMN: NOT NULL enforced
Definition persisted on reconnect: True
Temporary database removed: True
```

On SQLite 3.35.0–3.52.x, the `ALTER COLUMN` line instead reads `ALTER COLUMN: Unavailable in this SQLite version`; the other expected lines remain the same. Both versions teach the difference between the SQLite lab's current capability and the general SQL idea.

The script first compares the three course rows before and after the schema changes. It then closes and reopens the same temporary database file to show that the new definition persisted. Finally it leaves the temporary directory, so the lab file is gone. A Python `sqlite3` connection sends the `CREATE`/`ALTER`/`DROP` statements; calling `commit()` makes the chosen changes durable before reconnecting. A read-only query retrieves rows for checks but is not the main topic of this lesson.

### Controlled modification and expected result

Copy `schema_lab.py`. Change the added column from `delivery_mode` to `study_mode` in **both** the `ADD COLUMN` and later `DROP COLUMN` statements. Predict the two changed output lines. You should see `study_mode` at the end of the “After ADD” and “After RENAME” lists; the “After DROP COLUMN” list and row-preservation check remain the same. If you change only the first statement, `DROP COLUMN delivery_mode` fails because that name no longer exists. Repair the mismatch, rerun from a fresh temporary database, and record the initial error and corrected output.

### Independent variant: a small second table

In a fresh in-memory connection, create `course_tags` with `course_id INTEGER PRIMARY KEY` and `tag TEXT`. Insert `(101, 'foundation')`. Then add `source TEXT NOT NULL DEFAULT 'manual'` and rename `tag` to `tag_name`. Before checking the reference, predict the column names and the original row after both changes.

**Reference solution:**

```sql
CREATE TABLE course_tags (
    course_id INTEGER PRIMARY KEY,
    tag TEXT
);
INSERT INTO course_tags VALUES (101, 'foundation');
ALTER TABLE course_tags ADD COLUMN source TEXT NOT NULL DEFAULT 'manual';
ALTER TABLE course_tags RENAME COLUMN tag TO tag_name;
```

Expected columns: `course_id`, `tag_name`, `source`. Expected row: `(101, 'foundation', 'manual')`. The supplied `check_schema_lab.py` contains a working Python reference, but attempt the independent build first. The check program also verifies duplicate table creation fails, dropping the primary-key column fails without changing the schema, and `DROP TABLE IF EXISTS scratch` can be repeated for an absent disposable table.

## Diagnose before trying a different command

| Observation | Likely cause | Check and repair |
|---|---|---|
| `table courses already exists` | You created it twice in one database | Inspect the existing schema; use a fresh lab database if you meant a fresh exercise |
| `no such table: courses` after `RENAME TO` | Old name is still in a query | Use `course_catalogue` after the rename |
| `no such column: course_title` after `RENAME COLUMN` | Old column name is still in a query | Use `title` after the rename |
| `no such column: delivery_mode` while dropping | The column was never added or was renamed in your variation | Inspect the current schema and fix the statement's exact name |
| `DROP COLUMN` fails for `course_id` | It is this table's primary key | Keep the identifier; design a deliberate replacement migration if the key must change |
| Syntax error on `CREATE DATABASE` or `USE` in SQLite | Those are MySQL-style database commands | Open the SQLite file through the connection instead |
| Syntax error on `ALTER COLUMN` | SQLite version or requested change is unsupported | Inspect the version and supported forms; do not paste PostgreSQL type-change syntax into SQLite |

For any real schema change, compare the old and new column definitions and verify representative rows **before** and **after**. On a live system, also plan how queries, dependent objects, backups, and deployment will be handled. This lab's cleanup is safe because it acts only inside a newly made temporary directory; do not translate its deletion step into a command against a shared database.

## Check your understanding

1. Does MySQL `CREATE DATABASE course_lab` automatically select that database? What statement selects it?
2. In this SQLite lab, which action selects the database: `USE course_lab` or opening a connection to its file?
3. Does `CREATE TABLE courses (...)` add the three sample course rows?
4. After renaming `course_title` to `title`, what happens to “AI Foundations” in row 101?
5. What remains after `DROP COLUMN delivery_mode`? What remains after `DROP TABLE scratch`?
6. Does `DROP TABLE IF EXISTS` guarantee you named the correct table?
7. Can PostgreSQL's `ALTER COLUMN ... TYPE` statement be executed as written in the SQLite lab? What can SQLite 3.53.0+ change with its new `ALTER COLUMN` form?

**Answers with reasons**

1. No. `USE course_lab` selects it for the MySQL client session.
2. Opening/using the SQLite connection to that file. SQLite does not use MySQL's `USE` here.
3. No. It establishes the table schema; a separate data-insertion action supplies rows.
4. The value remains “AI Foundations”; only the column name changes.
5. Removing `delivery_mode` leaves the table with `course_id`, `title`, and `instructor_id` and its three rows. Dropping `scratch` leaves no `scratch` table; the catalogue and database remain.
6. No. It suppresses the missing-table error, not an error in your intention.
7. No. SQLite 3.53.0+ has `ALTER COLUMN` forms for setting or dropping a `NOT NULL` constraint; that is not PostgreSQL's type-change syntax.

## Remember and retain

- First identify the scope: database, table, or column. Then identify the action: create, select/connect, alter/rename, or drop.
- `CREATE TABLE` defines columns and rules; it does not populate sample rows.
- `ALTER TABLE` changes the definition; `ADD COLUMN`, `DROP COLUMN`, and `RENAME` affect different parts of it. `ALTER COLUMN` capabilities depend on the database and version.
- `DROP TABLE` removes a table; MySQL `DROP DATABASE` removes a database. `IF EXISTS` is not a substitute for verifying the intended target.
- SQLite file connections and MySQL's `CREATE DATABASE`/`USE`/`DROP DATABASE` express similar workflow intentions using different mechanisms.
- For your evidence, keep the before-and-after column lists, preserved row comparison, version-sensitive result, controlled failure and repair, and the independent `course_tags` result. Explain aloud why each operation changed—or did not change—the stored rows.

## Further reading

- [SQLite: CREATE TABLE](https://www.sqlite.org/lang_createtable.html)
- [SQLite: ALTER TABLE and supported forms](https://www.sqlite.org/lang_altertable.html)
- [SQLite: DROP TABLE](https://www.sqlite.org/lang_droptable.html)
- [MySQL 8.4: creating and selecting a database](https://dev.mysql.com/doc/refman/8.4/en/creating-database.html)
- [MySQL 8.4: DROP DATABASE](https://dev.mysql.com/doc/refman/8.4/en/drop-database.html)
- [PostgreSQL 18: ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html)
