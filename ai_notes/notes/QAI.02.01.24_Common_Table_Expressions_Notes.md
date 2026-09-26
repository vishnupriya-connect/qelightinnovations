# Common table expressions

## Give a query result a name

The course catalogue has five rows:

| course_id | title | duration_minutes |
|---:|---|---:|
| 101 | AI Foundations | 95 |
| 102 | Git Basics | 50 |
| 103 | Data Basics | 80 |
| 104 | Python Basics | 65 |
| 105 | SQL Basics | 70 |

A **common table expression**, often shortened to **CTE**, gives an inner query a name that a following SQL statement can use. `WITH` introduces the **named query**:

```sql
WITH long_courses AS (
    SELECT course_id, title, duration_minutes
    FROM course_catalogue
    WHERE duration_minutes >= 70
)
SELECT course_id, title
FROM long_courses
ORDER BY course_id;
```

`long_courses` names the rows produced inside the parentheses: 101 (95), 103 (80), and 105 (70). The final `SELECT` reads that named result and returns `(101, 'AI Foundations')`, `(103, 'Data Basics')`, and `(105, 'SQL Basics')`.

Think of it as a **temporary result for this statement**: it is a convenient name for the query's output, not a new permanent course table. After this statement finishes, a separate `SELECT * FROM long_courses` fails because that name is no longer defined. The actual course catalogue remains intact. “Temporary” here describes **scope**, not a promise that SQLite physically builds and stores every CTE row in memory; the database may choose how to evaluate it.

| Part | Role in this example |
|---|---|
| `WITH` | Starts the named-query definitions |
| `long_courses AS (...)` | Gives a query result a name within this statement |
| `SELECT ... FROM course_catalogue WHERE ...` | Defines which rows the name represents |
| Final `SELECT ... FROM long_courses` | Uses the named result to answer the question |

The CTE can make a longer query easier to read: state an intermediate set once, then use its name. It can also make the same intermediate set available at more than one place within that one statement when the query needs it. A CTE is not the same as a permanent view or table; it does not change stored rows merely by being read.

## Use multiple CTEs in one `WITH`

Separate two CTE definitions with a comma. A later CTE can read one defined earlier:

```sql
WITH long_courses AS (
    SELECT course_id, duration_minutes
    FROM course_catalogue
    WHERE duration_minutes >= 70
),
duration_summary AS (
    SELECT COUNT(*) AS course_count,
           SUM(duration_minutes) AS total_minutes
    FROM long_courses
)
SELECT course_count, total_minutes
FROM duration_summary;
```

This **multiple CTE** query has two named steps. `long_courses` contains 101, 103, and 105. `duration_summary` reads those rows and calculates count **3** and total **245** minutes (`95 + 80 + 70`). The final result is `(3, 245)`. It is one statement with one `WITH` and two comma-separated definitions, not two `WITH` statements.

**Controlled variation:** change the long-course boundary from 70 to 80. Now only 101 and 103 enter the first CTE; the second produces `(2, 175)`. Check the boundary row 103 at exactly 80 and excluded row 105 at 70. If the count changes but the sum does not match 95 + 80, inspect whether the second CTE is actually reading `long_courses`.

## A prerequisite chain needs repeated expansion

The ordinary CTE names a query result but does not need to refer to itself. A **recursive CTE** does refer back to its own named result to follow a chain. For this lesson, `course_prerequisites` stores a course and the course that must precede it:

| course_id | prerequisite_id | Meaning |
|---:|---:|---|
| 103 | 101 | Data Basics follows AI Foundations |
| 104 | 101 | Python Basics follows AI Foundations |
| 105 | 103 | SQL Basics follows Data Basics |

Course 102 has no relationship in this small prerequisite table. Starting from course 101, we want to find its directly reachable courses, and then the courses reachable from those. The arrows are **101 → 103 → 105** and **101 → 104**. The numeric IDs identify courses; they are not the number of learning steps.

```sql
WITH RECURSIVE path(course_id, depth) AS (
    SELECT course_id, 0
    FROM course_catalogue
    WHERE course_id = 101

    UNION ALL

    SELECT edge.course_id, path.depth + 1
    FROM course_prerequisites AS edge
    JOIN path ON edge.prerequisite_id = path.course_id
    WHERE path.depth < 2
)
SELECT path.course_id, c.title, path.depth
FROM path
JOIN course_catalogue AS c ON c.course_id = path.course_id
ORDER BY path.depth, path.course_id;
```

`WITH RECURSIVE` announces the recursive query. `path(course_id, depth)` gives names to its two result columns. The first `SELECT` is the **anchor query**: it selects the starting course 101 at depth 0. The second `SELECT` is the **recursive member**: for each reachable course ID, it finds rows in `course_prerequisites` whose `prerequisite_id` is that ID and returns the dependent course at the next depth. `UNION ALL` connects anchor and recursive member; a later lesson compares set operations in general. Here it means that generated path rows are included without automatic duplicate removal.

The stopping condition `WHERE path.depth < 2` lets depth-0 rows produce depth-1 rows and depth-1 rows produce depth-2 rows. Depth-2 rows cannot produce a next level in this query. This is a **recursive CTE** because the recursive member names `path` in its own `JOIN`.

## Trace the anchor and each recursive step

| Step | Input available to expand | Prerequisite edge followed | New `(course_id, depth)` |
|---|---|---|---|
| Anchor | Starting course 101 | None | `(101, 0)` |
| First expansion | 101 | 101 → 103 and 101 → 104 | `(103, 1)`, `(104, 1)` |
| Second expansion | 103 and 104 | 103 → 105; no edge from 104 | `(105, 2)` |
| Stop | 105 at depth 2 | Depth bound prevents another expansion | None |

The final sorted result is:

| course_id | title | depth |
|---:|---|---:|
| 101 | AI Foundations | 0 |
| 103 | Data Basics | 1 |
| 104 | Python Basics | 1 |
| 105 | SQL Basics | 2 |

Depth is the number of prerequisite links from the selected starting course, not a duration or difficulty measure. The outer `ORDER BY path.depth, path.course_id` sets the display order. Do not rely on the internal order in which the recursive query visits branches for the displayed sequence.

The anchor matters. Starting from course **103** at depth 0 finds 105 at depth 1; it does not find 101, because the edges run from a prerequisite to courses that depend on it. Starting from an ID absent from `course_catalogue` gives no anchor row and therefore an empty result. A wrong join direction such as `edge.course_id = path.course_id` walks toward prerequisites rather than dependents and answers a different question.

## Stop recursion deliberately

In this small dataset, the prerequisite edges form a simple branch with no cycle. Real relationship data may contain a cycle. Imagine adding `course_id = 101, prerequisite_id = 105`: following dependent links from 101 can eventually return to 101. With `UNION ALL`, the same course can then appear again at another depth. The lab's checker adds this edge to a **separate fresh in-memory copy** and uses maximum depth 3. It observes course 101 at depth 0 and again at depth 3, then stops because of the depth bound.

The depth condition makes this particular query finite, but it does **not** promise each course appears only once. In a general graph, several different paths could reach the same course even without a cycle. If the product needs each course once, you must design a rule for repeated visits and cycles; do not assume `UNION ALL` removes them. Even changing to `UNION` is not a complete fix when `depth` is part of the row, because `(101, 0)` and `(101, 3)` are different result rows. The course prerequisite example is intentionally small so you can inspect all edges and enforce the depth bound yourself.

## Guided lab: predict, run, change, diagnose

Download the [common table expressions lab](QAI.02.01.24_Common_Table_Expressions_Lab.zip), unzip it, and run from its folder:

```sh
python cte_examples.py
python check_cte_examples.py
```

Use `python3` if needed. The standard-library `sqlite3` module builds private in-memory tables. The first program prints:

```text
Long courses: [(101, 'AI Foundations'), (103, 'Data Basics'), (105, 'SQL Basics')]
Multiple CTE summary: (3, 245)
Root 101 through depth 2: [(101, 'AI Foundations', 0), (103, 'Data Basics', 1), (104, 'Python Basics', 1), (105, 'SQL Basics', 2)]
Root 103 through depth 2: [(103, 'Data Basics', 0), (105, 'SQL Basics', 1)]
Root 101 through depth 1: [(101, 'AI Foundations', 0), (103, 'Data Basics', 1), (104, 'Python Basics', 1)]
Stored tables unchanged: True
```

Predict the named-query rows and the recursive depth trace before running. Change `long_courses(db)` and `multiple_ctes(db)` to use boundary 80 in a copy: predict long-course IDs **101, 103** and summary `(2, 175)`. Change `path_from(db, 101, 2)` to `path_from(db, 101, 1)` and predict that 105 disappears while 101, 103, and 104 remain. Restore the original calls after recording your results. The Python helper binds the root ID, depth, and threshold using `?` data placeholders.

**Reproduce and repair a failure:** keep the depth bound intact, but reverse the edge comparison in a copy of the recursive query to `edge.course_id = path.course_id`. Starting at 101, this looks for a row whose *dependent* course ID is 101; there is none, so only the anchor row appears. Restore `edge.prerequisite_id = path.course_id` and verify all four expected path rows. The checker also adds the cyclic edge `105 → 101` to a separate fresh database and verifies that the bounded query repeats `(101, 'AI Foundations', 3)` and stops. Do not remove the depth bound while experimenting with a cycle.

The checker also verifies that an ordinary CTE name is not available in a later statement, that an unknown anchor returns no rows, and that the base tables are unchanged by these reads. Its successful run verifies the included examples; compare your own changed query with the predicted rows.

## Mini-project: a bounded course learning path

Make a course-path report rooted at **AI Foundations (101)**. Include the root at depth 0 and courses reachable by following prerequisite links through **depth 2**. Return course ID, title, and depth, sorted by depth then ID. Expected rows are `(101, 'AI Foundations', 0)`, `(103, 'Data Basics', 1)`, `(104, 'Python Basics', 1)`, and `(105, 'SQL Basics', 2)`. Course 102 is not connected to this root.

**Reference solution:**

```sql
WITH RECURSIVE path(course_id, depth) AS (
    SELECT course_id, 0
    FROM course_catalogue WHERE course_id = 101
    UNION ALL
    SELECT edge.course_id, path.depth + 1
    FROM course_prerequisites AS edge
    JOIN path ON edge.prerequisite_id = path.course_id
    WHERE path.depth < 2
)
SELECT path.course_id, c.title, path.depth
FROM path JOIN course_catalogue AS c ON c.course_id = path.course_id
ORDER BY path.depth, path.course_id;
```

The lab's `path_from(db, 101, 2)` implements the same rule with bound parameters. Check both branches at depth 1 and the single depth-2 continuation. With maximum depth 1, the result should have exactly the first three rows. If 105 appears at depth 1, inspect the edge direction and whether you counted links correctly.

**Independent variation:** root the same bounded query at **Data Basics (103)** and follow dependents through depth 2. Predict before looking at the reference: `(103, 'Data Basics', 0)` followed by `(105, 'SQL Basics', 1)`. No other dependent edge leaves 105 in the original data.

```sql
WITH RECURSIVE path(course_id, depth) AS (
    SELECT course_id, 0
    FROM course_catalogue WHERE course_id = 103
    UNION ALL
    SELECT edge.course_id, path.depth + 1
    FROM course_prerequisites AS edge
    JOIN path ON edge.prerequisite_id = path.course_id
    WHERE path.depth < 2
)
SELECT path.course_id, c.title, path.depth
FROM path JOIN course_catalogue AS c ON c.course_id = path.course_id
ORDER BY path.depth, path.course_id;
```

The lab's `path_from(db, 103, 2)` is the reference after your own attempt. Preserve your prediction, query, observed result, and an explanation of why the root has depth 0 and its dependent has depth 1. For a transfer check, root at course 102: only `(102, 'Git Basics', 0)` appears because no prerequisite edge lists 102 as a prerequisite.

## Diagnose a CTE mismatch

| Symptom | Cause to inspect | Repair |
|---|---|---|
| `no such table: long_courses` in a later statement | The CTE name belonged only to the preceding SQL statement | Put its `WITH` definition and consuming query in the same statement |
| Summary includes a short course | First CTE's threshold is wrong or second CTE reads the base table | Inspect intermediate IDs and ensure the second reads `long_courses` |
| Path omits root 101 | Anchor query does not select the root | Check its ID and return depth 0 from the anchor |
| Path reaches parents rather than dependents | Recursive edge equality faces the wrong direction | Match `edge.prerequisite_id` to the current `path.course_id` |
| Path stops before depth 2 | `WHERE path.depth < 1` or another overly small bound | Check depth values generated from the anchor |
| A course appears repeatedly | Cycle or several paths reach it; `UNION ALL` retains generated rows | Inspect edges and the depth bound; define repeated-visit handling if unique courses are required |
| A recursive query does not finish | No effective stopping rule for cyclic data | Do not run an unbounded cyclic example; restore a safe depth bound and inspect the relationship |

## Check your understanding

1. What does `WITH long_courses AS (...)` make available, and for how long?
2. Which courses meet the 70-minute boundary? What happens at 80?
3. In the two-CTE example, which named result does `duration_summary` read?
4. Which part of the recursive CTE is the anchor query, and what does it produce?
5. What does the recursive member do for path row `(103, 1)`?
6. Why does the depth-2 result include 105 but the depth-1 result exclude it?
7. Why can a depth bound stop a cycle without guaranteeing unique course IDs?

**Answers and reasoning**

1. It names the filtered query result for use in the **same SQL statement**. It is not a permanent table.
2. At least 70 gives **101, 103, 105**; at least 80 gives **101, 103**.
3. It reads `long_courses`, calculates the count and sum, and passes `(3, 245)` to the final `SELECT`.
4. `SELECT course_id, 0 FROM course_catalogue WHERE course_id = 101`; it produces `(101, 0)`.
5. It follows `prerequisite_id = 103` to course 105 and produces `(105, 2)`.
6. 105 is two links away, 101 → 103 → 105, so the stricter depth bound stops before it appears.
7. The bound limits the maximum number of links, but a course can be reached again before that limit through a cycle or another path.

## Remember and retain

- A CTE is a named query introduced by `WITH`; its name is available for one statement. Multiple CTEs can be defined together and later ones can read earlier ones.
- A recursive CTE combines an anchor query with a recursive member that refers to the named result. Trace the root at depth 0, then each edge and increasing depth.
- Include a finite stopping condition for bounded traversal. `UNION ALL` can retain repeated path rows; depth alone does not make IDs unique.
- Keep the ordinary CTE boundary trace, two-CTE summary, anchor/member trace, corrected direction or cycle diagnosis, mini-project path, and independent root variation.

## Further reading

- [SQLite: ordinary and recursive common table expressions](https://www.sqlite.org/lang_with.html)
- [SQLite: SELECT](https://www.sqlite.org/lang_select.html)
- [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)
