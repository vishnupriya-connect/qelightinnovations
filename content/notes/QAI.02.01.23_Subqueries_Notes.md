# Subqueries

## Let one query supply values to another

A **subquery** is a `SELECT` written inside another SQL statement. The containing statement is the **outer query**; the contained `SELECT` is the **inner query**. Its **subquery result** can be one value, a set of values, or an answer to whether matching rows exist.

Use these small tables from the join lessons:

| course_id | title | instructor_id | duration_minutes |
|---:|---|---:|---:|
| 101 | AI Foundations | 7 | 95 |
| 102 | Git Basics | 8 | 50 |
| 103 | Data Basics | 7 | 80 |
| 104 | Python Basics | 8 | 65 |
| 105 | SQL Basics | 42 | 70 |

| instructor_id | instructor_name |
|---:|---|
| 7 | Asha |
| 8 | Ben |
| 9 | Cora |

| course_id | tag |
|---:|---|
| 101 | starter |
| 101 | featured |
| 102 | starter |
| 104 | starter |

The course with instructor key 42 has no instructor row. Courses 103 and 105 have no tag row. These facts matter when you test presence and absence with subqueries. The lab uses an in-memory SQLite database; all statements in this lesson read data and leave the source tables unchanged.

## Scalar subquery: supply one value

A **scalar subquery** is used where one value is needed. First calculate the average duration by itself:

```sql
SELECT AVG(duration_minutes) FROM course_catalogue;
```

It returns **72.0** because `(95 + 50 + 80 + 65 + 70) / 5 = 72`. Then use that value as the comparison boundary in an outer query:

```sql
SELECT c.course_id, c.duration_minutes
FROM course_catalogue AS c
WHERE c.duration_minutes >
      (SELECT AVG(duration_minutes) FROM course_catalogue)
ORDER BY c.course_id;
```

The **inner query** supplies 72.0. The **outer query** compares each course against it and returns `(101, 95)` and `(103, 80)`. Course 105 at 70 is below the average. Parentheses mark the inner query. This particular inner query makes one aggregate value for the whole table; it does not refer to `c` and is **uncorrelated**.

Make a scalar subquery return one meaningful value deliberately. In SQLite, a scalar subquery with no row gives SQL `NULL`; one that unexpectedly returns several rows yields the first row's value, which can conceal a mistake. For example, an unknown instructor ID in `(SELECT instructor_name FROM instructors WHERE instructor_id = 99)` supplies `NULL`. If you intend an average, use `AVG`; if you intend a particular row, identify it precisely rather than relying on an arbitrary first value. Other database systems can reject a multi-row result used as a scalar, so a query that silently works in SQLite is not a reliable general pattern.

## Multi-row subquery: test membership

A **multi-row subquery** can return several values for an `IN` test. Ask for courses whose instructor appears among instructors named Asha or Cora:

```sql
SELECT c.course_id, c.title
FROM course_catalogue AS c
WHERE c.instructor_id IN
      (SELECT i.instructor_id
       FROM instructors AS i
       WHERE i.instructor_name IN ('Asha', 'Cora'))
ORDER BY c.course_id;
```

The inner result is the one-column set **7, 9**. The outer result has courses **101 and 103**, both with instructor key 7. Cora has no course, so key 9 contributes no outer row. Course 105's key 42 does not occur in the inner set. The inner query can return zero, one, or many rows; for this `IN` comparison it must supply a suitable single column of values. An inner query returning duplicate key 7 would not duplicate an outer course in this membership test.

Do not interchange `IN` and `NOT IN` carelessly when the inner result can contain SQL `NULL`. As in the filtering lesson, a missing candidate can turn an unmatched `NOT IN` comparison into unknown. If you need to find rows without matching related records, a correlated `NOT EXISTS` query often states that intent more directly.

## Correlated subquery: test each outer row

A **correlated subquery** refers to a column from the current outer row. To find courses with a `starter` tag:

```sql
SELECT c.course_id, c.title
FROM course_catalogue AS c
WHERE EXISTS
      (SELECT 1
       FROM course_tags AS t
       WHERE t.course_id = c.course_id
         AND t.tag = 'starter')
ORDER BY c.course_id;
```

`EXISTS` asks whether the inner query finds **at least one row** for the current `c.course_id`. The result is **101, 102, 104**. The `SELECT 1` is conventional: `EXISTS` is concerned with the presence of rows, not with the value 1. Course 101 has both `starter` and `featured` tags, but `EXISTS` includes its outer row **once**, not once per matching tag.

| Outer course | Matching `starter` row? | Included? |
|---:|---|---|
| 101 | Yes | Yes |
| 102 | Yes | Yes |
| 103 | No tag row | No |
| 104 | Yes | Yes |
| 105 | No tag row | No |

The condition `t.course_id = c.course_id` is the correlation: `t` belongs to the inner query and `c` to the outer query. Read it as “Does this particular course have a matching tag?” If you omit that equality, the inner query finds *some* `starter` row in the table and its `EXISTS` result is true for **all five** outer courses. The SQL still runs but answers the wrong question. Trace at least one tagged and one untagged course to catch the error.

Use `NOT EXISTS` to request courses with **no tag rows at all**:

```sql
SELECT c.course_id, c.title
FROM course_catalogue AS c
WHERE NOT EXISTS
      (SELECT 1 FROM course_tags AS t
       WHERE t.course_id = c.course_id)
ORDER BY c.course_id;
```

The result is **103, 105**. Course 101 is excluded even though it has two tags: the existence of any matching row is enough. The lack of a tag is different from a tag row whose `tag` field might be `NULL`; in this lab, `course_tags.tag` is required to be non-null. `EXISTS` and `NOT EXISTS` are tests on the *presence of inner rows*.

An **uncorrelated subquery** does not refer to the outer row. For example, `EXISTS (SELECT 1 FROM instructors WHERE instructor_id = 9)` is true for every course here because Cora exists. If you put it in an outer course `WHERE`, **all five** courses appear. The database is free to plan correlated and uncorrelated queries differently; the useful distinction for reading the SQL is whether the inner answer depends on the current outer row.

## Nested query: put a subquery inside another subquery

A **nested query** can have more than one level. Here we first find instructor keys associated with courses lasting at least 80 minutes, then keep existing instructor rows with those keys, then find all courses taught by those instructors:

```sql
SELECT c.course_id
FROM course_catalogue AS c
WHERE c.instructor_id IN
      (SELECT i.instructor_id
       FROM instructors AS i
       WHERE i.instructor_id IN
             (SELECT x.instructor_id
              FROM course_catalogue AS x
              WHERE x.duration_minutes >= 80))
ORDER BY c.course_id;
```

The deepest query sees course IDs 101 and 103, both with instructor key 7, so it yields key 7 (possibly twice). The middle query finds existing instructor key 7. The outer query returns courses **101, 103**. Work from the deepest result outward, naming which column each layer returns. This example uses nested membership checks to make the levels visible; a different formulation might be shorter for a real application.

## `ANY` and `ALL`: quantify a comparison

Some SQL systems support comparison with a subquery using **`ANY`** and **`ALL`**. Their meaning is worth learning even though **SQLite does not implement the literal `> ANY (SELECT ...)` or `> ALL (SELECT ...)` syntax**. The following two examples are conceptual SQL for systems that support quantified comparisons, such as PostgreSQL; do not paste them into the SQLite lab:

```sql
-- In a system that supports quantified comparisons:
c.duration_minutes > ANY
    (SELECT duration_minutes FROM course_catalogue WHERE instructor_id = 8)

c.duration_minutes > ALL
    (SELECT duration_minutes FROM course_catalogue WHERE instructor_id = 8)
```

Instructor 8's durations are **50 and 65**, both present numeric values. “Greater than **ANY**” means greater than **at least one** of them; “greater than **ALL**” means greater than **every** one. A course lasting exactly 65 is above 50 but is not above 65.

| Course | Duration | `> ANY (50, 65)`? | `> ALL (50, 65)`? |
|---:|---:|---|---|
| 101 | 95 | Yes | Yes |
| 102 | 50 | No | No |
| 103 | 80 | Yes | Yes |
| 104 | 65 | Yes | No |
| 105 | 70 | Yes | Yes |

The SQLite lab expresses the same *truth conditions for these non-null durations* with correlated existence tests. For “greater than at least one”:

```sql
SELECT c.course_id
FROM course_catalogue AS c
WHERE EXISTS
      (SELECT 1 FROM course_catalogue AS peer
       WHERE peer.instructor_id = 8
         AND c.duration_minutes > peer.duration_minutes)
ORDER BY c.course_id;
```

This returns **101, 103, 104, 105**. For “greater than every”, look for the **absence of a counterexample**, a peer duration greater than or equal to the course's duration:

```sql
SELECT c.course_id
FROM course_catalogue AS c
WHERE NOT EXISTS
      (SELECT 1 FROM course_catalogue AS peer
       WHERE peer.instructor_id = 8
         AND c.duration_minutes <= peer.duration_minutes)
ORDER BY c.course_id;
```

This returns **101, 103, 105**. In the lesson table, `duration_minutes` is `NOT NULL`, so every comparison of two durations is true or false. If either side could be `NULL`, an ordinary `<=` inside `NOT EXISTS` might be unknown instead of identifying a counterexample, and quantified comparisons have additional unknown-result rules. Decide how missing numbers should behave before treating this rewrite as generally equivalent.

An empty inner set distinguishes the quantifiers: `> ANY (empty set)` is false, while `> ALL (empty set)` is true because there is no counterexample. For example, instructor 99 has no courses. In the SQLite equivalents above, replacing instructor 8 with 99 returns **no IDs** for `EXISTS` and **all five IDs** for `NOT EXISTS`. This is not a database error; it follows the stated “at least one” and “every” meanings.

## Guided lab: predict, run, vary, repair

Download the [subqueries lab](QAI.02.01.23_Subqueries_Lab.zip), unzip it, and run both programs from its folder:

```sh
python subqueries.py
python check_subqueries.py
```

Use `python3` if needed. The Python standard-library `sqlite3` module builds private in-memory tables. The first program prints:

```text
Average duration: 72.0
Above average: [101, 103]
Instructors Asha or Cora: [101, 103]
Starter tag EXISTS: [101, 102, 104]
No tags NOT EXISTS: [103, 105]
Nested selection: [101, 103]
Greater than ANY instructor-8 duration: [101, 103, 104, 105]
Greater than ALL instructor-8 durations: [101, 103, 105]
Project candidates: [(101, 'AI Foundations', 95)]
Independent variation: [103, 105]
Stored tables unchanged: True
```

The two `ANY`/`ALL` print labels describe the **meaning** of executable SQLite `EXISTS`/`NOT EXISTS` statements; the program does not execute literal `ANY`/`ALL`. The checker deliberately attempts that syntax, verifies SQLite rejects it, and checks the working SQLite versions of the rules.

**Controlled change:** call `greater_than_any_peer(db, 99)` and `greater_than_all_peers(db, 99)` in a copy. Predict `[]` and `[101, 102, 103, 104, 105]` before running. Restore 8 after explaining the empty-set difference. The helper binds the instructor ID with `?` rather than inserting it into SQL text.

**Reproduce and repair a logic failure:** remove `t.course_id = c.course_id` from the `starter` query, keeping `t.tag = 'starter'`. It still finds a starter row, so the outer query incorrectly returns **all five** courses. Restore the correlation and confirm the correct three. The checker validates the provided functions, including the nested, scalar, and multi-row examples, but your own changed statement needs its own comparison against expected IDs.

## Mini-project: above-average starter courses

A course planner wants courses whose duration is **above the average of all five courses** and that have a `starter` tag. Return ID, title, and duration in ID order. First calculate the global average, **72.0**. Above it are course 101 (95) and 103 (80). Only 101 has a `starter` tag, so the expected row is `(101, 'AI Foundations', 95)`.

**Reference solution:**

```sql
SELECT c.course_id, c.title, c.duration_minutes
FROM course_catalogue AS c
WHERE c.duration_minutes >
      (SELECT AVG(duration_minutes) FROM course_catalogue)
  AND EXISTS
      (SELECT 1 FROM course_tags AS t
       WHERE t.course_id = c.course_id AND t.tag = 'starter')
ORDER BY c.course_id;
```

The scalar subquery supplies the single global threshold; the correlated `EXISTS` tests each course's tags. The lab's `project_candidates()` is the reference. Acceptance checks: course 103 exceeds the average but has no tag; course 104 has the tag but is below the average; course 101 meets both. Because course 101 also has a `featured` tag, a join on all tags without restricting the tag could accidentally return it more than once; the existence test still returns the outer course once.

**Independent variation:** return IDs of courses with **no tags** that last longer than **every instructor-8 course**. Use two `NOT EXISTS` tests: no tag row for this course, and no instructor-8 course with a duration greater than or equal to this course's duration. Instructor 8 has durations 50 and 65. Untagged courses 103 (80) and 105 (70) both exceed them, so expected IDs are **103, 105**. Attempt the query before inspecting this reference:

```sql
SELECT c.course_id
FROM course_catalogue AS c
WHERE NOT EXISTS
      (SELECT 1 FROM course_tags AS t
       WHERE t.course_id = c.course_id)
  AND NOT EXISTS
      (SELECT 1 FROM course_catalogue AS peer
       WHERE peer.instructor_id = 8
         AND c.duration_minutes <= peer.duration_minutes)
ORDER BY c.course_id;
```

The lab's `independent_variation()` provides the same reference. Course 101 is long enough but has tags; course 104 has a tag and also fails the strict `> 65` boundary. Save your prediction, SQL, actual IDs, and one trace of a rejected course. If your query returns all five, inspect each correlation to the current `c` row.

## Diagnose a subquery result

| Symptom | Likely cause | Repair |
|---|---|---|
| Scalar comparison has an unexpected boundary | Inner query returned the wrong aggregate or an unintended first row | Run the inner `SELECT` alone and verify its single value |
| Every course passes an `EXISTS` test | Forgot `t.course_id = c.course_id` | Link the inner condition to the current outer row and test an untagged course |
| An outer course repeats after looking up tags | Used a join that yields a row for each tag rather than an existence test | Decide whether the question is about tag rows or one answer per course |
| Missing-tag search finds tagged courses | Negation or correlation is wrong | Trace whether any inner tag row can match each course; use `NOT EXISTS` |
| SQLite reports an error near `ANY` or `ALL` | Literal quantified syntax is unsupported in SQLite | Use the demonstrated existence/counterexample form for non-null inputs |
| “Greater than all” includes every course when instructor 99 has no rows | Empty comparison set has no counterexample | Confirm whether the intended policy should treat an empty set as satisfying “all” |
| A `NOT IN` absence check excludes unexpected rows | Inner result contains `NULL` | Inspect missing values and express the relationship with `NOT EXISTS` where appropriate |

## Check your understanding

1. Which part is the outer query in the above-average example, and what value does the scalar inner query supply?
2. What instructor IDs does the Asha-or-Cora subquery produce? Which course IDs pass the outer `IN`?
3. Which reference makes the starter-tag `EXISTS` query correlated?
4. Why does course 101 appear once under `EXISTS` although it has two tag rows?
5. Which IDs are returned by the no-tag `NOT EXISTS` query?
6. For instructor-8 durations 50 and 65, why does course 104 satisfy “greater than any” but not “greater than all”?
7. What happens to the `ANY` and `ALL` meanings for an empty comparison set? Can literal quantified syntax run in this SQLite lab?

**Answers and reasoning**

1. The outer `SELECT c.course_id, c.duration_minutes ...` checks each course; the inner `AVG` supplies **72.0**.
2. The inner values are **7 and 9**; the outer course IDs are **101 and 103**, both matching key 7.
3. `t.course_id = c.course_id` refers to the outer row `c` from within the inner tag query.
4. `EXISTS` tests whether at least one qualifying inner row exists; it does not add one outer row per inner match.
5. **103 and 105**, because no row in `course_tags` refers to either course.
6. Its 65 is above 50 but not above 65; the latter comparison fails the “every” requirement.
7. `ANY` is false and `ALL` true for an empty set. SQLite does not run the literal `> ANY` or `> ALL` syntax; the lab runs the corresponding non-null `EXISTS` forms.

## Remember and retain

- A subquery supplies a result to an outer query. Trace the inner answer and then its use by each outer row.
- A scalar subquery supplies one value; a multi-row subquery can supply candidates for `IN`; deeper nesting can be read from the inside out.
- A correlated subquery refers to the current outer row. `EXISTS` checks for a matching inner row; `NOT EXISTS` checks that none exists.
- `ANY` means at least one comparison succeeds; `ALL` means every comparison succeeds. SQLite lacks their literal quantified syntax, so this lab uses existence tests with explicitly non-null durations.
- Keep the average trace, missing-correlation repair, empty-set prediction, mini-project query, and independent no-tag comparison for later review.

## Further reading

- [SQLite: subquery and EXISTS expressions](https://www.sqlite.org/lang_expr.html)
- [PostgreSQL: quantified subquery comparisons (`ANY` and `ALL`)](https://www.postgresql.org/docs/current/functions-subquery.html)
- [Python: sqlite3](https://docs.python.org/3/library/sqlite3.html)
