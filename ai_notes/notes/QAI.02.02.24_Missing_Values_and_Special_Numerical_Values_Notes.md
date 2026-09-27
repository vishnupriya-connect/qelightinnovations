# Missing values and special numerical values

## An absent measurement is not zero

Suppose rows are learners and columns are tasks. One task measurement is missing for each learner:

```python
import numpy as np

study = np.array([[10.0, np.nan, 20.0],
                  [5.0, 15.0, np.nan]])
print(study.shape) # (2, 3)
print(np.isnan(study).tolist())
# [[False, True, False], [False, False, True]]
```

A **missing value** means the observation was not recorded or is unavailable. `np.nan` is NumPy's floating-point **NaN** (“**not-a-number**”) value. We use it here as a missing marker; NaN can also arise from an invalid numerical calculation, so its cause should be checked. It is not the measured number zero. The array uses floating-point values because ordinary NumPy integer arrays cannot store NaN.

`np.isnan()` creates a Boolean mask showing precisely which elements are NaN. Do not test a missing entry using `== np.nan`: even `np.nan == np.nan` is false. Use `np.isnan()` and keep the mask if you later replace missing entries for a specific purpose.

## Distinguish NaN, infinity, and finite numbers

Positive infinity `np.inf` and negative infinity `-np.inf` are special floating-point values. They are not NaN, and a recorded `inf` is not a normal finite measurement:

```python
special = np.array([np.nan, np.inf, -np.inf, 5.0])
print(np.isnan(special).tolist())    # [True, False, False, False]
print(np.isinf(special).tolist())    # [False, True, True, False]
print(np.isfinite(special).tolist()) # [False, False, False, True]
```

`np.isinf()` detects both signs of infinity. A **finite value** is neither NaN nor positive or negative infinity; `np.isfinite()` detects these ordinary real numbers, including zero and negative finite values. Infinity can result from division by zero in floating-point calculations or can be inserted deliberately as a special marker. Ask which occurred before interpreting the data.

| Input | `isnan` | `isinf` | `isfinite` |
| --- | --- | --- | --- |
| `np.nan` | `True` | `False` | `False` |
| `np.inf` | `False` | `True` | `False` |
| `-np.inf` | `False` | `True` | `False` |
| `5.0` | `False` | `False` | `True` |

## Summarize available observations

Ordinary `np.sum(study)` and `np.mean(study)` propagate NaN. A **NaN-aware aggregate** deliberately skips NaNs:

```python
print(np.isnan(np.sum(study)), np.isnan(np.mean(study))) # True True
print(np.nansum(study, axis=1).tolist())  # [30.0, 20.0]
print(np.nanmean(study, axis=1).tolist()) # [15.0, 10.0]
```

For learner 0, the available values are 10 and 20, so the sum is 30 and the mean is 15. `np.nansum()` treats NaNs as zero for the *sum*; `np.nanmean()` omits them from both the total and the count. It does not divide by all three task slots. Neither function ignores infinities. For example, a positive infinity can still dominate an aggregate, and mixing positive and negative infinity can yield an invalid result. First inspect `np.isfinite()` when infinities may occur.

An entirely missing group needs separate handling:

```python
empty_row = np.array([np.nan, np.nan])
print(np.nansum(empty_row)) # 0.0
print(np.all(np.isnan(empty_row))) # True
```

The `0.0` from `nansum` means no values contributed; it is not evidence of an observed total of zero. `np.nanmean(empty_row)` returns NaN with a warning because no observed mean exists. Check for all-NaN groups before reporting summaries.

## Replace only with an explicit reason

**Missing-value replacement** supplies a chosen number in place of a marker. `np.nan_to_num()` can do this and, by default, also replaces infinities with very large finite numbers:

```python
missing_mask = np.isnan(study)
display_copy = np.nan_to_num(study, nan=0.0)
print(display_copy.tolist()) # [[10.0, 0.0, 20.0], [5.0, 15.0, 0.0]]
print(np.isnan(study).tolist()) # original still marks the missing entries
```

Here zeros are *display placeholders*, not observations. Preserve `missing_mask` so they can be distinguished from genuine zeros. A mean of `display_copy` would incorrectly include the placeholders; use `np.nanmean(study, axis=1)` for an available-observation mean. For an input that also contains infinities, `np.nan_to_num(special, nan=..., posinf=..., neginf=...)` lets you specify all replacements. Only choose finite bounds when the meaning of the data justifies them. Its default enormous replacements should not be mistaken for actual measurements. With the default `copy=True`, the original numeric array is not edited.

## Guided lab

Download [Missing and special values lab](QAI.02.02.24_Missing_Values_and_Special_Numerical_Values_Lab.zip), extract it, and run in the folder:

```bash
python -m pip install -r requirements.txt
python missing_and_special_values.py
python check_missing_and_special_values.py
```

The program prints detection masks, NaN-aware summaries, and an illustrative replacement. The checker verifies the masks, preserves the source, and handles an all-missing row; it prints `All checks passed.`

**Trace before running:** predict the masks for `special[0]` (NaN), `special[1]` (positive infinity), and `special[3]` (finite 5). Predict learner 0's available sum 30 and mean 15.

**Controlled variation:** copy `study` and replace `changed[0, 1]` with a genuine observed 30. Learner 0's `nansum` becomes 60 and `nanmean` becomes 20, using three observed values. The original remains missing at that position.

**Debug:** If `np.mean(study)` returns NaN, locate missing entries with `np.isnan()`. If a NaN-aware summary is still infinite or invalid, look for infinities with `np.isinf()`; NaN-aware does not mean infinity-aware. If an all-missing group's `nansum` displays 0, report it as missing rather than a measured zero.

## Independent mini-project: partial study records

Use `records = np.array([[12.0, np.nan, 18.0], [np.nan, 20.0, 22.0]])`. Print the missing mask, the number of missing entries per learner, available sums and means per learner, and a copy with NaNs replaced by zero for display. Preserve the original and state what the zeros mean. Compare with `mini_project_reference.py` in the lab.

Expected output:

```text
missing [[False, True, False], [True, False, False]]
missing counts [1, 1]
available sums [30.0, 42.0]
available means [15.0, 21.0]
display [[12.0, 0.0, 18.0], [0.0, 20.0, 22.0]]
original missing True
```

Full reference solution:

```python
import numpy as np

records = np.array([[12.0, np.nan, 18.0],
                    [np.nan, 20.0, 22.0]])
missing = np.isnan(records)
display = np.nan_to_num(records, nan=0.0)
print("missing", missing.tolist())
print("missing counts", np.sum(missing, axis=1).tolist())
print("available sums", np.nansum(records, axis=1).tolist())
print("available means", np.nanmean(records, axis=1).tolist())
print("display", display.tolist())
print("original missing", bool(np.isnan(records[0, 1])))
```

## Check your understanding

1. **Is NaN the same as an observed zero?** No. One marks an unavailable or invalid number; the other is a valid numerical value.
2. **Does `np.isnan(np.inf)` return true?** No. Use `np.isinf()` for infinity; neither NaN nor infinity is finite.
3. **Why is `np.nanmean([10, np.nan, 20])` equal to 15?** It sums the two observed values and divides by two.
4. **Does `np.nansum([np.nan, np.nan]) == 0` prove a measured total of zero?** No. Nothing was observed; check the missing mask.

Remember: detect first, interpret the cause, choose a summary or replacement rule, and retain the missingness information.

## Further reading

- [NumPy: isnan](https://numpy.org/doc/stable/reference/generated/numpy.isnan.html), [isinf](https://numpy.org/doc/stable/reference/generated/numpy.isinf.html), and [isfinite](https://numpy.org/doc/stable/reference/generated/numpy.isfinite.html)
- [NumPy: nan_to_num](https://numpy.org/doc/stable/reference/generated/numpy.nan_to_num.html), [nanmean](https://numpy.org/doc/stable/reference/generated/numpy.nanmean.html), and [nansum](https://numpy.org/doc/stable/reference/generated/numpy.nansum.html)
