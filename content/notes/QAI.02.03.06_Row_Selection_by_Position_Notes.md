# Row selection by position

A task may need the first record, the last few records, every second record, or one consecutive batch from a table. Positional selection answers “Which place in the current table?” It does not answer “Which learner has this identifier?” Keeping those questions separate prevents selecting the wrong person when row labels happen to be integers.

You should already know DataFrame rows, row-index labels, column labels, Series, shape, and column selection. This lesson uses those ideas to select rows and rectangular blocks. Label-based selection is the next lesson.

[Runnable lab ZIP](QAI.02.03.06_Row_Selection_by_Position_Lab.zip) · [Scripts and README](QAI.02.03.06_resources/README.md)

## Position, label, and positional indexer

A **row position** is a row's place in the current row order. Pandas counts positions from zero. The first row is at position `0`, the second at `1`, and so on. An **integer position** is a whole-number offset used for this selection.

A **row label** is the identifying value stored in the row index. A row can have label `40` while occupying position `0`. An integer label is still a label; it does not become a position merely because it is a number.

A **positional indexer** is an object that interprets a selection as positions. Pandas provides it through `iloc`. Write `df.iloc[...]`, using brackets, to select integer locations. `iloc` is not a method called with parentheses.

**Single-row selection** requests one position. **Multiple-row selection** requests a list of positions. **Row-range selection** uses a start and stop. **Row-step selection** skips through the positions at a specified interval. A **positional slice** packages start, stop, and step into the syntax `start:stop:step`.

A **negative position** counts backward from the end: `-1` means the last row, `-2` the second-last. **Row-and-column selection** supplies two selectors, with the row selector first and the column selector second.

Think of a queue with name badges. A person can stand second in the queue while wearing badge number 10. `iloc[1]` selects the second person because counting starts at zero. Reordering the queue changes who stands at that position without changing the person's badge.

## A table whose labels differ from positions

```python
import pandas as pd

df = pd.DataFrame({
    'learner': ['Anu', 'Bala', 'Chitra', 'Deepa', 'Eshan'],
    'python': [72, 85, 91, 68, 88],
    'sql': [80, 77, 89, 75, 90],
}, index=[40, 10, 70, 20, 60])
```

| Position | Row label | learner | python | sql |
|---:|---:|---|---:|---:|
| 0 | 40 | Anu | 72 | 80 |
| 1 | 10 | Bala | 85 | 77 |
| 2 | 70 | Chitra | 91 | 89 |
| 3 | 20 | Deepa | 68 | 75 |
| 4 | 60 | Eshan | 88 | 90 |

The shape is `(5, 3)`. Valid non-negative row positions are `0` through `4`. The labels `40, 10, 70, 20, 60` are retained in outputs; selection does not renumber them.

## Select a single row

```python
row = df.iloc[1]
print(type(row).__name__)
print(row.name)
print(row.shape)
print(row['learner'], int(row['python']), int(row['sql']))
```

Expected output:

```text
Series
10
(3,)
Bala 85 77
```

Pandas selects position `1`, then reduces the row dimension. The result is a Series indexed by the column names `learner`, `python`, and `sql`. The Series name is the selected row's label, `10`. It contains three values, so its shape is `(3,)`.

This row combines text and numeric fields. A Series has one dtype, so a row selected from mixed-type columns can use a general representation. The original DataFrame still has separate column dtypes. The `int()` calls here give stable printed numeric values across library versions; they are not needed to choose the row.

To retain a one-row DataFrame, supply a list containing the position:

```python
one = df.iloc[[1]]
print(type(one).__name__)
print(one.shape)
print(one.index.tolist())
```

Expected output:

```text
DataFrame
(1, 3)
[10]
```

The inner list says “select this collection of rows.” The outer brackets pass it to `iloc`. Use this form when the next function expects a two-dimensional table, even if only one row is requested.

## Select several rows in an explicit order

```python
chosen = df.iloc[[3, 0, 3]]
print(chosen.index.tolist())
print(chosen['learner'].tolist())
```

Expected output:

```text
[20, 40, 20]
['Deepa', 'Anu', 'Deepa']
```

The request contains three positions. Pandas returns them in that order. Position `3` occurs twice, so Deepa's row occurs twice in the result. The corresponding label `20` also appears twice. Repeated selection does not create a new learner or automatically give the repeated row a unique identifier.

A list is useful for arbitrary or reordered selections. It differs from a slice, which describes a regular progression of positions. Neither form shuffles rows randomly unless the supplied position list was generated randomly elsewhere.

## Positional slices: start included, stop excluded

For a positive step, `start:stop` selects positions from `start` up to, but excluding, `stop`.

```python
middle = df.iloc[1:4]
print(middle.index.tolist())
print(middle['learner'].tolist())
```

Expected output:

```text
[10, 70, 20]
['Bala', 'Chitra', 'Deepa']
```

The selected positions are `1, 2, 3`. Position `4`, Eshan, is excluded. An **exclusive stop** makes the slice length easy to reason about when boundaries are in range: `4 - 1 = 3` rows. It also permits adjoining slices such as `0:2` and `2:4` without overlapping position `2`.

Omitting the start begins at the first position for a forward slice. Omitting the stop continues through the end. A colon by itself, `:`, selects every row. `df.iloc[:]` therefore returns the complete row sequence; it is still a selection expression and should not be treated as a guarantee about independent editable memory.

## Step through the rows

The step is the amount added to the current position before choosing the next row.

```python
alternating = df.iloc[::2]
print(alternating.index.tolist())
print(alternating['learner'].tolist())
```

Expected output:

```text
[40, 70, 60]
['Anu', 'Chitra', 'Eshan']
```

Starting at position `0`, repeatedly add `2`: the positions are `0, 2, 4`. There is no valid position `6`, so selection ends. This regular selection is deterministic. It is not a representative random sample; a source sorted by class, date, or mark could make every second row systematically unrepresentative.

A step of zero is invalid because it would never advance:

```python
try:
    df.iloc[::0]
except ValueError:
    print('zero step: ValueError')
```

Expected output: `zero step: ValueError`. Choose a positive step for forward selection or a negative step for backward selection.

## Negative positions and backward slices

```python
last = df.iloc[-1]
print(last.name, last['learner'])
print(df.iloc[-2:].index.tolist())
print(df.iloc[::-1].index.tolist())
```

Expected output:

```text
60 Eshan
[20, 60]
[60, 20, 70, 10, 40]
```

For five rows, the position `-1` resolves to `5 - 1 = 4`; `-2` resolves to `5 - 2 = 3`. The slice `-2:` takes positions `3` and `4` in forward order. The slice `::-1` has a negative step and omitted boundaries, so it begins at the last row and walks backward through all rows.

Negative positions are relative to the current table length. They are not negative row labels. `-1` always means the final position for a non-empty table, even if the last row's label is `60` or a string.

An explicit negative stop is not the same as an omitted stop. For example, `4:-1:-1` is empty for this five-row table: explicit `-1` resolves to the last position, which is excluded, and the start is already that same position. Use `[::-1]` for a clear full reversal.

## Select rows and columns together

Use `df.iloc[row_selector, column_selector]`. Both selectors describe positions. The first axis is rows; the second is columns.

```python
block = df.iloc[1:4, [2, 0]]
print(block.to_csv(index=True).strip())
print(int(df.iloc[2, 1]))
```

Expected output:

```text
,sql,learner
10,77,Bala
70,89,Chitra
20,75,Deepa
91
```

The row positions are `1, 2, 3`. The column positions are `2, 0`, so `sql` comes before `learner`. This selection forms a rectangular block containing each selected row with each selected column. It is not a pairwise selection of only two cells.

The expression `df.iloc[2, 1]` supplies a scalar row and scalar column, so it returns one cell: Chitra's Python mark, `91`. If only one axis is scalar, the result is generally a Series; retaining collections on both axes preserves a DataFrame:

```python
print(type(df.iloc[:, 1]).__name__, df.iloc[:, 1].shape)
print(type(df.iloc[:, [1]]).__name__, df.iloc[:, [1]].shape)
```

Expected output:

```text
Series (5,)
DataFrame (5, 1)
```

The colon means every row. Column position `1` selects the numeric Python field. A list containing `1` retains the column dimension.

## Bounds: scalar and list requests differ from slices

An **out-of-bounds position** is outside the axis's valid locations. For five rows, `5` and `-6` are invalid scalar row positions. A list containing one invalid position also fails as a whole.

```python
for key in [5, -6, [0, 5]]:
    try:
        df.iloc[key]
    except IndexError:
        print('IndexError')
```

Expected output:

```text
IndexError
IndexError
IndexError
```

`IndexError` reports an invalid positional access. Diagnose it by inspecting `len(df)` and the requested positions. Remember that the last forward position is `len(df) - 1`, not `len(df)`.

Slices tolerate boundaries beyond the axis length:

```python
print(df.iloc[3:99].index.tolist())
print(df.iloc[5:99].shape)
```

Expected output:

```text
[20, 60]
(0, 3)
```

The first slice returns the existing rows at positions `3` and `4`. It does not fabricate missing rows up to `98`. The second slice starts beyond the end, so it returns an empty table with the same three columns. Empty results can be valid and expected, especially at the end of batch processing.

## A solved trace from request to values

Trace `df.iloc[1:5:2, [2, 0]]`:

1. Resolve the row slice. Begin at `1`, add `2`, and stop before `5`: positions `1` and `3`.
2. Find the retained row labels: `10` and `20`.
3. Resolve column positions `2` and `0`: `sql`, then `learner`.
4. Read both fields for each chosen row. Bala produces `77, Bala`; Deepa produces `75, Deepa`.
5. Both axis requests are collections, so the result is a DataFrame of shape `(2, 2)`.

Pandas handles positional normalization and data gathering. To see just the slice mechanism in raw Python, compare the positions generated from a list:

```python
positions = list(range(len(df)))
print(positions[1:5:2])
print(positions[::-1])
```

Expected output:

```text
[1, 3]
[4, 3, 2, 1, 0]
```

This small trace reveals ordinary slice arithmetic. Use the standard Pandas operation for real table work so labels and column dtypes are retained.

## Guided lab and controlled variation

From the resource folder, run:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

Before running `lab.py`, predict the labels returned by every row request. Compare the scalar and list shapes, then check the rectangular CSV output. The deliberate out-of-bounds and zero-step errors are handled so the script can demonstrate the resolution without stopping.

For a controlled variation, keep positions `0, 2, 4` and columns `0, 2`. Predict the labels and output before reading the solution:

```python
variation = df.iloc[0:5:2, [0, 2]]
print(variation.to_csv(index=False).strip())
```

Expected output:

```text
learner,sql
Anu,80
Chitra,89
Eshan,90
```

The table shape is `(3, 2)`. The retained row labels are `40, 70, 60`, even though they are omitted from this printed CSV. Anu's SQL mark is still `80`; skipping rows does not change the marks.

## Independent mini-project: consecutive processing batches

Build `select_batch(source, start, batch_size)`. It should return up to `batch_size` consecutive rows beginning at the zero-based `start`. Retain all columns and row labels. Return an independently editable table. Accept only Python integer arguments, reject a negative start or non-positive batch size, and return an empty table when the start is beyond the end. The final batch may be shorter than the requested size.

Try your implementation, then inspect the full reference:

```python
def select_batch(source, start, batch_size):
    if type(start) is not int or type(batch_size) is not int:
        raise TypeError('start and batch_size must be Python integers')
    if start < 0:
        raise ValueError('start must be non-negative')
    if batch_size <= 0:
        raise ValueError('batch_size must be positive')
    return source.iloc[start:start + batch_size, :].copy()
```

The stop is `start + batch_size`, because the stop is excluded. The column selector `:` retains every column. Slice clipping naturally permits a short final batch and an empty result past the end. The copy prevents subsequent assignment to the batch's simple numeric fields from changing the source.

The explicit `type(...) is int` policy also rejects Boolean values. Python treats `bool` as a subclass of `int`, but a batch size such as `True` would be a confusing interface. This function intentionally accepts Python `int`, not every possible third-party integer scalar. A broader interface can normalize validated integer types separately.

`project.py` processes starts `0, 2, 4`, with size `2`. Its full expected output is:

```text
batch start=0, rows=2
,learner,python,sql
40,Anu,72,80
10,Bala,85,77
batch start=2, rows=2
,learner,python,sql
70,Chitra,91,89
20,Deepa,68,75
batch start=4, rows=1
,learner,python,sql
60,Eshan,88,90
past end: (0, 3)
```

The tests compare the middle batch with a hand-built expected table, verify the short final batch, concatenate all batches to reconstruct the original table, check invalid inputs, and show that editing a returned batch does not modify the source. They also cover every selection mechanism taught here.

The mini-project does not stream data from disk or a database. The source DataFrame is already in memory. Batching can organize work performed on it, but does not reduce the memory already occupied by the source. An independent copy adds memory for the batch.

## Debugging and decision limits

**Off-by-one failure:** `df.iloc[1:3]` returns only positions `1` and `2`. If the requirement includes position `3`, use `1:4`. Trace the integer progression rather than guessing from the visible labels.

**Label confusion:** `df.iloc[10]` does not request label `10`. It requests the eleventh row and fails here. Use position `1` for Bala when the task is positional; use a label-based selection when the task is about identifier `10`.

**Wrong-axis failure:** `df.iloc[1:4, ['sql']]` supplies a string where integer column positions are required. Use `[2]` for that column in this specific schema, or use a label-based column selection. Do not mix coordinate meanings accidentally.

**Changed-order failure:** after sorting or filtering, positions refer to the new order. A saved position can identify a different learner. Use positions for explicitly ordered batches, and identifiers for identity-based retrieval.

**Duplicate labels:** positional selection still chooses exact locations even if two rows share a label. It does not prove that labels are unique or suitable as learner identifiers.

**Copying limits:** Pandas 3 uses Copy-on-Write, while older versions can differ in sharing behavior. The project uses an explicit copy and direct assignment to the returned table. Copies do not recursively clone arbitrary Python objects inside object-valued cells.

## Solved recall, implementation, and decision questions

**What does `iloc[0]` select?** The first row in the current table order, independent of its label. Here it is Anu, label `40`.

**What does `iloc[-2]` select?** The second-last row, Deepa at position `3`, label `20`.

**Predict `df.iloc[2:2].shape`.** `(0, 3)`. A forward slice with equal start and stop contains no positions.

**Predict `df.iloc[[4, 1]]['learner'].tolist()`.** `['Eshan', 'Bala']`, following list order rather than source order.

**Why use `df.iloc[[1]]` rather than `df.iloc[1]` for a table-processing function?** The list form retains a two-dimensional DataFrame. The scalar form returns a Series.

**Repair a loop that accesses `df.iloc[len(df)]`.** The last valid forward position is `len(df) - 1`. Prefer iterating `range(len(df))` for all positions, or use a clipped slice for batches.

**When is `iloc` a poor choice?** When the requirement identifies a learner by a stable label and row order can change. Position records where a row currently stands, not who the row represents.

**Why is every second row not a random sample?** It follows a fixed interval. If source order has a pattern, that selection inherits it. Random selection is a different operation.

**Does a final short batch indicate a failure?** No. When five rows are split into size-two batches, the expected batch lengths are `2, 2, 1`. The tests confirm that combining them reproduces the original five rows exactly once.

## Teach-back and evidence

Say: “Positions count from zero and refer to current order. `iloc` uses positions on both axes. A list keeps the requested order and can repeat rows. A slice includes the start, excludes the stop, and can skip with a step. A scalar outside the bounds fails, while a slice clips to existing positions.”

For a teaching demo, display the position-to-label table and ask which learner `iloc[1]` selects. Then show the Series versus one-row DataFrame. Ask for the positions in `1:5:2` before revealing the labels. Finish with `iloc[5]` versus `iloc[5:99]` to explain strict scalar bounds and valid empty slices.

Keep the lab output, the passing tests, the batch output, a debug note describing the off-by-one error, and a brief explanation of when identity should use labels instead. You are ready to continue when you can trace both axes without confusing labels with positions and can prove that your batches include every source row once.

## References

- [Pandas: DataFrame.iloc](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html)
- [Pandas: indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas: Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
