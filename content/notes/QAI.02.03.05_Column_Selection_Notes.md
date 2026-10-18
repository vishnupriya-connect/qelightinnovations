# Column selection

A table may contain more fields than the next task needs. A marks report needs a learner name and marks; it does not need a phone number. Column selection creates the required view of the data, in the required order, while retaining the rows. Header changes then give those fields names that the next reader or program understands.

You should already know how to create a DataFrame, identify its row index and columns, and inspect its shape. This lesson develops selection and header changes. Row filtering and positional row selection come later.

[Runnable lab ZIP](QAI.02.03.05_Column_Selection_Lab.zip) · [Scripts and README](QAI.02.03.05_resources/README.md)

## The vocabulary and mental model

A **column** is one vertical field in a table. Its **label** is the key used to identify that field: for example, `python`. A label is often a string, but Pandas can also use integers and other hashable objects. A **row index** identifies the horizontal records; selecting columns leaves that index in place.

A **Series** is a one-dimensional labeled sequence. A **DataFrame** is a two-dimensional labeled table. A **selected Series** contains one field's values plus their row labels. A **selected DataFrame** contains a list of fields, plus both row and column labels. A table containing only one column is still two-dimensional.

**Bracket notation** means writing a selection inside `[]`. **Attribute notation** means placing a name after a dot, such as `df.python`. A **rename** changes labels while keeping the values attached to the same fields. **Replacing column labels** supplies a complete new header sequence. That replacement is positional: the first new label names the first existing column.

Imagine a sheet with removable vertical strips. Selecting `['sql', 'student']` requests those two strips in that order. The marks remain attached to the correct learner rows. Renaming `sql` to `sql_mark` changes the strip's heading; it does not change marks, rearrange learners, or convert a data type.

## One concrete table

Use this setup for the following examples:

```python
import pandas as pd

df = pd.DataFrame({
    'student': ['Anu', 'Bala', 'Chitra'],
    'python': [72, 85, 91],
    'sql': [80, 77, 89],
    'phone': ['private-a', 'private-b', 'private-c'],
}, index=['s1', 's2', 's3'])
```

| Row label | student | python | sql | phone |
|---|---|---:|---:|---|
| s1 | Anu | 72 | 80 | private-a |
| s2 | Bala | 85 | 77 | private-b |
| s3 | Chitra | 91 | 89 | private-c |

The shape is `(3, 4)`: three rows, four columns. The labels are case-sensitive. `python` and `Python` are different keys. The phone values are invented demonstration values.

## Single-column selection: a scalar key

A **scalar key** is one label rather than a collection of labels.

```python
score = df['python']
print(type(score).__name__)
print(score.shape)
print(score.tolist())
print(score.index.tolist())
print(score.name)
```

Expected output:

```text
Series
(3,)
[72, 85, 91]
['s1', 's2', 's3']
python
```

Pandas looks up the column label `python` and returns that field as a Series when the label is unique. The Series has its own `name`, here `python`, and retains the DataFrame's row labels. `tolist()` exposes the values as a Python list; it leaves out the labels for this display. It is useful for checking values, not for preserving a table's identity information.

The shape `(3,)` has one dimension. A numeric column retains its dtype, the representation used for its values. Selection does not mean converting the marks to text.

**Misconception guard:** `df[0]` requests a column whose label is the integer `0`; it does not mean “the first column.” Our table has no such label, so that expression raises `KeyError`.

## Selecting one or several columns as a DataFrame

```python
one = df[['python']]
print(type(one).__name__)
print(one.shape)
print(one.columns.tolist())
```

Expected output:

```text
DataFrame
(3, 1)
['python']
```

There are two bracket pairs for different reasons. The inner `['python']` creates a Python list of labels. The outer brackets pass that list into the DataFrame's selection operation. Pandas keeps the table structure because the request is a collection of columns.

```python
requested = ['sql', 'student', 'python']
selected = df[requested]
print(selected.columns.tolist())
print(selected.to_csv(index=True).strip())
```

Expected output:

```text
['sql', 'student', 'python']
,sql,student,python
s1,80,Anu,72
s2,77,Bala,85
s3,89,Chitra,91
```

`to_csv()` returns a comma-separated text representation here; it writes no file because no path was supplied. `index=True` includes the row labels. The leading comma in the header represents the unnamed index column. `strip()` removes the final line break from this displayed string.

The output column order follows `requested`, not the source table's order. Every row remains. The source's `phone` field is omitted; the source itself still contains it. Selecting an allowed list is a useful way to keep unnecessary fields out of a report, although it does not erase those fields from the source or guarantee that selected values contain no private information.

An empty label list is valid:

```python
empty = df[[]]
print(empty.shape)
print(empty.index.tolist())
```

Expected output is `(3, 0)` followed by `['s1', 's2', 's3']`. This is a table with rows but no selected fields. It is different from a table with no rows.

## Attribute notation and its limits

```python
print(df.python.equals(df['python']))
```

Expected output: `True`. For this simple label, dot access finds the same field. `equals()` compares the two Series' values and labels.

Dot access is convenient for exploration, but it is not suitable for every column name. Python requires a usable identifier after a dot. A label containing a space cannot be written as `df.total mark`. Furthermore, a label can collide with an existing DataFrame attribute or method:

```python
collision = pd.DataFrame({'mean': [10, 20], 'total mark': [30, 40]})
print(callable(collision.mean))
print(collision['mean'].tolist())
print(collision['total mark'].tolist())
```

Expected output:

```text
True
[10, 20]
[30, 40]
```

`mean` is already a DataFrame method, a callable operation. The dot expression finds that method rather than the column. Brackets explicitly identify a column key. For a variable such as `name = 'python'`, use `df[name]`; `df.name` asks for the literal attribute `name`, not the value stored in the variable.

Prefer brackets in reusable code. They support spaces, dynamic names, and names that collide with attributes. Dot notation does not support selecting several columns at once.

## Missing-column errors: make the failure informative

```python
try:
    df[['student', 'Python']]
except KeyError:
    print('missing selection: KeyError')
```

Expected output: `missing selection: KeyError`. The whole selection fails; Pandas does not silently return only `student`. A `KeyError` means a requested key was not found. Exact exception messages can differ by version, so tests should check the exception type and the underlying schema issue.

Debug in this order:

1. Inspect `df.columns.tolist()` to see actual labels.
2. Compare spelling, case, spaces, and label types with the request.
3. Inspect the stage where headers were changed. A previous rename may have removed the old label.
4. Correct the request or deliberately normalize the source schema before selecting.

For invisible whitespace, `repr(label)` shows a label's Python representation. A trailing space appears inside the quotes. Do not automatically remove spaces unless that is the intended naming rule; two originally different names could become the same name.

A **schema** describes a table's structure, including its expected field names. A strict selection makes a schema mismatch visible early, before a later calculation uses the wrong field.

## Rename selected labels with `rename()`

A **mapping** connects an old name to its replacement. In Python, a dictionary can express that mapping.

```python
renamed = selected.rename(
    columns={'student': 'learner', 'python': 'python_mark'},
    errors='raise',
)
print(renamed.columns.tolist())
print(df.columns.tolist())
```

Expected output:

```text
['sql', 'learner', 'python_mark']
['student', 'python', 'sql', 'phone']
```

The `columns=` keyword explicitly chooses the column axis. Only the supplied old labels change. `sql` stays `sql`. Values, row labels, column order, and value dtypes remain associated with their fields.

`rename()` returns a new object by default. Assign that result to a variable to use the new labels. Calling `df.rename(columns=...)` and then continuing to use `df` does not retain the new labels. The source remains unchanged in this example.

By default, `errors='ignore'` ignores mapping keys that are absent. That can be helpful when applying an optional rename to several schemas, but it can also conceal a typo. With `errors='raise'`, an absent old name raises `KeyError`:

```python
try:
    df.rename(columns={'Python': 'python_mark'}, errors='raise')
except KeyError:
    print('strict rename: KeyError')
```

Expected output: `strict rename: KeyError`. Correct the old key to `python`. Strict rename checks the keys being renamed; it is not a full validation of every required field, data type, or resulting name.

Avoid `result = df.rename(..., inplace=True)`. With `inplace=True`, the method changes the receiving DataFrame and returns `None`, so `result` is not a table. The explicit returned-result style is easier to inspect and compose.

## Replace every header through `columns` assignment

```python
replaced = selected.copy()
replaced.columns = ['sql_mark', 'learner', 'python_mark']
print(replaced.columns.tolist())
print(replaced['sql_mark'].tolist())
```

Expected output:

```text
['sql_mark', 'learner', 'python_mark']
[80, 77, 89]
```

`columns` is the complete column-label sequence. Assignment replaces the labels on `replaced` itself. The first new label is attached to the first current column, which is `sql`. The length of the new sequence must equal the number of columns:

```python
try:
    replaced.columns = ['only_one']
except ValueError:
    print('wrong header count: ValueError')
```

Expected output: `wrong header count: ValueError`. A `ValueError` means the supplied value is invalid for this operation. Supply exactly three labels to fix it.

A more dangerous error has the right length but the wrong order. Assigning `['python_mark', 'learner', 'sql_mark']` to our selected table would name the SQL marks `python_mark`. There is no length error, but the meaning is wrong. Compare values and old-to-new names before replacing all headers.

| Task | Prefer | Reason |
|---|---|---|
| Read one unique field as a sequence | `df['python']` | Returns a Series |
| Keep a one-column table | `df[['python']]` | Keeps two dimensions |
| Prepare ordered report fields | `df[requested]` | Follows the requested field order |
| Change a few known names | `rename(columns=mapping, errors='raise')` | Maps by existing label |
| Replace a complete known header sequence | `copy.columns = new_names` | Maps by current position |
| Work with dynamic or unusual names | Brackets | Avoids attribute-name restrictions |

## Solved mechanism trace

Start with column order `student, python, sql, phone` and three learner rows.

For `df[['sql', 'student', 'python']]`, first construct the list. Pandas resolves all three labels; if one is absent, selection fails. It builds a three-column DataFrame in list order. The first row is now `80, Anu, 72`, still labeled `s1`. The shape is `(3, 3)`.

For `rename(columns={'student': 'learner'})`, resolve the old label `student`, replace its label, and leave that column's values and position unchanged. The first row is still `80, Anu, 72`. The headers become `sql, learner, python`. This is a header transformation, not a numeric transformation.

For complete header assignment, no old-name mapping is consulted. A new first label is attached to `80, 77, 89` because those are the values in the first current column. Therefore the replacement list must reflect the already-selected order.

## Assumptions, edge cases, and trade-offs

The main examples assume a flat column index and unique column labels. A flat index has one label per column; a hierarchical column index has multiple label levels and needs additional selection rules.

Duplicate column labels are possible. They change the apparent “one key returns one field” rule:

```python
duplicate = pd.DataFrame([[1, 2]], columns=['mark', 'mark'])
print(type(duplicate['mark']).__name__, duplicate['mark'].shape)
```

Expected output: `DataFrame (1, 2)`. One label matches two columns, so the result contains both. Check `df.columns.is_unique` when downstream code depends on unambiguous field names. Renaming or normalization should not merge distinct fields under the same name.

These examples select and rename without relying on shared-memory behavior. Pandas 3 uses Copy-on-Write, which delays physical copying until needed and prevents a derived object's write from accidentally updating another object. Older versions can behave differently for some selections. Use an explicit `.copy()` when preparing an independently editable numeric report, and write directly to the intended object. A deep DataFrame copy does not recursively clone arbitrary Python objects stored inside object-valued cells; this lesson's fields contain simple strings and numbers.

Selection reduces the fields carried forward, but allocating many large intermediate tables can still consume memory. Do not promise a particular memory saving without measuring the actual workload. Renaming clarifies a schema but does not validate mark ranges or convert strings into numeric values. Those are separate checks.

## Guided runnable lab

Open the resource folder or unzip the lab, then run:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

The lab contains the examples above in one runnable script. Predict the result type and shape before running each selection. Then inspect the CSV output to confirm that marks remain attached to the correct learners. Compare `renamed` with the source headers. Finally, observe the deliberate errors and their handled exception classes.

The lab also prints `duplicate scalar selection: DataFrame (1, 2)` and `empty column selection: (3, 0) ['s1', 's2', 's3']`. Full expected output is included in `expected_lab.txt`.

## Controlled variation with solution

Change the requirement to: “Include only `student` and `sql`, in that order, and rename `sql` to `database_mark`.” Predict `(3, 2)` and the columns `student, database_mark`.

```python
variation = df[['student', 'sql']].rename(
    columns={'sql': 'database_mark'}, errors='raise'
)
print(variation.to_csv(index=False).strip())
```

Expected output:

```text
student,database_mark
Anu,80
Bala,77
Chitra,89
```

The source still has four columns. The values `80, 77, 89` did not change. Only the selected table's second header changed.

## Independent mini-project: a learner marks report

Build a function that accepts a DataFrame in any source column order. It must require unique column labels and the fields `student`, `python`, and `sql`. Return only these fields, in that order, with headers `learner`, `python_mark`, `sql_mark`. Preserve row labels and values, exclude the phone field, and leave the source unchanged. A valid empty table should return an empty report with the correct three columns. Missing fields or duplicate headers must produce a clear error.

Try the implementation first, then compare with this full reference solution:

```python
def build_report(source):
    if not source.columns.is_unique:
        raise ValueError('Source column labels must be unique')
    required = ['student', 'python', 'sql']
    missing = [name for name in required if name not in source.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    report = source[required].copy()
    report = report.rename(columns={
        'student': 'learner',
        'python': 'python_mark',
        'sql': 'sql_mark',
    }, errors='raise')
    return report
```

The list comprehension collects every missing name rather than reporting only the first one. The uniqueness guard rejects ambiguous source fields before selection. `required` defines an explicit list of allowed fields and their order. A copy permits independent subsequent edits, and the mapping gives each field a clear output name.

`project.py` calls the function with our sample and prints:

```text
learner,python_mark,sql_mark
Anu,72,80
Bala,85,77
Chitra,91,89
```

The returned table retains `s1, s2, s3`; the printout excludes them because `index=False` was requested. This function validates field structure, not learner identity, mark ranges, or missing cell values. Do not infer those guarantees from the output names.

The test suite checks exact report values and order, retained row identity, omission of phone data, source preservation after editing the result, reordered source columns, absent required fields, duplicate headers, and the valid zero-row case. It also checks each selection and header-change behavior taught above. The README contains execution commands and the expected results.

## Solved recall, implementation, and decision questions

**What is the difference between `df['python']` and `df[['python']]`?** With unique flat labels, the first returns a Series of shape `(3,)`; the second returns a DataFrame of shape `(3, 1)`. Their marks agree but their dimensional structures differ.

**Predict the first row of `df[['sql', 'python']]`.** The row labeled `s1` contains `80, 72`, in requested field order. It is not `72, 80` simply because Python originally appeared first.

**Why does `df.mean` not reliably select a column called `mean`?** The DataFrame already has a method with that name. Use `df['mean']` to explicitly request the column.

**Repair `df[['student', 'Python']]`.** Inspect the actual labels, then use `df[['student', 'python']]`. Do not catch and ignore the error while continuing with a report missing marks.

**Repair a rename that has no visible effect.** Store the return value: `report = df.rename(columns={'python': 'python_mark'}, errors='raise')`. If the old name is wrong, fix the mapping key; strict mode exposes that mistake.

**A file's source fields arrive in a different order. Should you assign three new headers immediately?** No. First select by the expected old labels and desired order. Otherwise positional header replacement can mislabel correct values. A mapping-based rename is safer for a few named changes.

**Why check uniqueness separately from missing names?** Presence alone does not say there is exactly one field per name. A duplicate `sql` can produce additional output columns and ambiguous results.

**Does removing `phone` from the report remove it from the source?** No. It prevents that field from being carried into this result. The source remains unchanged and must still be handled appropriately.

**How do you prove that editing the report does not change the source?** Keep a copy of the original, build the report, change the report's numeric column, and compare the source with that original using `assert_frame_equal`. The supplied test does exactly this.

## Teach-back and completion evidence

Explain aloud: “A column label is a key. One unique key selects a Series; a list selects a DataFrame and determines column order. Renaming maps old labels to new labels. Complete header assignment maps new labels by position. Neither operation changes the meaning or values unless I attach the wrong name.”

For a short teaching demo, display the sample table, ask learners to predict the type and shape of each selection, run the two expressions, reorder `sql` and `python`, and ask them to trace Anu's marks. Then demonstrate the `mean` collision and missing `Python` key. Finish by comparing rename with positional header replacement.

Keep the passing test output, the generated report text, a brief debug record explaining the typo and header-length failures, and a teach-back note. You are ready to continue when you can construct the report from reordered source fields and explain both its correctness guarantees and its limits.

## References

- [Pandas: indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas: DataFrame.rename](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html)
- [Pandas: Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
- [Pandas: duplicate labels](https://pandas.pydata.org/docs/user_guide/duplicates.html)
