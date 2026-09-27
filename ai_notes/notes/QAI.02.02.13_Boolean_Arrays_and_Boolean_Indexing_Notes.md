# Boolean arrays and Boolean indexing

## Ask a yes-or-no question of each value

Suppose five practice sessions lasted **10, 25, 30, 15, and 40 minutes**. We want to find sessions lasting at least 25 minutes. A **Boolean value** is `True` or `False`. An **element-wise comparison** asks the same question of each array element:

```python
import numpy as np

minutes = np.array([10, 25, 30, 15, 40], dtype=np.int32)
mask = minutes >= 25
print(mask.tolist())  # [False, True, True, False, True]
print(mask.dtype)     # bool
```

The result is a **Boolean array** or **Boolean mask**. It has the same shape `(5,)` as `minutes`. Its **Boolean condition** is “value >= 25.” A **true element** marks a position meeting the condition; a **false element** marks one that does not. At index 1, `25 >= 25` is true, so the boundary value is included. Mask creation does not change `minutes`.

| Position | Minutes | `minutes >= 25` |
|---:|---:|---|
| 0 | 10 | `False` |
| 1 | 25 | `True` |
| 2 | 30 | `True` |
| 3 | 15 | `False` |
| 4 | 40 | `True` |

## Select matching elements

**Boolean indexing** uses a mask to retrieve values in positions marked `True`:

```python
selected = minutes[mask]
print(selected.tolist(), selected.shape)  # [25, 30, 40] (3,)
print(minutes.tolist())  # [10, 25, 30, 15, 40]
```

This is **mask selection** or **conditional selection**. The retrieved `selected` array is a copy of the selected numerical values in this example, not a view of the source. Its length is the number of `True` entries, not the original length. Changing `selected[0]` afterward will not alter `minutes[1]`. Predict both the selected values and their order; NumPy visits the positions in their array order.

The condition can be written directly: `minutes[minutes >= 25]`. Keeping a named mask helps when inspecting or reusing the selection rule.

## Combine conditions carefully

For minutes **at least 20 and at most 35**, create two comparisons and combine them element by element with `&`:

```python
between = (minutes >= 20) & (minutes <= 35)
print(between.tolist())       # [False, True, True, False, False]
print(minutes[between].tolist())  # [25, 30]
```

Use parentheses around each comparison so the intended condition is clear. `|` combines conditions with element-wise OR, and `~` reverses each Boolean value. Python's single `and` and `or` do not combine a multi-element NumPy mask element by element; using them generally raises an error about an ambiguous truth value. A mask means one answer **per position**, not one answer for the entire array.

## Update matching elements

**Conditional update**, also called **masked assignment**, uses the mask on the *left* side of `=`. Make a copy first if the original record must be preserved:

```python
updated = minutes.copy()
updated[mask] = updated[mask] + 5
print(updated.tolist())  # [10, 30, 35, 15, 45]
print(minutes.tolist())  # [10, 25, 30, 15, 40]
```

Only the three true positions change; false positions 0 and 3 stay 10 and 15. The right side `updated[mask]` produces selected values for the calculation; the left side `updated[mask] = ...` writes back into `updated`. A scalar assignment, `updated[mask] = 0`, would instead set all matching elements to zero. Choose an update that matches the actual task; do not treat a derived adjustment as if it were an observed measurement.

**Important distinction:**

```python
trial = minutes[mask]
trial[0] = 99
print(minutes[1])  # 25: selection made a separate array

direct = minutes.copy()
direct[mask] = 99
print(direct.tolist())  # [10, 99, 99, 15, 99]: assignment changed direct
```

The copy of `minutes` in the second case protects the original; it is the indexed assignment to `direct` that changes its selected positions. Do not assume modifying a previously selected result writes back.

## Two dimensions: element mask or row mask?

Consider two learners and three tasks:

```python
work = np.array([[12, 8, 5], [10, 15, 5]], dtype=np.int32)
element_mask = work >= 10
print(element_mask.tolist())  # [[True, False, False], [True, True, False]]
print(work[element_mask].tolist(), work[element_mask].shape)
# [12, 10, 15] (3,)
```

With a Boolean mask of the **same shape** as a two-dimensional array, selection returns matching individual elements as a **one-dimensional** array in row order. It does not preserve the original rectangular shape. A different question, “keep learner 1's entire row,” uses a one-dimensional **row mask** of length two:

```python
row_mask = np.array([False, True])
print(work[row_mask].tolist(), work[row_mask].shape)
# [[10, 15, 5]] (1, 3)
```

The mask must match the dimensions it is used to select. For a five-element one-dimensional `minutes` array, a four-element mask raises `IndexError` rather than silently matching the first four positions. Inspect both shapes before using a supplied mask.

## Diagnose boundary and empty results

The condition `minutes > 25` selects `[30, 40]`; `minutes >= 25` selects `[25, 30, 40]`. The change from `>` to `>=` matters at the boundary. A condition such as `minutes > 100` produces five false values and an empty selected array of shape `(0,)`. This may be a valid “no matches” result or a mistaken threshold. Check the question, input, condition, and mask before concluding that all measurements are absent.

## Guided lab

Download the [Boolean arrays and indexing lab](QAI.02.02.13_Boolean_Arrays_and_Boolean_Indexing_Lab.zip), unzip it, and run in its folder:

```sh
python boolean_indexing.py
python check_boolean_indexing.py
```

Use `python3` if needed. If NumPy is missing from that interpreter, install it with `python -m pip install -r requirements.txt`. Predict the mask, selected values, and copy-versus-assignment behavior before running. The checker verifies boundary inclusion, a changed threshold, no matches, both 2D mask meanings, and a mismatched-mask failure.

**Controlled change:** replace the threshold 25 with **30**. With `>= 30`, predict `[30, 40]` and mask `[False, False, True, False, True]`. With `> 30`, predict `[40]`. Explain why the session of exactly 30 minutes moves in or out of the result. Run the comparison on the same original data.

**Debugging practice:** try a four-entry mask for the five-entry `minutes` array, record the `IndexError`, then repair it by generating `minutes >= 25` from the actual source. Separately change a selected copy and verify that the original did not change; use indexed assignment on an independent source copy for an intended update.

## Independent mini-project: task threshold report

Start with `work = np.array([[12, 8, 5], [10, 15, 5]], dtype=np.int32)`. Independently construct a mask for values at least **10**, show its shape, and extract the matching values and result shape. On a copy of `work`, add **2** only at those positions. Show the unchanged source and updated copy. Then create a row mask that keeps only the second learner and explain why its result has two dimensions. Try a wrong-length row mask, diagnose it, and compare with `mini_project_reference.py` after your own attempt.

**Expected results and self-check:** element mask `[[True, False, False], [True, True, False]]` of shape `(2, 3)`; selected values `[12, 10, 15]` of shape `(3,)`; updated copy `[[14, 8, 5], [12, 17, 5]]`; source unchanged `[[12, 8, 5], [10, 15, 5]]`. Row mask `[False, True]` returns `[[10, 15, 5]]` of shape `(1, 3)`. A three-entry mask applied to the row axis is an error because the row axis length is two. Keep your prediction, output, unchanged-source check, and repaired mismatch.

## Check your understanding

1. Which positions are true in `minutes >= 25`, and is 25 itself included?
2. What are the values and shape of `minutes[minutes >= 25]`?
3. Why does changing `selected[0]` not change the original `minutes`?
4. What changes when you write `updated[mask] = updated[mask] + 5`?
5. Why does a same-shape 2D mask give a 1D result, while a one-dimensional row mask can keep a 2D result?
6. What does an empty result from `minutes > 100` prove, and what should you check?

**Answers and reasoning**

1. Indexes 1, 2, and 4 are true; 25 meets the `>=` boundary.
2. `[25, 30, 40]` with shape `(3,)`.
3. Boolean selection produces a copy of those numerical values, so editing that result does not write back.
4. Only positions where the mask is true increase by five in `updated`; the original `minutes` remains unchanged because it was copied first.
5. The 2D element mask selects individual matching cells and lists them in a 1D result. A row mask selects complete rows, retaining their task columns.
6. It proves there were no matches under that condition for the current data; verify the threshold, data, and intended comparison before interpreting it further.

## Remember and retain

- Compare values element by element → Boolean mask of `True` and `False`.
- `array[mask]` retrieves matching elements as a separate selected array; `array[mask] = value` updates the addressed array.
- For a full-shape 2D mask, matching cells form a 1D result; a row mask selects rows. Check shapes and boundary operators.
- Keep the threshold variation, copy-versus-assignment trace, and repaired mask mismatch for review.

## Further reading

- [NumPy indexing on ndarrays: Boolean indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy absolute basics: conditional selection](https://numpy.org/doc/stable/user/absolute_beginners.html)
