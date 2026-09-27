# Array splitting

## Divide a table at a known position

Suppose the rows of a table are learners and its columns are tasks. We can divide it into smaller arrays without changing the order of its values:

```python
import numpy as np

table = np.arange(24, dtype=np.int32).reshape(4, 6)
top, bottom = np.split(table, 2, axis=0)
print(table.shape)                     # (4, 6)
print(top.shape, bottom.shape)         # (2, 6) (2, 6)
print(top[0].tolist())                 # [0, 1, 2, 3, 4, 5]
print(bottom[0].tolist())              # [12, 13, 14, 15, 16, 17]
```

**Array splitting** returns a list of smaller arrays. `np.split(array, 2, axis=0)` asks for two **equal splits** of the row axis: four rows divide into two parts of two rows. The axis remains present in each result. In this example, the original `table[2, 4] == 16` becomes `bottom[0, 4] == 16`; the second piece begins at original row 2.

An integer number of parts requires the chosen axis length to divide evenly. `np.split(table, 3, axis=1)` gives three parts with two columns each. `axis=0` means rows; `axis=1` means columns.

## Split positions and unequal parts

For **unequal splits**, pass a list of **split positions** rather than the number of parts:

```python
left, middle, right = np.split(table, [2, 5], axis=1)
print([part.shape for part in (left, middle, right)])
# [(4, 2), (4, 3), (4, 1)]
print([part[0].tolist() for part in (left, middle, right)])
# [[0, 1], [2, 3, 4], [5]]
```

Position 2 makes a cut *before* column 2; position 5 makes another cut *before* column 5. Thus the column ranges are `[:2]`, `[2:5]`, and `[5:]`. Two cut positions produce three pieces. `table[2, 4] == middle[2, 2] == 16`: the original column 4 is the third column within the middle piece.

The same rule works for a one-dimensional vector:

```python
values = np.arange(8)
pieces = np.split(values, [3, 5])
print([p.tolist() for p in pieces]) # [[0, 1, 2], [3, 4], [5, 6, 7]]
```

Here the pieces have lengths 3, 2, and 3. To request *three nearly equal pieces* from eight values without choosing positions, use `np.array_split(values, 3)`, which gives lengths 3, 3, and 2. `np.split(values, 3)` instead raises `ValueError`, since eight is not divisible by three.

## Horizontal and vertical split

`np.hsplit()` is a **horizontal split**: on a two-dimensional table it divides columns (`axis=1`). `np.vsplit()` is a **vertical split**: it divides rows (`axis=0`). Both accept either a number of equal parts or a list of cut positions:

```python
columns = np.hsplit(table, 3)
rows = np.vsplit(table, 2)
print([p.shape for p in columns]) # [(4, 2), (4, 2), (4, 2)]
print([p.shape for p in rows])    # [(2, 6), (2, 6)]
print([p.shape for p in np.hsplit(table, [2, 5])])
# [(4, 2), (4, 3), (4, 1)]
```

For a one-dimensional vector, `hsplit()` divides its only axis, so `np.hsplit(values, 2)` produces two `(4,)` vectors. `vsplit()` requires at least two dimensions; use `split()` or `hsplit()` for a vector. On arrays with more axes, `hsplit()` still divides axis 1 and `vsplit()` still divides axis 0.

| Input | Operation | Divided axis | Result shapes |
| --- | --- | --- | --- |
| `table`, `(4, 6)` | `split(table, 2, axis=0)` | rows, axis 0 | two `(2, 6)` |
| `table`, `(4, 6)` | `hsplit(table, 3)` | columns, axis 1 | three `(4, 2)` |
| `table`, `(4, 6)` | `vsplit(table, 2)` | rows, axis 0 | two `(2, 6)` |
| `table`, `(4, 6)` | `hsplit(table, [2, 5])` | columns, axis 1 | `(4, 2)`, `(4, 3)`, `(4, 1)` |

## Split the depth axis

A three-dimensional array may use axes `(week, learner, task)`. A **depth split**, `np.dsplit()`, divides its third axis, `axis=2`; it does not create a new axis:

```python
cube = np.arange(24, dtype=np.int32).reshape(2, 3, 4)
early, late = np.dsplit(cube, 2)
print(cube.shape, early.shape, late.shape)
# (2, 3, 4) (2, 3, 2) (2, 3, 2)
print(cube[1, 2, 3], late[1, 2, 1]) # 23 23
```

The late piece starts at task position 2, so original task position 3 becomes local position 1. `np.split(cube, 2, axis=2)` gives the same pieces. `dsplit()` requires an array with at least three dimensions; a plain two-dimensional table has no depth axis.

Splitting normally returns **views** that share numeric data with the source. In these examples, changing `late[1, 2, 1]` also changes `cube[1, 2, 3]`. Use `.copy()` on a piece before changing it when the source must stay intact. Splitting does not independently create new measurements.

## Guided lab

Download [Array splitting lab](QAI.02.02.18_Array_Splitting_Lab.zip), extract it, and run inside that folder:

```bash
python -m pip install -r requirements.txt
python array_splitting.py
python check_array_splitting.py
```

The first program prints equal, unequal, horizontal, vertical, and depth pieces. The checker verifies shape and coordinate mappings and prints `All checks passed.`

**Trace before running:** locate `table[2, 4] == 16` in a row split at 2 and in a column split at `[2, 5]`; predict `bottom[0, 4]` and `middle[2, 2]`.

**Controlled variation:** create `changed = cube.copy()`, assign `changed[1, 2, 3] = 99`, and depth split `changed`. Verify the last piece contains 99 at `[1, 2, 1]`, while the original `cube` still has 23. In a separate trial, edit an un-copied split piece and observe how its source changes.

**Debug:** `np.split(values, 3)` fails because eight values cannot form three equal groups. Use explicit cuts such as `[3, 5]` when you need those exact boundaries, or `array_split(values, 3)` for nearly equal groups. If `dsplit(table, 2)` fails, check that the input has a third axis rather than guessing from how it is printed.

## Independent mini-project: separate study records

Build `records = np.arange(100, 124, dtype=np.int32).reshape(6, 4)` with axes `(learner, task)`. (1) Split the rows at positions `[2, 5]`; (2) split the columns at `[1, 3]`; (3) reshape a separate view into `(2, 3, 4)` with `(week, learner, task)` axes and depth split it into two equal task groups. Print the shapes and trace the original last value, 123, in the final piece from each operation. The lab has the full `mini_project_reference.py`.

Expected output:

```text
row shapes [(2, 4), (3, 4), (1, 4)] value 123
column shapes [(6, 1), (6, 2), (6, 1)] value 123
depth shapes [(2, 3, 2), (2, 3, 2)] value 123
```

Full reference solution:

```python
import numpy as np

records = np.arange(100, 124, dtype=np.int32).reshape(6, 4)
row_parts = np.vsplit(records, [2, 5])
column_parts = np.hsplit(records, [1, 3])
cube = records.reshape(2, 3, 4)
depth_parts = np.dsplit(cube, 2)
print("row shapes", [p.shape for p in row_parts], "value", row_parts[2][0, 3])
print("column shapes", [p.shape for p in column_parts], "value", column_parts[2][5, 0])
print("depth shapes", [p.shape for p in depth_parts], "value", depth_parts[1][1, 2, 1])
```

## Check your understanding

1. **What does `[2, 5]` mean in `split(table, [2, 5], axis=1)`?** Cut before columns 2 and 5, producing ranges `[:2]`, `[2:5]`, and `[5:]`.
2. **Why does `split(values, 3)` fail for eight values?** Three equal whole-number lengths cannot add to eight.
3. **Which axis does `dsplit()` divide?** The third axis, numbered 2, of an array with at least three axes.
4. **Can editing a split piece change the source?** Yes, the resulting pieces are views in these examples; copy before independent editing.

Remember: a count requests equal pieces; a list specifies cut positions. Keep axis meanings beside shapes and trace one known value.

## Further reading

- [NumPy: split](https://numpy.org/doc/stable/reference/generated/numpy.split.html) and [array_split](https://numpy.org/doc/stable/reference/generated/numpy.array_split.html)
- [NumPy: hsplit](https://numpy.org/doc/stable/reference/generated/numpy.hsplit.html), [vsplit](https://numpy.org/doc/stable/reference/generated/numpy.vsplit.html), and [dsplit](https://numpy.org/doc/stable/reference/generated/numpy.dsplit.html)
