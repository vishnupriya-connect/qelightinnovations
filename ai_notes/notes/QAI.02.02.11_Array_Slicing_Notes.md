# Array slicing

## Select a range of positions

An **index** selects one position. A **slice** selects a range of positions, producing a **partial array**. Suppose six sessions lasted 10, 20, 30, 40, 50, and 60 minutes:

```python
import numpy as np

minutes = np.array([10, 20, 30, 40, 50, 60], dtype=np.int32)
print(minutes[1:5].tolist())  # [20, 30, 40, 50]
```

The general slice form is `array[start:stop:step]`:

| Part | Meaning in `minutes[1:5:2]` | Resulting positions |
|---|---|---|
| **Start** | Begin at index 1 | 1 |
| **Stop** | Stop **before** index 5 | 5 is excluded |
| **Step** | Move two positions at a time | 1, 3 |

```python
print(minutes[1:5:2].tolist())  # [20, 40]
```

`[1:5]` is a **slice range** with the default step 1. The values come from indexes 1, 2, 3, and 4; the stop index 5 is not selected. An omitted start defaults to the beginning for a forward slice; an omitted stop continues to the end; an omitted step defaults to 1.

```python
print(minutes[:3].tolist())   # [10, 20, 30]
print(minutes[3:].tolist())   # [40, 50, 60]
print(minutes[:].tolist())    # [10, 20, 30, 40, 50, 60]
print(minutes[-3:].tolist())  # [40, 50, 60]
```

The negative `-3` start counts from the end, as with a single negative index. Unlike a single invalid integer index, a slice whose bounds go beyond the array normally clips to the available range: `minutes[4:99]` gives `[50, 60]`. An empty interval such as `minutes[2:2]` gives an empty array rather than an `IndexError`. Inspect the resulting size and shape when an empty result is unexpected.

## Step and reverse direction

A **stepped slice** skips positions according to its step:

```python
print(minutes[::2].tolist())    # [10, 30, 50]: indexes 0, 2, 4
print(minutes[1:6:2].tolist())  # [20, 40, 60]: indexes 1, 3, 5
```

A negative step gives a **reverse slice**. The default starting point then becomes the last position, and the default stopping boundary is before the first position:

```python
print(minutes[::-1].tolist())   # [60, 50, 40, 30, 20, 10]
print(minutes[5:1:-2].tolist())  # [60, 40]: indexes 5, 3; 1 excluded
```

When the step is negative, start must be on the appropriate side of stop. A step of zero is invalid and raises `ValueError`. For reverse slices, `[::-1]` is clearer than trying to force explicit `0` as the stop, which would exclude index 0. Trace the indexes before predicting the values.

## Slice rows and columns separately

Now take a four-learner by four-task table. Rows are learners and columns are tasks:

```python
work = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
    [40, 41, 42, 43],
], dtype=np.int32)
```

For a **two-dimensional slice**, put one selection for each axis, separated by a comma. A lone colon `:` means “keep all positions on this axis.”

```python
rows = work[1:3, :]
print(rows.tolist(), rows.shape)
# [[20, 21, 22, 23], [30, 31, 32, 33]] (2, 4)

columns = work[:, 1:3]
print(columns.tolist(), columns.shape)
# [[11, 12], [21, 22], [31, 32], [41, 42]] (4, 2)
```

`work[1:3, :]` is a **row slice**: rows 1 and 2, all columns. `work[:, 1:3]` is a **column slice**: all rows, columns 1 and 2. The first output has two rows and four columns; the second has four rows and two columns. The same `1:3` text refers to different axes depending on where it appears.

Combine a row slice and a column slice to select a smaller rectangle:

```python
block = work[1:4:2, 0:4:2]
print(block.tolist(), block.shape)  # [[20, 22], [40, 42]] (2, 2)
```

The chosen row indexes are 1 and 3; the chosen column indexes are 0 and 2. The two axes are handled independently. `work[::-1, :]` reverses the order of rows while keeping columns in their original order; `work[:, ::-1]` reverses the order of columns in every row.

**A slice can share the original array's data.** Reading a slice is fine, but changing it can change the source too. For an independent editable subset, call `.copy()` on the slice. The next lesson examines references, views, and copies in depth; for this lesson, do not mutate a slice unless that effect is deliberate.

## Diagnose a wrong selection

The request is “rows 1 and 2, columns 1 and 2,” but the code is `work[1:3, 1:2]`. It selects only column 1, producing `[[21], [31]]` with shape `(2, 1)`. The intended stop for columns must be 3 because the stop is excluded. Repair to `work[1:3, 1:3]`, which gives `[[21, 22], [31, 32]]` with shape `(2, 2)`. Predict both the indexes and resulting shape before running a slice.

## Guided lab

Download the [array slicing lab](QAI.02.02.11_Array_Slicing_Lab.zip), unzip it, and run from its folder:

```sh
python array_slicing.py
python check_array_slicing.py
```

Use `python3` if needed. If NumPy is missing from the interpreter running the lab, install it with `python -m pip install -r requirements.txt`. Predict selected *indexes*, values, and output shapes first. The checker covers forward, reverse, stepped, row, column, and rectangular slices, plus empty results and a zero-step error.

**Controlled change:** in a new source array, change the fourth session from 40 to **45**. Predict `minutes[1:6:2]` as `[20, 45, 60]`; `minutes[::-1]` starts `[60, 50, 45]`. Compare with the lab's changed-input run. No slice is used to change the source.

**Debugging practice:** run the incorrect `work[1:3, 1:2]`, compare its shape to the intended `(2, 2)`, then repair the stop to 3. Also try `minutes[::0]`, record the `ValueError`, and replace the step with a nonzero one suited to the question.

## Independent mini-project: select study records

Create this three-day by four-task `int32` array:

```python
daily = np.array([
    [5, 10, 15, 20],
    [6, 12, 18, 24],
    [7, 14, 21, 28],
], dtype=np.int32)
```

Without opening `mini_project_reference.py`, select days 1 and 2 and tasks 1 and 3 using **one two-dimensional stepped slice**. Show its values and shape. Reverse the order of days while leaving task order unchanged. Select the last two tasks of every day. Predict `daily[3:5, :]` and explain why it is empty. In a *new independent array* where day 1/task 3 becomes 25 instead of 24, repeat the first selection and explain which value changes. Compare your program with the reference after your independent attempt.

**Expected results and self-check:** `daily[1:3, 1:4:2]` gives `[[12, 24], [14, 28]]` with shape `(2, 2)`. `daily[::-1, :]` gives rows `[7, 14, 21, 28]`, `[6, 12, 18, 24]`, and `[5, 10, 15, 20]` in that order. `daily[:, -2:]` gives `[[15, 20], [18, 24], [21, 28]]` with shape `(3, 2)`. `daily[3:5, :]` has shape `(0, 4)` and no rows. In the changed array the first selection is `[[12, 25], [14, 28]]`. Keep predicted positions, actual values and shapes, changed-input trace, and repaired stop or step error.

## Check your understanding

1. Which indexes does `minutes[1:5:2]` select? Why is index 5 excluded?
2. What is the difference between `minutes[3:]` and `minutes[:3]`?
3. Why does `minutes[::-1]` include the first value at the end?
4. What shapes result from `work[1:3, :]` and `work[:, 1:3]`?
5. Why does `work[1:3, 1:2]` produce only one column?
6. Does `minutes[4:99]` raise the same error as `minutes[99]`?
7. Why should you consider `.copy()` before changing a selected region?

**Answers and reasoning**

1. Indexes 1 and 3; a slice excludes its stop boundary, so 5 is never selected.
2. `[3:]` selects index 3 through the end (`[40, 50, 60]`); `[:3]` selects indexes 0 through 2 (`[10, 20, 30]`).
3. The omitted bounds with step -1 cover positions from the last through the first; index 0 is included.
4. `(2, 4)` and `(4, 2)`, respectively.
5. The column stop 2 is excluded, leaving only column index 1.
6. No. The slice clips to available values and gives `[50, 60]`; single integer index 99 raises `IndexError`.
7. Basic NumPy slices can share source data; editing one may change the original. A copy creates an independent editable subset.

## Remember and retain

- `start:stop:step`: include the start if reached, **exclude the stop**, and never use step zero.
- In a 2D array, `array[row_selection, column_selection]` applies the selections independently.
- Trace index positions, then values, then result shape. An unexpected empty slice needs investigation even though it is not an error.
- Keep your corrected stop, reverse trace, and changed-input prediction for review.

## Further reading

- [NumPy indexing and slicing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy absolute basics: indexing and slicing](https://numpy.org/doc/stable/user/absolute_beginners.html)
