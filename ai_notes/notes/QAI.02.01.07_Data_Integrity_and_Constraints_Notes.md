# QAI.02.01.07 — Data integrity and constraints

> QAI.02.01.06 relationships and cardinality → **QAI.02.01.07 data integrity and constraints** → QAI.02.01.08 data redundancy and normalisation

## 1. Destination: make invalid course data fail at the database boundary

Previously, a learner could be linked to a course. Now ask: what stops the same learner ID from identifying two people, an enrolment from pointing to nobody, or a course from having a negative capacity? By the end, you can express these rules in a schema, insert valid data, observe invalid data being rejected, and explain limits of those rules.

Use the [runnable data integrity lab](QAI.02.01.07_Data_Integrity_Lab.zip). **S90 contract:** `C | L3 | H1–H3 | E2–E5 | A1–A4 | P0–P1`. Start with the predictions, run the programs, then change the schema and tests yourself.

## 2. From a business rule to an enforced constraint

**Data integrity** means the stored data obeys declared correctness rules. A **constraint** is a database rule that accepts or rejects a write. We will use a course catalogue with `learners`, `courses`, and `enrolments`. A **valid value** satisfies its applicable rules; an **invalid value** violates at least one. “Valid” here is relative to *these* rules: a syntactically allowed email need not be deliverable.

| Question about one row | Integrity rule | Database mechanism | Example |
|---|---|---|---|
| Which row is this? | **Entity integrity:** identifiable rows, with no duplicate primary key | **Primary-key constraint** | learner ID 1 appears once |
| Does its link point somewhere real? | **Referential integrity:** references match existing rows | **Foreign-key constraint** | enrolment for learner 1 and course 101 |
| Is the value allowed in this field? | **Domain integrity:** accepted value set/range and required presence | **Not-null** and **check constraints**; appropriate types | capacity is 1 through 100 |
| Must a reusable code be distinct? | Uniqueness for an alternate identifier | **Unique constraint** | `AI-FOUND` occurs once |

A **primary key** identifies a row within one table; the pair `(learner_id, course_id)` identifies one enrolment. A **foreign key** connects its row to a row in another table. A **UNIQUE** rule forbids repeated values for the constrained column(s); when an email or code is mandatory, combine `UNIQUE` with the **not-null constraint**, `NOT NULL`. A **CHECK** rule evaluates a condition on the row. A **DEFAULT value** supplies a value if the insert leaves that column out. Defaults make insertion convenient; they are not a substitute for validation.

### Predict before running

| Proposed write | Prediction | Reason |
|---|---|---|
| New learner ID 3, unique email, name “Meera” | Accepted | Key, email, name are valid |
| New learner ID 1 | Rejected | Duplicate primary key |
| New enrolment (999, 101) | Rejected | Learner 999 does not exist |
| Course 103 with capacity 0 | Rejected | Below allowed range |
| Course 103 with `published` omitted | Accepted; `published = 0` | Default applies |
| Course 103 with explicit `published = NULL` | Rejected | `NOT NULL` applies; default does not override an explicit NULL |

## 3. Inspect the actual SQL, line by line

```sql
CREATE TABLE learners (
    learner_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL CHECK (length(trim(full_name)) > 0)
);
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity BETWEEN 1 AND 100),
    published INTEGER NOT NULL DEFAULT 0 CHECK (published IN (0, 1))
);
CREATE TABLE enrolments (
    learner_id INTEGER NOT NULL REFERENCES learners(learner_id),
    course_id INTEGER NOT NULL REFERENCES courses(course_id),
    PRIMARY KEY (learner_id, course_id)
);
```

`INTEGER PRIMARY KEY` identifies each learner or course. `email TEXT NOT NULL UNIQUE` says a missing email or a repeated email is invalid; it does **not** validate an email's actual format or ownership. `trim(full_name)` removes edge spaces before `length(...) > 0`, rejecting a name made only of spaces. A blank string is not the same as SQL `NULL`, so both the `NOT NULL` and `CHECK` rules matter. `BETWEEN 1 AND 100` includes 1 and 100. `published` is represented by 0 or 1; the default is 0, while a supplied 2 is invalid. Each enrolment must contain both IDs and a pair may occur once.

The lab seeds Anu (1) and Ravi (2), AI Foundations (101) and Git Basics (102), with three valid enrolments. Git Basics omits `published` on insert, so the database stores 0; AI Foundations explicitly stores 1. This gives you a visible test of `DEFAULT`.

**SQLite-specific setup:** each newly opened connection executes `PRAGMA foreign_keys = ON` and verifies that its value is 1. Declaring a foreign key alone does not ensure that SQLite will enforce it on your connection. The Python lab uses `?` parameters for values, and a fixed table name when summarising counts.

## 4. Run and compare observations with your predictions

Unzip the lab. In its directory run:

```sh
python integrity.py
python check_integrity.py
```

Use `python3` if that is your command. The initial summary is:

```text
Foreign-key enforcement: on
Learners: 2
Courses: 2
Enrolments: 3
Course 101 published: 1
Course 102 published: 0
```

`check_integrity.py` performs each failed insert in a **fresh** seeded in-memory database, catches only `sqlite3.IntegrityError`, checks the intended failure class, and checks that the row count did not change. A rejection is evidence of the specific rule being enforced; a script that merely prints an error without asserting the expected one gives much weaker evidence.

| Invalid write | Expected failure class | Underlying rule |
|---|---|---|
| Learner ID 1 again | `UNIQUE constraint failed` | Primary key / entity integrity |
| Another course with code `AI-FOUND` | `UNIQUE constraint failed` | Unique course code |
| Missing learner name | `NOT NULL constraint failed` | Required value |
| Spaces-only learner name | `CHECK constraint failed` | Nonblank rule |
| Course capacity 0 or 101 | `CHECK constraint failed` | Allowed range |
| Published value 2 | `CHECK constraint failed` | Allowed set |
| Enrolment for learner 999 | `FOREIGN KEY constraint failed` | Referential integrity |
| Existing enrolment (1, 101) again | `UNIQUE constraint failed` | Composite primary key |
| Explicit `published = NULL` | `NOT NULL constraint failed` | Required value despite default |

The first, second, and repeated enrolment cases are forms of **duplicate-key error**. SQLite can report the primary-key conflict as a `UNIQUE constraint failed` error, so read *which key* was duplicated, not only the error word. The unknown learner produces a **foreign-key error**. If you see an unexpected accepted row, check the data, the relevant declaration, and foreign-key activation on that same connection.

## 5. Guided implementation: insert a valid draft course

Run `python integrity.py --add-course`. In `integrity.py` the option executes:

```python
with db:
    db.execute(
        "INSERT INTO courses (course_id, course_code, title, capacity) "
        "VALUES (?, ?, ?, ?)",
        (103, "DATA-INTRO", "Data Introduction", 20),
    )
```

Expected result: **Courses: 3** and **Course 103 published: 0**. `published` is absent from the column list, so the default applies; there is no enrolment yet for course 103, and that is allowed. Edit the code in a copy to pass capacity `0` instead of `20`: the insert now raises an `IntegrityError` and the program stops at that write. Restore `20`. The `with db:` block rolls back the failed transaction; the checker uses a fresh database for each case so one error cannot alter the next test.

## 6. H3 independent change: tighten capacity without breaking valid rows

**Requirement:** future courses may have a capacity from **1 to 50**, inclusive. In a copy of `integrity.py`, change the schema's capacity check accordingly; retain `NOT NULL`. In `check_integrity.py` add a proof that 50 is valid and 51 is invalid. Predict both results before running.

**Worked solution:** the supplied code already accepts a `max_capacity` argument so you can exercise the modified rule without corrupting your original baseline. The implementation uses `CHECK (capacity BETWEEN 1 AND 50)` when called with `max_capacity=50`:

```python
accepted(
    "capacity 50 under stricter rule",
    "INSERT INTO courses (course_id, course_code, title, capacity) "
    "VALUES (?, ?, ?, ?)",
    (103, "DATA-INTRO", "Data Introduction", 50),
    max_capacity=50,
)
rejected(
    "capacity 51 under stricter rule",
    "INSERT INTO courses (course_id, course_code, title, capacity) "
    "VALUES (?, ?, ?, ?)",
    (103, "DATA-INTRO", "Data Introduction", 51),
    "courses", "CHECK constraint failed",
    max_capacity=50,
)
```

You can also set the default capacity bound in `open_connection` to 50 and adjust the original 101 invalid case to 51; run the checker again. The sample helper embeds a validated integer bound in a fixed schema template; application data in inserts uses SQL parameters. Never build user-controlled SQL identifiers or arbitrary SQL text by string concatenation.

Expected final checker line: `PASS: 10 invalid cases rejected; 1 valid case accepted; stricter limit verified`. The printed tightened-limit rejection is an additional invalid case beyond the ten baseline invalid cases. A successful change requires a passing boundary case *and* a failing immediately out-of-range case. If capacity 51 succeeds, inspect whether you opened a database with `max_capacity=50` and created its table using the new rule; altering a Python variable alone does not retroactively change an already created table.

**One more independent case:** add a test that course 103 with code `DATA-INTRO` and `published = 1` succeeds; use `accepted(...)` with the five-column insert from the published-invalid test and values `(103, "DATA-INTRO", "Data Introduction", 20, 1)`. It proves that an explicitly supplied valid value is stored separately from the default. The test passes in a fresh database.

## 7. What these constraints do not establish

- A `CHECK` condition that evaluates to SQL `NULL` is accepted by SQLite. Pair a required `CHECK` column with `NOT NULL`. For example, `capacity INTEGER CHECK (capacity > 0)` alone permits `NULL`.
- SQLite's ordinary column type declaration is not, by itself, a complete strict validation policy for every input type. For tighter typing evaluate SQLite `STRICT` tables and test input conversion; this lab focuses on rule kinds and accepted range.
- `UNIQUE` without `NOT NULL` can allow multiple `NULL` values in SQLite. The lab explicitly combines both for required email and course code.
- `capacity BETWEEN 1 AND 100` validates a number on a course row. It does **not** ensure `COUNT(enrolments for that course) <= capacity`. Capacity admission is a cross-row decision; implement an appropriate transaction and concurrency controls when that application feature is built.
- A course may still have zero enrolments; a foreign key validates existing links, not a minimum child count for every parent. Deletes and updates require a documented reference policy.
- Correct SQL constraints are a backstop, not a replacement for user feedback, authorisation, privacy review, server-side validation, monitoring, and controlled schema changes. Test actual write paths, including direct scripts and batch imports.

## 8. Solved checks

| Check | Answer |
|---|---|
| Why can Anu enrol in course 102 when learner 1 already appears in enrolments? | The key is the **pair**; (1, 102) differs from (1, 101). |
| What rejects a second learner with ID 1? | The learners table's primary-key constraint, protecting entity integrity. |
| What rejects (999, 101)? | The enrolments table's foreign-key constraint, when enabled on that connection. |
| Can a new valid course omit `published`? | Yes; it stores the default 0. |
| Does specifying `published = NULL` use the default? | No; the explicit NULL violates `NOT NULL`. |
| Can two blank-but-different email strings pass these rules? | A single empty string is allowed once because no nonblank email rule exists; two identical empty strings fail `UNIQUE`. Real email validation is another requirement. |
| Will the current schema stop course 101 at 30 enrolments? | No; it validates `capacity` itself, not a count over another table. |
| Why inspect error message *and* row count? | They show which constraint rejected the write and that the attempted row was not stored. |

## Remember

- **Identity → reference → domain:** distinguish which correctness rule each failed write breaks.
- `PRIMARY KEY` identifies a row; `UNIQUE` additionally protects a candidate code; `NOT NULL` requires a value; `CHECK` limits allowed values; `FOREIGN KEY` protects links.
- `DEFAULT` supplies a value for an omitted column; it does not replace an explicitly supplied NULL.
- In SQLite, enable foreign keys per connection and combine a required column's `CHECK` with `NOT NULL`.
- Test accepted and rejected boundary cases, check persistent row state, and state what the schema cannot guarantee.

## Primary references

- [SQLite: CREATE TABLE, constraint types and CHECK semantics](https://www.sqlite.org/lang_createtable.html)
- [SQLite: foreign-key support and enabling enforcement](https://www.sqlite.org/foreignkeys.html)
- [SQLite: INSERT statement and omitted columns](https://www.sqlite.org/lang_insert.html)
- [SQLite: STRICT tables](https://www.sqlite.org/stricttables.html)
