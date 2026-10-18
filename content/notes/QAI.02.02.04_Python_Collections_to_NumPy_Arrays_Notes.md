# Python collections to NumPy arrays

## From a list of measurements to an array

Suppose three learners record study minutes: `20`, `30`, and `40`. A **Python list** keeps these values in order:

```python
minutes = [20, 30, 40]
print(type(minutes).__name__)  # list
```

To use NumPy's numerical array operations, perform an **array conversion** with `np.array(...)`:

```python
import numpy as np

array_minutes = np.array(minutes)
print(type(array_minutes).__name__)  # ndarray
print(array_minutes.shape)           # (3,)
print(array_minutes.tolist())        # [20, 30, 40]
```

The list is the input; `np.array()` constructs a NumPy `ndarray`. The resulting one-dimensional array has one axis of length three. `.tolist()` here is only a convenient way to display or compare its values as ordinary Python lists. When created from this numerical Python list, the array has its own stored values: changing `minutes[0]` afterward does not change `array_minutes[0]`. Assignment such as `other = array_minutes`, however, gives the *same array object* a second name. Do not confuse these cases.

For a small one-off sequence, a Python list may be sufficient. An array provides a consistent shape and data type for numerical work. Creation can fail or change value representation, so inspect both the result and the meaning of the input.

## Nesting gives dimensions

A **nested Python list** is a list containing other lists. Equal-length inner lists can form rows of a rectangular array. Use one list for one axis, a list of rows for two axes, and a list of equal-shaped tables for three axes:

```python
one_d = np.array([20, 30, 40], dtype=np.int32)
two_d = np.array([[20, 10], [30, 15], [40, 20]], dtype=np.int32)
three_d = np.array([
    [[20, 10], [30, 15]],
    [[40, 20], [50, 25]],
], dtype=np.int32)

print(one_d.shape, one_d.ndim)    # (3,) 1
print(two_d.shape, two_d.ndim)    # (3, 2) 2
print(three_d.shape, three_d.ndim)  # (2, 2, 2) 3
print(three_d[1, 0, 1])          # 20
```

Read `three_d[1, 0, 1]` as the second table, first row, second value. The array has eight values because `2 × 2 × 2 = 8`. The bracket levels in this example make the layout visible. The array does not automatically know whether an axis means week, learner, or task; attach and keep those meanings in your program or documentation.

## Inferred and specified data types

A **data type** describes how the array represents each element. With no `dtype` argument, NumPy **infers** a type that can represent the supplied values, according to its type-promotion rules. Inspect the actual `dtype`; an inferred default integer type can vary by platform.

```python
inferred = np.array([20, 30, 40])
print(inferred.dtype)  # an integer dtype; exact width may vary

mixed_numbers = np.array([20, 30.5, 40])
print(mixed_numbers.tolist())  # [20.0, 30.5, 40.0]
print(mixed_numbers.dtype.kind)  # f (floating-point)
```

The first input has **homogeneous data**: all three values are integers. The second has **heterogeneous input**: integers and a fractional value. NumPy chooses one common array type that can represent these particular values, so the integers are represented as floating-point values in this result. A normal numerical `ndarray` has a common data type for its elements. Some specialized data types can represent more complex records, but mixing arbitrary objects is not a sound default for numerical calculations.

Specify the type when its width or meaning matters. The `dtype=` **argument** tells `np.array()` the desired data type at creation:

```python
fixed_integers = np.array([20, 30, 40], dtype=np.int32)
fixed_fractions = np.array([20, 30.5, 40], dtype=np.float64)
print(fixed_integers.dtype, fixed_integers.itemsize)  # int32 4
print(fixed_fractions.dtype, fixed_fractions.itemsize)  # float64 8
```

`np.int32` stores 32-bit signed integers; `np.float64` stores 64-bit floating-point values. The `dtype` argument applies to the resulting array's elements, not to the original Python list. Numerical casts may lose information: forcing `30.5` into an integer type does not preserve the half minute. Do not use a forced integer conversion to silently repair fractional measurements. Validate units and the intended kind of data first.

## Two conversion failures to recognize

**Uneven rows.** These nested lists have different lengths:

```python
uneven = [[20, 10], [30]]
np.array(uneven, dtype=np.int32)  # ValueError: no rectangular numeric shape
```

There is no second value in the second row. If the input was meant to be a table, investigate the missing measurement; do not quietly insert zero and treat it as observed. After an authorized correction such as supplying the actual missing value `15`, `np.array([[20, 10], [30, 15]], dtype=np.int32)` has shape `(2, 2)`.

**Unusable numeric text.** A list can hold text as well as numbers:

```python
raw = ["20", "not recorded", "40"]
np.array(raw, dtype=np.int32)  # ValueError: "not recorded" cannot become an integer
```

Do not assume the string `"20"` is already the number `20`. Here `"not recorded"` is missing information, not a zero-minute session. Investigate and handle the missing value according to the task before conversion. Without a numeric `dtype`, a mixed list containing text may instead produce a string array; an apparent successful conversion does not prove the result is suitable for arithmetic.

## Guided lab

Download the [Python collections to NumPy arrays lab](QAI.02.02.04_Python_Collections_to_NumPy_Arrays_Lab.zip), unzip it, and run in its folder:

```sh
python collections_to_arrays.py
python check_collections_to_arrays.py
```

Use `python3` if required. Install NumPy in the interpreter running the files with `python -m pip install -r requirements.txt` if necessary. Predict the three shapes, the inferred floating type, and each controlled error before running. The checker verifies 1D/2D/3D construction, explicit types, source-list independence, and the errors.

**Controlled change:** change the second row of the two-dimensional input from `[30, 15]` to `[30, 18]` in a scratch copy. The shape stays `(3, 2)`, the data type stays `int32`, and `array[1, 1]` changes from 15 to 18. The first row stays `[20, 10]`. Run the variation and compare your prediction. Restore the supplied example before rerunning its checker.

**Repair a failure:** attempt `np.array([[20, 10], [30]], dtype=np.int32)` and record the exception. If the actual second measurement is later confirmed to be 15, add it and rerun; the corrected array has shape `(2, 2)` and contains four values. If it is unknown, leave it unresolved and do not claim that 15 or zero was observed.

## Independent mini-project: two weeks of activity data

Construct a numerical array from this nested Python list. The axes mean **week → learner → task**; each learner has reading and practice minutes in that order:

```python
records = [
    [[12, 8], [10, 5], [15, 10]],
    [[14, 6], [12, 8], [10, 15]],
]
```

Before viewing `mini_project_reference.py`, write a program that converts `records` to an `int32` array, reports its shape, dimensions, size, data type and `array[1, 2, 1]`, and computes the total minutes for each week. Modify the original list afterward and check whether the constructed array changes. Create a separate array from a new list where week 1, learner 2, practice changes from 15 to 20; report the changed week's total. Finally, try an uneven version with the last learner missing a task and explain the error. Compare with the reference only after an independent attempt.

**Expected result and self-check:** shape `(2, 3, 2)`, `ndim=3`, `size=12`, `dtype=int32`, selected value `15`. Week totals are `[60, 65]`: `12+8+10+5+15+10 = 60` and `14+6+12+8+10+15 = 65`. The changed week 1 total is **70**. Changing the original Python list after the conversion does not change the existing array. The uneven numeric nested input raises `ValueError`; seek the missing value rather than pretending it is zero. Keep your predicted outputs, program, actual outputs, and one repaired failure as evidence you can explain.

## Check your understanding

1. What changes when `[20, 30, 40]` is passed to `np.array()`?
2. What input shape produces a two-dimensional array? What is the shape of the supplied three-dimensional example?
3. Why might `[20, 30.5, 40]` produce floating-point array elements?
4. What does `dtype=np.int32` ask NumPy to do? Does it change the original list?
5. Why does `[[20, 10], [30]]` fail as a rectangular numeric array?
6. If a source list changes after conversion, does the constructed array in this lesson change? What does `other = existing_array` do instead?

**Answers and reasoning**

1. It creates a NumPy `ndarray` with shape `(3,)`, a common inferred type, and three values.
2. Equal-length rows nested in an outer list give two axes. The example with two tables of two rows and two values has shape `(2, 2, 2)`.
3. It contains a fractional value; NumPy promotes the integers to a common floating-point representation for this input.
4. It requests 32-bit signed integer elements in the new array. It does not edit the source list.
5. The rows have different lengths, so there is no rectangular second dimension for a numeric array.
6. No, because the new array constructed from the list stores its own values. `other = existing_array` only gives the *same* array another name; it does not create an independent copy.

## Remember and retain

- **List → `np.array()` → ndarray:** inspect `shape`, `ndim`, and `dtype` before interpreting output.
- Equal-length nested lists can form regular numeric dimensions; uneven rows require investigation.
- An inferred type may differ from your assumption. Specify `dtype` when representation matters and reject unvalidated or lossy conversions.
- Save the working 3D conversion, changed-input trace, and repaired uneven-row example for later review.

## Further reading

- [NumPy array creation](https://numpy.org/doc/stable/user/basics.creation.html)
- [NumPy `array` reference](https://numpy.org/doc/stable/reference/generated/numpy.array.html)
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)
