# Set operations

## Combine the outputs of two queries

Suppose two teams make lists of course IDs. The **core candidates** table contains `101, 103, 103, 105`. The **practice candidates** table contains `102, 103, 104, 104, 105`. Repeated IDs are intentional: a course can occur more than once within an input list. A separate course catalogue maps those IDs to titles:

| course_id | title |
|---:|---|
| 101 | AI Foundations |
| 102 | Git Basics |
| 103 | Data Basics |
| 104 | Python Basics |
| 105 | SQL Basics |

A **set operation** combines the *results of two `SELECT` statements* according to a rule. It does not combine source rows side by side the way a join does. First ask the two branches for the same kind of result, a single `course_id` column. Then choose whether you want all IDs, shared IDs, or IDs in one list but not the other.

| Question | Operator | Result IDs in this dataset |
|---|---|---|
| In either list, once each | `UNION` | 101, 102, 103, 104, 105 |
| All occurrences from both lists | `UNION ALL` | 101, 102, 103, 103, 103, 104, 104, 105, 105 |
| In both lists | `INTERSECT` | 103, 105 |
| In core but not practice | `EXCEPT` | 101 |
| In practice but not core | Reverse `EXCEPT` inputs | 102, 104 |

Each query returns rows. For these one-column examples, a row is just one ID, so the table above can talk about ID sets. Once you select more columns, the **entire output row** determines whether two results are duplicates.

## Use compatible queries

A **compatible query** pair must return the same number of result columns, in corresponding positions. For example, this is valid: both branches return one ID.

```sql
SELECT course_id FROM core_candidates
UNION
SELECT course_id FROM practice_candidates
ORDER BY course_id;
```

This is invalid because the left branch returns one column and the right returns two:

```sql
SELECT course_id FROM core_candidates
UNION
SELECT course_id, title FROM course_catalogue;
```

SQLite reports that the `SELECT` statements do not have the same number of result columns. Matching the **count** is not enough for a *meaningful* result: position 1 should have the same intended meaning in both branches, position 2 the same intended meaning, and so on. Do not accidentally put a title in the position used for an ID. SQLite's type rules are flexible, while another database can require more strict type compatibility; choose corresponding values that make sense in either system.

Place `ORDER BY` **once at the end** of the compound query to sort the combined output. It does not belong in each component `SELECT` in this SQLite form. Without the final sort, do not rely on the displayed order of set-operation results. The examples explicitly order IDs so you can compare them reliably.

## `UNION`: keep each output row once

`UNION` produces a **union result**: every distinct row found in either query. It performs **duplicate removal** across and within the inputs:

```sql
SELECT course_id FROM core_candidates
UNION
SELECT course_id FROM practice_candidates
ORDER BY course_id;
```

Expected IDs are **101, 102, 103, 104, 105**. The two copies of 103 in core and the one in practice turn into one output row for 103. The two copies of 104 in practice turn into one 104. The two copies of 105 across the lists turn into one 105. Think through the source rows before comparing with the five unique output IDs.

`UNION` does not edit the lists. A later `SELECT` from `core_candidates` still finds two rows with ID 103. “Removal” describes duplicate rows in this **query result**, not deletion from a table.

## `UNION ALL`: preserve each occurrence

`UNION ALL` combines both branch results with **duplicate preservation**:

```sql
SELECT course_id FROM core_candidates
UNION ALL
SELECT course_id FROM practice_candidates
ORDER BY course_id;
```

There are **nine** input rows, so the sorted output has nine IDs: `101, 102, 103, 103, 103, 104, 104, 105, 105`. Course 103 occurs three times in total: twice in core and once in practice. `UNION ALL` keeps those occurrences instead of reducing them to a single row. The final `ORDER BY` sorts the nine-row result; it does not change how many 103s exist.

| ID | Occurrences in core | Occurrences in practice | Under `UNION` | Under `UNION ALL` |
|---:|---:|---:|---:|---:|
| 101 | 1 | 0 | 1 | 1 |
| 102 | 0 | 1 | 1 | 1 |
| 103 | 2 | 1 | 1 | 3 |
| 104 | 0 | 2 | 1 | 2 |
| 105 | 1 | 1 | 1 | 2 |

Choose `UNION ALL` when each occurrence is meaningful to the question; choose `UNION` when you want distinct output rows. Do not use `UNION` merely to conceal accidental duplicates from a wrong join or data problem. First determine why repeats appear.

## `INTERSECT`: keep shared rows

An **intersection result** contains rows that appear in **both** branch results:

```sql
SELECT course_id FROM core_candidates
INTERSECT
SELECT course_id FROM practice_candidates
ORDER BY course_id;
```

The result is **103, 105**. Course 103 appears in both lists, and so does 105. Duplicates are removed from the intersection result: the two 103 rows in core do not produce two shared IDs. This is a direct way to ask for the common ID set, distinct from a join that can multiply matching occurrences.

If you reverse the two input branches of `INTERSECT`, the shared set remains 103 and 105. The question “in both” has no preferred direction.

## `EXCEPT`: keep one side's difference

A **difference result** keeps rows from the **left** branch that do not appear in the **right** branch:

```sql
SELECT course_id FROM core_candidates
EXCEPT
SELECT course_id FROM practice_candidates
ORDER BY course_id;
```

This returns **101**. Core IDs 103 and 105 are removed from the result because each also appears in practice. Course 101 occurs only in core.

Reverse the branch order and the question changes:

```sql
SELECT course_id FROM practice_candidates
EXCEPT
SELECT course_id FROM core_candidates
ORDER BY course_id;
```

The result is **102, 104**. These occur in practice but not core. Although practice contains 104 twice, the `EXCEPT` result contains it once: `EXCEPT` removes duplicates. Unlike `INTERSECT`, **direction matters** for `EXCEPT`. Read it aloud as “left minus right” before running it. Neither statement deletes from its source table.

## A duplicate is an entire output row

Suppose you also select a label telling the reader which list an ID came from:

```sql
SELECT course_id, 'core' AS source FROM core_candidates
UNION
SELECT course_id, 'practice' AS source FROM practice_candidates
ORDER BY course_id, source;
```

The output is `(101, 'core')`, `(102, 'practice')`, `(103, 'core')`, `(103, 'practice')`, `(104, 'practice')`, `(105, 'core')`, `(105, 'practice')`. Within core, repeated `(103, 'core')` rows collapse; within practice, repeated `(104, 'practice')` rows collapse. But `(103, 'core')` and `(103, 'practice')` are **different rows** because their second values differ. `UNION` does not promise “one row per course ID” when other selected fields differ. To obtain one row per course ID, select only the ID when forming the set, then join it to the catalogue for a title if needed.

SQLite treats two `NULL` values as equal when checking duplicates for compound `SELECT` results. For example, `SELECT NULL UNION SELECT NULL` produces **one** `NULL` row, while `SELECT NULL UNION ALL SELECT NULL` produces **two**. This is a duplicate-checking rule for these query results; it is not the same as writing a normal `WHERE value = NULL` condition. The lab verifies both outcomes.

## Guided lab: predict, run, vary, repair

Download the [set operations lab](QAI.02.01.25_Set_Operations_Lab.zip), unzip it, and run from its folder:

```sh
python set_operations.py
python check_set_operations.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module builds the two candidate lists and the course catalogue in memory. The first program prints:

```text
UNION: [101, 102, 103, 104, 105]
UNION ALL: [101, 102, 103, 103, 103, 104, 104, 105, 105]
INTERSECT: [103, 105]
Core EXCEPT practice: [101]
Practice EXCEPT core: [102, 104]
UNION with source labels: [(101, 'core'), (102, 'practice'), (103, 'core'), (103, 'practice'), (104, 'practice'), (105, 'core'), (105, 'practice')]
Project shared: [(103, 'Data Basics'), (105, 'SQL Basics')]
Independent variation: [(102, 'Git Basics'), (104, 'Python Basics')]
Stored tables unchanged: True
```

Before running, write the two input lists, then predict the five operation outputs without SQL. **Controlled change:** reverse `EXCEPT` by calling `one_column(db, 'EXCEPT', reverse=True)` in a copy. Explain why `[101]` changes to `[102, 104]`. Restore the original call afterward. Then add a source label to a `UNION` as in the example above and predict that 103 and 105 each appear once for each different label. The checker also verifies that a mismatched column count raises an error and that the stored tables are unchanged.

**Reproduce and repair a logic failure:** a report wants *one ID per course that appears in either list*, but you use `UNION ALL`. It returns nine rows, with repeated 103, 104, and 105. Repair it to `UNION` on the **single ID column**, then check the five distinct IDs. If you instead select a different source label in each branch, ID 103 still appears twice, because the complete output rows differ. Select the ID set first and attach the title later. The checker verifies the supplied examples; compare your own edited query with your prediction as well.

## Mini-project: courses recommended by both lists

A planner wants **one row per course appearing in both lists**, with course ID and title in ID order. Use `INTERSECT` to determine the shared IDs, then attach titles from `course_catalogue`. The shared IDs are **103 and 105**, so expected rows are `(103, 'Data Basics')` and `(105, 'SQL Basics')`. The repeated 103 in the core list should not create a repeated final row.

**Reference solution:**

```sql
WITH shared_ids AS (
    SELECT course_id FROM core_candidates
    INTERSECT
    SELECT course_id FROM practice_candidates
)
SELECT c.course_id, c.title
FROM shared_ids AS s
JOIN course_catalogue AS c ON c.course_id = s.course_id
ORDER BY c.course_id;
```

The CTE gives the intermediate shared-ID result a name for this one statement. A matching join attaches the title. The lab's `project_shared()` runs this query. Check that 101 is not shared, 104 is not shared despite appearing twice within practice, and 103 and 105 each appear once. The source tables remain unchanged.

**Independent variation:** find courses listed in **practice but not core** and show their ID and title, each once, in ID order. Before looking at the reference, predict **102 and 104**. In particular, the repeated 104 in the practice source should yield one final course row.

```sql
WITH practice_only AS (
    SELECT course_id FROM practice_candidates
    EXCEPT
    SELECT course_id FROM core_candidates
)
SELECT c.course_id, c.title
FROM practice_only AS p
JOIN course_catalogue AS c ON c.course_id = p.course_id
ORDER BY c.course_id;
```

Expected rows are `(102, 'Git Basics')` and `(104, 'Python Basics')`. The lab's `independent_variation()` is the reference after your own attempt. If your output is 101 instead, you reversed the sides of `EXCEPT`. Keep your draft query, predicted rows, actual rows, and the corrected order if needed.

## Diagnose set-operation output

| Symptom | What to inspect | Repair |
|---|---|---|
| SQLite says the branches have different column counts | One `SELECT` returns more fields than the other | List corresponding columns explicitly and match their positions |
| Rows repeat when one row per ID was wanted | Used `UNION ALL`, or selected extra fields that differ | Choose `UNION` over matching ID columns for a distinct ID set |
| `UNION` still displays ID 103 twice | One output has `(103, 'core')`, another `(103, 'practice')` | Recognise that duplicate removal compares entire rows; form the one-column ID set first |
| Difference query returns 101 rather than 102 and 104 | `EXCEPT` branches are in the wrong order | Read left minus right and reverse the branches |
| Row order seems unstable | No final `ORDER BY` on the compound result | Sort once at the end of the combined statement |
| Common courses seem to repeat | A join on repeated source rows was used instead of a distinct common-ID result | Calculate `INTERSECT` IDs first and trace the later title join |

## Check your understanding

1. Why must both branches of a set operation return compatible columns?
2. How many output rows does `UNION` return for these lists? How many does `UNION ALL` return?
3. Why does ID 103 occur three times in the sorted `UNION ALL` output?
4. What is the `INTERSECT` result, and why does it not repeat 103?
5. What is core `EXCEPT` practice? What is practice `EXCEPT` core?
6. Why does adding different `source` labels make ID 105 occur twice under `UNION`?
7. Does any of these queries delete repeated IDs from the source tables?

**Answers and reasoning**

1. The result has one shared column layout; both branches need the same number of fields and corresponding meanings.
2. **Five** distinct ID rows under `UNION`; **nine** occurrence rows under `UNION ALL`.
3. Core has two rows with 103 and practice has one; `UNION ALL` preserves all three.
4. **103, 105**. `INTERSECT` includes shared rows once in its result, removing duplicates.
5. Core minus practice is **101**; practice minus core is **102, 104**.
6. `(105, 'core')` and `(105, 'practice')` are distinct complete output rows.
7. No. These are read queries that construct results; the source lists remain unchanged.

## Remember and retain

- `UNION` combines branch results and removes duplicate **rows**. `UNION ALL` keeps every occurrence.
- `INTERSECT` keeps rows common to both sides. `EXCEPT` keeps distinct left-side rows absent from the right; direction matters.
- The branches must return the same number of meaningfully corresponding columns. Duplicate removal compares every selected output field.
- Sort the combined result with one final `ORDER BY`. Use a named intermediate ID set when titles or other details must be attached after a set operation.
- Keep the two input lists, repeated-ID trace, reversed-`EXCEPT` repair, mini-project query, and independent variation for later review.

## Further reading

- [SQLite: compound SELECT statements and set operators](https://www.sqlite.org/lang_select.html)
- [SQLite: common table expressions](https://www.sqlite.org/lang_with.html)
- [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)
