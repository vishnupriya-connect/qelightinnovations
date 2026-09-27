# Array references, views, and copies

## Three ways to derive an array name

Suppose a four-day study log contains `[10, 20, 30, 40]` minutes. You want to inspect or edit a smaller part while preserving the original record. Before editing, find out whether your second name refers to the same object, to a view of its data, or to independent storage.

```python
import numpy as np

original = np.array([10, 20, 30, 40], dtype=np.int32)
alias = original
view = original[1:3]
independent = original[1:3].copy()
```

| Expression | Result | Same array object? | Shared element data? |
|---|---|---|---|
| `alias = original` | Another **reference** or **alias** | Yes | Yes |
| `view = original[1:3]` | New array **view** of positions 1 and 2 | No | Yes |
| `independent = original[1:3].copy()` | New numeric array **copy** | No | No |

An **array reference** is a Python name that points to an array object. **Object identity** asks whether two names point to the *same object*. `alias is original` is `True`, but `view is original` and `independent is original` are `False`. Different objects can still share the same underlying element data. That is the central difference between identity and shared memory.

## Alias: same object, shared mutation

`alias = original` does not construct a second array. Both names identify the same object, so an **array mutation** through either name changes what the other sees:

```python
alias = original
print(alias is original)  # True
alias[0] = 11
print(original.tolist())  # [11, 20, 30, 40]
```

This is **aliasing** and **shared mutation**. Assigning a new name is cheap and useful when shared editing is intended, but it is not a backup. For the rest of the examples, start again with a fresh `[10, 20, 30, 40]` array so each outcome can be traced separately.

## Slice or `.view()`: different object, shared data

A basic slice creates a **view-based slice**. A view is a derived array object that reads from, and can write into, the original numeric data:

```python
original = np.array([10, 20, 30, 40], dtype=np.int32)
middle = original[1:3]
print(middle.tolist())                      # [20, 30]
print(middle is original)                   # False
print(np.shares_memory(middle, original))  # True
middle[0] = 25
print(original.tolist())                    # [10, 25, 30, 40]
```

The mutation to the view's position 0 changes the source's position 1. NumPy's `.view()` explicitly creates another array object sharing data without selecting a smaller region:

```python
original = np.array([10, 20, 30, 40], dtype=np.int32)
whole_view = original.view()
print(whole_view is original)                   # False
print(np.shares_memory(whole_view, original))  # True
whole_view[-1] = 45
print(original.tolist())                       # [10, 20, 30, 45]
```

Both directions matter: changing the source later is also visible through a view of the affected values. `np.shares_memory(a, b)` can check actual overlap for these ordinary arrays. Merely checking `a is b` cannot decide whether data are shared. A view can avoid copying data and can be useful for efficient inspection, but its effect on a source must be intentional. The full rules for every possible indexing operation are broader; here we focus on basic slices and `.view()`.

## `.copy()`: independent numeric storage

To edit part of a numeric array without changing the original, copy the selected part:

```python
original = np.array([10, 20, 30, 40], dtype=np.int32)
snapshot = original[1:3].copy()
print(np.shares_memory(snapshot, original))  # False
snapshot[0] = 25
print(snapshot.tolist())  # [25, 30]
print(original.tolist())  # [10, 20, 30, 40]
```

The **original array** and **derived array** now have independent element storage for these numeric values. `original.copy()` copies the entire array instead of the selected region. A copy costs time and memory proportional to the data copied, so use one when independent editing or preservation is needed. A view avoids that copy but can create a surprising link to the source. `nbytes` for a view describes the bytes in its elements, not proof that those bytes were allocated again.

## The object-array exception: shallow versus deep copy

An array with `dtype=object` can hold references to mutable Python objects, such as dictionaries containing lists. `array.copy()` duplicates the array's *slots* but does not recursively copy the objects stored in those slots. This is a **shallow copy** of an object array:

```python
import copy

records = np.empty(1, dtype=object)
records[0] = {"minutes": [10, 20]}
shallow = records.copy()
print(np.shares_memory(records, shallow))  # False: separate array slots
print(shallow[0] is records[0])             # True: same dictionary
shallow[0]["minutes"].append(30)
print(records[0]["minutes"])              # [10, 20, 30]
```

For an independent nested snapshot, use a **deep copy** when the contained Python objects support it:

```python
deep = copy.deepcopy(records)
deep[0]["minutes"].append(40)
print(deep[0]["minutes"])     # [10, 20, 30, 40]
print(records[0]["minutes"])  # [10, 20, 30]
```

`copy.deepcopy` recursively copies supported nested objects. It is more costly and can be inappropriate for resources that cannot or should not be copied. A regular numerical array does not need this extra step to make its ordinary numeric elements independent. **Deep copy** here refers to the nested Python objects, not a different kind of numerical `ndarray.copy()` operation.

## Diagnose a changed source

An engineer says, “I made a backup with `backup = original`; why did it change?” That expression creates a **shared reference**. Inspect `backup is original`, then repair with `backup = original.copy()` for a numerical backup. If a sliced selection unexpectedly changes the source, inspect `np.shares_memory(selection, original)` and make `selection = original[start:stop].copy()` *before* editing. Copying after the source has already been changed does not restore the earlier values; preserve the original or reload it from a trustworthy source.

## Guided lab

Download the [array references, views, and copies lab](QAI.02.02.12_Array_References_Views_and_Copies_Lab.zip), unzip it, and run from its folder:

```sh
python array_references_views_copies.py
python check_array_references_views_copies.py
```

Use `python3` if needed. If NumPy is absent in that interpreter, install it with `python -m pip install -r requirements.txt`. Predict object identity, shared-memory status, and both arrays' contents *before and after* each mutation. The checker uses separate fresh arrays for alias, slice view, explicit view, numeric copy, and nested object cases.

**Controlled change:** from `[10, 20, 30, 40]`, select `original[2:4]` and change the selected first value to **35**. Predict that a view changes the original to `[10, 20, 35, 40]`. Repeat from a *fresh* original with `original[2:4].copy()`; predict the selected copy `[35, 40]` while the original stays `[10, 20, 30, 40]`. The lab prints both cases.

**Repair a failure:** create `backup = original`, update `backup[0]`, and observe the source change. Replace the line with `backup = original.copy()` and rerun from a fresh source. Record `is`, `np.shares_memory`, the original values, and the repaired result. For an object array, test whether a nested object is still shared after `.copy()` before claiming independence.

## Independent mini-project: protect a study record

Start with a 2D `int32` table where rows are learners and columns are three tasks:

```python
records = np.array([[12, 8, 5], [10, 15, 5], [14, 6, 10]], dtype=np.int32)
```

Without opening `mini_project_reference.py`, demonstrate three separate cases from fresh copies of this starting table: (1) an alias updates learner 0/task 0 from 12 to 13; (2) a **row view** selected with `records[1, :]` changes learner 1/task 1 from 15 to 16; (3) a copied row changes its task 1 from 15 to 16 while its source remains 15. Report object identity and shared-memory status for each derived object, show before/after source and derived values, and explain which form to use when correcting the authoritative record versus preparing an independent trial. Compare with the reference only after an independent attempt.

**Expected results and self-check:** alias is the *same object* and yields source row 0 `[13, 8, 5]`; row view is a *different object sharing memory* and yields source row 1 `[10, 16, 5]`; copied row is a *different object without shared numerical storage*, becomes `[10, 16, 5]`, and leaves its source row 1 `[10, 15, 5]`. Use fresh starting tables for the cases so they do not affect one another. A complete record includes predictions, observed identities and arrays, the repaired backup mistake, and the object-array exception in your own words.

## Check your understanding

1. Does `alias = original` make another array object?
2. Can two different `ndarray` objects share the same element data?
3. What does mutation of `original[1:3]` do to the source in the numerical example?
4. Why does `original[1:3].copy()` preserve the source when the result is edited?
5. What do `a is b` and `np.shares_memory(a, b)` ask differently?
6. Why can modifying a nested dictionary through an object-array `.copy()` still change the original?
7. When is `copy.deepcopy` useful in the given example?

**Answers and reasoning**

1. No. It binds another name to the same array; `alias is original` is `True`.
2. Yes. A view is a distinct array object whose numerical data overlap the source.
3. The basic slice is a view, so changing its first element changes the corresponding source position.
4. It has separate numeric element storage; changing the copied region does not mutate the original.
5. `is` asks whether names refer to the same Python object; `shares_memory` asks whether array element memory overlaps.
6. Only the array's references are copied; both entries still point to the same nested dictionary.
7. When the nested Python list/dictionary needs an independent snapshot and recursive copying is suitable.

## Remember and retain

- **Alias:** same object, same data. **View:** different object, shared data. **Numeric copy:** different object, independent element data.
- Check both `is` and memory sharing when investigating a surprising change.
- `.copy()` of an object array is shallow for nested Python objects; `copy.deepcopy` can make those nested objects independent.
- Keep a before/after trace for the alias, view, copy, and nested-object case so you can explain each mutation.

## Further reading

- [NumPy copies and views](https://numpy.org/doc/stable/user/basics.copies.html)
- [NumPy `ndarray.copy`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.copy.html)
- [NumPy `shares_memory`](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html)
