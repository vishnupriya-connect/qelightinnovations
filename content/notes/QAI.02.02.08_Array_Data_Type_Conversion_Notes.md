# Array data-type conversion

## Why change an array's type?

An array's **data type** (`dtype`) tells NumPy how its items are represented. A list of counted minutes may use an **integer array**; durations measured with fractions may use a **floating-point array**. Converting values to another representation is called **type casting**. Before casting, ask whether the destination can represent *every relevant value* and whether the meaning will survive.

```python
import numpy as np

counts = np.array([20, 30], dtype=np.int32)
durations = counts.astype(np.float64)
print(counts.tolist(), counts.dtype)        # [20, 30] int32
print(durations.tolist(), durations.dtype)  # [20.0, 30.0] float64
```

`.astype(np.float64)` is an **explicit conversion**: the program names the desired type. By default it produces a new array; the original `counts` remains `int32`. `np.float64` has more precision than `np.float32`, but floating-point types do not represent every real number exactly.

## Explicit and implicit conversion

NumPy can also choose a result type **implicitly** while combining arrays of different types:

```python
whole = np.array([1, 2], dtype=np.int32)
fraction = np.array([0.5, 0.25], dtype=np.float64)
combined = whole + fraction
print(combined.tolist(), combined.dtype)  # [1.5, 2.25] float64
print(whole.dtype)                         # int32 (unchanged)
```

Here the operation produces a floating-point result because it combines integer and fractional inputs. The full rules depend on the participating NumPy and Python types; inspect `combined.dtype` instead of assuming every mixed calculation has this exact outcome. A type change does not guarantee no information loss: very large integers or very small fractions can exceed a floating type's exact range or precision.

| Kind | Example `dtype` | Values in this lesson | Typical use |
|---|---|---|---|
| Integer | `int32` | `20`, `30` | Whole-number counts |
| Floating point | `float64` | `20.0`, `30.5` | Measurements with fractions |
| Boolean | `bool` | `False`, `True` | A tested yes/no condition |
| String | Unicode text type | `"10"`, `"20"` | Text, even when characters look numeric |
| Object | `object` | `1`, `"2"` | References to Python objects of different kinds; handle deliberately |

## Boolean, string, and object arrays

A **Boolean array** contains `True` and `False`. Casting numerical data to Boolean treats zero as false and nonzero as true:

```python
values = np.array([0, 2, -3], dtype=np.int32)
print(values.astype(np.bool_).tolist())  # [False, True, True]
```

This loses the original magnitudes; `2` and `-3` both become `True`. It is useful for a specific yes/no question, but does not answer whether minutes were positive or valid. Name the intended condition if the distinction matters.

A **string array** holds text. Text containing digits is not automatically numeric data:

```python
text = np.array(["10", "20"])
numbers = text.astype(np.int32)
print(text.tolist(), text.dtype.kind)  # ['10', '20'] U (Unicode text)
print(numbers.tolist(), numbers.dtype)  # [10, 20] int32
```

If a text value is `"unknown"`, `astype(np.int32)` raises `ValueError`. Investigate what it means rather than quietly replacing it with zero. An **object array** can hold references to different Python object kinds:

```python
mixed = np.array([1, "2"], dtype=object)
print(mixed.tolist(), mixed.dtype)  # [1, '2'] object
```

Its `dtype` is `object`; `itemsize` accounts for references stored in the array, not all memory occupied by the referenced objects. Do not use an object array as an automatic repair for dirty numerical measurements. Parse and validate those measurements into a suitable numerical type.

## Four ways conversion loses information

**1. Fractional loss.** Casting floating-point values to integers discards the fractional part toward zero for these finite, in-range examples:

```python
fractions = np.array([2.9, -2.9], dtype=np.float64)
print(fractions.astype(np.int32).tolist())  # [2, -2]
```

It does not round to the nearest integer. Decide separately whether rounding is appropriate; casting alone is not a rounding rule for a measurement.

**2. Integer overflow.** An `int8` signed integer can hold only -128 through 127. Converting an existing wider integer array with `.astype(np.int8)` can wrap values outside that range:

```python
large = np.array([128, 300], dtype=np.int16)
print(large.astype(np.int8).tolist())  # [-128, 44] in the checked NumPy example
```

The output is not the original measurement. This example is a demonstration of an unsafe narrowing cast, not a method for reducing storage safely. NumPy's `casting="safe"` option blocks an unsafe *dtype-level* conversion such as `int16` to `int8`; a real application should also validate its domain and actual values. Direct construction from out-of-range Python integers may raise an error instead of behaving exactly like this array-to-array cast.

**3. Floating-point underflow.** A very small, nonzero value can be too close to zero for a narrower floating type:

```python
tiny = np.array([1e-50], dtype=np.float64)
print(tiny.astype(np.float32).tolist())  # [0.0]
```

This is **underflow**: the conversion loses the small magnitude. Do not mistake the returned zero for evidence that the input was zero.

**4. Precision loss.** A number can be within a type's broad range yet not exactly representable:

```python
exact = np.array([16_777_217], dtype=np.int64)
less_precise = exact.astype(np.float32)
print(less_precise.tolist())  # [16777216.0]
```

`float32` cannot represent this particular adjacent integer exactly. Casting it back to an integer does not recover the lost 1. **Precision** concerns how closely a stored value matches the intended value; it is separate from whether the number is within the approximate range of a type.

## Check a conversion before accepting it

For whole-number durations intended for `int16`, inspect the source values, check that they are finite (not infinity or an undefined numeric value), check that they have no fractional part, and compare them with `np.iinfo(np.int16).min` and `.max`. Only then cast and verify the result. These are **value-level** checks for this particular application; a `casting="safe"` setting reasons about *types* and may reject a narrowing cast even when all current values happen to fit.

```python
measurements = np.array([20.0, 30.0], dtype=np.float64)
limits = np.iinfo(np.int16)
valid = (
    np.all(np.isfinite(measurements))
    and np.all(measurements == np.trunc(measurements))
    and np.all((measurements >= limits.min) & (measurements <= limits.max))
)
if valid:
    checked = measurements.astype(np.int16)
    print(checked.tolist())  # [20, 30]
```

For a different application, acceptance may require a stricter range, a chosen rounding policy, or a rule for missing values. Do not convert first and then try to infer whether information was lost from the converted result alone.

## Guided lab

Download the [array data-type conversion lab](QAI.02.02.08_Array_Data_Type_Conversion_Lab.zip), unzip it, and run from its folder:

```sh
python array_type_conversion.py
python check_array_type_conversion.py
```

Use `python3` if needed. Install NumPy in that interpreter with `python -m pip install -r requirements.txt` if it is missing. Predict the output values **and the output types** before running. The checker covers all four loss examples, a rejected string, and accepted and rejected validated conversions.

**Controlled change:** replace the in-range whole-number measurements `[20.0, 30.0]` with `[20.0, 30.5]`. Predict that the safe application conversion rejects the second value because it is fractional; it does **not** silently store 30. Repair by obtaining a valid whole-number measurement or by preserving fractions in a floating-point representation when the task allows them. Compare the checked run.

**Debugging practice:** reproduce the `int16` → `int8` wrap with `128`. Inspect the intended input, destination bounds, and observed value `-128`. Do not “repair” it by assuming the input was `-128`; retain `int16` or use an appropriate wider type. Record the failure and the correction.

## Independent mini-project: validated practice minutes

You receive `[15.0, 25.0, 35.0]` as a `float64` array. Produce an `int16` array only after verifying finite values, no fractions, and the type's bounds. Show both arrays' values, `dtype`, `itemsize`, and `nbytes`. Then independently test `[15.0, 25.5, 35.0]`, `[15.0, 40_000.0, 35.0]`, and `[15.0, float("nan"), 35.0]`. Explain why each bad input must be rejected, without displaying a misleading converted array. Compare your work with `mini_project_reference.py` only after your own attempt.

**Expected result and self-check:** valid input gives `[15, 25, 35]`, `dtype=int16`, `itemsize=2`, `nbytes=6`; the original `float64` array remains `[15.0, 25.0, 35.0]`, with `itemsize=8`, `nbytes=24`. The fractional input fails the whole-number check; 40,000 exceeds `int16`'s maximum 32,767; `nan` fails the finite-value check. A complete attempt includes predicted and actual results, the three reasons for rejection, the overflow diagnosis, and an explanation of why the smaller representation is acceptable only for validated whole values in range.

## Check your understanding

1. What changes and what stays unchanged after `counts.astype(np.float64)`?
2. What is the difference between explicit casting and implicit result-type promotion?
3. Why does `[2.9, -2.9].astype(np.int32)` yield `[2, -2]`?
4. Why is `int16` → `int8` potentially unsafe even if the original array is valid?
5. How do underflow and precision loss differ in the two given examples?
6. Why should `"unknown"` not become a zero-minute measurement by default?
7. Does an object array's `nbytes` account for all referenced Python objects?

**Answers and reasoning**

1. A new floating-point array is produced; the original integer array remains unchanged with its original `dtype`.
2. An explicit cast names the destination type; an implicit conversion is selected during an operation with participating types.
3. Conversion truncates the fractional part toward zero in these finite, in-range cases; it does not round.
4. The narrower type cannot represent some `int16` values, such as 128, without changing them.
5. `1e-50` becomes zero in `float32` (underflow); `16_777_217` becomes a nearby representable `float32` value (precision loss).
6. It is missing or nonnumeric information, not evidence of an observed zero; investigate before choosing a representation.
7. No. Object-array entries are references; the referenced Python objects may use additional memory.

## Remember and retain

- **Meaning → bounds → type → cast → check.** Inspect input values and destination limits before narrowing.
- `astype()` requests an explicit type; mixed operations may promote types implicitly. Inspect both values and `dtype`.
- Fraction loss, overflow, underflow, and precision loss are distinct ways a cast can change meaning.
- Keep the validated conversion, changed fractional input, and overflow repair as evidence you can explain.

## Further reading

- [NumPy `ndarray.astype` reference](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html)
- [NumPy data types](https://numpy.org/doc/stable/user/basics.types.html)
- [NumPy data type promotion](https://numpy.org/doc/stable/reference/arrays.promotion.html)
