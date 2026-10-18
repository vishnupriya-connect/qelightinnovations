# Array-axis transformations

## Turn a learner-by-task table around

Suppose rows represent learners and columns represent tasks. To look at one task across learners, **transpose** the table:

```python
import numpy as np

work = np.array([[12, 8, 5], [10, 15, 5]], dtype=np.int32)
turned = work.T
print(work.shape, turned.shape)  # (2, 3) (3, 2)
print(turned.tolist())          # [[12, 10], [8, 15], [5, 5]]
print(work[1, 0], turned[0, 1])  # 10 10
```

`work` has axes `(learner, task)`; the **transposed array** has axes `(task, learner)`. An element at original coordinate `[learner, task]` appears at `[task, learner]`. Transposing does not reverse each row or change any measured value. `work.transpose()` gives the same result as `work.T` for this two-dimensional table. Both return a view in this example, so copying first is prudent if you intend to edit the turned data independently.

| Operation | Resulting axis meanings | Shape |
| --- | --- | --- |
| `work` | learner, task | `(2, 3)` |
| `work.T` | task, learner | `(3, 2)` |
| `work.transpose()` | task, learner | `(3, 2)` |

## A one-dimensional array is neither a row nor a column

The vector below has one axis, so its `.T` is still one-dimensional. To make a **row-to-column conversion**, first give it a second axis. `np.expand_dims()` inserts an axis of length one, called a **singleton dimension**:

```python
v = np.array([12, 8, 5], dtype=np.int32)
row = np.expand_dims(v, axis=0)
column = np.expand_dims(v, axis=1)
print(v.shape, v.T.shape)       # (3,) (3,)
print(row.shape, column.shape)  # (1, 3) (3, 1)
print(row.tolist())             # [[12, 8, 5]]
print(column.tolist())          # [[12], [8], [5]]
print(row.T.shape, column.T.shape)  # (3, 1) (1, 3)
```

`axis=0` inserts a row axis before the existing item axis; `axis=1` inserts a column axis after it. Once the array is two-dimensional, `row.T` performs row-to-column conversion and `column.T` performs **column-to-row conversion**. Shapes `(3,)`, `(1, 3)`, and `(3, 1)` are distinct even though they hold the same three numbers.

`np.squeeze()` removes singleton dimensions. Specify the axis to make your intention clear:

```python
print(np.squeeze(row, axis=0).shape)     # (3,)
print(np.squeeze(column, axis=1).shape)  # (3,)
```

Trying `np.squeeze(row, axis=1)` raises `ValueError`: axis 1 has length three, so removing it would lose a real dimension. Without an `axis` argument, `squeeze()` removes *all* singleton axes. Neither `expand_dims()` nor `squeeze()` invents or discards numeric elements.

## Three axes: choose the new order deliberately

Imagine a cube with axes `(week, learner, task)` and distinct axis lengths `(2, 3, 4)`. The lengths make each resulting order easy to recognize:

```python
cube = np.arange(24, dtype=np.int32).reshape(2, 3, 4)
by_task = cube.transpose(2, 0, 1)
swapped = cube.swapaxes(0, 2)
moved = np.moveaxis(cube, 0, 2)
print(cube[1, 2, 3])                       # 23
print(by_task.shape, by_task[3, 1, 2])     # (4, 2, 3) 23
print(swapped.shape, swapped[3, 2, 1])     # (4, 3, 2) 23
print(moved.shape, moved[2, 3, 1])         # (3, 4, 2) 23
```

| Expression | How it treats axes | New axis meanings | Shape |
| --- | --- | --- | --- |
| `cube.transpose(2, 0, 1)` | List every old axis in its new order | task, week, learner | `(4, 2, 3)` |
| `cube.swapaxes(0, 2)` | Exchange old axes 0 and 2 | task, learner, week | `(4, 3, 2)` |
| `np.moveaxis(cube, 0, 2)` | Move week to the last position; shift the others left | learner, task, week | `(3, 4, 2)` |
| `cube.T` or `cube.transpose()` | Reverse all three axes | task, learner, week | `(4, 3, 2)` |

For `transpose(2, 0, 1)`, each number names an old axis. `swapaxes()` exchanges just two. `moveaxis()` relocates a chosen axis and keeps the relative order of the others. With three axes, `.T` happens to match `swapaxes(0, 2)`; it reverses *all* axes in general. Every result above has 24 elements, and each operation maps an old coordinate to a new one without changing its value. For these arrays the results are views: editing one can affect the cube. Use `.copy()` for an independent result.

## Guided lab

Download [Array-axis transformations lab](QAI.02.02.16_Array_Axis_Transformations_Lab.zip), extract it, then in that folder run:

```bash
python -m pip install -r requirements.txt
python array_axis_transformations.py
python check_array_axis_transformations.py
```

The first program prints the table, vector, and cube mappings. The checker tests shapes, values, and coordinates, then reports `All checks passed.`

**Trace before running:** the source cell `cube[1, 2, 3]` is 23. Week 1, learner 2, task 3 becomes `by_task[3, 1, 2]`, `swapped[3, 2, 1]`, and `moved[2, 3, 1]`. Predict these positions and compare with the printed results.

**Controlled variation:** in a fresh copy, set `changed[1, 2, 3] = 99`. Run the three transformations on `changed`, and check the same three destination coordinates. Each becomes 99, while `cube[1, 2, 3]` remains 23. This checks mapping and the reason for making a copy.

**Debug a shape mistake:** `v.T` does not make a column because `v.ndim` is 1. Use `np.expand_dims(v, axis=1)` and check for shape `(3, 1)`. If squeezing fails, inspect the requested axis length; only length-one axes can be removed. A transpose order such as `(0, 0, 1)` repeats an axis and is invalid for a three-axis array; use each axis exactly once.

## Independent mini-project: rearrange study records

Create `records = np.arange(100, 124, dtype=np.int32).reshape(2, 3, 4)`, with axes `(week, learner, task)`. Write a program that (1) puts the week axis last using `moveaxis`, (2) puts the task axis first using `transpose`, (3) exchanges week and task using `swapaxes`, and (4) converts `records[1, 2]` from a one-dimensional task vector into a column and back into a vector. Print each shape and track the original value `records[1, 2, 3]` through the three cube transformations. Check your work against `mini_project_reference.py` in the lab.

Expected shapes are `(3, 4, 2)`, `(4, 2, 3)`, `(4, 3, 2)`, `(4, 1)`, and `(4,)`, in that order. The tracked value is 123 in each cube arrangement. The full reference solution is:

```python
import numpy as np

records = np.arange(100, 124, dtype=np.int32).reshape(2, 3, 4)
weeks_last = np.moveaxis(records, 0, 2)
tasks_first = records.transpose(2, 0, 1)
exchanged = records.swapaxes(0, 2)
vector = records[1, 2]
column = np.expand_dims(vector, axis=1)
back = np.squeeze(column, axis=1)

print(weeks_last.shape, weeks_last[2, 3, 1])   # (3, 4, 2) 123
print(tasks_first.shape, tasks_first[3, 1, 2]) # (4, 2, 3) 123
print(exchanged.shape, exchanged[3, 2, 1])     # (4, 3, 2) 123
print(column.shape, back.shape)                  # (4, 1) (4,)
print(back.tolist())                             # [120, 121, 122, 123]
```

## Check your understanding

1. **Why does `v.T` retain shape `(3,)`?** A single axis has no second axis to exchange. Insert a singleton axis to obtain a row or column.
2. **Where does `cube[1, 2, 3]` land after `moveaxis(cube, 0, 2)`?** At `[2, 3, 1]`: learner, task, week.
3. **Do `swapaxes(cube, 0, 2)` and `moveaxis(cube, 0, 2)` mean the same thing?** No. The former gives `(task, learner, week)`; the latter gives `(learner, task, week)`.
4. **When can `squeeze()` remove an axis?** When that axis has length one; the number of numeric elements remains the same.

Remember: write the meaning of each axis next to its shape, and trace a known coordinate before trusting a rearrangement.

## Further reading

- [NumPy: transpose](https://numpy.org/doc/stable/reference/generated/numpy.transpose.html)
- [NumPy: swapaxes](https://numpy.org/doc/stable/reference/generated/numpy.swapaxes.html) and [moveaxis](https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html)
- [NumPy: expand_dims](https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html) and [squeeze](https://numpy.org/doc/stable/reference/generated/numpy.squeeze.html)
