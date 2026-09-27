# Scalar, vector, matrix, and tensor

## One measurement or many?

Suppose a study group records minutes of reading and practice. A single total, a sequence of daily totals, and a rectangular table answer different questions. We describe these arrangements by the number of **axes** needed to locate one value. An axis is a direction of positions in an array; its **length** is the count of positions in that direction. Axis numbers start at zero.

| Arrangement | Example | Shape | Axes | Often called |
|---|---|---|---:|---|
| One number | `45` | `()` as an array | 0 | scalar |
| Three daily totals | `[20, 30, 40]` | `(3,)` | 1 | vector |
| Two learners × three tasks | `[[12, 8, 5], [10, 15, 5]]` | `(2, 3)` | 2 | matrix |
| Two weeks × two learners × three tasks | two such tables stacked | `(2, 2, 3)` | 3 | three-dimensional array, often called a tensor |

These terms describe the arrangement; they do not by themselves say whether a number is a duration, a score, or a price. In applied computing, **tensor** often means a multi-dimensional numerical array, and may include arrays with any number of axes. Mathematical tensor has a more specific meaning; the number of array axes alone does not establish all its mathematical properties. Here we use the practical array meaning.

## A scalar and a zero-dimensional array

A **scalar value** is one number, such as a 45-minute total. A NumPy **zero-dimensional array** is an `ndarray` that holds one such value, has no axes, and has shape `()`. A plain Python number or a NumPy scalar value can behave like a scalar in calculations but is a different *object type* from a zero-dimensional `ndarray`.

```python
import numpy as np

total = np.array(45, dtype=np.int32)
print(total.ndim, total.shape, total.size)  # 0 () 1
print(type(total).__name__)                # ndarray
print(type(total[()]).__name__)            # int32: extracted NumPy scalar
```

There is **one element**, although the array has **zero axes**. `total[()]` uses an empty index tuple to retrieve it. It is incorrect to infer `size == 0` from `ndim == 0`. For comparison, `np.array([], dtype=np.int32)` has shape `(0,)`, one axis of length zero, and no elements.

## A vector and its single axis

A **vector** in this introductory array sense is a one-dimensional arrangement. One position locates each value:

```python
daily = np.array([20, 30, 40], dtype=np.int32)
print(daily.ndim, daily.shape, daily.size)  # 1 (3,) 3
print(daily[1])                            # 30
```

The comma in `(3,)` makes it a one-entry shape tuple, not a plain number. There is one axis, **axis 0**, with length **3**. The indexes on it are 0, 1, and 2. A spatial vector in mathematics may carry additional structure; the array shape alone tells us only how these values are organized for computation.

## A matrix: rows and columns

A **matrix** is a two-dimensional arrangement. Read the following as two **rows** (one per learner) and three **columns** (one per task):

```python
work = np.array([[12, 8, 5], [10, 15, 5]], dtype=np.int32)
print(work.ndim, work.shape, work.size)  # 2 (2, 3) 6
print(work[1, 1])                       # 15: second learner, second task
```

In `work.shape == (2, 3)`, **axis 0** has length **2** (row positions), and **axis 1** has length **3** (column positions). The indexes `work[1, 1]` select row 1 and column 1. Shape `(3, 2)` would describe three rows and two columns; it is not interchangeable with `(2, 3)`, even though both contain six elements.

An operation that **reduces** an axis combines the values along it and removes that axis from the result, unless instructed to keep it. With `sum`:

```python
print(work.sum(axis=0))  # [22 23 10]: combine rows, one total per column
print(work.sum(axis=1))  # [25 30]: combine columns, one total per row
```

Trace the first output: task 0 is `12 + 10 = 22`, task 1 is `8 + 15 = 23`, and task 2 is `5 + 5 = 10`. Trace the second: learner 0 has `12 + 8 + 5 = 25`; learner 1 has `10 + 15 + 5 = 30`. **Axis 0 is the row-position direction**, but `sum(axis=0)` *removes that direction*, leaving totals indexed by columns. Saying “axis 0 always returns rows” is a common mistake. In a matrix, `work.shape[0]` and `work.shape[1]` report the axis lengths; `work.sum(axis=0).shape` is `(3,)`, while `work.sum(axis=1).shape` is `(2,)`.

## A three-dimensional array

Add a second week's table in the same task order:

```python
weeks = np.array([
    [[12, 8, 5], [10, 15, 5]],
    [[14, 6, 5], [12, 10, 8]],
], dtype=np.int32)
print(weeks.shape, weeks.ndim, weeks.size)  # (2, 2, 3) 3 12
print(weeks[1, 0, 1])                      # 6: week 1, learner 0, task 1
```

The first axis counts weeks (length 2), the second learners (length 2), and the third tasks (length 3). Twelve values follow from `2 × 2 × 3`. A three-dimensional array need not be imagined as a physical cube: here it means a stack of two ordinary tables. More generally, a **multi-dimensional array** can have any number of axes; `ndim` reports that number and `shape` gives each axis length in order.

```python
print(weeks.sum(axis=0))
# [[26 14 10]
#  [22 25 13]]
```

This combines corresponding entries *across weeks*. The result has shape `(2, 3)`: learner and task remain; the week axis has been removed. If you want one total *per week*, combine both learner and task axes: `weeks.sum(axis=(1, 2))` gives `[55 55]`. Tuple axis syntax is a useful preview; the core skill here is to name each axis and predict the shape before running.

## Guided lab

Download the [scalar, vector, matrix, and tensor lab](QAI.02.02.03_Scalar_Vector_Matrix_and_Tensor_Lab.zip), unzip it, and run in its folder:

```sh
python array_dimensions.py
python check_array_dimensions.py
```

Use `python3` if needed. If NumPy is missing from this Python environment, run `python -m pip install -r requirements.txt`. Predict the five shapes and the two matrix-sum outputs before running. The checker includes an incorrect axis number, the zero-dimensional/empty distinction, and the changed-input case.

**Controlled change:** make a copy of `work` and change the second learner's third task from 5 to 9. Predict `sum(axis=1) == [25, 34]` and `sum(axis=0) == [22, 23, 14]`; shape stays `(2, 3)`. Run the supplied change function, compare, and explain why just one row total and one column total change. The lab creates a copy so the original table still gives `[25, 30]` and `[22, 23, 10]`.

**Diagnose:** `work.sum(axis=2)` raises `AxisError`. Inspect `work.ndim == 2`: its only non-negative axis numbers are 0 and 1. To get the second learner's total, use `work.sum(axis=1)[1]`, which is 30 in the original table. Keep the error, correction, and observed result in your practice record.

## Independent mini-project

Record two days of minutes for three learners, with reading and practice as the two tasks. Use this data in that order:

```text
Day 0: [[10, 5], [20, 10], [15, 5]]
Day 1: [[12, 8], [18, 12], [10, 10]]
```

Build a NumPy array and print its shape, number of dimensions, size, axis lengths, and the value for day 1, learner 1, practice. Calculate totals per day by reducing learner and task axes, and totals per learner and task across days by reducing the day axis. Predict before running. Then create an independent copy and change day 1, learner 1, practice from 12 to 17. Show the changed day total and confirm the original remains intact. Compare your work with `mini_project_reference.py` only after your attempt.

**Expected result and self-check:** shape `(2, 3, 2)`, `ndim=3`, `size=12`, axis lengths 2, 3, 2; selected value 12; day totals `[65, 70]`; across-day learner/task totals `[[22, 13], [38, 22], [25, 15]]`. The copied change makes day 1 total **75**; the original stays **70**. A complete result includes the predicted and actual arrays, an explanation of which axis each reduction removes, and a repaired incorrect-axis example. Six-value and twelve-value arrangements here are small enough to check by hand; compare shape and meaning before choosing an axis in a real data task.

## Check your understanding

1. Can a zero-dimensional array have an element? How does it differ from an empty one-dimensional array?
2. For `work.shape == (2, 3)`, what do `shape[0]` and `shape[1]` count?
3. Why does `work.sum(axis=0)` have three values, while `work.sum(axis=1)` has two?
4. Which value does `weeks[1, 0, 1]` find, and in what order are the indexes given?
5. What shape results from `weeks.sum(axis=0)`? What shape results from reducing axes 1 and 2?
6. Does a three-axis NumPy array by itself establish the full mathematical meaning of a tensor?

**Answers and reasoning**

1. Yes: shape `()`, `ndim=0`, `size=1`. An empty one-dimensional array has shape `(0,)`, `ndim=1`, `size=0`.
2. `shape[0] == 2` counts row positions (learners); `shape[1] == 3` counts column positions (tasks).
3. Reducing axis 0 combines the two row entries in each column, leaving three columns; reducing axis 1 combines three tasks within each row, leaving two learners.
4. It finds `6`, using week, learner, task positions in that order.
5. `(2, 3)` after reducing weeks. `(2,)` after reducing learners and tasks, leaving weeks.
6. No. In applied array work “tensor” is often used for a multi-dimensional numerical array; the mathematical concept has additional structure.

## Remember and retain

- `ndim` counts axes; `shape` lists their lengths; the product of the lengths is `size`. Shape `()` has a product of one.
- For the study example: **week → learner → task** maps to axes **0 → 1 → 2**. State that meaning before indexing or reducing.
- A reduction with `axis=k` combines entries along axis `k` and normally removes it. Predict the remaining shape before checking values.
- Save your first prediction, run output, changed-input trace, and invalid-axis repair so you can teach the distinction from memory.

## Further reading

- [NumPy quickstart: axes, shape, and reductions](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy absolute basics: dimensions](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy array objects and scalar objects](https://numpy.org/doc/stable/reference/arrays.html)
