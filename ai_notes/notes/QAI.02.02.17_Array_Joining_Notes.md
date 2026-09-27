# Array joining

## Join batches along an existing axis

Suppose rows are learners and columns are tasks. A new batch adds one learner:

```python
import numpy as np

first = np.array([[10, 20], [30, 40]])
extra = np.array([[50, 60]])
rows = np.concatenate((first, extra), axis=0)
print(rows.shape, rows.tolist())
# (3, 2) [[10, 20], [30, 40], [50, 60]]
```

**Array joining** combines arrays. To **concatenate** means to place arrays end to end along an *existing* axis. The **concatenation axis** here is `axis=0`, the learner/row axis. Its lengths add (`2 + 1 = 3`), while the task/column lengths must match (`2`). `np.concatenate()` returns a new array. This is **vertical concatenation**.

To add a task for the *same* learners, use `axis=1`:

```python
new_task = np.array([[7], [9]])
columns = np.concatenate((first, new_task), axis=1)
print(columns.shape, columns.tolist())
# (2, 3) [[10, 20, 7], [30, 40, 9]]
```

This is **horizontal concatenation**. The learner counts must match. Write down what each axis means before choosing it; equal numeric shapes alone do not prove that rows represent the same learners.

## Convenience functions

For the two-dimensional arrays above, `np.vstack((first, extra))` gives `rows`, and `np.hstack((first, new_task))` gives `columns`. Their names mean vertical stack and horizontal stack; these examples join along existing axes. One-dimensional inputs behave differently:

```python
a = np.array([10, 20, 30])
b = np.array([40, 50, 60])
print(np.hstack((a, b)).shape)          # (6,)
print(np.hstack((a, b)).tolist())       # [10, 20, 30, 40, 50, 60]
print(np.vstack((a, b)).shape)          # (2, 3)
print(np.vstack((a, b)).tolist())       # [[10, 20, 30], [40, 50, 60]]
print(np.column_stack((a, b)).shape)    # (3, 2)
print(np.column_stack((a, b)).tolist()) # [[10, 40], [20, 50], [30, 60]]
```

**Column stack**, `column_stack()`, treats each vector as one column. **Row stack**, `row_stack()`, is an older alias of `vstack()`. Where present, `np.row_stack((a, b))` has shape `(2, 3)`, but the alias is deprecated in recent NumPy; prefer `vstack()` in new code. For two-dimensional inputs, `column_stack()` joins columns as `hstack()` does, provided their row counts match.

| Operation on two vectors of shape `(3,)` | Shape | Meaning |
| --- | --- | --- |
| `concatenate((a, b))` or `hstack((a, b))` | `(6,)` | One longer vector |
| `vstack((a, b))` or legacy `row_stack((a, b))` | `(2, 3)` | Two rows |
| `column_stack((a, b))` | `(3, 2)` | Two columns |

## Stack along a new axis

`np.stack()` creates a *new* axis. Its inputs must have exactly the same shape:

```python
print(np.stack((a, b), axis=0).tolist())
# [[10, 20, 30], [40, 50, 60]]; shape (2, 3)
print(np.stack((a, b), axis=1).tolist())
# [[10, 40], [20, 50], [30, 60]]; shape (3, 2)
```

These happen to match the `vstack()` and `column_stack()` results for vectors. The distinction matters for tables:

```python
second = np.array([[50, 60], [70, 80]])
print(np.concatenate((first, second), axis=0).shape) # (4, 2)
print(np.stack((first, second), axis=0).shape)        # (2, 2, 2)
print(np.stack((first, second), axis=0)[1, 0, 1])     # 60
```

Concatenating makes four learner rows. Stacking keeps two tables and introduces a source axis: `(source, learner, task)`. The original `second[0, 1] == 60` becomes `[1, 0, 1]` in the stacked array.

## Depth concatenation

**Depth concatenation** joins along a third axis. For two two-dimensional tables, `np.dstack()` promotes them to three dimensions and places them side by side in depth:

```python
depth = np.dstack((first, second))
print(depth.shape)          # (2, 2, 2)
print(depth[0, 1].tolist()) # [20, 60]
print(depth[0, 1, 1])       # 60
```

The axes now mean `(learner, task, source)`. Although leading-axis `stack()` has the same shape here, its axis meanings and coordinates differ. For already three-dimensional arrays, `dstack()` concatenates along their existing third axis. With one-dimensional inputs, `np.dstack((a, b)).shape` is `(1, 3, 2)`.

| Inputs | Operation | Shape | Axis meanings |
| --- | --- | --- | --- |
| Two `(2, 2)` tables | `concatenate(..., axis=0)` | `(4, 2)` | learner, task |
| Two `(2, 2)` tables | `stack(..., axis=0)` | `(2, 2, 2)` | source, learner, task |
| Two `(2, 2)` tables | `dstack(...)` | `(2, 2, 2)` | learner, task, source |

## Guided lab

Download [Array joining lab](QAI.02.02.17_Array_Joining_Lab.zip), extract it, and run inside the extracted folder:

```bash
python -m pip install -r requirements.txt
python array_joining.py
python check_array_joining.py
```

The program shows shapes, values, and coordinate mappings. The checker reports `All checks passed.`

**Trace before running:** predict where `second[0, 1] == 60` lands after vertical concatenation, leading-axis stacking, and depth stacking. The destination coordinates are `[2, 1]`, `[1, 0, 1]`, and `[0, 1, 1]`.

**Controlled variation:** make a copy of `second`, set its `[0, 1]` value to 99, and join it all three ways. The destination coordinates above become 99; the original `second[0, 1]` stays 60.

**Debug shapes:** `np.concatenate((first, np.array([[7, 8, 9]])), axis=0)` raises `ValueError`: the non-joining column lengths 2 and 3 disagree. A valid added row has two task values. `np.stack((first, extra))` also fails because `(2, 2)` and `(1, 2)` are not identical input shapes. If `hstack()` unexpectedly produces one long vector, choose `vstack()` for rows or `column_stack()` for columns.

## Independent mini-project: combine study sessions

Let `morning = np.array([[5, 7], [9, 11]])` and `evening = np.array([[6, 8], [10, 12]])`, with `(learner, task)` axes. (1) Append evening rows under morning rows; (2) make a new session axis first; (3) place session on the depth axis; (4) combine the first task from both sessions as two columns. Print shapes and trace `evening[1, 0] == 10` through every result. The lab contains `mini_project_reference.py`.

Expected output:

```text
rows (4, 2) 10
sessions (2, 2, 2) 10
depth (2, 2, 2) 10
first task (2, 2) [[5, 6], [9, 10]]
```

Full reference solution:

```python
import numpy as np

morning = np.array([[5, 7], [9, 11]])
evening = np.array([[6, 8], [10, 12]])
rows = np.concatenate((morning, evening), axis=0)
sessions = np.stack((morning, evening), axis=0)
depth = np.dstack((morning, evening))
first_task = np.column_stack((morning[:, 0], evening[:, 0]))
print("rows", rows.shape, rows[3, 0])
print("sessions", sessions.shape, sessions[1, 1, 0])
print("depth", depth.shape, depth[1, 0, 1])
print("first task", first_task.shape, first_task.tolist())
```

## Check your understanding

1. **What changes on `axis=0` concatenation?** Row lengths add; the other dimensions must match.
2. **What does `hstack((a, b))` do to two `(3,)` vectors?** It produces one `(6,)` vector, not two columns.
3. **Why may two `(2, 2, 2)` results mean different things?** They may order source, learner, and task axes differently. Trace a known cell.
4. **When is `stack()` appropriate?** When equal-shaped arrays need a new axis, such as a session axis.

Remember: choose a longer existing axis or a new axis deliberately, then check shape and a known coordinate.

## Further reading

- [NumPy: concatenate](https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html) and [stack](https://numpy.org/doc/stable/reference/generated/numpy.stack.html)
- [NumPy: hstack](https://numpy.org/doc/stable/reference/generated/numpy.hstack.html), [vstack](https://numpy.org/doc/stable/reference/generated/numpy.vstack.html), and [dstack](https://numpy.org/doc/stable/reference/generated/numpy.dstack.html)
- [NumPy: column_stack](https://numpy.org/doc/stable/reference/generated/numpy.column_stack.html) and [row_stack](https://numpy.org/doc/stable/reference/generated/numpy.row_stack.html)
