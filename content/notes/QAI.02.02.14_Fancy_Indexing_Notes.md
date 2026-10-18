# Fancy indexing

## Choose positions in your own order

Suppose five study sessions lasted `12, 18, 25, 30, 40` minutes. A slice selects positions that follow a range and step. What if we want the fifth session, then the second, then the fifth again, then the first? Use an **integer index array**:

```python
import numpy as np

minutes = np.array([12, 18, 25, 30, 40], dtype=np.int32)
positions = np.array([4, 1, 4, 0], dtype=np.intp)
picked = minutes[positions]
print(picked.tolist())  # [40, 18, 40, 12]
```

`positions` is an **index array**: its values identify positions in `minutes`, not minute amounts. This form of selecting values is called **fancy indexing**, or integer-array indexing. The **selected index positions** are `4, 1, 4, 0`; the result uses that exact order. The **repeated index** 4 repeats its source value 40 in the result. `np.intp` is NumPy's platform-sized integer type for indexing; an ordinary integer list such as `[4, 1, 4, 0]` also works as an index here.

| Result position | Source index | Source value |
|---:|---:|---:|
| 0 | 4 | 40 |
| 1 | 1 | 18 |
| 2 | 4 | 40 |
| 3 | 0 | 12 |

The resulting array has shape `(4,)`, equal to the shape of this one-dimensional index array. It does not inherit the source's five-element shape.

## A fancy-indexed result is a copy

The **fancy-indexed result** has separate numerical element data from the source:

```python
print(np.shares_memory(picked, minutes))  # False
picked[0] = 99
print(picked.tolist())   # [99, 18, 40, 12]
print(minutes.tolist())  # [12, 18, 25, 30, 40]
```

This is a **fancy-indexed copy**. Changing `picked` does not change source position 4. Do not assume a previously selected copy is a writable window into the source. Direct assignment such as `minutes[positions] = ...` has different behavior because the indexed expression is on the *left* side of the assignment. Avoid repeated positions in update rules unless the intended result has been specified and tested; this lesson uses repeats to study **selection**, where their meaning is clear.

## Fancy indexing versus slicing

Compare a contiguous **slice** with an explicit list of the same positions:

```python
by_slice = minutes[1:4]
by_positions = minutes[np.array([1, 2, 3])]
print(by_slice.tolist(), by_positions.tolist())  # [18, 25, 30] [18, 25, 30]
print(np.shares_memory(by_slice, minutes))       # True
print(np.shares_memory(by_positions, minutes))   # False
```

The displayed values match, but the data relationship does not. A basic slice is a **view** sharing source data; fancy indexing creates a **copy**. Use a slice for a regular contiguous or stepped range when a view is appropriate. Use an integer index array when you need an arbitrary selection, rearranged order, or repeated values, and account for its copied data. `.copy()` can make a slice independent when needed.

## Reorder whole rows

An index array can choose rows of a two-dimensional array. This selects rows 2, 0, and 2 of a three-learner table, preserving every task column:

```python
work = np.array([[12, 8], [10, 15], [14, 6]], dtype=np.int32)
chosen_rows = work[[2, 0, 2]]
print(chosen_rows.tolist(), chosen_rows.shape)
# [[14, 6], [12, 8], [14, 6]] (3, 2)
```

The duplicate row is intentional in this demonstration, and the new table is a copy. If your actual data should count each learner once, deduplicate or validate the requested positions first. Indexing is a selection operation; it does not decide whether repeated records are semantically correct.

With an integer array for *each* axis, NumPy matches corresponding positions **pairwise**:

```python
print(work[[0, 2], [1, 0]].tolist())  # [8, 14]
```

This selects coordinates `(0, 1)` and `(2, 0)`, not every combination of two rows and two columns. The pairwise example helps avoid a common mistaken prediction; selecting a rectangular subtable is a separate indexing question.

## Validate index boundaries and meaning

For a five-element source, valid nonnegative indexes are 0 through 4; negative indexes -5 through -1 count from the end. `minutes[np.array([4, 5])]` raises `IndexError` because 5 is outside the source. Unlike a slice such as `minutes[4:99]`, an invalid integer in a fancy index does not simply clip.

An empty integer index array produces an empty selected array, which may mean the requested positions list was empty. Before accepting a selection, check that positions have the intended type, are within bounds, and correspond to the right labels. A list of IDs or measurement values is not automatically a list of array positions.

## Guided lab

Download the [fancy indexing lab](QAI.02.02.14_Fancy_Indexing_Lab.zip), unzip it, and run from its folder:

```sh
python fancy_indexing.py
python check_fancy_indexing.py
```

Use `python3` if appropriate. If NumPy is absent in that interpreter, install it with `python -m pip install -r requirements.txt`. Predict output order, repetition, shape, and whether the source changes after editing the selection. The checker covers arbitrary positions, repeats, a slice/view comparison, reordered rows, pairwise coordinates, an empty selection, and an invalid index.

**Controlled change:** request positions `[0, 4, 0]` rather than `[4, 1, 4, 0]`. Predict selected values `[12, 40, 12]` and shape `(3,)`. Changing the selected copy's last value to 99 leaves source position 0 equal to 12. Run the variant in the lab and compare.

**Debugging practice:** try `minutes[[4, 5]]`. Inspect `minutes.size == 5`: source index 5 does not exist. If the request meant “fifth session,” the index is 4; repair the selection accordingly. If it meant a sixth session, the source is incomplete and should not be silently reinterpreted. Record error, intended meaning, correction, and output.

## Independent mini-project: learner reorder

Create this `int32` table, where rows are learners and columns are reading and practice minutes:

```python
records = np.array([[12, 8], [10, 15], [14, 6], [20, 10]], dtype=np.int32)
```

Select rows in the order **3, 1, 3, 0** with an integer index array. Report resulting values and shape, then change the selected copy's first reading value to 99 and verify the source remains 20 there. Compare with the regular slice `records[1:4]`: report its rows and whether it shares memory with `records`. Finally, select pairwise coordinates `(0, 1)` and `(2, 0)` in one expression, and diagnose an attempted row index 4. Read `mini_project_reference.py` only after your own attempt.

**Expected results and self-check:** reordered rows `[[20, 10], [10, 15], [20, 10], [12, 8]]` with shape `(4, 2)`; after editing the selected copy, its first row is `[99, 10]`, while source row 3 stays `[20, 10]`. Slice `records[1:4]` gives `[[10, 15], [14, 6], [20, 10]]` and shares source memory. Pairwise coordinates return `[8, 14]`; row 4 is out of bounds. Keep your predicted and actual rows, shared-memory checks, and repaired invalid-index explanation.

## Check your understanding

1. What do the values `[4, 1, 4, 0]` represent when used as `minutes` indexes?
2. Why does source value 40 appear twice in the selected result?
3. Does editing `minutes[[1, 2, 3]]` after storing it in another variable edit the source?
4. How can `minutes[1:4]` and `minutes[[1, 2, 3]]` have the same values but different mutation behavior?
5. What rows does `work[[2, 0, 2]]` produce?
6. Does `work[[0, 2], [1, 0]]` select four coordinates or two?
7. What happens if an index array includes a value equal to the source's `size`?

**Answers and reasoning**

1. They are requested *positions* in the source, not study-minute amounts.
2. Position 4 appears twice in the index array; each occurrence retrieves source value 40.
3. No. The stored fancy-indexing result is a separate numerical copy.
4. The basic slice shares data with the source, whereas advanced integer-array indexing copies the selected elements.
5. Learner rows 2, 0, and 2: `[[14, 6], [12, 8], [14, 6]]`.
6. Two pairwise coordinates, `(0, 1)` and `(2, 0)`, producing `[8, 14]`.
7. It is out of bounds for nonnegative indexes and raises `IndexError`.

## Remember and retain

- An integer index array selects positions in the **order listed**; repeats in the request repeat values in the output.
- Fancy indexing yields a numerical **copy**. Basic slicing yields a **view** in these examples.
- For multiple axis index arrays, pair corresponding positions; do not assume a rectangular combination.
- Keep the repeated-selection trace, copy-versus-view comparison, and invalid-index repair for review.

## Further reading

- [NumPy advanced indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy quickstart: advanced indexing](https://numpy.org/doc/stable/user/quickstart.html)
