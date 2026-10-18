# Special filtering conditions

## Start with a familiar catalogue

Our course catalogue still has four courses. A new `topic_note` column may contain a short description or a missing SQL value, `NULL`:

| course_id | title | instructor_id | duration_minutes | lesson_count | topic_note |
|---:|---|---:|---:|---:|---|
| 101 | AI Foundations | 7 | 95 | 4 | intro |
| 102 | Git Basics | 8 | 50 | 3 | `NULL` |
| 103 | Data Basics | 7 | 80 | 4 | tables |
| 104 | Python Basics | 8 | 65 | 3 | `NULL` |

The preceding lesson used comparisons, `AND`, `OR`, `NOT`, and parentheses. This lesson adds compact ways to ask whether a value is in a group, inside a range, shaped like a text pattern, or missing. Every example uses `ORDER BY course_id` to make its displayed row order predictable. Filtering does not change the stored catalogue.

## Membership: `IN` and `NOT IN`

A **membership condition** checks whether a value belongs to a set of candidate values. Use `IN` for the included IDs:

```sql
SELECT course_id, title
FROM course_catalogue
WHERE course_id IN (101, 104)
ORDER BY course_id;
```

The rows are `(101, 'AI Foundations')` and `(104, 'Python Basics')`. The list contains two possible values; each row is included once if its ID matches either. `course_id = 101 OR course_id = 104` expresses the same rule for this nonmissing ID column.

Use `NOT IN` to request IDs outside a list:

```sql
SELECT course_id
FROM course_catalogue
WHERE course_id NOT IN (101, 104)
ORDER BY course_id;
```

The result is **102, 103**. The tested `course_id` values are never `NULL` in this table. If a membership list can contain `NULL`, `NOT IN` needs extra care. For example, `course_id NOT IN (101, NULL)` returns **no rows** here: row 101 is a known match and thus fails `NOT IN`; for every other ID, the unresolved comparison with `NULL` makes the result unknown, which `WHERE` excludes. Remove missing candidates before constructing the list or decide explicitly how they should affect the rule. `NOT IN` is not a general test for missing values.

When IDs come from program input, bind each candidate to a placeholder:

```python
db.execute(
    "SELECT course_id FROM course_catalogue "
    "WHERE course_id IN (?, ?) ORDER BY course_id",
    (101, 104),
).fetchall()
```

Each `?` stands for **one value**. The number of placeholders must agree with the number of supplied values; passing a single comma-separated string does not turn it into two IDs.

## Range: `BETWEEN` includes both ends

A **range condition** tests whether a value falls between a lower and upper boundary. In this catalogue:

```sql
SELECT course_id, duration_minutes
FROM course_catalogue
WHERE duration_minutes BETWEEN 50 AND 80
ORDER BY course_id;
```

The results are `(102, 50)`, `(103, 80)`, and `(104, 65)`. `BETWEEN 50 AND 80` includes **50 and 80**. For these nonmissing numeric values it asks the same question as `duration_minutes >= 50 AND duration_minutes <= 80`.

| Course | Duration | At least 50? | At most 80? | Selected? |
|---:|---:|---|---|---|
| 101 | 95 | Yes | No | No |
| 102 | 50 | Yes | Yes | Yes; lower boundary |
| 103 | 80 | Yes | Yes | Yes; upper boundary |
| 104 | 65 | Yes | Yes | Yes; inside range |

If the rule excludes both endpoints, use `duration_minutes > 50 AND duration_minutes < 80`: only course **104** qualifies. The word `AND` inside `BETWEEN 50 AND 80` separates the range's two bounds; when you add another filter, write it as an additional condition, for example `WHERE duration_minutes BETWEEN 50 AND 80 AND instructor_id = 8`. That returns **102, 104**.

**Controlled variation:** change the bounds to `BETWEEN 51 AND 79`. Predict that 102 and 103 disappear while 104 stays. If lower and upper bounds are reversed, do not expect the database to swap them: for this catalogue, `BETWEEN 80 AND 50` returns no rows.

## Patterns: `LIKE` and its two wildcards

A **pattern condition** matches the shape of text rather than one complete text value. SQL's `LIKE` operator uses two **wildcards** in its pattern:

| Pattern symbol | Meaning | Example using the catalogue |
|---|---|---|
| `%` (**percent wildcard**) | Any sequence of zero or more characters | `Data%` matches `Data Basics` |
| `_` (**underscore wildcard**) | Exactly one character | `Git Basic_` matches `Git Basics` |

The literal letters and spaces still have to occur in the specified positions. Do not read `%` as “one or more”: it can match **zero** characters too. A `LIKE` pattern without a wildcard still tests the entire text shape, though use `=` when you mean exact equality. Examples below use plain ASCII letters so their behavior is easy to reproduce in SQLite; case matching and collation can vary between database systems and configurations.

### Prefix match: text begins with a phrase

Put `%` after a known beginning:

```sql
SELECT course_id FROM course_catalogue
WHERE title LIKE 'Data%'
ORDER BY course_id;
```

The **prefix match** returns **103**. `Data` is fixed at the start; `%` permits the remaining ` Basics`.

### Suffix match: text ends with a phrase

Put `%` before a known ending:

```sql
SELECT course_id FROM course_catalogue
WHERE title LIKE '%Basics'
ORDER BY course_id;
```

The **suffix match** returns **102, 103, 104**. It includes different beginnings (`Git`, `Data`, `Python`) followed by `Basics`.

### Substring match: text contains a phrase

Put `%` on both sides:

```sql
SELECT course_id FROM course_catalogue
WHERE title LIKE '%Basic%'
ORDER BY course_id;
```

The **substring match** also returns **102, 103, 104** for this dataset. The two queries happen to agree here; they ask different questions. If a title were `Basic Tools`, `%Basic%` would include it while `%Basics` would not.

The underscore tests a different shape:

```sql
SELECT course_id FROM course_catalogue
WHERE title LIKE 'Git Basic_'
ORDER BY course_id;
```

This returns **102**, since `s` fills the single `_` position. `Git Basic__` returns no rows because there are not two characters after `Git Basic`. The pattern `Git Basic` also returns no rows: it lacks the final `s`. When accepting a user's search phrase, bind it as a parameter; if the phrase may contain literal `%` or `_`, decide how to escape them rather than silently treating them as wildcard instructions.

## Missing values: `IS NULL` and `IS NOT NULL`

A **null condition** asks whether a field has the SQL missing value. `NULL` is not the text `'NULL'`, and it is not the empty string `''`. In the sample data, course 102 has a missing topic note, not a note containing those four letters.

```sql
SELECT course_id FROM course_catalogue
WHERE topic_note IS NULL
ORDER BY course_id;
```

`IS NULL` returns **102, 104**. Its counterpart asks for present values:

```sql
SELECT course_id FROM course_catalogue
WHERE topic_note IS NOT NULL
ORDER BY course_id;
```

`IS NOT NULL` returns **101, 103**. The note may be any present value; this condition does not require the text to match a particular phrase. If your data contains empty strings as well as `NULL`, `IS NOT NULL` still includes those empty strings: “present” and “nonempty” are different policies.

Do not try `topic_note = NULL` to find missing notes. An ordinary comparison to `NULL` evaluates to unknown here, so `WHERE topic_note = NULL` returns **no rows**, despite two missing notes. Similarly, `topic_note <> NULL` does not find present notes. Use `IS NULL` and `IS NOT NULL` and check the resulting IDs.

| Question | Condition | IDs in this catalogue |
|---|---|---|
| Which notes are missing? | `topic_note IS NULL` | 102, 104 |
| Which notes are present? | `topic_note IS NOT NULL` | 101, 103 |
| Which notes equal SQL `NULL` by ordinary equality? | `topic_note = NULL` | None; comparison is unknown |

## Guided lab: predict, run, change, repair

Download the [special filtering lab](QAI.02.01.14_Special_Filtering_Lab.zip), unzip it, and run from that folder:

```sh
python special_filters.py
python check_special_filters.py
```

Use `python3` if needed. Both programs use only Python's standard `sqlite3` module and a temporary in-memory table. The first prints:

```text
IN 101, 104: [101, 104]
NOT IN 101, 104: [102, 103]
BETWEEN 50 and 80: [102, 103, 104]
Prefix Data: [103]
Suffix Basics: [102, 103, 104]
Substring Basic: [102, 103, 104]
One-character ending: [102]
Missing notes: [102, 104]
Present notes: [101, 103]
Project rows: [(102, 'Git Basics'), (104, 'Python Basics')]
Independent variation: [101, 103]
Stored rows unchanged: True
```

Before you run it, predict which rows the exact `BETWEEN` endpoints include, then verify the printed result. Next, change the `BETWEEN` call in `main()` from `(50, 80)` to `(51, 79)`: its output should become `[104]`. Change the `LIKE` pattern `"Git Basic_"` to `"Git Basic__"`; its output should become `[]`. Restore the original values after recording what changed.

**Reproduce and repair a real mistake:** in your own copy, query `topic_note = NULL`. It runs but returns `[]`; compare it to the two visually missing notes, then repair it to `topic_note IS NULL` and check for `[102, 104]`. Try `course_id NOT IN (101, NULL)` and observe `[]`; replace the missing list item with 104 and check for `[102, 103]`. The checker covers these failures, endpoint distinctions, all three pattern shapes, and the reference project. Its successful run confirms the included examples; still test your own edits and explain any difference.

## Mini-project: find courses awaiting topic notes

The catalogue editor wants **Basics** courses that have **no topic note** and last **from 50 through 65 minutes, including both endpoints**. Return each matching course's ID and title in ID order. Before writing SQL, trace the four rows: course 102 qualifies at 50; course 104 qualifies at 65; course 103 has a note and lasts 80; course 101 is not a Basics course. Expected rows: `(102, 'Git Basics')`, `(104, 'Python Basics')`.

**Reference solution:**

```sql
SELECT course_id, title
FROM course_catalogue
WHERE title LIKE '%Basics'
  AND topic_note IS NULL
  AND duration_minutes BETWEEN 50 AND 65
ORDER BY course_id;
```

The lab's `selected_courses()` runs the same rule with the pattern and bounds passed as values. The three conditions are all required. If you accidentally write `topic_note = NULL`, no row passes. If you accidentally replace `BETWEEN 50 AND 65` with `> 50 AND < 65`, both qualifying boundary rows disappear. Trace those boundary failures before changing other parts of the query.

**Independent variation:** return IDs of courses lasting from **65 through 95 minutes**, including both endpoints, **whose topic notes are present**. Predict from the table, write your own query, then compare with this reference:

```sql
SELECT course_id
FROM course_catalogue
WHERE duration_minutes BETWEEN 65 AND 95
  AND topic_note IS NOT NULL
ORDER BY course_id;
```

Expected IDs are **101, 103**. Course 104 is at the lower boundary but is missing a note; course 102 is below the range and missing a note. For evidence you can keep, write down your predicted IDs, your query, its actual IDs, an explanation of one included boundary and one excluded row, and the fixed query if your first attempt differed. The included `independent_variation()` is a reference to compare **after** attempting your own statement.

## Diagnose a mismatch

| Symptom | Likely cause | Check and repair |
|---|---|---|
| Course 102 or 103 vanishes from a 50–80 range | Used strict comparisons | Use `BETWEEN 50 AND 80` for inclusive boundaries; check both exact endpoints |
| A `%Basics` query matches too much or too little | `%` was placed on the wrong side, or a literal `%` was treated as a wildcard | State whether you want prefix, suffix, or substring; inspect the pattern character by character |
| `Git Basic_` and `Git Basic__` appear identical | `_` was read as an arbitrary-length match | Count exact character slots after `Git Basic` |
| Missing notes are not found | Used `= NULL` or compared to text `'NULL'` | Use `IS NULL`; inspect whether the actual stored value is SQL `NULL` |
| `NOT IN` unexpectedly produces no IDs | The candidate list includes `NULL` | Inspect the list and its missing-value policy; use nonmissing candidates for this rule |
| A query returns zero rows without an error | Conditions might be too restrictive or the empty result is correct | Test each condition against the four rows, then combine the conditions |

The same words can denote different rules. Specify whether a range includes endpoints, whether a text phrase is at the start or end, and whether missing values are included. Then test one matching row, one excluded row, and one boundary or missing row.

## Check your understanding

1. Which IDs are returned by `course_id IN (102, 103)` and by `NOT IN (102, 103)`?
2. Does `BETWEEN 50 AND 80` include both courses at exact boundaries?
3. What is the difference between `%` and `_` in a `LIKE` pattern?
4. Which pattern tests for a title beginning with `Python`: `Python%`, `%Python`, or `%Python%`?
5. Why does `topic_note = NULL` return no rows despite two missing notes?
6. Why does `course_id NOT IN (101, NULL)` return no rows for this table?
7. Which IDs meet the independent variation's range **and** present-note condition?

**Answers and reasoning**

1. `IN` returns **102, 103**; `NOT IN` returns **101, 104**. All candidate and tested IDs here are nonmissing.
2. Yes. Course 102 is exactly 50 and course 103 is exactly 80; course 104 at 65 is also inside.
3. `%` allows zero or more characters; `_` allows exactly one character.
4. `Python%` fixes the start of the title; here it matches course **104**.
5. Ordinary equality with SQL `NULL` produces unknown rather than true for those rows; `WHERE` includes only true. Use `IS NULL`.
6. The unmatched rows cannot establish that they differ from the missing list member, so their result is unknown; course 101 matches a listed ID and is excluded too.
7. **101, 103**. They have topic notes and durations 95 and 80. Course 104 has no note even though 65 meets the range.

## Remember and retain

- `IN` checks membership and `NOT IN` excludes listed values when the candidates are known; check lists that can contain `NULL`.
- `BETWEEN lower AND upper` includes **both** ends; strict comparisons exclude them.
- `LIKE` uses `%` for zero or more characters and `_` for exactly one; place `%` after, before, or around a phrase for a prefix, suffix, or substring match.
- `IS NULL` finds missing values; `IS NOT NULL` finds present values. Neither is an ordinary equality comparison to `NULL`.
- Save your endpoint prediction, wildcard change, repaired missing-value query, mini-project query, and independent variation so you can revisit your reasoning.

## Further reading

- [SQLite: SQL expression syntax for `IN`, `BETWEEN`, `LIKE`, and `IS NULL`](https://www.sqlite.org/lang_expr.html)
- [SQLite: SELECT and WHERE](https://www.sqlite.org/lang_select.html)
- [Python: using placeholders with sqlite3](https://docs.python.org/3/library/sqlite3.html)
