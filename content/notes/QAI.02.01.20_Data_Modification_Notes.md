# Data modification

## Read the rows before changing them

The last lesson inserted new courses. This lesson changes **existing rows** and removes rows in a private course catalogue. The runnable lab starts from six rows:

| course_id | title | instructor_id | duration_minutes | lesson_count | topic_note | status |
|---:|---|---:|---:|---:|---|---|
| 101 | AI Foundations | 7 | 95 | 4 | intro | published |
| 102 | Git Basics | 8 | 50 | 3 | `NULL` | published |
| 103 | Data Basics | 7 | 80 | 4 | tables | published |
| 104 | Python Basics | 8 | 65 | 3 | `NULL` | published |
| 105 | SQL Basics | 7 | 70 | 3 | `NULL` | draft |
| 106 | Query Practice | 8 | 45 | 2 | `NULL` | draft |

**Data modification** changes values already stored in a row. **Data deletion** removes stored rows. Both are write operations. Unlike a `SELECT`, the result can affect later queries on the same database. This lab uses separate in-memory tables for broad changes; use the intended target database and confirm the target rows before running a write in your own work.

A useful preview is a read query using the same selection rule you plan for the write:

```sql
SELECT course_id, title, status
FROM course_catalogue
WHERE course_id = 105;
```

It identifies the one row to edit. Later, select it again to confirm the stored result. Also check a row that should **not** have changed.

## `UPDATE` and `SET` change selected rows

`UPDATE` names the table to modify. `SET` assigns new values to one or more columns. The **update condition** in `WHERE` selects existing rows to receive those assignments:

```sql
UPDATE course_catalogue
SET topic_note = 'queries', status = 'published'
WHERE course_id = 105;
```

Only course 105 matches the ID condition. After the statement, its selected fields are `(105, 'queries', 'published')`. Course 106 remains `(106, NULL, 'draft')`; courses 101–104 are unchanged. This is an **update of a selected row**. The row's ID stays 105 because we did not assign a new ID. `SET` can update more than one field in that row, separated by commas.

When a new value comes from application input, bind it rather than inserting it directly into SQL text:

```python
changed = db.execute(
    "UPDATE course_catalogue SET topic_note = ?, status = ? WHERE course_id = ?",
    ("queries", "published", 105),
).rowcount
db.commit()
```

In this lab, `changed` is **1**. Check the selected row and another row after committing. An affected-row count alone does not show that the right values were assigned, and its interpretation may have implementation details; the selected stored data is the main evidence.

A condition can match several rows. From a **fresh copy of the starting table**, this statement marks both draft rows for review:

```sql
UPDATE course_catalogue
SET status = 'review'
WHERE status = 'draft';
```

The selected rows are **105 and 106**. Their status becomes `review`; the four published rows retain `published`. This is an **update of selected rows** using one condition rather than repeating two ID-specific statements. A `WHERE` condition that matches no row is allowed: it changes zero rows, so inspect whether that is expected.

## Omitting `WHERE` updates all rows

Compare the targeted statement with this **update-all-rows** statement:

```sql
UPDATE course_catalogue
SET status = 'archived';
```

Without `WHERE`, **all six rows** have their `status` set to `archived`, including courses that were published. The lab runs it on a separate fresh in-memory table to make that consequence visible. This is a **destructive query** if you intended to edit only one course, even though its SQL syntax is valid. Do not infer that SQLite will supply a missing condition for you.

| Intended action | Statement shape | Affected IDs on fresh six-row data |
|---|---|---|
| Correct course 105 | `UPDATE ... SET ... WHERE course_id = 105` | 105 |
| Mark drafts for review | `UPDATE ... SET status = 'review' WHERE status = 'draft'` | 105, 106 |
| Set every status to archived | `UPDATE ... SET status = 'archived'` | 101–106 |

**Controlled failure and repair:** on a fresh copy only, omit `WHERE course_id = 105` from the first update. Predict that all six rows receive the new topic note and status, then inspect them. Start again from a fresh table and add the exact `WHERE` clause. Check that 105 changed and 101–104 and 106 retained their original values. Editing a dataset you can recreate makes the difference easy to observe; on shared data, inspect the target and transaction plan before executing a broad write.

## `DELETE` removes selected rows

`DELETE FROM` names the table. A **delete condition** in `WHERE` identifies rows to remove:

```sql
DELETE FROM course_catalogue
WHERE course_id = 106;
```

Only course 106 is removed. The original four courses and course 105 remain, so the catalogue now has **five rows**. `DELETE` removes a row; it does not erase the table definition. If you later query ID 106, no row is returned. If you query IDs 101–105, those rows still exist, with any previously committed updates. `DELETE FROM course_catalogue WHERE course_id = 999` affects zero rows in this data and is a valid statement, not a command to delete all rows.

`DELETE` without a condition means **delete all rows**:

```sql
DELETE FROM course_catalogue;
```

On a fresh six-row copy in the lab, this removes all six rows and leaves the now-empty table in place. `SELECT COUNT(*) FROM course_catalogue` then returns 0. This is a destructive query. The lab uses a separate fresh in-memory table for it so that other exercises still have their data.

| Command on a fresh table | Rows remaining | Table still exists? |
|---|---:|---|
| `DELETE FROM course_catalogue WHERE course_id = 106` | 5 | Yes |
| `DELETE FROM course_catalogue` | 0 | Yes |

If the intention is to remove some rows, first run `SELECT course_id ... WHERE <same condition>` and compare those IDs with the intended removal. After the deletion, verify both absence of selected IDs and presence of rows meant to remain. For an irreversible real-world removal, use appropriate backups, permissions, and transaction handling for that database; the lab's in-memory rows are disposable.

## What about `TRUNCATE`?

Some database systems use `TRUNCATE TABLE table_name` to remove all rows. **SQLite does not support `TRUNCATE TABLE` syntax**. In the lab:

```sql
TRUNCATE TABLE course_catalogue;
```

raises a syntax error and leaves all six rows in that fresh lab table. To empty a SQLite table while retaining the table definition, use `DELETE FROM course_catalogue` as demonstrated above. This describes the visible row-removal goal; do not assume that another database's `TRUNCATE` command has the same transaction, identity, trigger, or constraint behavior as SQLite's `DELETE`. If you work in another SQL system, check that system's documentation before choosing its all-row operation.

`TRUNCATE` and `DELETE FROM ...` are **not** ways to modify selected values. Use `UPDATE` to change existing rows, and use a conditioned `DELETE` to remove selected rows. A missing `WHERE` on either `UPDATE` or `DELETE` broadens the action to the entire table.

## Guided lab: predict, run, diagnose

Download the [data modification lab](QAI.02.01.20_Data_Modification_Lab.zip), unzip it, and run from its folder:

```sh
python data_modification.py
python check_data_modification.py
```

Use `python3` if needed. The standard-library `sqlite3` module builds private in-memory tables. The first program prints a preview before changing the project rows, then:

```text
Preview project IDs: [(105,), (106,)]
Project affected (updated, deleted): (1, 1)
Project rows: [(101, 'AI Foundations', 4, 'intro', 'published'), (102, 'Git Basics', 3, None, 'published'), (103, 'Data Basics', 4, 'tables', 'published'), (104, 'Python Basics', 3, None, 'published'), (105, 'SQL Basics', 3, 'queries', 'published')]
Independent update count: 2
Independent rows: [(101, 'AI Foundations', 4, 'intro', 'published'), (102, 'Git Basics', 4, None, 'published'), (103, 'Data Basics', 4, 'tables', 'published'), (104, 'Python Basics', 4, None, 'published'), (105, 'SQL Basics', 3, 'queries', 'published')]
All-row update on a fresh table: (6, [('archived',)])
All-row delete on a fresh table: (6, 0)
SQLite TRUNCATE attempt: ('near "TRUNCATE": syntax error', 6)
```

The precise wording of a SQLite error can vary, but its meaning here is that the command is unsupported; the checker verifies that the attempt fails and all six rows remain. The separate program checks both changed and unchanged rows, a zero-match delete, the broad-update and broad-delete outcomes, and the independent variation. Before running, predict the remaining IDs and status of 105 and 106. To reproduce the missing-`WHERE` failure, use a **new private connection** and inspect all six rows, then start fresh for the corrected statement. The two destructive demonstrations in the supplied program already use separate fresh connections.

## Mini-project: correct a listing and remove an obsolete one

A catalogue editor decides to publish SQL Basics, record its topic note as `queries`, and remove the obsolete Query Practice listing. Starting from the six-row table, update **only ID 105** and delete **only ID 106**. Return the remaining IDs, the new values of course 105, and the number of rows. Predict: remaining IDs **101, 102, 103, 104, 105**; course 105 has note `queries` and status `published`; the count is **5**.

**Reference solution:**

```sql
SELECT course_id, title FROM course_catalogue
WHERE course_id IN (105, 106) ORDER BY course_id;

UPDATE course_catalogue
SET topic_note = 'queries', status = 'published'
WHERE course_id = 105;

DELETE FROM course_catalogue
WHERE course_id = 106;

SELECT course_id, title, topic_note, status
FROM course_catalogue
WHERE course_id IN (105, 106) ORDER BY course_id;

SELECT COUNT(*) FROM course_catalogue;
```

The verification query after the writes returns only `(105, 'SQL Basics', 'queries', 'published')`; the count is 5. The lab's `project_changes()` performs the two writes with bound values and commits them. Its returned `(1, 1)` reports one update and one deletion. The checker also ensures the other rows keep their intended values. If the count is 0 or all statuses became `published`, examine the missing or incorrect `WHERE` condition and restart on a fresh private table.

**Independent variation:** after the project, the editor adds one lesson to every **remaining course taught by instructor 8**. Write a single `UPDATE` using `SET lesson_count = lesson_count + 1` and a suitable `WHERE`. From the remaining five rows, instructor 8 has courses **102** and **104**. Their lesson counts go from **3 to 4**. Course 105 remains at 3; the removed course 106 does not return. Compare your attempt with this reference:

```sql
UPDATE course_catalogue
SET lesson_count = lesson_count + 1
WHERE instructor_id = 8;
```

The lab's `independent_variation()` returns an affected-row count of 2. Confirm the selected output `(102, 4)` and `(104, 4)` and check unaffected course `(105, 3)`. Save your preview IDs, statement, predicted after-state, actual after-state, and one explanation of why ID 106 is absent. Applying this increment twice would add two lessons; restart a fresh lab database for a new attempt rather than treating repeated execution as a harmless rerun.

## Diagnose a write mismatch

| Symptom | What to inspect | Repair |
|---|---|---|
| Every row's status changed | `UPDATE` had no `WHERE` or the condition matched all rows | Preview IDs with `SELECT` and add the exact condition; restart from clean test data |
| Course 105 did not change | Wrong ID or condition matched zero rows | Select ID 105, check the condition, then inspect its fields after writing |
| Too many rows disappeared | `DELETE` had no `WHERE` or a broad condition | Preview target IDs, use a precise delete condition on a fresh dataset |
| Query of deleted ID returns no row | Expected effect of a successful targeted deletion | Confirm other IDs still exist and inspect total count |
| `TRUNCATE TABLE` causes a syntax error | SQLite does not implement that statement | Use `DELETE FROM table_name` for an all-row removal when that is the intended action |
| Lesson count rose by 2 instead of 1 | Repeated the incremental `UPDATE` | Restart the private lab or compare before and after counts once per run |

## Check your understanding

1. Which part of `UPDATE ... SET ... WHERE ...` chooses the target rows, and which part specifies the new values?
2. Which IDs are modified by `WHERE status = 'draft'` on the fresh six-row catalogue?
3. What changes if you omit `WHERE` from the update setting `status = 'archived'`?
4. Does a targeted `DELETE` change the table definition?
5. How many rows remain after deleting ID 106 from the fresh six-row table? What if you omit `WHERE`?
6. What happens when `TRUNCATE TABLE course_catalogue` is run in SQLite?
7. After the mini-project, why does an update for instructor 8 change only IDs 102 and 104?

**Answers and reasoning**

1. `WHERE` is the update condition selecting rows. `SET` gives the new column values.
2. **105 and 106**. They are the two draft rows in the starting data.
3. All **six** rows are updated to `archived`; the query no longer selects only a subset.
4. No. The table remains and the selected row is removed from its contents.
5. **Five** remain with a targeted deletion. Without `WHERE`, all six rows are removed and the table is empty.
6. It raises a syntax error and does not remove rows; SQLite uses `DELETE FROM` for an all-row deletion.
7. ID 106 was deleted, while IDs 102 and 104 remain with instructor 8. Other surviving IDs belong to instructor 7.

## Remember and retain

- `UPDATE table SET column = value WHERE condition` changes selected existing rows. Without `WHERE`, it updates all rows.
- `DELETE FROM table WHERE condition` removes selected rows. Without `WHERE`, it removes all rows while retaining the table.
- `TRUNCATE TABLE` is used in some other systems; SQLite rejects it. Check the database system before choosing an all-row command.
- A write may be syntactically valid yet affect the wrong rows. Preview intended IDs, inspect both changed and unchanged rows, and check counts afterward.
- Keep the corrected missing-`WHERE` example, mini-project before/after evidence, and independent lesson-count update to revisit how conditions control writes.

## Further reading

- [SQLite: UPDATE](https://www.sqlite.org/lang_update.html)
- [SQLite: DELETE](https://www.sqlite.org/lang_delete.html)
- [SQLite: supported SQL statements](https://www.sqlite.org/lang.html)
- [Python: sqlite3 transactions and parameters](https://docs.python.org/3/library/sqlite3.html)
