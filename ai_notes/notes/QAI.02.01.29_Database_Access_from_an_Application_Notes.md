# Database access from an application

## From an application request to a database row

An application does not need a person to type every SQL query. It opens a database connection, sends a statement, receives rows, and closes or returns the connection when finished. This lesson uses a small course catalogue so each step can be observed:

| course_id | title | duration_minutes |
|---:|---|---:|
| 101 | AI Foundations | 95 |
| 102 | Git Basics | 50 |
| 103 | Data Basics | 80 |
| 104 | Python Basics | 65 |

The example application needs two reads: find course **103**, and list courses lasting at least **70** minutes. It also inserts course **105**, SQL Basics, lasting 70 minutes. The result of each request must be checked before the application shows it to a user.

A **database driver** is software that speaks to a particular database engine through an application's language. A **database connector** is often the module or interface used to make that connection. In Python, the built-in `sqlite3` module plays this role for SQLite. Client-server databases use their own drivers and protocols; Python's `sqlite3` does not become a PostgreSQL driver by changing a filename.

## Identify the destination and access information

A **connection string** or connection settings tell a driver how to find the intended database. The required fields depend on the engine.

| Field | Meaning for a client-server database | This SQLite lab |
|---|---|---|
| **Host** | Server name or network address | None: SQLite opens a file directly |
| **Port** | Network service endpoint on that host | None: no database server port |
| **Database name** | Named database on the server | A temporary `courses.sqlite` file path instead |
| **Username** | Database identity presented to the server | None in this SQLite connection |
| **Password** | Secret used for an authentication method, when needed | None in this SQLite connection |

For example, a PostgreSQL connection configuration may contain `host=db.example.invalid`, `port=5432`, `dbname=learning`, and `user=app_reader`, with a password obtained from an approved secret source. This illustrates the fields; it is not a live endpoint or a runnable part of the SQLite lab. Do not put a real password into shared notes, source code, query logs, or a screenshot. A client-server setup may also need TLS settings, network permissions, and a bounded connection timeout.

SQLite accepts a filename or path through `sqlite3.connect(...)`. A special `:memory:` database is private to a connection in the ordinary use shown here; two independent connections would not see the same in-memory tables. The lab therefore uses a temporary **file** so two connections in the pool can read the same catalogue. A wrong file path can create or select the wrong database; the application should check its configured path and expected schema, not silently treat an empty database as valid.

## Open a connection, execute, and fetch

The lab's connector function opens a **connection object**:

```python
import sqlite3

db = sqlite3.connect(str(path), timeout=1, isolation_level=None)
db.execute('PRAGMA foreign_keys=ON')
```

The connection represents access to that database file and owns transaction state. The `timeout` is a short wait for a locked database. `isolation_level=None` lets this example control write transactions explicitly with SQL `BEGIN`, `COMMIT`, and `ROLLBACK`; another application or Python version might configure transaction control differently.

A **cursor** executes a query and walks its result. Here is a one-course request:

```python
cursor = db.cursor()
try:
    cursor.execute(
        'SELECT course_id, title FROM courses WHERE course_id = ?',
        (103,)
    )
    row = cursor.fetchone()
finally:
    cursor.close()
```

`execute()` sends one SQL statement. The question mark is a value placeholder and `(103,)` is the one-item tuple supplied to the driver. This keeps the value separate from the SQL text. The later SQL safety lesson examines untrusted input and injection in depth. Here the key point is that the app can change the requested ID without building a new SQL string by concatenation.

`fetchone()` returns the next row, here `(103, 'Data Basics')`, or `None` when there is no row. Requesting course 999 returns `None`; the application must handle that absent result rather than assuming `row[1]` exists. A cursor can execute a query without fetching all its rows, and a `SELECT` does not automatically print its result.

For a list, the lab uses **fetch all rows**:

```python
cursor = db.cursor()
try:
    cursor.execute('''
        SELECT course_id, title
        FROM courses
        WHERE duration_minutes >= ?
        ORDER BY course_id
    ''', (70,))
    rows = cursor.fetchall()
finally:
    cursor.close()
```

The initial list is `[(101, 'AI Foundations'), (103, 'Data Basics')]`. The boundary matters: a 70-minute course qualifies. `fetchall()` reads the remaining rows from that cursor; if `fetchone()` already consumed its first row, `fetchall()` on the *same result* would return only those still remaining. For a large result, loading all rows into memory may be unsuitable; use paging or streaming with an appropriate driver and stable ordering. `ORDER BY course_id` makes this small result predictable.

## Write and close deliberately

The lab inserts SQL Basics as course 105 inside an explicit transaction:

```python
db.execute('BEGIN IMMEDIATE')
db.execute(
    'INSERT INTO courses VALUES (?, ?, ?)',
    (105, 'SQL Basics', 70)
)
db.execute('COMMIT')
```

The actual `add_course()` function catches a failure and rolls back any still-active transaction. A second insert with the same ID fails the primary-key rule, then leaves the successful course 105 intact. The list at 70 minutes becomes `[(101, 'AI Foundations'), (103, 'Data Basics'), (105, 'SQL Basics')]`. Closing and reopening the database file still finds course 105 because its insert committed.

**Close connection** means releasing its database resources when the request or program is finished. The lab uses a small context manager that closes in a `finally` block and rolls back an unfinished transaction before closing:

```python
from contextlib import contextmanager

@contextmanager
def open_database(path):
    db = sqlite3.connect(str(path), isolation_level=None)
    try:
        yield db
    finally:
        if db.in_transaction:
            db.rollback()
        db.close()
```

The lab's actual helper also sets the lock timeout and enables foreign keys. A plain Python `with db:` controls transaction behavior but does **not** itself close the SQLite connection; use an explicit close or a helper that owns it. A closed connection cannot execute another query. Do not count on closing as a way to commit pending work; commit intentionally, and roll back failed work.

## Reusing connections through a bounded pool

Creating a new database connection for every small request can have a cost, especially with a remote server. A **connection pool** holds a bounded number of open connections. A request borrows one, performs its work, and returns it. When all are borrowed, another request waits up to a configured limit or receives an exhaustion error. A pool does not mean one connection can be used by unrelated requests at the same time.

The lab includes a **single-threaded teaching pool of size two**:

1. Borrow first and second connections.
2. A third simultaneous checkout reports pool exhaustion.
3. The second borrower starts a transaction and leaves an insert of temporary course 106 unfinished.
4. Returning it rolls back that unfinished transaction, so course 106 is absent.
5. After borrowers return, one existing connection is reused, and the pool closes its two underlying connections.

Its output is `(True, True, True, [(101, 'AI Foundations'), (103, 'Data Basics')], True)` for exhausted, cleaned, reused, the selected rows, and closed. The demonstration deliberately has no threads, wait queue, reconnect logic, health checks, or cross-process coordination. Use a vetted driver or framework pool for a service, and size it with the database's connection limit and application concurrency in mind. SQLite's file access and locking model differs from a remote server; many small SQLite applications do not need a pool at all.

A pooled connection has **state**: an open transaction, temporary objects, connection settings, and perhaps session-level settings in a server database. Return it only after finishing or rolling back a transaction, closing cursors, and applying the pool's reset policy. The lab verifies rollback on return, but it is not a production pool. A pool exhaustion signal points to too many simultaneous borrowers, long-held connections, or a leak; blindly raising the pool size can overload the database.

## Guided lab: predict, run, change, repair

Download the [database access from an application lab](QAI.02.01.29_Database_Access_from_an_Application_Lab.zip), unzip it, and run from its folder:

```sh
python application_database.py
python check_application_database.py
```

Use `python3` if needed. The scripts create and delete a temporary SQLite file, without a server, network, password, or third-party package. The example program prints:

```text
One course: (103, 'Data Basics')
Unknown course: None
At least 70 minutes: [(101, 'AI Foundations'), (103, 'Data Basics')]
After insert: [(101, 'AI Foundations'), (103, 'Data Basics'), (105, 'SQL Basics')]
After reopen: (105, 'SQL Basics')
Pool demo (exhausted, cleaned, reused, rows, closed): (True, True, True, [(101, 'AI Foundations'), (103, 'Data Basics')], True)
```

**Trace.** Predict the one-row and multi-row results before running. Find the `connect()` call, the cursor's `execute()`, both fetch methods, the close path, and the separate pooled checkout path. Explain why the unknown course returns `None` and why the pool can reuse a connection only after it has been returned.

**Controlled change.** Change the call `courses_at_least(db, 70)` in a copy of the program to `courses_at_least(db, 80)` before the insert. The list should be **101 and 103**. After inserting 105 at 70, the 80-minute list is still **101 and 103**. Restore 70 before running the checker, which verifies the supplied path.

**Reproduce and repair a failure.** In a copy, request course 999 and then try to use `course_by_id(db, 999)[1]` without checking the return value. Python raises a `TypeError` because the function returned `None`. Repair the application boundary with `row = course_by_id(db, 999)` and an explicit `if row is None` branch. Do not change the query to invent a fake row. The checker verifies the `None` result, a duplicate-key rollback, and that closed connections reject queries.

## Mini-project: course lookup and filtered catalogue

Build a small application access layer that accepts a course ID and a minimum duration. It must find one course or report “not found,” list qualifying courses in ID order, insert one new course, and show it on a new connection. Each request should release its cursor and connection. Keep SQL values bound separately from the SQL text.

**Reference implementation:** the lab's `connect()`, `open_database()`, `course_by_id()`, `courses_at_least()`, and `add_course()` form a runnable solution. The essential application flow is:

```python
initialize(path)
with open_database(path) as db:
    one = course_by_id(db, 103)
    if one is None:
        print('Not found')
    else:
        print(one)
    print(courses_at_least(db, 70))
    add_course(db, 105, 'SQL Basics', 70)
with open_database(path) as db:
    print(course_by_id(db, 105))
```

Expected outputs are `(103, 'Data Basics')`, the initial list of **101 and 103**, and `(105, 'SQL Basics')` after reopening. An unknown ID returns `None`. The checker covers both read and write paths and the error path. Keep the queries, predicted results, actual results, failure record, and resource cleanup explanation.

**Independent variation:** after inserting course 105, list courses lasting at least **60** minutes. Predict IDs **101, 103, 104, 105** (95, 80, 65, 70 minutes); 102 at 50 is excluded. The reference call is:

```python
with open_database(path) as db:
    print(courses_at_least(db, 60))
```

The expected result is `[(101, 'AI Foundations'), (103, 'Data Basics'), (104, 'Python Basics'), (105, 'SQL Basics')]`. Run it after your own prediction on a fresh program database with 105 inserted. Explain why `fetchall()` returns four rows and why their order is stable. If you see only three, check whether your new connection points to the same file and whether course 105 was committed.

## Operate database access reliably

| Risk or symptom | Likely cause | Check or response |
|---|---|---|
| `no such table: courses` | Wrong/empty SQLite file or initialization skipped | Verify path, schema, and initialization; avoid silently creating the wrong file |
| One course lookup crashes on missing ID | `fetchone()` returned `None` | Handle not-found explicitly |
| Results disappear after closing | Write was not committed or a different file was opened | Check transaction outcome and configured path |
| Too many rows in memory | Unbounded `fetchall()` | Page or stream a large result with a stable order |
| Pool is exhausted | Borrowers hold connections too long, leak them, or capacity is too small | Measure checkout wait and usage; shorten request scope; size responsibly |
| Reused connection has unexpected state | Borrower returned an unfinished transaction or altered settings | Reset and verify on return; use a supported production pool |
| Database is locked or unavailable | Write contention, server/network issue, or bad timeout settings | Bound waits and retries; observe error type and transaction state |
| A log reveals credentials | Secret placed in a URL or exception dump | Redact logs, use approved secret storage and driver configuration |

For a service, monitor connection count, checkout wait, pool exhaustion, query latency, timeout/error rate, and transaction rollbacks. Define a limit for open connections and requests waiting on them. Set appropriate connection and query timeouts; a connection that succeeds but runs an unbounded query can still exhaust workers. On a remote database, configure encrypted transport and least-privilege identities according to the deployment. Keep any secret or real personal data out of shared lab files and diagnostic output.

## Check your understanding

1. What role does Python's `sqlite3` module play in this example?
2. Which of host, port, database name, username, and password does a file-based SQLite connection use here?
3. What is a connection object, and what does a cursor do?
4. What do `fetchone()` for ID 999 and `fetchall()` for a 70-minute threshold return initially?
5. Why does the app use `(103,)` with a `?` rather than concatenating an ID into SQL?
6. Does `with db:` alone guarantee the SQLite connection is closed?
7. What happens if a third request checks out a size-two pool while both connections are borrowed?
8. Why must a pool clean transaction state before another borrower reuses a connection?

**Answers and reasoning**

1. It is the database driver/connector interface for SQLite.
2. It uses a local file path; there is no database server host, port, username, or password in this lab.
3. The connection represents an open database session; a cursor executes SQL and fetches its result rows.
4. `None` for ID 999; `[(101, 'AI Foundations'), (103, 'Data Basics')]` for at least 70 minutes.
5. The driver binds a value separately; the SQL structure remains fixed even when the ID changes.
6. No. Use `close()` or a context manager that explicitly closes in a `finally` block.
7. This teaching pool reports exhaustion; a production pool may wait up to a configured timeout.
8. A returned unfinished transaction could affect a later request's data or locks; roll it back and reset the connection.

## Remember and retain

- Configure the **right driver and destination**, then open a connection, execute through a cursor, fetch the expected shape, and close resources.
- `fetchone()` can return `None`; `fetchall()` can consume a large result. Handle both intentionally.
- A local SQLite path is not a client-server host, port, or login. Do not expose real credentials in code or logs.
- A bounded pool lends and reuses connections. A borrowed connection must return clean; a pool is not automatically needed for SQLite.
- Keep your connection settings without secrets, predicted and actual rows, missing-ID handling, failed insert rollback, pool trace, and independent threshold result for review.

## Further reading

- [Python: sqlite3 connection and cursor](https://docs.python.org/3/library/sqlite3.html)
- [Python DB-API specification](https://peps.python.org/pep-0249/)
- [PostgreSQL: connection parameters](https://www.postgresql.org/docs/current/libpq-connect.html)
- [SQLAlchemy: connection pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
