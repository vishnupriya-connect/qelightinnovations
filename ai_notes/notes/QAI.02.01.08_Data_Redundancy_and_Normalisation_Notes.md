# Data redundancy and normalisation

## One course catalogue, two ways to store it

We need to store **learners**, **courses**, **instructors**, and the date each learner joined a course. A learner may join several courses; a course may have several learners. Imagine starting with this spreadsheet-like table:

| learner_id | learner_name | course_id | course_title | instructor_id | instructor_name | joined_on |
|---:|---|---:|---|---:|---|---|
| 1 | Anu | 101 | AI Foundations | 7 | Nisha | 2026-09-01 |
| 2 | Ravi | 101 | AI Foundations | 7 | Nisha | 2026-09-02 |
| 1 | Anu | 102 | Git Basics | 8 | Kiran | 2026-09-03 |

Here, one row represents **one enrolment**. Its key is the pair `(learner_id, course_id)`: learner 1 can appear in multiple rows and course 101 can appear in multiple rows, but the same pair may appear only once.

Notice the **duplicate data**: course 101's title and instructor are written in every enrolment for course 101. **Data redundancy** is storing the same fact in several places when those copies must agree. Repeating learner 1 in *different enrolments* is a necessary representation of different relationships; repeating learner 1's *name* in every enrolment creates a consistency risk.

**Destination:** give each fact one natural home, keep the links, and still answer “which learner joined which course, taught by whom, and when?”

## See what goes wrong before fixing it

A **data anomaly** is a problem that appears when adding, changing, or removing data because facts are stored in unsuitable places.

| Action in the single enrolment table | Anomaly | Concrete result |
|---|---|---|
| Create course 103 before anyone joins | **Insertion anomaly** | No enrolment row exists; an enrolment row needs a learner ID and join date |
| Rename course 101 but change only Anu's row | **Update anomaly** | One row says “AI Basics,” another still says “AI Foundations” |
| Remove the last enrolment in course 102 | **Deletion anomaly** | The only stored course 102 title and instructor disappear with that enrolment |

These are different problems. Deleting *an enrolment* is correct; losing *course details* as an unintended side effect is the anomaly. A primary key alone does not prevent any of these.

Run the accompanying [normalisation lab](QAI.02.01.08_Normalisation_Lab.zip):

```sh
python normalisation.py
python check_normalisation.py
```

Use `python3` if needed. The first program demonstrates the inconsistent course title and loss of the final course 102 row in separate fresh databases:

```text
After changing one enrolment row, course 101 titles: AI Basics, AI Foundations
After removing the last enrolment, remaining course 102 rows: 0
Learners: 2
Instructors: 2
Courses: 2
Enrolments: 3
Reconstructed enrolment rows match the original: 3
```

## Which fact belongs to which identifier?

A **functional dependency** says that one set of columns determines another: for any two valid rows, if the columns on the left are equal, the columns on the right must also be equal. Write “determines” as `→`. It is a rule about the meaning of the data over time, not merely a coincidence in three sample rows.

Our stated course rules imply:

- `learner_id → learner_name`: a learner ID has one current stored name.
- `course_id → course_title, instructor_id`: a course ID has one current title and assigned instructor.
- `instructor_id → instructor_name`: an instructor ID has one current stored name.
- `(learner_id, course_id) → joined_on`: a particular learner–course enrolment has one join date.

The last dependency needs **both** IDs: learner 1 joined two courses on different dates; course 101 has two learners with different join dates. A dependency from `course_id` to `course_title` needs only *part* of the two-column enrolment key. That is a **partial dependency** of a non-key column on part of a candidate key.

Follow another path: `course_id → instructor_id → instructor_name`. If the course table stores both instructor ID and instructor name, the name depends on the course through a separate instructor fact. That is a **transitive dependency** in this example. The course's *assignment* to an instructor is a course fact; the instructor's *name* is an instructor fact.

**Important rule of interpretation:** this design assumes a course has one current instructor. If the business needs several instructors per course, the dependency and table design change. If instructor names may change over time, a historical enrolment snapshot is a different, explicitly modelled requirement.

## The first three normal forms, applied in order

**Normalisation** means examining which facts depend on which identifiers and organising the tables to reduce unwanted redundancy and anomalies. A **normal form** is a condition the table structure meets.

### First normal form: one value in each field; no repeating groups

Suppose one row contains `course_ids = "101,102"` for Anu, or has columns `course_1`, `course_2`. The courses are hidden as a group inside one learner row. Separate them into one learner–course association per row. Each field then holds one value according to the table's chosen domain, and rows can be identified.

Our displayed enrolment table **already has this row shape**: it has one learner, one course, and one join date per row. It therefore illustrates a first-normal-form design for this simple set of fields, even though it still repeats names and titles. First normal form does **not** guarantee low redundancy.

| Before | After |
|---|---|
| Anu → `course_ids = "101,102"` | (Anu, 101) and (Anu, 102) as distinct associations |

“Atomic” is relative to the data operation: a course title is one field here; we do not split it into individual words. Store separate components when the application needs to address them independently.

### Second normal form: no non-key fact depends on only part of a composite key

The enrolment key is `(learner_id, course_id)`. In the displayed table:

- `learner_name` depends on just `learner_id`.
- `course_title` and `instructor_id` depend on just `course_id`.
- `joined_on` depends on the whole pair.

Move learner-specific fields into `learners`, course-specific fields into `courses`, and keep enrolment-specific fields in `enrolments`. This removes those partial dependencies from the enrolment table. To isolate the steps, the intermediate course table could still store `instructor_name`; that would leave the next problem.

| Table after removing partial dependencies | Key | Fields |
|---|---|---|
| `learners` | `learner_id` | `learner_name` |
| `courses` (intermediate design) | `course_id` | `course_title`, `instructor_id`, `instructor_name` |
| `enrolments` | (`learner_id`, `course_id`) | `joined_on` |

Second normal form builds on first normal form. For this example, the reason it matters is the **composite** enrolment key. If a table has only a one-column candidate key, that key has no proper nonempty part on which such a non-key column can depend.

### Third normal form: move the separate instructor fact to its own table

In the intermediate `courses` table, `course_id → instructor_id → instructor_name`. The instructor's name belongs with `instructor_id`. Keep `instructor_id` on `courses` as a reference to the instructor, then put the name in `instructors`:

| Final table | Primary key | Fields kept there |
|---|---|---|
| `learners` | `learner_id` | `learner_name` |
| `instructors` | `instructor_id` | `instructor_name` |
| `courses` | `course_id` | `course_title`, `instructor_id` (reference) |
| `enrolments` | (`learner_id`, `course_id`) | `joined_on`; both IDs also reference parent rows |

Here the non-key details of each table describe the fact identified by that table's key. The simple “no non-key through another non-key” rule diagnoses *this* transitive dependency; full formal third-normal-form analysis must consider **all candidate keys** and prime attributes, not just a chosen primary key. For this catalogue, each stated identifier is the only candidate key we use for that entity.

Read a final row: `enrolments(1, 101, 2026-09-01)` means Anu joined course 101 on that date; `courses(101, "AI Foundations", 7)` identifies its instructor; `instructors(7, "Nisha")` gives the instructor's name. Course 102 exists in `courses` even after its last enrolment is removed.

## Build the repair in SQL

After examining the original rows for conflicting details, create four related tables:

```sql
CREATE TABLE learners (
    learner_id INTEGER PRIMARY KEY,
    learner_name TEXT NOT NULL
);
CREATE TABLE instructors (
    instructor_id INTEGER PRIMARY KEY,
    instructor_name TEXT NOT NULL
);
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_title TEXT NOT NULL,
    instructor_id INTEGER NOT NULL REFERENCES instructors(instructor_id)
);
CREATE TABLE enrolments (
    learner_id INTEGER NOT NULL REFERENCES learners(learner_id),
    course_id INTEGER NOT NULL REFERENCES courses(course_id),
    joined_on TEXT NOT NULL,
    PRIMARY KEY (learner_id, course_id)
);
```

The accompanying Python program builds these tables in an in-memory SQLite database, transfers the three sample enrolments, and checks that joining the four tables gives back all three original rows:

```sql
SELECT l.learner_name, c.course_title, i.instructor_name, e.joined_on
FROM enrolments AS e
JOIN learners AS l ON l.learner_id = e.learner_id
JOIN courses AS c ON c.course_id = e.course_id
JOIN instructors AS i ON i.instructor_id = c.instructor_id
ORDER BY l.learner_id, c.course_id;
```

Expected joined rows: **Anu—AI Foundations—Nisha—2026-09-01**; **Anu—Git Basics—Kiran—2026-09-03**; **Ravi—AI Foundations—Nisha—2026-09-02**. The lab prints counts instead of the joined names; look at `reconstructed(db)` in the script to see and edit the query.

**Migration caution:** before choosing one value for a repeated learner, course, or instructor ID, compare all repeated values. The lab's `records_by_key` raises a clear error if the same instructor ID has conflicting names. Silently keeping whichever row appears first could turn a data error into a lasting stored fact. A real migration needs conflict review, an explicit choice, backups, a rollback plan, a validation query, and a controlled deployment window.

## Practice: make changes, then check what survives

First run `python check_normalisation.py`. It checks that renaming instructor 7 **once** changes that instructor's name in every joined result, and that deleting the final enrolment in course 102 leaves course 102 in `courses`. It then adds course 103 before any enrolment and rejects an enrolment for unknown learner 999. The script also tries to migrate inconsistent source rows and confirms the conflict is caught before the new tables are created.

Now copy the files. Starting from a newly migrated database, make this change yourself:

1. Insert instructor 9, **Leela**.
2. Insert course 103, **Data Basics**, taught by instructor 9, while it has no learners.
3. Insert learner 3, **Meera**.
4. Enrol Meera in Data Basics on `2026-09-04`.
5. Print the joined result and assert that course 103 had zero enrolments **before** step 4 and one **after**.

**Worked solution:** add this to a copied script after `create_flat(db)` and `migrate(db)`:

```python
with db:
    db.execute("INSERT INTO instructors VALUES (?, ?)", (9, "Leela"))
    db.execute("INSERT INTO courses VALUES (?, ?, ?)", (103, "Data Basics", 9))
    db.execute("INSERT INTO learners VALUES (?, ?)", (3, "Meera"))

before = db.execute(
    "SELECT COUNT(*) FROM enrolments WHERE course_id = ?", (103,)
).fetchone()[0]
assert before == 0

with db:
    db.execute(
        "INSERT INTO enrolments VALUES (?, ?, ?)",
        (3, 103, "2026-09-04"),
    )

after = db.execute(
    "SELECT COUNT(*) FROM enrolments WHERE course_id = ?", (103,)
).fetchone()[0]
assert after == 1
print([row for row in reconstructed(db) if row[2] == 103])
```

Expected printed list:

```text
[(3, 'Meera', 103, 'Data Basics', 9, 'Leela', '2026-09-04')]
```

The course can exist before anyone joins because a course row lives in `courses`, and joining it is a separate fact in `enrolments`. If the insert fails with a foreign-key error, insert the referenced instructor and learner first and check `PRAGMA foreign_keys` for that connection. If a name still differs across joined rows, look for duplicate descriptive facts stored outside their home table.

## A deliberate performance choice: denormalisation

**Denormalisation** is a *deliberate* decision to store or materialise some facts again for a specific access pattern. For example, a reporting system may keep a precomputed daily count of enrolments per course. That count can make a frequent report cheaper, but must be updated or refreshed when enrolments change. A report count is **derived data**; its owner, update rule, acceptable delay, and reconciliation check must be documented.

| Choice | Advantage | Cost to control |
|---|---|---|
| Four linked tables | One natural home for each fact; fewer contradictory copies | Queries may need joins |
| Copy instructor name into every enrolment | Can simplify a particular read | A rename can leave inconsistent copies |
| Materialise a course's daily enrolment count | Can speed a repeated report | Counts may become stale; requires refresh and checks |

Do not assume every join is slow or every duplicated field is wrong. Measure the actual query and state whether a copy is a **current fact**, a **historical snapshot**, or a **derived value**. A true historical snapshot of the name shown at enrolment time has a different meaning from a redundant copy of the instructor's current name.

## Check your understanding

| Question | Answer |
|---|---|
| Does one row per learner–course pair guarantee no anomaly? | No. The flat table is already in first-normal-form shape but repeats descriptive facts. |
| Why does `learner_name` create a second-normal-form problem in the flat enrolment table? | It depends only on `learner_id`, part of the composite key. |
| Why does `instructor_name` leave a third-normal-form issue in the intermediate `courses` table? | `course_id` determines `instructor_id`, which determines the instructor's name. |
| Is storing course 101's ID in several enrolments redundant in the same way as repeating its title? | No. Each ID records a different learner–course link; one authoritative course title can live in `courses`. |
| Why did the migrated version still have three enrolments? | Splitting descriptive facts into their home tables did not remove any of the three association facts. |
| What must be checked before migrating a flat sheet with inconsistent titles? | Identify conflicting rows and resolve them according to the actual business record; do not silently select one. |
| Can you keep a cached count of course enrolments? | Yes, if you define its refresh/consistency policy and verify it against authoritative enrolments. |

## Remember

- Identify the **fact** in a field and the **identifier** that determines it.
- One stored association per row addresses repeating groups; it does not settle all dependencies.
- A partial dependency from part of a composite key is the problem addressed by second normal form.
- A transitive dependency through a separate non-key fact is the problem illustrated by third normal form here.
- A normalised schema lets courses and instructors exist independently of enrolments, while keys and references preserve valid links.
- Validate source conflicts and compare reconstructed results during migration; treat denormalisation as a measured design decision.

## Further reading

- [IBM: database normalization, dependencies, and anomalies](https://www.ibm.com/think/topics/database-normalization)
- [Microsoft Learn: description of database normalization basics](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
- [SQLite: foreign-key support](https://www.sqlite.org/foreignkeys.html)
