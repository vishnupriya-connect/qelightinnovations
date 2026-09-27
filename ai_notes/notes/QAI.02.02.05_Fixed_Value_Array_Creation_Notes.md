# Fixed-value array creation

## Start with a known shape and value

Suppose we have **three learners** and **two activities** (reading and practice). Before recording any real minutes, we may need a rectangular numerical array with one position for each learner and activity. A **shape argument** specifies the length of each axis: `(3, 2)` means three rows and two columns, with six elements in total.

```python
import numpy as np

minutes = np.zeros((3, 2), dtype=np.int32)
print(minutes.tolist())  # [[0, 0], [0, 0], [0, 0]]
print(minutes.shape)     # (3, 2)
```

`np.zeros()` fills *all* six positions with the **zero value**. In this example zero is only an initial placeholder: it must not be reported as an observed zero-minute activity before measurements arrive. `dtype=np.int32` asks for 32-bit integers, making the stored type explicit. A shape of `3` alone would make a one-dimensional array of length three; `(3, 2)` makes a two-dimensional array. A shape `(0, 2)` is valid and contains no elements, while a negative axis length is invalid.

## Choose zero, one, or another fill value

The constructors differ in which **fill value** is placed at every position:

```python
zeros = np.zeros((2, 3), dtype=np.int32)
ones = np.ones((2, 3), dtype=np.int32)
fives = np.full((2, 3), 5, dtype=np.int32)

print(zeros.tolist())  # [[0, 0, 0], [0, 0, 0]]
print(ones.tolist())   # [[1, 1, 1], [1, 1, 1]]
print(fives.tolist())  # [[5, 5, 5], [5, 5, 5]]
```

`np.ones()` puts the **one value** in each position. `np.full(shape, fill_value, dtype=...)` puts the specified value in each position. Choose a fill value that has a real meaning for the task: ones can be a starting numerical weight; five could be a planned five-minute practice allocation. A constant does not turn into a measurement merely because it is stored in an array. With an explicit `dtype`, ensure the fill value can be represented without unwanted conversion or loss; for example, `dtype=np.int32` would not retain the fractional part of a value such as `2.5`.

| Need | Function | Example shape | All values initially |
|---|---|---|---|
| Clear numeric starting point | `np.zeros()` | `(2, 3)` | `0` |
| Multiplicative or counting starter | `np.ones()` | `(2, 3)` | `1` |
| A chosen constant | `np.full()` | `(2, 3)` | e.g. `5` |

The default type for `np.zeros` and `np.ones` is generally floating point; specify `dtype` when an integer representation matters. For `np.full`, the fill value influences the inferred type if `dtype` is omitted. Read `array.dtype` to verify the actual result.

## `np.empty()` does not mean zero

`np.empty(shape, dtype=...)` allocates an array **without initializing ordinary numerical elements to known values**. Here “empty” refers to *uninitialized content*, not necessarily an array with zero elements:

```python
buffer = np.empty((2, 3), dtype=np.int32)
print(buffer.shape, buffer.size)  # (2, 3) 6
# Do not print or calculate with its contents yet.

buffer[:] = 7  # Assign every element before reading any of them.
print(buffer.tolist())  # [[7, 7, 7], [7, 7, 7]]
```

Values seen before the assignment are not a reliable result. They depend on allocated storage and must not be treated as zeros, random samples, or recorded data. The safe rule is to **write every position before reading it**; use `np.zeros` or `np.full` if you need a known initial value. By contrast, `np.empty((0, 3), dtype=np.int32)` has zero elements because its *shape* contains zero. `np.empty((2, 3))` has six positions with unspecified initial content. NumPy may initialize certain object-containing types differently; the rule about not relying on initial content here concerns the ordinary numeric array shown above.

## Identity and diagonal arrays

A **diagonal** of a two-dimensional array contains positions where the row and column numbers are equal: `[0, 0]`, `[1, 1]`, and so on. An **identity matrix** is square, has ones on its main diagonal, and zeros elsewhere. It leaves a compatible vector unchanged under matrix multiplication, which is why it is called an identity.

```python
identity = np.identity(3, dtype=np.int32)
print(identity.tolist())
# [[1, 0, 0],
#  [0, 1, 0],
#  [0, 0, 1]]
```

`np.identity(n)` always makes a square `n × n` array. `np.eye(N, M=None, k=0, dtype=...)` is more flexible: it can have a different number of columns, and `k` moves the diagonal of ones. With the default `k=0`, it creates the same main-diagonal pattern for a square array:

```python
square_eye = np.eye(3, dtype=np.int32)
print(np.array_equal(identity, square_eye))  # True

wide_eye = np.eye(2, 3, dtype=np.int32)
print(wide_eye.tolist())  # [[1, 0, 0], [0, 1, 0]]

shifted = np.eye(3, k=1, dtype=np.int32)
print(shifted.tolist())  # [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
```

`wide_eye` and `shifted` are **identity-like patterns**, not square identity matrices. The `k=1` positions lie one column above the main diagonal. Do not infer that every call to `np.eye` produces an identity matrix in the algebraic sense. The exact choice depends on whether you need a square unchanged-under-multiplication operator or just a diagonal pattern.

## Guided lab

Download the [fixed-value array creation lab](QAI.02.02.05_Fixed_Value_Array_Creation_Lab.zip), unzip it, and run the files from its folder:

```sh
python fixed_value_arrays.py
python check_fixed_value_arrays.py
```

Use `python3` if appropriate. If NumPy is not installed in the interpreter running the lab, use `python -m pip install -r requirements.txt`. Predict each shape and filled result before running. The `np.empty` example does not inspect its uninitialized numbers; it assigns all entries and then verifies them.

**Controlled change:** replace the planned `np.full((3, 2), 5, dtype=np.int32)` with a value of `8`. Predict six eights, shape `(3, 2)`, and total `48`. Change only that input in a scratch copy and compare the run. Restore the supplied file before running its checker.

**Diagnose:** if you call `np.ones(3, dtype=np.int32)` while expecting three learners by two activities, inspect its shape `(3,)`. Repair the shape argument to `(3, 2)`; the result now has six ones. If you see arbitrary numbers after `np.empty((3, 2), dtype=np.int32)`, the repair is to initialize every position or choose a known-fill constructor; do not rely on whether the current run happens to show zero.

## Independent mini-project: an activity setup

For **two learners** and **three activities**, construct:

1. An `int32` array of zero recorded counts with shape `(2, 3)`.
2. An `int32` array giving every activity a starting weight of one.
3. An `int32` array assigning a planned duration of 7 minutes to every position.
4. An `int32` square identity matrix for the three activities, plus an `np.eye` array with two rows and three columns.
5. A numeric `np.empty((2, 3), dtype=np.int32)` buffer that you fully fill with 4 **before** reading it.

Predict all shapes, totals for the known-filled arrays, and where the diagonal ones appear. Run your own code, then compare with `mini_project_reference.py`.

**Expected results:** the first three arrays have shape `(2, 3)` and totals **0**, **6**, and **42**. The filled buffer has total **24** only *after* every value is assigned. The square identity has shape `(3, 3)` and main diagonal `[1, 1, 1]`; `np.eye(2, 3)` has shape `(2, 3)` and rows `[[1, 0, 0], [0, 1, 0]]`. Check the outputs and explain why the planned duration is not yet measured time. Keep a short record of your prediction, run result, changed input, and repaired shape or initialization error.

## Check your understanding

1. What does `(3, 2)` mean when passed as `shape`?
2. How do `np.zeros`, `np.ones`, and `np.full` differ?
3. Does `np.empty((2, 3))` have zero items? Are its initial numeric contents trustworthy?
4. What do you need to do before calculating with a numeric array created by `np.empty`?
5. Where are the ones in `np.identity(3)`? Why is `np.eye(2, 3)` not a square identity matrix?
6. What changes when `np.eye(3, k=1)` is used instead of `np.eye(3)`?

**Answers and reasoning**

1. Three positions along axis 0 and two along axis 1, so six elements.
2. They fill all positions with zero, one, or a chosen value, respectively.
3. It has six items. Their initial numeric values are unspecified and cannot be trusted.
4. Assign every element, or use a known-fill constructor instead.
5. `[0,0]`, `[1,1]`, and `[2,2]` hold ones. `np.eye(2, 3)` is rectangular and therefore is only an identity-like pattern.
6. The ones move one column above the main diagonal; the final row contains all zeros.

## Remember and retain

- **Shape first:** `(rows, columns)` determines positions; the function determines initial values.
- `zeros` → 0, `ones` → 1, `full` → chosen constant. Choose a `dtype` that preserves the values you intend.
- `empty` → allocated positions with unspecified initial numeric content. Fill before reading.
- `identity(n)` → square main diagonal; `eye` → configurable diagonal pattern.

## Further reading

- [NumPy array creation guide](https://numpy.org/doc/stable/user/basics.creation.html)
- [NumPy array creation functions](https://numpy.org/doc/stable/reference/routines.array-creation.html)
- [NumPy `empty` reference](https://numpy.org/doc/stable/reference/generated/numpy.empty.html)
