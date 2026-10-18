# Array reshaping

## Arrange the same values into a new shape

Suppose six task durations are stored in one sequence. We want to display them as two learners with three tasks each:

```python
import numpy as np

values = np.array([10, 20, 30, 40, 50, 60], dtype=np.int32)
table = values.reshape(2, 3)
print(values.shape, table.shape)  # (6,) (2, 3)
print(table.tolist())             # [[10, 20, 30], [40, 50, 60]]
```

**Reshape** changes how positions are organized into axes. The **original shape** is `(6,)`; the **target shape** is `(2, 3)`. The values stay in their ordinary row-by-row order for these examples. A target is **compatible** when its dimension lengths multiply to the same number of elements: `2 × 3 = 6`. `reshape()` returns an array with the new shape; it does not change `values.shape` in this example.

Another compatible choice, `(3, 2)`, groups the values differently:

```python
print(values.reshape(3, 2).tolist())
# [[10, 20], [30, 40], [50, 60]]
```

Changing a shape does not rearrange values to match a business label. If the original six values mean different things, decide which axis should represent learner or task *before* reshaping. Reshape is not the same as swapping the axes of an existing table; that is treated in the next lesson.

## Count elements first

For six items, `(2, 3)`, `(3, 2)`, `(1, 6)`, and `(6, 1)` are compatible. `(4, 2)` is not, since it requires eight items:

```python
values.reshape(4, 2)  # ValueError: cannot reshape six elements into eight slots
```

The error indicates an inconsistent target shape. Investigate whether the data are incomplete or the intended shape is mistaken. Do not silently duplicate or discard observations merely to satisfy a requested shape.

`-1` asks NumPy to infer **one dimension** from the element count and the other supplied lengths:

```python
print(values.reshape(2, -1).shape)  # (2, 3)
print(values.reshape(-1, 3).shape)  # (2, 3)
```

With six elements and two rows, the inferred length is `6 / 2 = 3`. Only one target dimension may be `-1`; two unknown dimensions cannot be inferred uniquely. If the count is not divisible by the known lengths, the shape is incompatible. An **inferred dimension** is a computed axis length, not an instruction to create missing data.

## Flatten and ravel: one dimension again

To **flatten** an array is to represent its values along one axis. Both `.flatten()` and `.ravel()` produce a **flattened array** of shape `(size,)` in default row-by-row order:

```python
table = np.array([[10, 20, 30], [40, 50, 60]], dtype=np.int32)
flat_copy = table.flatten()
flat_maybe_view = table.ravel()
print(flat_copy.tolist(), flat_copy.shape)       # [10, 20, 30, 40, 50, 60] (6,)
print(flat_maybe_view.tolist(), flat_maybe_view.shape)  # same values and shape
```

The data relationship differs: `.flatten()` **always returns a copy**. `.ravel()` returns a **view where possible**, otherwise a copy. For this regular table, it shares element memory with `table`:

```python
print(np.shares_memory(table, flat_copy))       # False
print(np.shares_memory(table, flat_maybe_view)) # True for this example
```

For a non-contiguous selection such as `table[:, ::2]`, `ravel()` may need a copy. Do not assume it always shares memory. If you need an independent flattened numeric result, use `.flatten()` or an explicit `.copy()` and verify before editing. If you need to avoid an unnecessary copy, `ravel()` is useful, but account for possible shared mutation.

## Can reshape itself share memory?

`values.reshape(2, 3)` gives a new array object, but for a regular contiguous array it can be a **view** sharing numerical data:

```python
values = np.array([10, 20, 30, 40, 50, 60], dtype=np.int32)
table = values.reshape(2, 3)
print(table is values)                    # False
print(np.shares_memory(table, values))   # True in this example
```

In a different layout, reshape may have to copy instead. Do not infer independence or sharing from the word “reshape.” Check memory sharing if a later mutation matters, and call `.copy()` when you require an independent trial. The visible values and target shape alone do not reveal ownership.

## `resize()` and shape assignment change the object

There are two more ways to change a shape, with different effects. `ndarray.resize()` modifies the **same array object** and may change its number of elements. In this fresh, owning array, expanding from six to eight items fills the new numeric slots with zeros:

```python
growing = np.array([10, 20, 30, 40, 50, 60], dtype=np.int32)
growing.resize((2, 4))
print(growing.tolist(), growing.shape)
# [[10, 20, 30, 40], [50, 60, 0, 0]] (2, 4)
```

The two added zeros are **new initialized slots**, not observed study durations. `resize()` can fail when an array does not own suitable memory or has other references; do not bypass its safety checks casually. It differs from `np.resize(array, new_shape)`, a separate function that can repeat input values to fill a larger result. Do not treat either behavior as a way to invent real measurements.

An existing array's `shape` attribute can sometimes be assigned directly when the element count stays the same and no copy is needed:

```python
owning = np.array([10, 20, 30, 40, 50, 60], dtype=np.int32)
owning.shape = (3, 2)
print(owning.tolist())  # [[10, 20], [30, 40], [50, 60]]
```

This **shape assignment** changes the same object's shape. It may fail for an incompatible shape or layout requiring a copy. Use `reshape()` when you want an explicit result and predictable error handling; use in-place mutation only when you intend to change the existing object and have checked who else may reference it.

| Operation | Element count | Changes source object? | Element sharing |
|---|---|---|---|
| `a.reshape(...)` | Preserved | No shape change to `a` | View if possible, otherwise copy |
| `a.flatten()` | Preserved | No | Independent copy |
| `a.ravel()` | Preserved | No | View if possible, otherwise copy |
| `a.resize(...)` | May change | Yes | Mutates `a`; subject to ownership/reference checks |
| `a.shape = ...` | Preserved | Yes | Same object; fails if in-place reshape impossible |

## Guided lab

Download the [array reshaping lab](QAI.02.02.15_Array_Reshaping_Lab.zip), unzip it, and run in its folder:

```sh
python array_reshaping.py
python check_array_reshaping.py
```

Use `python3` if needed. If NumPy is absent in the interpreter running the lab, install it with `python -m pip install -r requirements.txt`. Predict shape and value order before running. The checker covers compatible and incompatible shapes, one inferred dimension, flattened results, memory sharing in the supplied layouts, and in-place `resize` and shape assignment on separate fresh arrays.

**Controlled change:** take eight values `[1, 2, 3, 4, 5, 6, 7, 8]` and request `reshape(2, -1)`. Predict shape `(2, 4)` and rows `[1, 2, 3, 4]` and `[5, 6, 7, 8]`. Try `reshape(3, -1)` and diagnose the incompatible count. Preserve the original sequence while investigating.

**Debugging practice:** attempt `values.reshape(4, 2)` with six values. Record the `ValueError`, compare required `4 × 2 = 8` with available `6`, then repair the target to `(2, 3)` if that is what the data mean. Do not use `resize` to make the error disappear without obtaining the missing measurements.

## Independent mini-project: inspect a score grid

Start with the six-value `int32` array `[10, 20, 30, 40, 50, 60]`. Independently produce a `(2, 3)` table, a `(3, 2)` table, and a `(2, -1)` table; report the actual shapes and rows, and show that the original still has shape `(6,)`. Flatten the `(2, 3)` table with both methods, report their values, and test memory sharing with the table. In *separate fresh arrays*, demonstrate `.resize((2, 4))` and `.shape = (3, 2)`, naming which changes the element count. Compare with `mini_project_reference.py` after your own attempt.

**Expected results and self-check:** `(2, 3)` gives `[[10, 20, 30], [40, 50, 60]]`; `(3, 2)` gives `[[10, 20], [30, 40], [50, 60]]`; `(2, -1)` infers `(2, 3)`. Both flattened results are `[10, 20, 30, 40, 50, 60]`; for the supplied contiguous table, `flatten` does not share data, while `ravel` does. Fresh `resize((2, 4))` yields `[[10, 20, 30, 40], [50, 60, 0, 0]]`; fresh shape assignment yields `(3, 2)` with six items. Keep predictions, run results, the incompatible-shape repair, and one explanation of why new zero slots are not measurements.

## Check your understanding

1. Why is `(2, 3)` compatible with six elements but `(4, 2)` is not?
2. What does `-1` mean in `values.reshape(2, -1)`?
3. Does `reshape()` necessarily allocate independent element data?
4. What is the practical difference between `.flatten()` and `.ravel()` when you edit the result?
5. How does `a.resize((2, 4))` differ from `a.reshape(2, 4)` for a six-element array?
6. What can be changed by `a.shape = (3, 2)`?

**Answers and reasoning**

1. `2 × 3 = 6`; `4 × 2 = 8` would require two additional elements.
2. Infer the one unspecified dimension from six total items and the known length two; it becomes three.
3. No. It can return a view sharing data when possible, or a copy if needed.
4. `flatten` returns an independent copy; `ravel` may share element memory, so editing it can change the source in the regular-table example.
5. `resize` mutates the owning array and can add initialized slots; `reshape` preserves six elements and rejects the eight-slot target.
6. The existing object's shape, when compatible and possible in place; its element count remains six.

## Remember and retain

- **Count first:** the product of target shape lengths must equal the original size for reshaping.
- One `-1` can be inferred; it does not create data.
- `flatten` copies; `ravel` and `reshape` may share memory. Inspect before editing.
- `ndarray.resize` can change the element count in place; shape assignment changes layout in place without changing count. Keep your failure-and-repair trace for review.

## Further reading

- [NumPy `reshape`](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)
- [NumPy quickstart: shape-changing operations](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy copies and views](https://numpy.org/doc/stable/user/basics.copies.html)
- [NumPy `ndarray.resize`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.resize.html)
