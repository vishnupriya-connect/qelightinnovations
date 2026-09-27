# Array inspection

## Inspect before calculating

Suppose a table should hold **three learners × two activities** of study minutes. A calculation may run even when the axes are reversed or the values use an unintended type. Inspect the array's **representation** (what is displayed) and its structural properties before interpreting its results.

```python
import numpy as np

minutes = np.array([[20, 10], [30, 15], [40, 20]], dtype=np.int16)
print(minutes)
```

```text
[[20 10]
 [30 15]
 [40 20]]
```

`print(minutes)` displays an easy-to-read arrangement. `repr(minutes)` provides a Python-oriented representation, including `array(...)` syntax; for an explicit nondefault type, it can also show that type. The display is useful for a small array, but printing values alone does not tell us what a row or column *means*. It may also be shortened for large arrays. Read properties and keep the axis meanings alongside the data.

## Six properties and what they answer

The properties below belong to the array object. They are **attributes**, so use `minutes.shape`, for example, rather than `minutes.shape()`.

```python
print(minutes.shape)     # (3, 2)
print(minutes.ndim)      # 2
print(minutes.size)      # 6
print(minutes.dtype)     # int16
print(minutes.itemsize)  # 2
print(minutes.nbytes)    # 12
```

| Inspection | Meaning | In this example |
|---|---|---|
| `shape` | Length along each axis, in order | `(3, 2)` = three learners, two activities |
| `ndim` | Number of axes or dimensions | `2` |
| `size` | Total number of elements | `3 × 2 = 6` |
| `dtype` | How each item is represented | `int16`, a 16-bit signed integer type |
| `itemsize` | Bytes per array item | `2` bytes |
| `nbytes` | Bytes for the array elements | `6 × 2 = 12` bytes |

The two checks `len(minutes.shape) == minutes.ndim` and `minutes.size * minutes.itemsize == minutes.nbytes` should hold. Multiplying all the shape lengths also gives `size`; a shape `()` represents a zero-dimensional array with one element, so that case has size 1. `nbytes` reports **element-data bytes**. It does not include all NumPy object metadata, every referenced Python object, or other process memory, and does not by itself tell whether a view owns separate storage. It is a useful size comparison, not a full memory profiler.

## Inspect a problem, not just the numbers

Two arrays can have **the same size and element bytes** but mean different things:

```python
correct = np.array([[20, 10], [30, 15], [40, 20]], dtype=np.int16)
reversed_axes = np.array([[20, 10, 30], [15, 40, 20]], dtype=np.int16)
print(correct.shape, reversed_axes.shape)  # (3, 2) (2, 3)
print(correct.size, reversed_axes.size)    # 6 6
print(correct.nbytes, reversed_axes.nbytes)  # 12 12
```

If the first axis must be learners and the second activities, only `(3, 2)` matches the agreed layout. `size == 6` alone cannot validate that meaning. Conversely, two arrays can have the **same shape and values** but a different representation:

```python
wide = correct.astype(np.int32)
print(wide.shape, wide.size)          # (3, 2) 6
print(wide.dtype, wide.itemsize, wide.nbytes)  # int32 4 24
```

The values still read the same, but each `int32` element takes four bytes instead of two. Inspecting `dtype` is also necessary because numerical range and precision depend on the type. This comparison is not a recommendation to use the smallest type indiscriminately; choose one that can represent the valid values. Type conversion and its possible loss are treated in the next lesson.

## Display and representation

To **display an array** is to show its values for a person. These methods serve different needs:

```python
print(minutes)           # compact NumPy display
print(repr(minutes))     # representation useful for inspection
print(minutes.tolist())  # ordinary nested Python lists
```

For this small array the three outputs show the same numbers in different forms. `.tolist()` converts values into Python lists and is convenient for testing or simple exchange, but the resulting list no longer carries the array's `dtype`, `shape`, or NumPy methods. A screen display is not proof of the original representation: inspect the actual object before applying operations. If the array is large, output may be abbreviated; report the structural attributes rather than pasting many rows.

## Boundary cases

```python
single = np.array(7, dtype=np.int16)
empty_rows = np.empty((0, 2), dtype=np.int16)
print(single.shape, single.ndim, single.size, single.nbytes)  # () 0 1 2
print(empty_rows.shape, empty_rows.ndim, empty_rows.size, empty_rows.nbytes)
# (0, 2) 2 0 0
```

The zero-dimensional array holds one value. The `(0, 2)` array has two axes but zero elements, so its element-data byte count is zero. The `np.empty` call here has **no elements**; for a *nonzero* shape, `np.empty` would have unspecified numeric contents until initialized. Neither zero dimensions nor zero element bytes is a reason to assume the same situation as the other.

## Guided lab

Download the [array inspection lab](QAI.02.02.07_Array_Inspection_Lab.zip), unzip it, and run from its folder:

```sh
python array_inspection.py
python check_array_inspection.py
```

Use `python3` if appropriate. If NumPy is absent in the interpreter running the lab, install it with `python -m pip install -r requirements.txt`. Before running, predict the six properties for the `(3, 2)` `int16` example, then for the same values stored as `int32`. The checker verifies shapes, bytes, scalar and zero-element boundaries, and a validation function that raises a useful error for wrong shape or type.

**Controlled change:** make an `int32` copy of the `(3, 2)` `int16` data. Predict unchanged shape `(3, 2)` and size 6; `itemsize` rises from 2 to 4 and `nbytes` from 12 to 24. Compare the actual inspection. Then substitute the `(2, 3)` arrangement. It still has six elements and 12 bytes in `int16`, but the expected-shape check rejects it.

**Repair a mistake:** if a learner reports that `(2, 3)` is correct because `size == 6`, use the stated learner/activity axis meanings to repair the expected shape to `(3, 2)` and inspect it again. If `dtype` differs while shape matches, inspect `dtype` and the allowed measurement range before choosing a correction; the next lesson covers conversion in detail. Record expected versus observed values and the property that exposed the mismatch.

## Independent mini-project: inspect a results grid

Build a `float32` grid with **three days × four learners**. Use these rows:

```python
[[1.5, 2.0, 2.5, 3.0],
 [2.5, 3.0, 3.5, 4.0],
 [3.5, 4.0, 4.5, 5.0]]
```

Display the grid, write its representation and all six properties, and calculate the expected `nbytes` by hand. Make a `float64` version with the same values and compare its properties. Then create a `(4, 3)` arrangement of twelve values and explain why a days-by-learners shape check rejects it even if its size remains twelve. Try the validator in the lab, and only after your independent attempt compare with `mini_project_reference.py`.

**Expected results:** `float32` has `shape=(3, 4)`, `ndim=2`, `size=12`, `dtype=float32`, `itemsize=4`, `nbytes=48`. The `float64` version has unchanged shape, dimensions, and size, but `itemsize=8` and `nbytes=96`. The reversed layout `(4, 3)` still has 12 values; a correct validator rejects its shape. A complete record includes the two displays or representations, predicted and actual attributes, a mismatch diagnosis, and a short explanation of why `nbytes` is not the entire application's memory use.

## Check your understanding

1. For a shape `(3, 2)`, what do `ndim` and `size` report?
2. Why cannot `size=6` prove that a grid has three learners and two activities?
3. How do `itemsize` and `nbytes` differ for six `int16` items?
4. Does `nbytes=12` include all object metadata and application memory?
5. Why can `.tolist()` be useful while not preserving the array's `dtype` information?
6. Compare the `(0, 2)` array with a zero-dimensional one-element array.

**Answers and reasoning**

1. `ndim=2`, `size=3 × 2=6`.
2. `(2, 3)` also has six elements; the axis order has a different meaning.
3. `itemsize=2` bytes per element; `nbytes=6 × 2=12` bytes for elements.
4. No. It counts element data as defined by the array, not all surrounding memory.
5. It creates ordinary Python lists for display or comparison; lists do not carry an `ndarray`'s `dtype` attribute.
6. `(0, 2)` has two axes and no elements (`size=0`, `nbytes=0`); shape `()` has no axes but one value (`size=1`).

## Remember and retain

- **Meaning first:** label each axis, then check `shape`, `ndim`, and `size`.
- **Representation next:** check `dtype` and `itemsize`, then `nbytes = size × itemsize`.
- Display helps investigation; it does not replace structural inspection or account for all process memory.
- Keep your two type comparisons and the repaired wrong-shape diagnosis for later review.

## Further reading

- [NumPy quickstart: ndarray attributes](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy `ndarray.nbytes` reference](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.nbytes.html)
- [NumPy array objects](https://numpy.org/doc/stable/reference/arrays.html)
