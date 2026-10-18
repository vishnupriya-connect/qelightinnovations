# One-dimensional indexing

## Locate a value in a sequence

Suppose four days of practice lasted **12, 18, 15, and 20 minutes**. A one-dimensional array holds those four values in order:

```python
import numpy as np

minutes = np.array([12, 18, 15, 20], dtype=np.int32)
print(minutes.shape, minutes.size)  # (4,) 4
```

An **index** is a position used to locate an element. The **indexed value** is what is stored at that position. NumPy's first position is **0**, so `minutes[0]` is `12`, not `18`. The last nonnegative position is `size - 1`, which is `3` here.

| Day in ordinary counting | Nonnegative index | Negative index | Value |
|---:|---:|---:|---:|
| 1 | `0` | `-4` | `12` |
| 2 | `1` | `-3` | `18` |
| 3 | `2` | `-2` | `15` |
| 4 | `3` | `-1` | `20` |

The **first index** is `0`; `-1` is the **last index** when the array is nonempty. A **positive index** such as `2` counts from the start (with zero as the first position). A **negative index** counts back from the end: `-1` is last, `-2` second-last. For a length of four, `minutes[-2]` and `minutes[2]` identify the same element, `15`. An index is not the day label or minute amount; it is a position.

## Read an element

**Element access** means using an index to get a stored value:

```python
print(minutes[0])          # 12
print(minutes[2])          # 15
print(minutes[-1])         # 20
print(minutes[minutes.size - 1])  # 20
```

The single accessed value is a NumPy scalar of this array's item type, rather than a one-element array. If you want an ordinary Python integer for display or a small interface, `int(minutes[2])` returns `15`; the original array stays unchanged. When the array may be empty, check `minutes.size > 0` before requesting a first or last item.

## Boundaries and a useful error

For an array of length `n`, valid nonnegative indexes are `0` through `n - 1`; valid negative indexes are `-n` through `-1`. Here the allowed ranges are `0..3` and `-4..-1`.

```python
print(minutes[-4])  # 12: earliest valid negative index
print(minutes[3])   # 20: last valid nonnegative index

minutes[4]   # IndexError: beyond the final position
minutes[-5]  # IndexError: before the earliest position
```

Those last two lines are examples to try separately in the lab; they stop execution if uncaught. An **index out of bounds** means the requested position does not exist. Diagnose it with `shape` or `size` and the intended meaning of the index. Do not silently replace an invalid requested day with the last day: that would answer a different question. A zero-length array has no valid element index, including `0` and `-1`.

## Update one stored value

An array is mutable. **Element assignment** or an **indexed update** writes to a selected position:

```python
corrected = minutes.copy()
corrected[2] = 17
print(corrected.tolist())  # [12, 18, 17, 20]
print(minutes.tolist())    # [12, 18, 15, 20]
```

The third day's value changes from 15 to 17 in the copy. The array's shape, size, and dtype remain `(4,)`, `4`, and `int32`. Negative indexing also works for assignment:

```python
corrected[-1] = 22
print(corrected.tolist())  # [12, 18, 17, 22]
```

`corrected = minutes` alone would make a second name for the **same array**; changing through one name would be visible through the other. Use `.copy()` if the original measurements must remain available. If your task is to correct the authoritative source itself, assigning directly to `minutes[2]` deliberately changes that source. Make that decision from the task, not by accident. An assigned value is represented using the array's dtype; investigate incompatible or lossy values rather than assuming the stored result equals what was requested.

## Trace a repair

A request says “show day 4,” but the code uses `minutes[4]`. The programmer has confused the human day number with the zero-based position. Trace the mapping: day 1 → index 0, day 2 → 1, day 3 → 2, day 4 → 3. Repair the expression to `minutes[3]` (or `minutes[-1]` for the last value), which gives **20**. Before using `-1` in other code, be clear whether the requirement is “last element” or a specific labelled day; those may differ when more days are added.

## Guided lab

Download the [one-dimensional indexing lab](QAI.02.02.09_One_Dimensional_Indexing_Lab.zip), unzip it, and run in its folder:

```sh
python one_dimensional_indexing.py
python check_one_dimensional_indexing.py
```

Use `python3` if appropriate. If NumPy is missing in that interpreter, run `python -m pip install -r requirements.txt`. Predict all first, last, second-last, and updated values before running. The checker verifies the positive/negative index pairs, original-versus-copy behavior, invalid boundaries, and the empty-array case.

**Controlled change:** after copying, change day 3 from `15` to `19` using index `2` and independently read it with index `-2`. Both accesses should give **19**; the original remains **15** at those positions. The changed array retains size **4**. Run the supplied helper with `new_value=19` and compare.

**Debugging practice:** try to read index `4` and `-5`, recording both errors. Inspect `size == 4`, then repair the intended “day 4” read to index `3` and the intended “first day” read to `-4` or `0`. Keep the failed expression, diagnosis, corrected expression, and observed value.

## Independent mini-project: five-session log

Create an `int32` array of session minutes `[25, 30, 20, 35, 15]`. Without looking at the reference program, show first, last, and second-last values using both a nonnegative and a negative index for each. Report the original total. Make an independent copy; correct the first session to **28** and last session to **18**, once with a nonnegative index and once with a negative index. Report both arrays and the new total. Then test one out-of-bounds access and explain the valid ranges. Compare with `mini_project_reference.py` after your own attempt.

**Expected results and self-check:** first **25** (`0` or `-5`), last **15** (`4` or `-1`), second-last **35** (`3` or `-2`); original total **125**. The copy is `[28, 30, 20, 35, 18]` with total **131**, while the source remains `[25, 30, 20, 35, 15]`. Valid positions are `0..4` and `-5..-1`; `5` or `-6` raises `IndexError`. A complete record includes a prediction, actual output, the unchanged source, and a repaired out-of-bounds attempt.

## Check your understanding

1. Why does `minutes[0]` refer to the first day rather than `minutes[1]`?
2. Which nonnegative position is equivalent to `minutes[-2]` in a length-four array?
3. Are indexes `4` and `-5` valid when the array has four items?
4. How does `corrected = minutes.copy()` differ from `corrected = minutes`?
5. After updating `corrected[2]` to `17`, what changes about its shape and size?
6. Why does `minutes[-1]` fail if `minutes` is empty?

**Answers and reasoning**

1. Indexing starts at zero: positions 0, 1, 2, 3 correspond to days 1, 2, 3, 4.
2. Index `2`, the third value, which is initially `15`.
3. No. The allowed ranges are `0..3` and `-4..-1`, so both requests raise `IndexError`.
4. `.copy()` creates an independent array; plain assignment gives the same array a second name.
5. Only the stored value changes; shape `(4,)` and size `4` stay the same.
6. An empty array has no first or last element to locate.

## Remember and retain

- **Day number → position:** for a sequence starting with day 1, subtract one to obtain the zero-based index.
- **Negative index:** `-1` means last, `-2` second-last, down to `-n` for the first of `n` values.
- **Read versus assign:** `a[i]` retrieves a value; `a[i] = value` updates it. Copy first when preserving the source matters.
- Check `size` and intended labels before repairing an out-of-bounds index. Keep the mapping and correction trace for later review.

## Further reading

- [NumPy indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy absolute basics: indexing](https://numpy.org/doc/stable/user/absolute_beginners.html)
