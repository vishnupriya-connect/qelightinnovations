# QAI.02.01.05 — Keys and row identity

> QAI.02.01.04 entities and attributes → **QAI.02.01.05 keys and row identity** → QAI.02.01.06 relationships and cardinality

## 1. Destination: identify one row and reject broken links

In our course catalogue, two learners can have the same name, a learner can join several courses, and a course can have several learners. We need a dependable way to refer to **one** learner, **one** course, or **one** enrolment. We also need the database to reject a link to a learner who does not exist.

Use the accompanying [mini-project](QAI.02.01.05_Keys_and_Row_Identity_Lab.zip): run a valid three-table catalogue, provoke controlled errors, add a valid record, and explain what the database enforced. **S90 target:** `C | L3 | H1–H3 | E2–E5 | A1–A4 | P0–P1`. This is an implementation node; reading the definitions alone does not finish it.

## 2. An identifier, a key, and a constraint are different

An **identifier** is a value used to refer to a specific item: `learner_id = 1`. A **key** is one or more fields used to identify or link rows under stated rules. A **key constraint** makes the DBMS reject rows that violate those rules.

| Question | Example | Answer |
|---|---|---|
| What points to Anu's row? | `learner_id = 1` | An identifier value |
| Which field did we choose to identify learners? | `learner_id` | Primary key column |
| What makes a duplicate ID fail? | `PRIMARY KEY` in the table definition | Enforced primary-key constraint |

A field named `learner_id` is **not** automatically unique: naming alone is documentation, not enforcement. A row's display position is not a stable identifier; results can come back in a different order.

## 3. Candidate, primary, alternate, unique

A **candidate key** is a *minimal* set of attributes that can uniquely identify each row under the real business rules. “Minimal” means removing any part would lose the required uniqueness. Choosing it requires more than seeing unique values in a tiny sample.

For the practice `courses` table, both `course_id` and `course_code` are treated as candidate keys **under the exercise rule** that every course has a non-null, unique code. We select `course_id` as the **primary key**: the designated identity for each course row. A **primary-key value** is a concrete instance, such as `course_id = 101`. The **primary-key constraint** rejects a second course with the same ID.

`course_code` is then an **alternate key**: a candidate key not chosen as primary. The declaration `UNIQUE`, together with `NOT NULL`, enforces the lab's rule that codes cannot repeat or be missing. A **unique key** is a field or combination protected against duplicate non-null values by a uniqueness rule. Be precise: a nullable `UNIQUE` column can accept multiple `NULL` values in SQLite; **UNIQUE by itself is not proof of a candidate key for every row**.

**Worked trace:** Courses `(101, 'AI-FOUND', 'AI Foundations')` and `(102, 'GIT-BASICS', 'Git Basics')` have two different IDs and codes. Adding `(103, 'AI-FOUND', 'Another course')` violates the course-code uniqueness rule even though ID 103 is new.

## 4. Surrogate, natural, and composite keys

A **surrogate key** is an artificial ID assigned for identification; `course_id = 101` has no lesson meaning. A **natural key** uses a domain value that already has meaning; `course_code = 'AI-FOUND'` is a possible natural candidate in this exercise. Natural keys can change when business names, registration rules, or formats change, so choose them only after checking long-term identity rules. Email may look unique today but can change or be recycled; this lab keeps `email` unique as a contact rule while using `learner_id` for row identity.

A **composite key** uses *more than one field together*. In `enrolments` the pair `(learner_id, course_id)` is the primary key:

| learner_id | course_id | Allowed? |
|---:|---:|---|
| 1 | 101 | Yes: Anu joins AI Foundations |
| 1 | 102 | Yes: the same learner joins a different course |
| 2 | 101 | Yes: another learner joins the first course |
| 1 | 101 again | No: that **pair** already represents an enrolment |

Neither `learner_id` nor `course_id` alone identifies an enrolment: both repeat legitimately. The *pair* identifies one row under the business rule “one active enrolment per learner–course pair.” If the business later permits repeated historical attempts, that identity rule must change; the chosen key is not universal law.

## 5. Foreign keys: links must point somewhere valid

A **foreign key** is a field or group of fields in one table whose values are required to match an allowed key in another table. In this lab `enrolments.learner_id` points to `learners.learner_id`:

- `enrolments` = **referencing table**, holding the foreign-key field.
- `learners` = **referenced table**, holding the **referenced key** `learner_id`.
- `(999, 101)` = invalid enrolment when there is no learner 999; with enforcement active, inserting it is a **key violation**.

The other foreign key, `enrolments.course_id`, refers to `courses.course_id`. A foreign key can repeat across enrolment rows; it does **not** by itself enforce “only one learner per course.” The composite primary key handles a different rule: the pair cannot repeat. The next node discusses relationship shapes in depth.

**SQLite-specific operation:** immediately after opening a SQLite connection, run `PRAGMA foreign_keys = ON` and confirm it reports `1`, **before beginning a transaction**. Foreign-key enforcement is a per-connection setting and may be disabled by default. Declaring `REFERENCES` without enabling enforcement is not enough for this SQLite lab. The demo explicitly enables it on each new connection. Other DBMSs have different setup and enforcement semantics; do not carry this switch over as universal SQL syntax.

## 6. Build and read the valid sample

After unzipping, run `python db_keys.py` (or `python3` if that is your command). The project uses only Python's standard-library `sqlite3` and no external database.

Expected:

```text
Foreign-key enforcement: on
Learners: 2
Courses: 2
Enrolments: 3
Course 101 learners: Anu, Ravi
```

Look at `db_keys.py`:

1. `open_database()` opens an in-memory database, enables foreign keys, and checks the setting.
2. `create_tables()` declares two entity tables and the enrolment table with its pair primary key and foreign-key references.
3. `seed()` inserts valid learners and courses **before** inserting enrolments that refer to them.
4. `summary()` counts and displays the result.

This is one running program plus a reusable module; it does not produce a persistent database file. The README explains how to run the separate checks.

### Predict the three valid enrolments

`(1,101)`, `(2,101)`, and `(1,102)` are all valid. Course 101 has Anu and Ravi. Reversing the pair to `(101,1)` would not mean the same thing: the first component is a learner ID, the second is a course ID, so it attempts to reference nonexistent IDs.

## 7. Trigger, understand, and repair failures

Run `python check_keys.py`. The script uses a **fresh database per case**, so one error cannot contaminate the next demonstration. It checks:

| Attempt | Expected cause and result | Repair |
|---|---|---|
| Reuse learner ID `1` | Primary key rejected | Assign a new ID only if it is genuinely another learner |
| Reuse course code `AI-FOUND` with new ID | Unique alternate code rejected | Use an approved new code; do not silently rename an existing course |
| Insert enrolment `(1,101)` again | Composite primary key rejected | Keep the existing relationship or change the data model if history is intended |
| Link learner `999` to course `101` | Foreign key rejected | Create the legitimate learner first, or correct the ID |
| Insert learner with missing email | Non-null rule rejected | Provide the required value or change a justified business rule |

An SQLite `IntegrityError` identifies an enforced rule failure. It does not automatically tell you what the human *meant* to do. Inspect the attempted values and the table rule; do not “solve” errors by turning off constraints. A raw exception string can vary by SQLite/Python version; the checker prints stable exercise labels while verifying the failure class.

### Two controlled modifications

**Guided H2:** run `python db_keys.py --add-learner`. This inserts learner `3` and a *valid* enrolment `(3,102)`. Expected learners = 3, courses = 2, enrolments = 4, and course 101 still contains Anu and Ravi. Compare these outputs with the baseline; identify the extra two records.

**Independent H3, with complete solution:** add a third course and enrol Anu in it. Below is one valid change to `seed()`, after the existing course and enrolment inserts:

```python
connection.execute(
    "INSERT INTO courses (course_id, course_code, title) VALUES (?, ?, ?)",
    (103, "DATA-INTRO", "Data Introduction"),
)
connection.execute(
    "INSERT INTO enrolments (learner_id, course_id) VALUES (?, ?)",
    (1, 103),
)
```

Run `python db_keys.py` again: courses = 3, enrolments = 4, learner count = 2, course 101 learners unchanged. Put the two lines **after** the existing seed so references already exist. To keep the supplied `check_keys.py` baseline checks passing, do the independent variation in a copy of the project, then restore `seed()` before running the original checker; the checker intentionally tests the original baseline and violation cases. A more advanced follow-up is to update the checker to accept the new intended counts.

## 8. Decisions for a real course system

- Choose IDs that remain meaningful as references when a title or email changes.
- Write down whether a learner may re-enrol in a course after cancellation; the pair key encodes one policy.
- Decide the right response to deleting a course with enrolments: reject, preserve historical rows, or carefully plan a cascading action. The lab uses the default restrictive behaviour rather than automatically deleting enrolments.
- Validate and normalise business fields, such as email or course code, before relying on uniqueness. In this exercise case-sensitive SQLite comparisons do not enforce every human notion of “the same email.”
- Ensure foreign-key checking is enabled **on every SQLite connection**, including test and application connections.
- Use parameter placeholders (`?`) for input values rather than building SQL by joining untrusted text. SQL safety and transactions receive dedicated later coverage.

## 9. Solved assessment

| Question | Answer and explanation |
|---|---|
| Does `UNIQUE(email)` automatically make email the selected primary key? | No. The table can have a different primary key; email is a separate uniqueness rule and may change in practice. |
| Why does enrolment `(1,102)` succeed when `(1,101)` exists? | Only the *pair* must be unique. The learner may join another course. |
| Why does enrolment `(999,101)` fail? | The referencing `learner_id` has no matching referenced learner key, with SQLite enforcement enabled. |
| What should you check if an invalid enrolment unexpectedly succeeds in SQLite? | Whether `PRAGMA foreign_keys` is enabled **on the same connection** before the insert, and whether the foreign-key constraint was declared correctly. |
| Is course code necessarily a natural candidate forever? | No. It is one in this exercise only under the stated non-null uniqueness and identity assumptions; a business code may change. |
| Are a foreign key and the pair primary key interchangeable? | No. Foreign keys demand valid references; the pair primary key prevents repeated learner–course pairs. |

## Remember

- A value used as an identifier becomes reliable when a suitable declared rule makes its use valid.
- Candidate key = minimal unique row identifier under business rules; primary = chosen candidate; alternate = another candidate.
- Surrogate = assigned ID; natural = domain value; composite = several fields together.
- Unique, primary, and foreign-key constraints enforce **different** conditions.
- Referencing table holds the foreign key; referenced table holds the matching key.
- In SQLite, verify foreign-key enforcement for each connection.

## Primary references

- [SQLite: CREATE TABLE, primary and unique constraints](https://sqlite.org/lang_createtable.html)
- [SQLite: foreign-key support and per-connection enablement](https://sqlite.org/foreignkeys.html)
- [PostgreSQL: primary, unique, and foreign-key constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
