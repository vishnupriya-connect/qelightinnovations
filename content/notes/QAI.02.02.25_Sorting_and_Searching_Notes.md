# Sorting and searching

## Put values in order

Suppose four task scores are stored in their original task order:

```python
import numpy as np

scores = np.array([40, 10, 30, 20])
ordered = np.sort(scores)
print(ordered.tolist()) # [10, 20, 30, 40]
print(scores.tolist())  # [40, 10, 30, 20]
```

**Array ordering** places values in a chosen sequence. To **sort** is to arrange them, usually in **ascending order** from smallest to largest. The result is a **sorted array**. `np.sort()` makes a **copied sort**: the original task order remains available. If task identity depends on position, keep that original array or an accompanying label array.

For **descending order**, reverse a sorted one-dimensional result:

```python
descending = np.sort(scores)[::-1]
print(descending.tolist()) # [40, 30, 20, 10]
```

The array method `sort()` is an **in-place sort**: it changes that array and returns `None`, rather than providing a new sorted array:

```python
editable = scores.copy()
returned = editable.sort()
print(editable.tolist(), returned) # [10, 20, 30, 40] None
print(scores.tolist())             # [40, 10, 30, 20]
```

Do not write `editable = editable.sort()`; it assigns `None` to the name.

## Choose a sort axis

For a two-dimensional table, the default **sort axis** is its last axis (`axis=-1`), which is the columns within each row:

```python
table = np.array([[4, 1, 3], [2, 6, 5]])
print(np.sort(table, axis=1).tolist()) # [[1, 3, 4], [2, 5, 6]]
print(np.sort(table, axis=0).tolist()) # [[2, 1, 3], [4, 6, 5]]
```

With `axis=1`, each learner's task values are rearranged within that row. With `axis=0`, each task column is sorted down the learner rows. Sorting may break the original correspondence between a score and its task or learner label. Decide whether that is acceptable before using the sorted table as data.

## Sort indices to preserve a link to the original positions

**Index sort**, `np.argsort()`, returns original positions in ascending value order:

```python
positions = np.argsort(scores)
print(positions.tolist())       # [1, 3, 2, 0]
print(scores[positions].tolist()) # [10, 20, 30, 40]
```

The first sorted value 10 came from original position 1. `np.argsort(table, axis=1)` similarly gives column positions for each sorted row. With equal values, their relative ordering is not guaranteed by an unstable sort. Use `kind="stable"` if the original order of ties matters.

## Find positions that meet a condition

A **search value** is what you want to locate; a **search position** is its array index. With one Boolean condition, `np.where()` returns positions where it is true:

```python
print(np.where(scores >= 30)[0].tolist()) # [0, 2]
rows, columns = np.where(table >= 5)
print(rows.tolist(), columns.tolist())    # [1, 1] [1, 2]
print(table[rows, columns].tolist())       # [6, 5]
```

`np.where(condition)` returns a tuple of index arrays, one per axis. For a one-dimensional vector, `[0]` takes its only index array. For the table, coordinate pairs are `(1, 1)` and `(1, 2)`. The three-argument form of `np.where()` selects values based on a condition and is covered in the next lesson.

`np.nonzero()` also returns positions where the input values are nonzero, or where a Boolean mask is true:

```python
flags = np.array([0, 7, 0, 9])
print(np.nonzero(flags)[0].tolist()) # [1, 3]
print(np.nonzero(scores >= 30)[0].tolist()) # [0, 2]
```

Numeric zero is false for this search; other numeric entries are treated as true. To test a specific property such as `scores >= 30`, pass that explicit Boolean condition.

## Find where a value belongs in a sorted array

`np.searchsorted()` returns the **insertion position** that keeps a one-dimensional ascending array sorted:

```python
print(np.searchsorted(ordered, [15, 30, 50]).tolist()) # [1, 2, 4]
print(np.searchsorted(ordered, 30, side="left"))  # 2
print(np.searchsorted(ordered, 30, side="right")) # 3
```

At position 1, 15 fits between 10 and 20. For an existing 30, `side="left"` inserts before equal values and `side="right"` after them. The default is `"left"`. An insertion position does **not** prove the search value occurs: 15 is absent. If you need membership, also check that the position is within the array and `ordered[position]` equals the target. The input must already be ascending for this ordinary use; do not pass unsorted `scores` and interpret the result as a valid location.

`np.unique()` returns each **unique value** once, in sorted order by default:

```python
repeated = np.array([3, 1, 3, 2, 1])
print(np.unique(repeated).tolist()) # [1, 2, 3]
```

It removes repeated values; it does not preserve their original positions in this simple form.

| Goal | Expression | Example result |
| --- | --- | --- |
| New ascending array | `np.sort(scores)` | `[10, 20, 30, 40]` |
| Change a copy in place | `editable.sort()` | `editable` becomes `[10, 20, 30, 40]` |
| Original positions by value | `np.argsort(scores)` | `[1, 3, 2, 0]` |
| Positions meeting a condition | `np.where(scores >= 30)[0]` | `[0, 2]` |
| Insertion position in sorted data | `np.searchsorted(ordered, 30)` | `2` |
| Distinct values | `np.unique(repeated)` | `[1, 2, 3]` |

## Guided lab

Download [Sorting and searching lab](QAI.02.02.25_Sorting_and_Searching_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python sorting_and_searching.py
python check_sorting_and_searching.py
```

The program displays copies, changed arrays, index positions, and insertion positions. The checker verifies the original remains intact where intended and prints `All checks passed.`

**Trace before running:** in `scores`, 10 is at original index 1. Predict it becomes the first sorted value, that `argsort` begins with 1, and that scores at original indices 0 and 2 meet `>= 30`.

**Controlled variation:** make a copy of `scores`, change the first value 40 to 5, then sort and search again. The sorted copy becomes `[5, 10, 20, 30]`, its `argsort` begins with original index 0, and the positions meeting `>= 30` become `[2]`. The original remains `[40, 10, 30, 20]`.

**Debug:** If `x = x.sort()` makes `x` become `None`, keep the array and call `x.sort()` separately or use `x = np.sort(x)`. If `searchsorted` appears to find an absent value, remember it returns an insertion point and verify equality. If sorting a table changes the relationship between columns and task names, use `argsort()` to carry the original positions with the values.

## Independent mini-project: review score positions

Use `marks = np.array([70, 55, 90, 70, 60])`. Produce ascending and descending copies, stable original positions in ascending score order, positions of marks at least 70, insertion positions immediately before and after 70 in the ascending array, and the unique values. The lab includes `mini_project_reference.py`.

Expected output:

```text
ascending [55, 60, 70, 70, 90]
descending [90, 70, 70, 60, 55]
original positions [1, 4, 0, 3, 2]
at least 70 [0, 2, 3]
insert 70 2 4
unique [55, 60, 70, 90]
original [70, 55, 90, 70, 60]
```

Full reference solution:

```python
import numpy as np

marks = np.array([70, 55, 90, 70, 60])
ascending = np.sort(marks)
descending = ascending[::-1]
original_positions = np.argsort(marks, kind="stable")
at_least_70 = np.where(marks >= 70)[0]
left = np.searchsorted(ascending, 70, side="left")
right = np.searchsorted(ascending, 70, side="right")
print("ascending", ascending.tolist())
print("descending", descending.tolist())
print("original positions", original_positions.tolist())
print("at least 70", at_least_70.tolist())
print("insert 70", left, right)
print("unique", np.unique(marks).tolist())
print("original", marks.tolist())
```

## Check your understanding

1. **Which sort changes its input array?** The array method `x.sort()`; `np.sort(x)` returns a sorted copy.
2. **What does `np.argsort(scores)[0] == 1` mean?** The smallest score came from original index 1.
3. **Does `searchsorted(ordered, 15) == 1` mean 15 exists?** No. It means 15 could be inserted at index 1 without breaking ascending order.
4. **What does `np.where(table >= 5)` return for a two-dimensional table?** Two arrays of matching row and column positions where the condition is true.

Remember: preserve original labels when ordering, and distinguish value, original position, and insertion position.

## Further reading

- [NumPy: sort](https://numpy.org/doc/stable/reference/generated/numpy.sort.html) and [argsort](https://numpy.org/doc/stable/reference/generated/numpy.argsort.html)
- [NumPy: where](https://numpy.org/doc/stable/reference/generated/numpy.where.html), [nonzero](https://numpy.org/doc/stable/reference/generated/numpy.nonzero.html), and [searchsorted](https://numpy.org/doc/stable/reference/generated/numpy.searchsorted.html)
- [NumPy: unique](https://numpy.org/doc/stable/reference/generated/numpy.unique.html)
