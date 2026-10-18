# SQL safety

## Keep a value from becoming SQL instructions

A course search receives a title from a caller. That title is **untrusted input**: even if it comes from a familiar form or another application component, the database code must treat it as data. The intended question is “find the course whose title exactly equals this value.”

The small lab has four invented courses, including `O'Brien's SQL`. It deliberately shows an unsafe way of building the query against this disposable data:

```python
sql = "SELECT course_id FROM courses WHERE title = '" + text + "'"
rows = db.execute(sql).fetchall()
```

If `text` contains characters that end the quoted value and add another condition, the SQL parser can treat part of the input as query structure. This is **SQL injection**: input data changes the SQL instructions. The lab's harmless demonstration value is `x' OR 1=1 --`. In the unsafe query, it changes an exact-title lookup into a condition that returns **all four IDs**: 101, 102, 103, 104. The lab performs no destructive statement and uses only a temporary local database. The failure is that the application answered a much broader question than requested.

Compare the intended fixed query:

```python
rows = db.execute(
    'SELECT course_id FROM courses WHERE title = ? ORDER BY course_id',
    (text,)
).fetchall()
```

The `?` is a **placeholder** for a value. `text` is a **query parameter**, passed to the driver separately; the driver uses it as a **bound parameter**. This is a **parameterised query**. With the same demonstration input, the safe query looks for a literal title `x' OR 1=1 --` and returns `[]`, because no course has that title. For the real invented title `O'Brien's SQL`, it correctly returns `[(104,)]`. The apostrophe is part of the title, not a reason to reject the learner's data.

| Input | Unsafe concatenation | Bound-value query |
|---|---|---|
| `O'Brien's SQL` | Quote can break a hand-built literal or require special handling | Finds ID 104 as an exact value |
| `x' OR 1=1 --` | Changes the `WHERE` logic; four IDs in this lab | Searches for the literal title; no rows |

The boundary matters more than the particular punctuation: the SQL structure comes from trusted code, while the caller supplies values for its placeholders. Use the placeholder syntax of the chosen driver; `?` is the style used by Python's `sqlite3` here. Bind values in `SELECT`, `INSERT`, `UPDATE`, and `DELETE` rather than rebuilding strings from input. Parameter binding by itself does not decide whether a caller is *allowed* to see a row or perform a change; authorization is a separate decision.

## An escaped value is not the application pattern

An **escaped value** is a representation in which characters that have special meaning in a particular context are encoded so they can appear as data. For example, SQLite's `quote(?)` displays the title fragment `O'Brien` as the SQL-literal-looking string `'O''Brien'`: the embedded quote is doubled in that representation.

That display is useful for understanding why handwritten SQL is error-prone. Do **not** build application queries by manually replacing apostrophes and then concatenating the result. Escaping rules depend on the database and context, and a later refactor can miss a path. Use a driver's bound parameters for values. Escaping a value for HTML output is a different context from SQL binding; one does not replace the other.

A value placeholder cannot stand for a SQL identifier or SQL syntax. For example, `ORDER BY ?` does not select a column by the text of its name as intended. If the UI lets a user choose a sort key, map a small set of permitted choices to SQL written by the application:

```python
SORT_COLUMNS = {'id': 'course_id', 'title': 'title'}
if sort_key not in SORT_COLUMNS:
    raise ValueError('unsupported sort key')
column = SORT_COLUMNS[sort_key]
rows = db.execute(
    f'SELECT course_id, title FROM courses ORDER BY {column}'
).fetchall()
```

This interpolation uses only one of two **trusted constant identifiers** after an allowlist check. It never interpolates the original untrusted `sort_key` into SQL. A request such as `title; DROP TABLE courses` is rejected as an unsupported sort key. The lab verifies the table remains unchanged. Limit the allowed columns and direction to what the product needs.

## Grant only the access a component needs

**Least privilege** means a component gets only the permissions needed for its task. A course catalogue page needs **read permission**; a course editor needs a limited **write permission**. A reporting request should not use a database identity that can alter all tables simply because that identity was convenient during development.

In a client-server database, a **database user** identifies a login, and a **database role** groups or carries privileges. PostgreSQL, for example, can grant `SELECT` on the course table to a reader role and appropriate `UPDATE` rights to an editor role. A role with `SELECT` can read the allowed object; a role with `UPDATE` can change allowed rows or columns according to its privileges and any additional policies. Real authorization may require rules about *which* course a person may edit, not just whether the identity has broad table write access.

SQLite does not have the same built-in database-user and `GRANT` role system. The lab demonstrates two narrower controls:

1. A SQLite connection opens the file with `mode=ro`; an attempted `UPDATE` fails at the database connection.
2. An application function checks whether its supplied role is `editor` before attempting a change; a `reader` call is refused.

The application role check is **illustrative**, not a full authentication or authorization system. If an attacker can open the SQLite file directly with write access, that Python check is bypassed. A deployed application must protect the file, set appropriate operating-system permissions, and establish actor identity from a trusted session or service. With PostgreSQL or another server, grant a dedicated identity only the needed privileges and keep its credentials out of source code and logs.

Least privilege limits damage if a coding defect remains, but it does not repair an unsafe SQL query: a reader with overly broad `SELECT` rights could still expose information. Use both parameter binding and appropriate permissions. Likewise, a bound query can still reveal another learner's course data if the application forgets to check ownership or tenant scope.

## Record meaningful changes without exposing inputs

An **audit log** records an important action so that an authorized reviewer can reconstruct *who did what to which record and when or in what sequence*. In the lab, a successful editor operation changes course 104's duration from **65** to **70** and writes this audit row in the **same database transaction**:

```text
('trainer', 'UPDATE_DURATION', 104, 65, 70)
```

The database log uses an increasing event ID for order. A failed update of a nonexistent course rolls back and adds no committed change row. A denied reader action is captured separately as a small, sanitized application event, `{'event': 'write_denied', 'role': 'reader'}`. The lab's denial events live only in process memory; a real service would send structured security events to a protected, durable destination. Do not put raw input payloads, passwords, connection strings containing secrets, or sensitive records into an audit log merely to make debugging easy.

The actor name in the lab is fixed sample data. In a real application, derive actor identity from the authenticated context; do not let a caller choose a trusted audit actor by supplying a plain form field. An audit row written in the same transaction as a successful change can describe committed changes consistently. For failures and denied attempts, use an appropriate separate event path because rolling back a transaction would also roll back audit rows written inside it.

## Guided lab: compare, diagnose, repair

Download the [SQL safety lab](QAI.02.01.30_SQL_Safety_Lab.zip), unzip it, and run from its folder:

```sh
python sql_safety.py
python check_sql_safety.py
```

Use `python3` if needed. It creates and cleans up a temporary SQLite file with invented courses. The main program prints:

```text
Unsafe synthetic demonstration: [(101,), (102,), (103,), (104,)]
Bound same input: []
Apostrophe as bound data: [(104,)]
Allowed title sort: [(101, 'AI Foundations'), (103, 'Data Basics'), (102, 'Git Basics'), (104, "O'Brien's SQL")]
Unapproved sort rejected: True
Read-only connection blocked write: True
Reader role denied: True
Updated duration: [(104,)] (70,)
Committed audit: [('trainer', 'UPDATE_DURATION', 104, 65, 70)]
Sanitized denial events: [{'event': 'write_denied', 'role': 'reader'}]
```

**Trace first.** Read the unsafe SQL construction and predict why the demonstration value expands its result. Then read `safe_search()` and predict why the same string produces no match. Confirm that a legitimate apostrophe in a title still works. Compare the database's read-only connection with the separate application role check; describe what each can and cannot enforce.

**Controlled change.** Search for the ordinary title `Git Basics`, then for `O'Brien's SQL`, then for a title that does not exist. The bound query returns `[(102,)]`, `[(104,)]`, and `[]`. Keep the query text unchanged and change only the bound value. For the sort key, compare `id` and `title`: ID order is 101, 102, 103, 104; title order is 101, 103, 102, 104.

**Reproduce and repair a failure.** Pass `title; DROP TABLE courses` as a sort choice. If untrusted text were copied into the SQL syntax, it could alter the intended statement; the lab's allowlist raises `ValueError` before executing anything. Do not turn off the allowlist. Repair a deliberately direct interpolation in your own copy by selecting the mapped trusted column, as in `sorted_courses()`. The checker confirms four course rows remain. Another error path in the checker attempts a write through the SQLite read-only connection; the handler rolls back any open failed transaction before later reads so it does not keep an old snapshot.

## Mini-project: safe course search and edit

Build two application paths over the same catalogue:

- A reader searches by exact course title and sorts by one approved column; it cannot change a duration.
- An editor changes a course duration and records the old/new value with a verified actor identity in an audit record.

**Reference implementation:** the lab's `safe_search()`, `sorted_courses()`, `open_reader()`, and `update_duration()` form the runnable solution. The main safety-sensitive pieces are:

```python
rows = db.execute(
    'SELECT course_id FROM courses WHERE title = ? ORDER BY course_id',
    (title,)
).fetchall()

if sort_key not in {'id', 'title'}:
    raise ValueError('unsupported sort key')

# update_duration() checks role, begins a transaction, updates the row,
# inserts the audit row with bound values, then commits or rolls back.
```

Expected evidence: the demonstration payload produces no rows through `safe_search`, the apostrophe title matches ID 104, the reader write is refused, the editor's successful change appears as duration 70 and one committed audit entry, and a nonexistent-course update produces no audit entry. Save the query and result pairs, error outcomes, audit result, and explanation of the permission boundary.

**Independent variation:** add a fifth course with the title `Learner's Guide`, then search for it with a bound parameter and sort the expanded catalogue by `title`. Predict an exact one-row match and five rows in title order. Here is a reference addition for a fresh lab database:

```python
editor.execute(
    'INSERT INTO courses (course_id, title, duration) VALUES (?, ?, ?)',
    (105, "Learner's Guide", 55)
)
print(safe_search(reader, "Learner's Guide"))
print(sorted_courses(reader, 'title'))
```

With the lab's `open_editor()` auto-commit setup, the new row is visible to a fresh reader statement: `safe_search` returns `[(105,)]`. Title order becomes **101, 103, 102, 105, 104**. Run this variation on a fresh disposable database before the editor's duration change, or say which state you used. The extra apostrophe must not require manual string escaping. In a real application, put authorized inserts behind an explicit checked write function and audit them as well; the variation isolates binding and ordering.

## Diagnose and operate safely

| Symptom | What it may mean | Repair or operational check |
|---|---|---|
| Search for a strange title returns every course | Input was concatenated into SQL | Use a fixed query and bound value; test the same input again |
| A legitimate apostrophe causes a syntax error | Hand-built quoted SQL literal | Bind the title as data |
| `ORDER BY ?` does not choose a column | Placeholder is a value, not an identifier | Map approved choices to trusted identifiers |
| Reader can modify records | Connection or server role has too much access | Use a read-only connection or restrictive server grants; test a denied write |
| Reader is denied by the app but can write directly to file | App role check is bypassable | Protect file and process boundary; use server-side roles where supported |
| Read-only attempt fails, then later read is stale | An open failed transaction kept an older snapshot | Roll back active transaction; close cursors and re-read |
| Change has no audit row | Write and audit were not committed together or path skipped logging | Put successful change and change record in one transaction; verify both |
| Logs contain raw payloads or secrets | Diagnostics collect more than necessary | Redact and limit access; record action type, identity, target, outcome |

For an operated application, review every path where data reaches SQL, including filters, writes, sorting, and admin tools. Test a normal value, an apostrophe, a no-match value, an unapproved sort, a denied write, and a failed update. Monitor denied actions, unexpected broad result counts, SQL errors, and missing audit events without exposing raw private input. Recheck permissions as new features or tables are added. Treat an audit trail as evidence requiring access control, retention, and integrity, not merely as another output file.

## Check your understanding

1. What exactly changed in the unsafe title query when its input contained `OR 1=1` after a quote?
2. What are a placeholder and bound parameter in this lab? What does the same demonstration input return safely?
3. Why does `O'Brien's SQL` work with the bound query?
4. Why is manual escaping a weaker application pattern than driver binding?
5. Why must a selectable sort column come from an allowlist rather than a value placeholder?
6. What is the difference between a database user/role and the Python role check in this SQLite lab?
7. Which permission should a catalogue reader have? What permission does an editor need for a duration change?
8. Where is the successful duration change recorded, and how is a denied attempt represented?

**Answers and reasoning**

1. Input escaped the intended string value and changed the `WHERE` logic, returning all four rows in the local demo.
2. `?` reserves a value position; the separately supplied Python value is bound there. The same demonstration string safely returns `[]`.
3. Its apostrophe stays within the title value rather than ending an SQL literal assembled by the app.
4. Manual escaping is context- and dialect-sensitive and easy to miss in a later code path; binding keeps SQL structure separate from values.
5. A placeholder represents a value; syntax such as a column name must be chosen from trusted constants.
6. A database user/role is enforced by a server's privileges when supported; the lab's Python check runs only when callers use that function. SQLite has no equivalent built-in user/role grants.
7. Read permission to the needed data; the editor needs limited write permission plus any required read access and application authorization.
8. One audit row is committed with the change. A denied reader attempt is a sanitized in-process event in this lab.

## Remember and retain

- Treat external values as untrusted. Keep SQL text fixed and pass values separately to the driver.
- Use an allowlist for identifiers or sort syntax that cannot be bound as values. Escaping for display does not replace binding.
- Least privilege limits read and write ability; parameter binding does not itself authorize a user or record.
- Commit successful changes with their audit entry; record denials through a separate protected event path without secrets or raw payloads.
- Keep the unsafe/safe result comparison, apostrophe check, denied write, allowlist rejection, committed audit row, and independent title variation for review.

## Further reading

- [Python: SQLite placeholders and bound values](https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries)
- [OWASP: SQL injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [SQLite: bind parameters](https://www.sqlite.org/lang_expr.html#varparam)
- [PostgreSQL: GRANT privileges](https://www.postgresql.org/docs/current/sql-grant.html)
