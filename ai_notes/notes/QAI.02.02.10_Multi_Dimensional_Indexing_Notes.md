# Multi-dimensional indexing

## Give each axis a meaning

Suppose two learners record minutes for three tasks: reading, exercises, and review.

```python
import numpy as np

work = np.array([
    [12, 8, 5],
    [10, 15, 5],
], dtype=np.int32)
print(work.shape)  # (2, 3)
```

This array has two axes: **axis 0 = learner (row)** and **axis 1 = task (column)**. A **row index** selects a learner position; a **column index** selects a task position. Both start at zero. An individual value needs a **coordinate index** containing one position for each axis.

| Meaning | Coordinate | Value |
|---|---|---:|
| Learner 0, reading | `(0, 0)` | 12 |
| Learner 0, review | `(0, 2)` | 5 |
| Learner 1, exercises | `(1, 1)` | 15 |

An array does not store the words “learner” or “task” in these numeric elements. We must retain that axis description with the data. Reversing the coordinate changes the question: `work[0, 1]` is 8, while `work[1, 0]` is 10.

## Access one value in two dimensions

NumPy accepts two positions separated by a comma. The pair is a **tuple index**: a tuple is an ordered group, here `(row, column)`.

```python
print(work[1, 1])     # 15
print(work[(1, 1)])   # 15: explicit tuple form
print(work[0, 2])     # 5
```

The returned item is a scalar value from an array with `dtype=int32`, not a two-dimensional array. For a shape `(2, 3)`, nonnegative row indexes are `0..1` and column indexes are `0..2`. Negative indexes can count from the end of either axis: `work[-1, -2]` selects learner 1, exercises, again yielding 15. A request such as `work[2, 0]` raises `IndexError` because row 2 does not exist.

Using one index changes the result:

```python
row = work[1]
print(row.tolist(), row.shape)  # [10, 15, 5] (3,)
```

This is **row selection**, a one-dimensional sub-array, not the single number 15. `work[1][1]` can reach 15 in two steps, but `work[1, 1]` expresses the complete coordinate directly and makes each axis easier to check.

## Select a complete column

The colon `:` means **all positions on this axis** in the following simple examples. To choose the exercise column for every learner, keep all rows and set column index 1:

```python
column = work[:, 1]
print(column.tolist(), column.shape)  # [8, 15] (2,)
```

Compare `work[1, :]`, which keeps all columns for learner 1 and gives `[10, 15, 5]`. The order of positions is always axis 0, then axis 1. One integer index removes an axis from the result; `:` keeps the corresponding axis. This lesson only uses `:` to mean the whole axis. Ranges, steps, and reverse slices are treated next. These simple selections may share storage with the source, so treat them as read-only in this lesson; the later view-and-copy lesson explains mutation behavior.

## Add a depth axis for a stack of tables

Now record the same learners and tasks for two weeks:

```python
weeks = np.array([
    [[12, 8, 5], [10, 15, 5]],  # week 0
    [[14, 6, 5], [12, 10, 8]],  # week 1
], dtype=np.int32)
print(weeks.shape)  # (2, 2, 3)
```

Call the first axis the **depth index** or stack position for this example: **axis 0 = week**, **axis 1 = learner/row**, **axis 2 = task/column**. A three-dimensional element needs all three positions, in that order:

```python
print(weeks[1, 0, 1])       # 6: week 1, learner 0, exercises
print(weeks[(1, 0, 1)])     # 6: the same tuple coordinate
print(weeks[-1, 0, 1])      # 6: final week, learner 0, exercises
```

In this shape, valid nonnegative indexes are `0..1` for week, `0..1` for learner, and `0..2` for task. The *role* of axis 0 is decided by the dataset, not by NumPy; it could represent a day, image channel, or another ordered category in a different task.

## Select a sub-array, not one item

Omit the later coordinates to select an entire lower-dimensional piece:

```python
week_one = weeks[1]
print(week_one.tolist(), week_one.shape)
# [[14, 6, 5], [12, 10, 8]] (2, 3)

one_learner = weeks[1, 0]
print(one_learner.tolist(), one_learner.shape)  # [14, 6, 5] (3,)

exercise_column = weeks[1, :, 1]
print(exercise_column.tolist(), exercise_column.shape)  # [6, 10] (2,)
```

The first selection is a two-dimensional table for week 1; the second is one-dimensional task data for its first learner; the third is a one-dimensional exercise column across that week's learners. `weeks[1, 0]` is **not** an error for a three-dimensional array. It returns a sub-array because the task axis remains. If the intended answer is exactly one number, supply the remaining task coordinate as in `weeks[1, 0, 1]`.

## Trace a wrong coordinate

A learner expects week 1, learner 0, exercises (`6`) but writes `weeks[0, 1, 1]`, obtaining `15`. Check the shape and the axis labels: the first index chooses week, the second learner, the third task. Correct the tuple to `(1, 0, 1)`. Another mistake is `weeks[2, 0, 1]`; with only two weeks, depth index 2 is out of bounds. Do not substitute a value from another week to hide the error.

For a program that promises a *single* reading, you can validate that the coordinate has exactly as many entries as the array has axes before indexing. The lab does so; it rejects an incomplete tuple like `(1, 0)` for a three-dimensional single-reading request. NumPy itself permits that shorter tuple and returns a sub-array, which may be correct when a sub-array was intended.

## Guided lab

Download the [multi-dimensional indexing lab](QAI.02.02.10_Multi_Dimensional_Indexing_Lab.zip), unzip it, and run from its folder:

```sh
python multi_dimensional_indexing.py
python check_multi_dimensional_indexing.py
```

Use `python3` if needed. If NumPy is not installed in the interpreter running the lab, use `python -m pip install -r requirements.txt`. Before running, predict each selected value **and result shape**. The checker covers two- and three-axis coordinates, full rows and columns, incomplete single-reading coordinates, and an out-of-bounds week.

**Controlled change:** a corrected week 1 reading for learner 0 is **16** instead of 14. Make an independent copy and assign at `(1, 0, 0)`. Predict `weeks[1, 0]` on the copy as `[16, 6, 5]`; `weeks[1, :, 0]` as `[16, 12]`; the original remains 14 at that coordinate. The lab helper performs this change so you can compare outputs.

**Debugging practice:** record the wrong result for `weeks[0, 1, 1]` when the request is week 1, learner 0, exercises. State why it yields 15, then repair to `(1, 0, 1)` and confirm 6. Attempt `weeks[2, 0, 1]`, inspect shape `(2, 2, 3)`, and explain the `IndexError`.

## Independent mini-project: two days of task records

Build an `int32` array with **day → learner → task** axes, and tasks in **reading, practice** order:

```python
records = [
    [[10, 5], [20, 10], [15, 5]],
    [[12, 8], [18, 12], [10, 10]],
]
```

Without opening `mini_project_reference.py`, report shape, the value at day 1/learner 1/practice, the complete table for day 1, the row for learner 2 on day 0, and the practice column for all learners on day 1. Predict every result's shape. Then make a copy, correct day 1/learner 1/practice from 12 to 17, and show the new column and unchanged original value. Include one incomplete-coordinate diagnosis and one out-of-bounds diagnosis.

**Expected results and self-check:** shape `(2, 3, 2)`; single value **12** at `(1, 1, 1)`; day 1 table `[[12, 8], [18, 12], [10, 10]]` with shape `(3, 2)`; day 0 learner 2 row `[15, 5]` with shape `(2,)`; day 1 practice column `[8, 12, 10]` with shape `(3,)`. The copied update changes that column to `[8, 17, 10]` and leaves the original selected value 12. `records_array[1, 1]` is a row rather than a scalar; `records_array[2, 0, 0]` is out of bounds. Keep predicted and actual values, result shapes, changed-input trace, and corrected coordinates.

## Check your understanding

1. What do the two positions in `work[1, 0]` mean?
2. What are the shapes of `work[1]` and `work[:, 1]`? What differs in their values?
3. Why do `weeks[1, 0]` and `weeks[1, 0, 1]` return different kinds of result?
4. What does the first coordinate of `weeks[1, 0, 1]` mean in this dataset?
5. Is `weeks[(1, 0, 1)]` a different location from `weeks[1, 0, 1]`?
6. Why is `weeks[2, 0, 1]` invalid? Why is `weeks[1, 0]` valid?

**Answers and reasoning**

1. Learner row 1 and task column 0, yielding 10.
2. `(3,)` for the complete learner row `[10, 15, 5]`; `(2,)` for the exercise column `[8, 15]`.
3. The first omits the task position and returns all three tasks as a one-dimensional array; the second chooses one task and returns the scalar 6.
4. Week 1, the second week; the meaning comes from the chosen axis order.
5. No. Comma-separated indexing supplies the same ordered tuple of positions.
6. Axis 0 has length two, so only 0 and 1 are valid nonnegative week indexes. The shorter valid coordinate selects a sub-array rather than requiring a task index.

## Remember and retain

- **Name axes first.** In `work`: learner → task. In `weeks`: week → learner → task.
- An integer position chooses one place on an axis; `:` here keeps all positions along that axis.
- A complete coordinate returns one element; leaving trailing coordinates out can return a sub-array.
- Predict both value and result shape. Keep the wrong-order repair and copied-update trace for later review.

## Further reading

- [NumPy indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy quickstart: indexing](https://numpy.org/doc/stable/user/quickstart.html)
