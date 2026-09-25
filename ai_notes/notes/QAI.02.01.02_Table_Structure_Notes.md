# QAI.02.01.02 — Table structure

> QAI.02.01.01 data and data systems → **QAI.02.01.02 table structure** → QAI.02.01.03 database data types

## 1. Destination: inspect a table without confusing its parts

Suppose a course catalogue accidentally contains the same lesson twice and does not yet know one lesson's duration:

| code | title | minutes |
|---|---|---:|
| QAI.01.31 | Configuration and secrets | 35 |
| QAI.01.32 | Git fundamentals | 55 |
| QAI.02.01.02 | Table structure | NULL |
| QAI.01.31 | Configuration and secrets | 35 |

After this lesson you can identify the table and its parts, say what its structure permits, count records and columns, and distinguish a missing value from a duplicated record. The accompanying [micro-lab](QAI.02.01.02_Table_Structure_Demo.py) prints the same observations from an in-memory database. You only need to run and modify it once; writing SQL independently comes later.

## 2. One table: names, rows, columns, cells

A **table** organises a collection of records into rows and columns. Its **table name** identifies it inside a database; here the name is `lessons`. The printed Markdown table is a *view* of those records. A database may also contain other tables, such as `instructors`.

| Term | Point to it in the example | What to remember |
|---|---|---|
| **Row** | `QAI.01.32 / Git fundamentals / 55` | One complete record across the table's columns |
| **Column** | All entries under `minutes` | The same kind of field across records |
| **Column name** | `minutes` | A label the database/program uses to select that field |
| **Cell** | `55` where Git fundamentals meets `minutes` | The position at one row and one column, holding a value or a null marker |
| **Column order** | `code`, then `title`, then `minutes` | The order declared in this table's definition; an individual query can select or display columns in another order |
| **Record count** | Four rows | Number of records in this displayed table, including duplicates |
| **Column count** | Three columns | Number of fields defined for each row in this table |

**Check:** `35` appears twice in the `minutes` column. That does not make *every* row with a value of `35` a duplicate; compare the **entire row** or the specific identity rule you have chosen.

### Count before you write code

- Record count: **4**.
- Column count: **3**.
- Cells in this rectangular display: **4 × 3 = 12** positions; one holds `NULL`.
- Distinct full rows: **3**; one full row repeats.

The cell count includes positions without a known duration. “No known value” is not the same as “no cell.”

## 3. What is a schema?

A **schema** is a stated plan for how data is organised and which rules it should follow. It is a design description, not the current list of lesson values.

- A **table schema** describes one table's name, column names, **column data types**, and possibly rules on allowed values or identity.
- A **database schema** describes the collection of tables and their definitions and connections. If a database has only one table, its database schema is still broader in scope than that table's schema.
- A **data type** says what general kind of value belongs in a place: text such as `Git fundamentals`, or a whole number such as `55`. A **column data type** is the chosen type for a particular column.

For this *teaching* table, a readable design sketch is:

```text
Database: course_catalogue
Table: lessons
Columns in order:
    code     → text
    title    → text
    minutes  → whole number or unknown
```

**Important:** that sketch describes intended meaning. The executable SQLite micro-lab declares `TEXT` and `INTEGER` columns. SQLite's ordinary type declarations do **not** enforce every business rule implied by this English sketch. In particular, the micro-lab deliberately allows repeated records and a missing duration. Later sections teach data types, keys, constraints, and validation. Do not infer correctness just from a declared column name or type.

**Distinguish:** the column's *name* is `minutes`; its declared *data type* is `INTEGER`; its value for Git fundamentals is `55`. Replacing `55` with `60` changes a record, not the table schema. Adding a new column named `difficulty` changes the schema.

## 4. Missing, null, and empty are different

A **missing value** is the data-quality observation that information expected for a particular item is unavailable or not recorded. The third row has no known duration. A **null value**, written `NULL` in SQL, is a special database marker commonly used to represent that absence. It is not the number zero, the word `"NULL"`, or an empty text string.

| Stored or received form | Example | What you may infer |
|---|---|---|
| Database `NULL` | Third row's `minutes` | No ordinary duration value is stored there; ask *why* before interpreting |
| Zero | `0` minutes | A known numeric value, perhaps valid or invalid under a separate rule |
| Empty text | `""` | A text value with no characters; it is not SQL `NULL` |
| Absent field in source JSON | `{"code": "QAI.02.01.02"}` | Source omitted that field; an import rule decides whether to reject or map it to NULL |
| Literal text `"NULL"` | Text containing those four letters | Ordinary text unless an explicit import rule converts it |

**Mental model:** “missing” describes an information problem; `NULL` is one database representation of it. `NULL` does not tell you whether the duration is unknown, not applicable, pending measurement, or deleted. That meaning requires a separate rule or source documentation.

## 5. Duplicate row and unique row

A **duplicate row**, in this lesson, repeats **all displayed values** of another row. The first and fourth rows are equal in `code`, `title`, and `minutes`, so the fourth is a duplicate **by full-row comparison**. The second and third are **unique rows** by that comparison: each full value combination occurs once.

An **identity rule** may ask a different question: “Should each `code` occur only once?” Under that rule, the first and fourth rows also violate code uniqueness. A database can have two *different* rows with the same code but different titles; then they are not full-row duplicates, yet they may still violate the chosen code-identity rule. Establish the rule before reporting “duplicates.”

Many database engines provide internal row identities even when two visible rows are identical. That internal distinction does not remove the duplicate-content issue you would see in a course catalogue. The micro-lab avoids a uniqueness constraint on purpose so you can observe the issue. In a real catalogue you would validate lesson identity and design an appropriate uniqueness constraint.

### Solved comparison

If a fifth row is `QAI.01.32 / Git fundamentals / 60`, is it a duplicate?

- Compared with the second row across **all three fields**: **no**, because `60 ≠ 55`.
- Compared by **lesson code** alone: **yes**, the code repeats. Decide whether the two entries represent an update to one lesson or two separate records before deleting anything.

## 6. Run one micro-lab

Run `python QAI.02.01.02_Table_Structure_Demo.py` in the folder containing the script, or `python3` if that is your Python command. Its Python standard-library `sqlite3` module creates a temporary in-memory database and the four rows. Expected:

```text
Table: lessons
Columns: code, title, minutes
Column count: 3
Record count: 4
NULL durations: 1
Repeated full rows: 1
Distinct full rows: 3
```

The program reads the column names from SQLite's table definition, fetches the records, and counts in Python. It does not assume records come back in the order in which they were inserted; a database query needs an explicit sort request if order matters.

### Change one input and predict

In the `rows = [...]` input list, delete **only the last duplicate tuple**, run again, and compare:

| Output | Before | After |
|---|---:|---:|
| Column count | 3 | 3 |
| Record count | 4 | 3 |
| NULL durations | 1 | 1 |
| Repeated full rows | 1 | 0 |
| Distinct full rows | 3 | 3 |

The changed list contains three records. The definition of the three columns is unchanged. Restore the tuple if you want to repeat the exercise.

## 7. Check understanding, with answers

| Prompt | Answer |
|---|---|
| Where is the cell containing `55`? | In the second displayed row, under the `minutes` column. |
| Does adding an extra lesson change the table schema? | No, it changes the records. Adding a new column changes the table schema. |
| Is the third row a missing *row*? | No. The row exists; its duration value is represented as `NULL`. |
| Are there two duplicate rows or one repeated occurrence? | One full-row value appears twice; this lesson reports **one repeated occurrence** beyond its first appearance. |
| Does `NULL` mean `0` minutes? | No. It represents absence of an ordinary value here; zero is a number. |
| Must the result return rows in the same order they were entered? | No. Request an explicit result order when it matters. |

## Remember

- Table name identifies a table; a row is a record; a column is a named field; a cell is their intersection.
- Record count includes repeated rows; column count comes from the table definition.
- Table schema defines one table; database schema covers the database's organised design.
- A declared type describes intended value kind; it does not prove real-world correctness.
- Missing information may be represented by `NULL`; empty text, zero, and the literal word `"NULL"` differ.
- “Duplicate” needs a comparison rule: full row or selected identity fields.

## Primary references

- [SQLite: CREATE TABLE](https://sqlite.org/lang_createtable.html)
- [SQLite: SELECT results and ordering](https://sqlite.org/lang_select.html)
- [Python: sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
