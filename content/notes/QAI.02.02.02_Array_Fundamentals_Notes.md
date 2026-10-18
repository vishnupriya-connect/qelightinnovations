# Array fundamentals

## A question about study time

Suppose three learners each record minutes spent on two activities:

| Learner | Reading | Practice |
|---|---:|---:|
| A | 20 | 10 |
| B | 30 | 15 |
| C | 40 | 20 |

The six measurements form a small rectangular arrangement. We want to keep their positions clear while calculating, for example, the total time for learner B. A **NumPy array** is an object that holds values in an organized arrangement and provides numerical operations on them. The NumPy class that represents it is called `ndarray` (short for “N-dimensional array”). **Array** may mean a general organized collection; here it means a NumPy `ndarray` unless stated otherwise.

```python
import numpy as np

minutes = np.array([[20, 10], [30, 15], [40, 20]], dtype=np.int32)
print(type(minutes))  # <class 'numpy.ndarray'>
print(minutes)
```

```text
[[20 10]
 [30 15]
 [40 20]]
```

`minutes` names the **array object**. Each stored entry is an **element** or **item**; the **value** of the first element is `20` minutes. In this example each item is an integer, and `np.int32` asks NumPy to store each as a 32-bit signed integer. The explicit data type makes later byte counts predictable. `np.array(...)` creates the object here; array creation methods receive fuller treatment in the later lesson on converting Python collections.

## Locate an element

An **index** identifies a position. NumPy starts counting positions at **0**. For this rectangular array, provide two indexes: first the learner's position, then the activity's position.

```python
print(minutes[0, 0])  # 20: A, reading
print(minutes[1, 0])  # 30: B, reading
print(minutes[1, 1])  # 15: B, practice
print(minutes[2, 1])  # 20: C, practice
print(minutes[1, 0] + minutes[1, 1])  # 45 minutes for B
```

**Trace:** `minutes[1, 0]` means the second learner and first activity. The indexes are positions, while `30` is the value found there. The labels A, B, C, Reading, and Practice are explanations outside this numerical array; the array itself stores the six numbers. An index that lies outside a dimension raises `IndexError`: `minutes[3, 0]` asks for a fourth learner, but there are only three.

## Read the object's structure

An array **dimension** is one independent position needed to locate an item. Our array needs two positions. The **number of dimensions**, reported by `ndim`, is therefore 2. The **shape** says how many positions exist along each dimension: `(3, 2)` means three learner positions and two activity positions. Shape is a tuple (an ordered group of numbers); `(3, 2)` is different from `(2, 3)`.

The **size**, also called the **number of elements**, counts *all* stored items, not just the number of learners. For this shape it is `3 × 2 = 6`.

```python
print(minutes.ndim)   # 2
print(minutes.shape)  # (3, 2)
print(minutes.size)   # 6
```

For any array, `len(array.shape) == array.ndim` and the product of the shape lengths equals `array.size`. A simple one-dimensional array `np.array([20, 30, 40])` has `ndim == 1`, `shape == (3,)`, and `size == 3`. The comma in `(3,)` marks a one-entry tuple. More dimensions do **not** necessarily mean more total items: a `(2, 3)` array and a `(6,)` array each have six.

## Read the stored type and bytes per item

The **array data type**, `dtype`, describes how NumPy interprets its items. For our explicit `np.int32` choice, `minutes.dtype` displays `int32`. An array normally has one data type for its items; placing a fractional number into an integer array may lose the fractional part. Always check the type before trusting an interpretation.

The **array item size**, `itemsize`, is the number of **bytes per element**, not the number of elements. A byte is a unit of computer storage; eight bits make one byte. `int32` takes 32 bits, or 4 bytes, per item here.

```python
print(minutes.dtype)     # int32
print(minutes.itemsize)  # 4
print(minutes.size * minutes.itemsize)  # 24 bytes of array element data
```

The product is the element-data byte count (`minutes.nbytes` is also 24 here). It does **not** claim that the whole Python and NumPy object occupies only 24 bytes; metadata and other storage have their own costs. Likewise, the value `40` does not use 40 bytes. A separate array declared with `dtype=np.float64` uses eight bytes for each item, even if one value looks like `20.0`. On another machine, an *inferred* integer type may vary; use the explicit types here for reproducible checks.

| Property | Ask | Example answer |
|---|---|---|
| `ndim` | How many position numbers locate an element? | `2` |
| `shape` | How many positions along each dimension? | `(3, 2)` |
| `size` | How many elements in total? | `6` |
| `dtype` | How is an element represented? | `int32` |
| `itemsize` | How many bytes per element? | `4` |

## Change one value and predict what stays fixed

We want B's practice time to be 18 rather than 15 minutes. Make an independent copy so the original measurement table remains available:

```python
revised = minutes.copy()
revised[1, 1] = 18
print(revised[1, 0] + revised[1, 1])  # 48
print(minutes[1, 1])                  # 15 (original)
print(revised.shape, revised.size, revised.dtype, revised.itemsize)
# (3, 2) 6 int32 4
```

Changing an item changes its **value**, but does not change the number or layout of positions or the array's declared data type. A tempting mistake is to write `revised = minutes` and expect an independent second array: that only gives the *same object* another name. Use `.copy()` when you need to preserve the original values. If you ask for `[3, 0]`, diagnose the error by inspecting `shape`: the first index must be 0, 1, or 2, and the second must be 0 or 1.

## Guided lab and mini-project

Download the [array fundamentals lab](QAI.02.02.02_Array_Fundamentals_Lab.zip), unzip it, and run these commands from its folder:

```sh
python array_fundamentals.py
python check_array_fundamentals.py
```

Use `python3` if necessary. If NumPy is missing in that interpreter, run `python -m pip install -r requirements.txt`. The main program prints the original structure, B's total of 45, the revised total of 48, the unchanged original value 15, and the invalid-index error. The checker tests these outcomes and an empty array boundary.

**Guided change:** in a separate scratch copy, revise C's reading value from 40 to 50. Predict C's new total: `50 + 20 = 70`. The revised array still has shape `(3, 2)`, size `6`, data type `int32`, and item size `4`. Run your copy and compare; restore the supplied file before checking it.

**Independent mini-project:** a small workshop has two learners with three recorded tasks each. Create an `int32` NumPy array with values `[[12, 8, 5], [10, 15, 5]]`. Without copying the example's output, print the array type, its five structural properties, the second learner's second value, and that learner's total. Preserve the original, make a copy, change the first learner's last value to 9, and show the original and revised first-learner totals. Record one invalid index, the resulting exception, and the correct index range. Use `mini_project_reference.py` only *after* your independent attempt.

**Expected mini-project results:** type `numpy.ndarray`; `ndim=2`, `shape=(2, 3)`, `size=6`, `dtype=int32`, `itemsize=4`; selected value `15`; second learner total `30`; first learner total changes from `25` to `29`, while the original stays `25`; `[2, 0]` raises `IndexError` because the first index can only be 0 or 1. The data portion is `6 × 4 = 24` bytes. A successful solution shows these values by running the code and explains why the changed value does not change shape or dtype.

## Check your understanding

1. In `minutes[1, 0]`, which parts are indexes and which number is the stored value?
2. What is the difference between `ndim`, `shape`, and `size` for `minutes`?
3. If the shape is `(4, 2)`, what is the size? Is `[4, 0]` valid?
4. What do `dtype=int32` and `itemsize=4` mean here? Does `size * itemsize` describe all Python object overhead?
5. After `other = minutes`, what happens to `minutes` if you assign `other[0, 0] = 99`? How can you avoid that?
6. If `minutes[1, 1]` changes from 15 to 18, what are B's total and the array's shape?

**Answers and reasoning**

1. `1` and `0` are positions; the value there is `30`.
2. Two indexes locate an item, so `ndim=2`. There are three positions along the first dimension and two along the second, so `shape=(3, 2)`. There are six items in total, so `size=6`.
3. `4 × 2 = 8` items. `[4, 0]` is outside the first index range `0..3`.
4. Items are represented as 32-bit signed integers taking four bytes each. The product measures element data, not all object overhead.
5. Both names refer to the same array, so its first value becomes 99. Use `other = minutes.copy()` to preserve the original.
6. `30 + 18 = 48` minutes; the shape remains `(3, 2)`.

## Remember and retain

- **Object → positions → values:** the `ndarray` stores items; zero-based indexes locate them.
- **Shape → dimensions → count:** `len(shape) == ndim`, and multiplying shape lengths gives `size`.
- **Type → bytes:** `dtype` describes item representation; `itemsize` counts bytes per item, not items.
- Keep your prediction, run result, copied-array variation, and repaired invalid-index example so you can explain them to another learner.

## Further reading

- [NumPy quickstart: ndarray attributes](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy array objects](https://numpy.org/doc/stable/reference/arrays.html)
- [NumPy absolute basics](https://numpy.org/doc/stable/user/absolute_beginners.html)
