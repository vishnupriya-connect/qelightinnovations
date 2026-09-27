# Number-sequence array creation

## Three questions before generating values

Suppose you want checkpoints for a practice session. Do you know the **gap** between checkpoints, the **number** of checkpoints, or the **multiplicative change** between them? A **sequence** is an ordered set of values. NumPy has different constructors because those questions specify a sequence in different ways.

| You know | Use | Example request |
|---|---|---|
| Starting value and fixed step | `np.arange()` | Every 2 minutes, beginning at 2, before 11 |
| Starting value, ending value, and count | `np.linspace()` | Five equally spaced checkpoints from 0 to 1 |
| Starting and ending powers of a base | `np.logspace()` | Powers of ten from 1 to 1000 |

Import NumPy before the examples:

```python
import numpy as np
```

## `np.arange()`: start, stop, step

The **start** is the first value. The **step** is the amount added each time. The **stop** is the boundary, normally **excluded** from the sequence:

```python
checkpoints = np.arange(2, 11, 2)
print(checkpoints.tolist())  # [2, 4, 6, 8, 10]
```

Trace it: start at 2; add 2 repeatedly. `10` is below the exclusive stop `11`; the next value `12` would pass it. The call `np.arange(5)` uses default start 0 and step 1, giving `[0, 1, 2, 3, 4]`. An explicit `dtype` can request a representation, such as `np.arange(2, 11, 2, dtype=np.int32)`.

A negative step counts down:

```python
print(np.arange(10, 1, -3).tolist())  # [10, 7, 4]
```

For a decreasing sequence, a positive step would not advance toward a smaller stop. `np.arange(10, 1, 3)` produces an empty array. A step of zero is invalid and raises an error. Diagnose an empty result by checking start, stop, and the sign of step before assuming measurements are missing.

**Boundary caution:** a fractional step such as `0.1` can produce rounding surprises in floating-point arithmetic, including an unexpected length or endpoint near the boundary. Use an integer step where practical. If the exact *count* and endpoint matter, use `np.linspace()` instead.

## `np.linspace()`: a known count

`np.linspace(start, stop, num=...)` makes a specified **number of generated values** with equal additive spacing. By default, its stop is an **inclusive endpoint**:

```python
fractions = np.linspace(0, 1, num=5)
print(fractions.tolist())  # [0.0, 0.25, 0.5, 0.75, 1.0]
```

There are five points but only four gaps between the first and last. Each gap is `(1 − 0) / (5 − 1) = 0.25`. The result is floating-point even though the start and stop are written as whole numbers. A requirement for *five points including both ends* is different from a requirement for *step 0.25*. When the count is fixed, use `linspace` and verify the result.

Set `endpoint=False` for an **exclusive endpoint**. NumPy then divides the interval into `num` equal parts, returning the first `num` points and omitting stop:

```python
without_last = np.linspace(0, 1, num=4, endpoint=False)
print(without_last.tolist())  # [0.0, 0.25, 0.5, 0.75]
```

Compare `np.linspace(0, 1, num=5)` with `np.linspace(0, 1, num=5, endpoint=False)`: each produces five values, but the latter ends at `0.8`, not `1.0`. If `num=1`, only the start is returned, even with the default endpoint setting. Do not use an integer `dtype` for a fractional grid unless you intentionally accept conversion and possible repeated or changed values.

## `np.logspace()`: evenly spaced exponents

Sometimes checkpoints grow by multiplication, such as `1`, `10`, `100`, `1000`. `np.logspace(start, stop, num=..., base=10)` first chooses evenly spaced **exponents** and raises `base` to each. Here `start` and `stop` are **powers**, not the output values themselves:

```python
powers_of_ten = np.logspace(0, 3, num=4, base=10)
print(powers_of_ten.tolist())  # [1.0, 10.0, 100.0, 1000.0]
```

The exponents are `0, 1, 2, 3`, so the values are `10⁰, 10¹, 10², 10³`. In particular, `np.logspace(0, 3, ...)` begins at **1**, not 0, and ends at **1000**, not 3. The default base is 10. With `base=2`, `np.logspace(0, 3, num=4, base=2)` gives `[1.0, 2.0, 4.0, 8.0]`.

The `endpoint` setting applies to the **stop exponent**:

```python
print(np.logspace(0, 3, num=3, endpoint=False, base=10).tolist())
# [1.0, 10.0, 100.0]
```

This excludes exponent `3` (and hence the value `1000`). The multiplicative ratio is constant in these examples, unlike `linspace`, whose additive difference is constant. `logspace` is useful when exploring a wide positive range of scales. Choose `linspace` for equally spaced *values*. Both may return approximate floating-point values for other endpoints, so use a tolerance when comparing non-exact results.

## Compare the same bounds with different questions

```python
print(np.arange(0, 5, 1).tolist())                   # [0, 1, 2, 3, 4]
print(np.linspace(0, 5, num=6).tolist())             # [0., 1., 2., 3., 4., 5.]
print(np.linspace(0, 5, num=5, endpoint=False).tolist())
# [0., 1., 2., 3., 4.]
```

The first knows a step and excludes the boundary. The second knows a count and includes 5. The third knows a count, explicitly excludes 5, and happens to match the first five values. The same-looking output can come from different requirements; state the requirement before selecting a constructor.

## Guided lab

Download the [number-sequence array creation lab](QAI.02.02.06_Number_Sequence_Array_Creation_Lab.zip), unzip it, and run from its folder:

```sh
python number_sequences.py
python check_number_sequences.py
```

Use `python3` if appropriate. If NumPy is absent from the interpreter running the files, install it with `python -m pip install -r requirements.txt`. Write down predictions before running. The checker verifies endpoints, lengths, descending order, both logarithmic bases, zero step, and a wrong-direction result. It uses `np.allclose` when checking fractional values, since floating-point arithmetic may be approximate.

**Controlled change:** make six equally spaced values from 0 to 10, including both ends. Predict `[0, 2, 4, 6, 8, 10]`; now set `endpoint=False` while keeping six values. Predict the first value `0`, the omitted stop `10`, and a gap of `10/6`, so the final value is approximately `8.33333333`. Explain why the count stays six even though the gap changes. The supplied lab checks this comparison.

**Debugging practice:** try `np.arange(2, 11, -2)` and inspect its size; the direction is wrong for an increasing sequence. Repair the step to `2`. Try `np.arange(0, 5, 0)` in a scratch file, record the error, and repair the step to a nonzero value. A disappearing sequence is a diagnostic clue, not evidence that data were collected as an empty set.

## Independent mini-project: three checkpoint plans

Build and label these three arrays yourself before opening `mini_project_reference.py`:

1. Every 3 minutes from 3 up to but **not including** 16.
2. Exactly five equally spaced percentages from 0 to 100, **including** both endpoints.
3. Four multiplicative scales from `2⁰` through `2³`, including both endpoint exponents.

Then create a fourth plan: four points from 0 to 100 that **exclude** 100. Report each result and size. Explain which input specifies step, which specifies count, and which specifies exponents. Modify plan 1 to use step 4, predict the changed values, and compare.

**Expected results and self-check:** `[3, 6, 9, 12, 15]` (size 5); `[0.0, 25.0, 50.0, 75.0, 100.0]` (size 5); `[1.0, 2.0, 4.0, 8.0]` (size 4); `[0.0, 25.0, 50.0, 75.0]` (size 4). Changing the first step to 4 gives `[3, 7, 11, 15]`. A complete attempt includes the input rule, predicted endpoints and size, run output, changed variant, and a repaired wrong-direction or zero-step example.

## Check your understanding

1. What are start, stop, and step in `np.arange(2, 11, 2)`? Is 11 included?
2. Why are there five values but four equal gaps in `np.linspace(0, 1, num=5)`?
3. What changes when `endpoint=False` in `linspace` while `num` stays the same?
4. What are the first and last *values* of `np.logspace(0, 3, num=4)`?
5. What do `start=0` and `stop=3` mean in that `logspace` call?
6. Why may a fractional-step `arange` be unsuitable when the exact count and endpoint matter?
7. What does `np.arange(10, 1, 3)` produce, and what is a sensible repair?

**Answers and reasoning**

1. Start 2, exclusive stop 11, step +2; the output is `[2, 4, 6, 8, 10]`.
2. Both endpoints are included by default, leaving four intervals between five positions; the gap is 0.25.
3. The stop is omitted, so the spacing and final returned value change even though the count remains `num`.
4. `1` and `1000`, because they are `10⁰` and `10³`.
5. They are the first and last **exponents**, not the returned numerical endpoints.
6. Floating-point rounding can make the length or boundary behavior surprising; `linspace` takes an explicit count and endpoint setting.
7. An empty array, since a positive step moves away from the smaller stop. Use a negative step, such as `np.arange(10, 1, -3)` → `[10, 7, 4]`.

## Remember and retain

- `arange(start, stop, step)`: specify the gap; stop is normally exclusive.
- `linspace(start, stop, num)`: specify the count; stop is inclusive unless `endpoint=False`.
- `logspace(start, stop, num, base)`: specify evenly spaced **exponents** and produce powers of the base.
- Predict first value, last value, and size before running. Save the changed endpoint trace and repaired sequence error for later review.

## Further reading

- [NumPy `arange`](https://numpy.org/doc/stable/reference/generated/numpy.arange.html)
- [NumPy `linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)
- [NumPy `logspace`](https://numpy.org/doc/stable/reference/generated/numpy.logspace.html)
