# Indexes and query performance

## Start with a slow question, not an index name

Imagine a learning application with an `enrollments` table. Each row records an event ID, a course ID, a status such as `complete` or `pending`, and an integer `created_at` value that orders events. A report asks for the five most recent **completed** events for course **42**:

```sql
SELECT event_id, created_at
FROM enrollments
WHERE course_id = 42 AND status = 'complete'
ORDER BY created_at DESC
LIMIT 5;
```

The accompanying lab builds **6,000 synthetic rows**. Its first result is:

| event_id | created_at |
|---:|---:|
| 5942 | 5941 |
| 5742 | 5741 |
| 5642 | 5641 |
| 5442 | 5441 |
| 5342 | 5341 |

A **slow query** is one whose response time exceeds what its user or application can tolerate under the actual data and workload. A correct result can still take too much time or use too many resources. Define the question, the expected rows, the data size, and the response target before changing the schema. A measured slow query deserves investigation; the existence of `WHERE` alone does not prove that an index is needed.

## Scan, index, lookup, plan

An **index** is a separate database structure ordered by one or more chosen fields. An **indexed column** is a field included in that structure. A useful mental model is an alphabetized book index: it helps locate selected entries without reading every page, but it takes space and must be updated when the book changes. A database index is maintained by the database, and its use depends on the actual query and the optimiser's choice.

With no suitable index, the database may do a **table scan**, examining table rows to find qualifying events, then sort matches to get the newest five. An **index lookup** can instead search the ordered entries for the requested course and status, then read the newest entries in the needed order. In SQLite, the planner may also perform a **covering index** read when all fields the query needs can be obtained from the index and its row identifier. The lab's query selects `event_id` (an integer primary key) and `created_at`, making that possible in this example.

Ask SQLite to show its proposed **query plan**:

```sql
EXPLAIN QUERY PLAN
SELECT event_id, created_at
FROM enrollments
WHERE course_id = 42 AND status = 'complete'
ORDER BY created_at DESC LIMIT 5;
```

For the lab's unindexed data, the plan includes `SCAN enrollments` and `USE TEMP B-TREE FOR ORDER BY`. The first detail describes reading the table; the second describes a temporary ordering step. The exact wording and plan choices can change across SQLite versions or different data. Look for the important operation and verify it on **your** database rather than treating one printed plan as a universal promise. A `SCAN` can also mean walking a whole index in order, so read the full detail; it does not always mean raw table pages.

The **query optimiser** compares possible ways to execute a SQL request and chooses an estimated low-cost plan. **Query cost** is an estimate involving work such as rows examined, lookups, sorting, and I/O; it is not simply the number of characters in the SQL statement. Statistics, data distribution, available indexes, selected fields, and ordering all affect the choice. `EXPLAIN QUERY PLAN` shows the chosen access path, not an exact elapsed-time prediction.

## Build an index for this access pattern

Our report constrains `course_id` and `status` by equality and wants newest `created_at` first. A **composite index** places those fields together in the order useful for this report:

```sql
CREATE INDEX idx_enroll_course_status_recent
ON enrollments (course_id, status, created_at DESC);
```

This is **index creation**. With the lab's data, the plan changes to a `SEARCH enrollments USING COVERING INDEX idx_enroll_course_status_recent` detail, showing constraints on `course_id` and `status`. The ordered third field supports the requested recent-first reading, so the lab's indexed plan no longer reports a separate temporary sort. The five result rows are **unchanged**. The index changes *how* the database finds rows, not *which* rows satisfy the SQL.

Column order is part of the design. A lookup on `course_id = ?` can use the **leftmost prefix** of this index; the report's equality conditions on both course and status can use the first two fields before following `created_at`. A query that filters **only** on `status` has no equality condition on the leftmost `course_id`. The lab's status-only query scans. SQLite can have other strategies depending on statistics and version, so do not claim that a status-only query can *never* benefit from this index. Inspect that query's plan and workload separately. A very common status such as `complete` may also make an index less selective than expected.

The chosen index answers this particular report well. It does not automatically optimize every filter, join, aggregate, or sort on the table. For example, adding `title` from a separate course table introduces a join, and selecting more fields can require table reads rather than a covering index. Inspect the *whole* report plan after each real query change. Avoid adding an index for every field by habit.

## Measure correctness and speed separately

The lab prints the rows and plan before and after index creation. It also measures repeated local query runs and prints **illustrative median milliseconds per query**. The measured numbers depend on the machine, SQLite build, cache, and competing work. The checker deliberately makes **no speed-ratio assertion**; it checks equal results and the observed plan pattern for its controlled dataset.

For an application, measure the actual slow query under representative row counts and parameter values. Record a baseline such as median, tail latency, frequency, and rows returned. Measure again after the change under comparable conditions. Check the read improvement alongside index storage, index-build time, and write latency. SQLite's `PRAGMA optimize` can help maintain planner statistics; statistics can affect the chosen plan. An index that helps one frequent read can still be a poor choice if it slows far more important writes or consumes unacceptable space.

| Evidence to collect | Why it matters |
|---|---|
| Exact query and bound values | A plan for course 42 may differ from another course or status |
| Row count and distribution | A rare value and a common value may justify different access paths |
| Plan before and after | Reveals scan/search and sorting decisions |
| Result row comparison | Detects accidental changes in filter or order while optimizing |
| Read latency distribution | Shows whether users benefit under comparable load |
| Write latency and index size | Makes maintenance and storage costs visible |

An index is a *candidate optimization*, not a guarantee of faster execution. If the query still scans, inspect the predicate and plan: the optimiser may reasonably prefer the scan for a small table or broad selection, or a function around an indexed field may prevent the simple lookup you expected. Query optimisation can involve changing a predicate, narrowing requested columns, improving an index, maintaining statistics, or fixing a needless join. Verify semantic equivalence whenever you rewrite SQL.

## Uniqueness is another reason to index

An ordinary index helps access. A **unique index** also rejects duplicate non-`NULL` keys. The lab uses a separate `learners` table with two synthetic email addresses:

```sql
CREATE UNIQUE INDEX ux_learner_email ON learners (email);
```

Trying to insert a third learner with the same `learner1@example.invalid` address raises a constraint error, leaving two learners. An address not already present succeeds. The lab marks `email NOT NULL`; SQLite's unique-index semantics otherwise allow multiple `NULL` values. Choose a uniqueness rule based on the product's actual identity rules: a display name often is not unique, and a composite unique index can enforce uniqueness on a *combination* of fields. Do not create a unique index just because a column usually looks distinct in a sample.

The lab uses the reserved `.invalid` domain and keeps everything in memory. In a real system, avoid copying sensitive values into shared plan screenshots, logs, or benchmark datasets. A query plan is most useful when paired with safe, representative counts and parameter categories rather than personal records.

## Writes maintain indexes; dropping an index does not drop data

When an indexed field changes, SQLite maintains the index entries for the row. The lab changes event **5942** from `complete` to `pending`; it leaves the completed-event report, and the next matching row, event **5142**, enters the five-row output. There is no manual “refresh index” step after a normal `UPDATE`.

That automatic **index maintenance** has a cost for `INSERT`, `UPDATE`, and `DELETE`, in addition to storage and index creation. More indexes are therefore not automatically better. The unique index also enforces its rule at write time. Index design should balance read paths, write volume, and the importance of the constraint.

You can remove the experiment's performance index with:

```sql
DROP INDEX idx_enroll_course_status_recent;
```

The `enrollments` rows remain; the report still returns correct rows, but the lab's fresh plan reverts to a scan. Keep a named index change and a rollback instruction when deploying, and confirm that dropping the index does not also remove a constraint the application depends on. In this example, the composite index is for performance, while the separate unique index protects email uniqueness.

## Guided lab: inspect, change, repair

Download the [indexes and query performance lab](QAI.02.01.27_Indexes_and_Query_Performance_Lab.zip), unzip it, and run from its folder:

```sh
python index_performance.py
python check_index_performance.py
```

Use `python3` if needed. The program generates the same 6,000 rows each time. The plan and result portions are expected to resemble:

```text
Before plan: ['SCAN enrollments', 'USE TEMP B-TREE FOR ORDER BY']
Before rows: [(5942, 5941), (5742, 5741), (5642, 5641), (5442, 5441), (5342, 5341)]
After plan: ['SEARCH enrollments USING COVERING INDEX idx_enroll_course_status_recent (course_id=? AND status=?)']
After rows: [(5942, 5941), (5742, 5741), (5642, 5641), (5442, 5441), (5342, 5341)]
Results unchanged: True
Status-only plan: ['SCAN enrollments']
After status update: [(5742, 5741), (5642, 5641), (5442, 5441), (5342, 5341), (5142, 5141)]
Duplicate email rejected: True
Learner count: 2
```

A timing line also appears; its values are intentionally omitted here because they depend on your machine. A different valid SQLite build can print a different plan. Investigate plan differences, but treat correct rows and valid index behavior as the core result.

**Trace.** Predict why the report gives five rows, why event 5942 qualifies, and why 5142 enters after the status update. Identify the two equality filters and the ordering field. In the plan, point to the scan/search evidence and check whether an explicit sort is reported.

**Controlled change.** In a copy, change the report's course parameter from **42** to **43** (in both `result()` and its displayed plan call). Predict that the event IDs end in **43**, then run and compare five descending rows. Restore the supplied code before running the checker. Explain why the same composite index can serve either course value without making two separate indexes.

**Reproduce and repair a mismatch.** Change the index definition in your copy to `(status, created_at DESC)` and inspect the plan for course 42. You have removed `course_id` from the index; the SQL result must stay the same, but the access path may be less suitable because many courses share the same status. Repair it to `(course_id, status, created_at DESC)` and compare plans and timings under the same data. Do **not** infer performance from one timing run alone. The included checker verifies the supplied index, uniqueness, status update, and post-drop plan; compare your altered plans manually.

## Mini-project: a recent completions report

Build a report for a course activity page. The request is: for a chosen course, show the five latest completed events. Deliver the query, a suitable named index, result rows, before-and-after plans, and a brief recommendation that includes write and storage costs.

**Reference solution:**

```sql
SELECT event_id, created_at
FROM enrollments
WHERE course_id = 42 AND status = 'complete'
ORDER BY created_at DESC LIMIT 5;

CREATE INDEX idx_enroll_course_status_recent
ON enrollments (course_id, status, created_at DESC);
```

Run `EXPLAIN QUERY PLAN` on the `SELECT` both before and after `CREATE INDEX`. The five rows stay `5942, 5742, 5642, 5442, 5342` before the update; the scan changes to a lookup in the lab. Record the actual details and measured values from your run, then state whether the query is frequent enough and slow enough to justify the index in your own application. The answer may be “no” for a tiny table. For a high-write workload, measure its effect on writes before recommending deployment.

**Independent variation:** the course page now wants the **five most recent pending** events for course **42**. Predict IDs before changing the query. Replace the status parameter with `pending`, run the same ordered query, and compare its plan. The reference query is:

```sql
SELECT event_id, created_at
FROM enrollments
WHERE course_id = 42 AND status = 'pending'
ORDER BY created_at DESC LIMIT 5;
```

On the *original* 6,000-row dataset before the lab's update of event 5942, expected event IDs are **5842, 5542, 5242, 4942, 4642** in descending order. The same composite index can support the two equality conditions and newest-first order. If you run after the lab's status update, event 5942 becomes the newest pending row and the five IDs change accordingly. Make a fresh `make_db()` for the original-state reference, or state which database state your result represents. Save your query, prediction, plan, actual rows, and the reason for any difference.

## Operate the change deliberately

For a live application, capture an approved query and baseline, test the index against representative data, and check both read and write behavior. Build and deploy schema changes through the application's normal migration process; index creation may take time and lock or contend with writers depending on the database engine and setup. Watch query latency, error rate, write latency, and database/storage growth after rollout. Keep the `DROP INDEX` rollback available if the benefit does not justify its cost. Retest the plan after data distribution changes, because an optimiser may choose differently over time.

Do not treat a visible index name in a plan as proof of acceptable user experience. Also verify the correct rows and the application's latency target. The lab is an in-memory teaching example; its tiny, warm, single-process timing is not a production benchmark.

## Diagnose an unexpected result

| Symptom | What to inspect | Repair or next check |
|---|---|---|
| Query still scans after index creation | Predicate, index column order, row selectivity, statistics | Inspect plan and real parameters; use an index matching the access pattern if warranted |
| Rows changed after adding the index | SQL or test data changed too | Compare the exact same query, parameters, and database state |
| Separate sort remains | Index order does not match filter and `ORDER BY` needs | Review equality prefix and ordered field; compare plan |
| Status-only query scans | Leftmost course column is unconstrained | Measure that workload separately before considering another index |
| Insert with duplicate email fails | Unique index is enforcing its rule | Correct duplicate input or revisit intended identity rule |
| Recent report changes after a status update | Indexed entries are maintained with writes | Verify the new status and expected next matching row |
| One timing says “faster,” another “slower” | Noise, caching, load, different data or parameters | Repeat comparable runs; inspect distribution and latency percentiles |

## Check your understanding

1. What is the difference between a table scan and an index lookup in this report?
2. What does `EXPLAIN QUERY PLAN` tell you, and what does it not guarantee?
3. Why are `course_id` and `status` placed before `created_at DESC` in the composite index?
4. Does the five-row result change merely because the index is created?
5. Why may `WHERE status = 'complete'` still scan with this index?
6. What happens to event 5942 after its status changes to `pending`?
7. What extra behavior does `CREATE UNIQUE INDEX` provide? What about `NULL` in SQLite?
8. Which read and write measurements would you check before keeping an index in a live system?

**Answers and reasoning**

1. A scan examines the table broadly; a suitable lookup navigates ordered entries for course 42 and completed status.
2. It describes a chosen access path, including scans, searches, and sorting; it does not promise a particular elapsed time or a fixed plan across data and versions.
3. The query has equality conditions on the first two fields and then requests newest values first.
4. No. The lab gives the same five rows before the source update; only the access path changes.
5. The leftmost `course_id` condition is missing, and a broad common status may not benefit; inspect the actual plan.
6. It leaves the completed report; the next qualifying event 5142 enters the five-row result.
7. It rejects duplicate non-`NULL` indexed values; SQLite treats multiple `NULL`s as distinct for uniqueness, though the lab's email field is `NOT NULL`.
8. Compare representative read latency and correctness, write latency, index size, and rollout behavior under the application's actual workload.

## Remember and retain

- Start with a real query and a measured problem. Indexes are access paths with storage and write costs.
- Use the plan to distinguish scan, search, and sort. Check semantic equality before evaluating speed.
- Choose composite column order from the filters and ordering the query actually uses.
- A unique index enforces a data rule; ordinary indexes only offer possible read-path benefits.
- Keep the SQL, parameters, row counts, before-and-after plans, timings, status-update trace, and rollback step as evidence for later review.

## Further reading

- [SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
- [SQLite: query planning](https://www.sqlite.org/queryplanner.html)
- [SQLite: CREATE INDEX](https://www.sqlite.org/lang_createindex.html)
- [SQLite: PRAGMA optimize and statistics](https://www.sqlite.org/lang_analyze.html)
