# Row selection by label

Tables often identify rows by meaningful keys: learner IDs, invoice numbers, dates, or product codes. Label selection retrieves rows by those identities. It answers “Which record has this key?” rather than “Which row currently appears third?”

You should already know DataFrame structure, column selection, and positional selection with `iloc`. This lesson develops row labels, label slices, two-axis label selection, and reliable failure handling.

[Runnable lab ZIP](QAI.02.03.07_Row_Selection_by_Label_Lab.zip) · [Scripts and README](QAI.02.03.07_resources/README.md)

## Core vocabulary and mental model

A **row label** is the value identifying a row on the row axis. The complete row-label sequence is the DataFrame's **index**; therefore a row label is also called an **index label**. A label may be text, a number, a timestamp, or another supported hashable value.

A **label indexer** interprets supplied keys as labels. Pandas exposes the label indexer through `loc`: write `df.loc[...]`. A **single-label selection** supplies one row label. A **multiple-label selection** supplies a list-like collection. A **label-range selection** supplies a slice such as `'L10':'L20'`. A **label slice** is inclusive at both ends when both boundary labels exist. **Row-and-column label selection** supplies a row selector first and a column selector second.

Think of a set of files whose tabs contain learner IDs. Position asks for “the second file in this pile.” Label selection asks for “the file tabbed L10.” Reordering the pile changes the second file, but it does not change which file is L10.

**Misconception guard:** `loc[5]` means the index label `5`, never the sixth row. If the index contains strings such as `L40`, the integer `5` is simply absent.

## Working table

```python
import pandas as pd

df = pd.DataFrame(
    {
        'learner': ['Anu', 'Bala', 'Chitra', 'Deepa', 'Eshan'],
        'python': [72, 85, 91, 68, 88],
        'sql': [80, 77, 89, 75, 90],
    },
    index=['L40', 'L10', 'L70', 'L20', 'L60'],
)
```

| Position | Index label | learner | python | sql |
|---:|---|---|---:|---:|
| 0 | L40 | Anu | 72 | 80 |
| 1 | L10 | Bala | 85 | 77 |
| 2 | L70 | Chitra | 91 | 89 |
| 3 | L20 | Deepa | 68 | 75 |
| 4 | L60 | Eshan | 88 | 90 |

The labels deliberately differ from the current positions and are not sorted alphabetically. That makes the meaning of each selection visible.

## Single label: one row as a Series

```python
row = df.loc['L10']
print(type(row).__name__)
print(row.name)
print(row.shape)
print(row['learner'], int(row['python']), int(row['sql']))
```

Expected output:

```text
Series
L10
(3,)
Bala 85 77
```

Pandas searches the index for label `L10`. The result contains the three fields of Bala's row. Selecting one unique row with one scalar label reduces the row axis, producing a Series indexed by the column labels. Its `name` stores the selected row label.

To retain a two-dimensional table, pass a one-element list:

```python
one = df.loc[['L10']]
print(type(one).__name__)
print(one.shape)
print(one.index.tolist())
```

Expected output:

```text
DataFrame
(1, 3)
['L10']
```

Use the list form when a downstream function requires a DataFrame even for one learner.

## Multiple labels: request order and repetition

```python
chosen = df.loc[['L20', 'L40', 'L20']]
print(chosen.index.tolist())
print(chosen['learner'].tolist())
```

Expected output:

```text
['L20', 'L40', 'L20']
['Deepa', 'Anu', 'Deepa']
```

The result follows request order, not source order. Repeating `L20` repeats its row. This can be intentional, but it can also duplicate records in a report. Validate request uniqueness when each identity must appear once.

All requested labels must exist. A list containing one absent label raises `KeyError`; Pandas does not silently return only the labels that exist. This strictness helps expose stale or misspelled identifiers.

## Label slices are inclusive and follow current index order

```python
part = df.loc['L10':'L20']
print(part.index.tolist())
print(part['learner'].tolist())
```

Expected output:

```text
['L10', 'L70', 'L20']
['Bala', 'Chitra', 'Deepa']
```

Both boundary labels are included. Pandas begins at the current location of `L10`, walks forward through `L70`, and stops after including `L20`. It does not select labels according to alphabetical or numeric meaning. The text `L70` appears between the boundaries because that is where the row currently stands.

This differs from a Python or `iloc` slice, whose stop position is excluded. It also differs from a test such as “all labels alphabetically between L10 and L20.” A label slice is navigation across the current index order.

A negative step walks backward:

```python
print(df.loc['L20':'L10':-1].index.tolist())
```

Expected output:

```text
['L20', 'L70', 'L10']
```

The direction must agree with the boundary order. On this index, `df.loc['L20':'L10']` with the default positive step is empty because `L10` occurs before `L20`.

For predictable slicing, use an index with unique labels and an understood order. Duplicate or non-monotonic labels make boundary reasoning harder. An index is **monotonic** when its labels consistently increase or consistently decrease. Exact-label lists remain clearer for a small known identity set.

## Rows and columns by label

The syntax is `df.loc[row_selector, column_selector]`. Both axes use labels.

```python
block = df.loc[['L70', 'L10'], ['sql', 'learner']]
print(block.to_csv(index=True).strip())
print(int(df.loc['L70', 'python']))
```

Expected output:

```text
,sql,learner
L70,89,Chitra
L10,77,Bala
91
```

The row request chooses Chitra and Bala in that order. The column request chooses `sql` before `learner`. The result is the rectangular intersection of every selected row and every selected column. The scalar pair `('L70', 'python')` returns one cell: `91`.

A colon means every label on that axis:

```python
print(type(df.loc[:, 'python']).__name__, df.loc[:, 'python'].shape)
print(type(df.loc[:, ['python']]).__name__, df.loc[:, ['python']].shape)
```

Expected output:

```text
Series (5,)
DataFrame (5, 1)
```

A scalar column label reduces the column axis; a one-label list retains it. This is the same dimensional distinction seen in row selection.

## Non-existent labels and deliberate debugging

```python
for operation in [
    lambda: df.loc['L99'],
    lambda: df.loc[['L10', 'L99']],
    lambda: df.loc['L10', 'Python'],
]:
    try:
        operation()
    except KeyError:
        print('KeyError')
```

Expected output:

```text
KeyError
KeyError
KeyError
```

A **non-existent label error** means at least one requested key is absent from the relevant axis. Diagnose it systematically:

1. Inspect `df.index.tolist()` for row labels or `df.columns.tolist()` for column labels.
2. Check spelling, capitalization, whitespace, and type. String `'10'` and integer `10` are different labels.
3. Confirm that an earlier operation did not replace or reset the index.
4. Decide whether absence is a genuine data-quality failure or an optional request.
5. If it is a failure, report the missing labels explicitly. If optional, use a deliberate alternative such as intersection or reindexing and document the semantics.

Do not broadly catch `KeyError` and continue with a partial identity report. That can conceal missing learners. A strict project should compare requested labels with the index before selection and raise a domain-specific message.

## Duplicate labels change the return shape

An index is **unique** when every label appears once. Pandas permits duplicate labels, but scalar lookup can then match several rows:

```python
duplicated = pd.DataFrame({'mark': [70, 80, 90]}, index=['A', 'A', 'B'])
result = duplicated.loc['A']
print(type(result).__name__, result.shape)
print(result['mark'].tolist())
```

Expected output:

```text
DataFrame (2, 1)
[70, 80]
```

With a unique index, a scalar label normally produces a Series. With two `A` rows, it produces a two-row DataFrame. Code that assumes one record per learner can therefore fail or, worse, process two records as if both were authoritative. Check `df.index.is_unique` before identity-based work. A label is not automatically a valid unique identifier merely because it is stored in the index.

## Solved mechanism trace

Trace `df.loc[['L70', 'L10'], ['sql', 'learner']]`:

1. Read the row request as labels, never positions.
2. Find `L70` at position 2 and `L10` at position 1. Preserve request order, producing row order `L70`, then `L10`.
3. Find column label `sql` at position 2 and `learner` at position 0. Preserve request order.
4. Gather the rectangular intersections: Chitra gives `89, Chitra`; Bala gives `77, Bala`.
5. Both selectors are list-like, so the result remains a DataFrame of shape `(2, 2)`.

The positions help explain how values are retrieved internally, but they are not part of the public request. If the source rows are reordered, the same labels still identify Chitra and Bala.

## Guided runnable lab

From the resource directory, run:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

Before each selection, predict the result type, shape, label order, and values. The lab shows scalar, list, inclusive slice, reverse slice, two-axis, and dimensional selections. It deliberately triggers missing row, list-member, and column errors, then handles them so the rest of the demonstration continues.

The output also shows that selecting duplicate label `A` returns a DataFrame of shape `(2, 1)`. Compare the exact output with `expected_lab.txt`.

## Controlled variation with solution

Requirement: choose Eshan and Anu by learner ID, in that order, and keep only learner name and SQL mark.

```python
variation = df.loc[['L60', 'L40'], ['learner', 'sql']]
print(variation.to_csv(index=True).strip())
```

Expected output:

```text
,learner,sql
L60,Eshan,90
L40,Anu,80
```

The source positions are 4 and 0, but the result follows the requested identities and order. The shape is `(2, 2)`. The source remains unchanged.

## Independent mini-project: verified learner report

Build `learner_report(source, learner_ids)`. The function must:

- require a unique source index;
- reject repeated requested IDs;
- require columns `learner`, `python`, and `sql`;
- report every unknown ID before selection;
- return exactly the requested learners, fields, and order;
- return an independently editable table;
- accept an empty request and return a zero-row table with the valid schema.

Try first, then compare with the complete reference:

```python
def learner_report(source, learner_ids):
    if not source.index.is_unique:
        raise ValueError('Source row labels must be unique')
    if len(learner_ids) != len(set(learner_ids)):
        raise ValueError('Requested learner labels must be unique')
    required_columns = ['learner', 'python', 'sql']
    missing_columns = [name for name in required_columns if name not in source.columns]
    if missing_columns:
        raise ValueError(f'Missing required columns: {missing_columns}')
    missing_ids = [label for label in learner_ids if label not in source.index]
    if missing_ids:
        raise ValueError(f'Unknown learner labels: {missing_ids}')
    return source.loc[list(learner_ids), required_columns].copy()
```

The uniqueness checks establish the one-request-to-one-row assumption. The missing lists make failures inspectable. The explicit column list establishes report schema and order. `.copy()` makes later assignment to the returned simple numeric table independent of the source.

`project.py` requests `L70` and `L10` and prints:

```text
,learner,python,sql
L70,Chitra,91,89
L10,Bala,85,77
```

The tests verify exact values, identity order, dimensional behavior, inclusive and reverse slices, missing labels, duplicate indexes, duplicate requests, missing columns, source preservation, empty requests, and an empty valid source. They do not claim that names are verified identities, marks are within a valid range, or cell values are complete; those are separate validation requirements.

## Assumptions, limitations, and trade-offs

- Labels identify rows only under the data contract that created them. A wrong learner ID can still point to a real but unintended row.
- Unique labels support one-record lookup; enforce uniqueness when that is required.
- A label slice follows current index order and includes both boundaries. It is not a semantic range query over unsorted strings.
- Exact label lists provide clear auditing for a small requested set. Very large identity queries may be better joined against a request table so matches and omissions can be reviewed.
- Copying makes the result independently editable for ordinary numeric and text columns, but it costs memory. A DataFrame deep copy does not recursively clone arbitrary Python objects stored inside object-valued cells.
- Pandas 3 uses Copy-on-Write; older versions can differ in sharing behavior. Explicit copies and direct assignments make intent clearer across supported versions.
- Selecting fewer columns reduces what this report carries forward, but the source still contains all original data and requires appropriate privacy controls.

## Solved recall, implementation, and decision questions

**What does `df.loc['L10']` select?** The row whose index label equals `L10`: Bala. It does not select position 10 or the tenth row.

**Why is `df.loc[['L10']]` different?** The list-like request retains the row axis and returns a `(1, 3)` DataFrame rather than a Series.

**Predict `df.loc['L10':'L20'].index.tolist()`.** `['L10', 'L70', 'L20']`. Both endpoints are included, and traversal follows current order.

**Does `df.loc[['L20', 'L40']]` sort the result?** No. It preserves the request order: Deepa, then Anu.

**Why does one absent label make a multi-label request fail?** `loc` treats all requested labels as required. Strict failure prevents an incomplete identity selection from looking successful.

**How should optional IDs be handled?** Compute and report missing IDs, decide explicitly whether they are allowed, then select the intersection in a documented order. Do not accidentally weaken strict selection.

**Why check `index.is_unique`?** With duplicates, scalar lookup can return multiple rows and break the assumption that one learner ID identifies one record.

**When should you prefer `iloc`?** Use it when the requirement is explicitly about current order or batch positions. Use `loc` when the requirement is about identities or named axis values.

**Why can a label slice become misleading after sorting?** Sorting changes the path between boundary labels. The endpoints remain identities, but the included intermediate rows depend on current index order.

**How do tests prove source preservation?** Save a deep copy of the source, build the report, change a returned mark column, and compare the source with the saved copy using `assert_frame_equal`.

## Remember and teach back

- `loc` is label based; an integer key remains a label.
- A scalar unique row label normally returns a Series; a list retains a DataFrame.
- A list preserves request order and can repeat rows.
- A label slice includes both boundary labels and traverses current index order.
- The row selector precedes the column selector.
- Missing labels raise `KeyError`.
- Duplicate index labels invalidate one-label-one-record assumptions.

Teach it aloud: “Positions say where a row currently stands; labels say how a row is identified. `loc` resolves labels on both axes. Lists preserve request order, slices include both endpoints, and missing labels fail. Before treating labels as identities, I verify uniqueness.”

For a trainer demo, first ask learners to compare `loc['L10']` with `iloc[1]`. Reorder the table and repeat both requests to reveal the identity/position distinction. Then ask them to predict the three labels in the inclusive slice. End with the duplicate-`A` table and ask why the result type changes.

Keep the exact lab output, passing tests, generated report, a debug note for the `L99` failure, and a short teach-back explanation. You are ready to continue when you can select identities without confusing them with positions and can state the assumptions under which one label means one record.

## References

- [Pandas: DataFrame.loc](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
- [Pandas: indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas: duplicate labels](https://pandas.pydata.org/docs/user_guide/duplicates.html)
- [Pandas: Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
