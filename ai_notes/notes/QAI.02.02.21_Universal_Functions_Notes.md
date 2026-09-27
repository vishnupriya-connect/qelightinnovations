# Universal functions

## Apply one rule across an array

Suppose an array records signed differences between planned and actual study minutes:

```python
import numpy as np

differences = np.array([[-3, 0, 4], [5, -1, 2]], dtype=np.float64)
absolute = np.abs(differences)
squared = np.square(differences)
print(absolute.tolist()) # [[3.0, 0.0, 4.0], [5.0, 1.0, 2.0]]
print(squared.tolist())  # [[9.0, 0.0, 16.0], [25.0, 1.0, 4.0]]
```

A **universal function**, or **ufunc**, is a NumPy function that applies a rule element by element to array inputs. The **input array** here is `differences`; each **output array** has the same shape `(2, 3)` for these examples. `np.abs()` discards the sign: `-3` becomes `3`. `np.square()` multiplies each value by itself: `-3` becomes `9`. The inputs stay unchanged. This is an **element-wise function**: output at `[row, column]` comes from input at the same coordinate.

These are **unary ufuncs**: each output element uses one input element. A **binary ufunc** uses two inputs at corresponding positions. The preceding lesson's `np.add(a, b)` is one:

```python
print(np.add(np.array([1, 2, 3]), np.array([10, 20, 30])).tolist())
# [11, 22, 33]
```

For now, use equal-shaped inputs or a scalar as the second input. NumPy's rules for different compatible shapes appear in the next lesson.

## Square roots, exponentials, and logarithms

`np.sqrt()` asks which nonnegative number, multiplied by itself, gives each input:

```python
counts = np.array([0, 1, 4, 9], dtype=np.float64)
print(np.sqrt(counts).tolist()) # [0.0, 1.0, 2.0, 3.0]
```

`np.exp(x)` computes the natural constant `e` (approximately 2.71828) raised to each value of `x`. `np.log(y)` asks which exponent on `e` gives a positive value `y`; `log` here means the *natural* logarithm:

```python
x = np.array([0.0, 1.0, 2.0])
growth = np.exp(x)
print(np.round(growth, 3).tolist()) # [1.0, 2.718, 7.389]
print(np.round(np.log(growth), 6).tolist()) # [0.0, 1.0, 2.0]
```

The functions undo each other for these valid small inputs, up to floating-point approximation: `log(exp(2))` is approximately 2. `np.sqrt()` on a negative *real* value returns `nan` with a warning; `np.log()` on a negative real value returns `nan`, and at zero it returns negative infinity. Check what the input represents before accepting those results. Do not silently turn an invalid measurement into a valid one.

## Sine and cosine use radians

`np.sin()` and `np.cos()` evaluate each angle. The inputs use **radians**: 0 is no turn, `π/2` is a quarter turn, and `π` is a half turn. `np.pi` supplies π:

```python
angles = np.array([0.0, np.pi / 2, np.pi])
print(np.round(np.sin(angles), 6).tolist()) # [0.0, 1.0, 0.0]
print(np.round(np.cos(angles), 6).tolist()) # [1.0, 0.0, -1.0]
```

The round calls make tiny floating-point differences display as zero; for example `sin(π)` need not be stored as exactly zero. An input of 90 means 90 *radians*, not 90 degrees. If angles were recorded in degrees, convert first with `np.deg2rad()`.

## Round, floor, and ceiling

`np.floor()` moves each real value down to the greatest integer no larger than it. `np.ceil()` moves up to the smallest integer no smaller than it:

```python
measurements = np.array([-1.6, -1.2, 1.2, 1.6])
print(np.floor(measurements).tolist()) # [-2.0, -2.0, 1.0, 1.0]
print(np.ceil(measurements).tolist())  # [-1.0, -1.0, 2.0, 2.0]
print(np.round(measurements).tolist()) # [-2.0, -1.0, 1.0, 2.0]
```

`np.round()` rounds to a requested number of decimal places (zero by default). It acts element by element, but unlike `np.floor()` and `np.ceil()`, **`np.round()` itself is not a ufunc**. At exact halfway values it uses nearest-even rounding, for example `np.round([2.5, 3.5])` gives `[2.0, 4.0]`. Rounding is not the same as floor, ceiling, or truncation toward zero. It can also hide small differences when displaying results.

| Expression | Input at one position | Output | Practical meaning |
| --- | --- | --- | --- |
| `np.abs(x)` | `-3` | `3` | Magnitude without sign |
| `np.square(x)` | `-3` | `9` | Value times itself |
| `np.sqrt(x)` | `9` | `3` | Nonnegative square root |
| `np.exp(x)` | `0` | `1` | `e` to a power |
| `np.log(x)` | `1` | `0` | Exponent on `e` |
| `np.sin(x)` | `π/2` | approximately `1` | Sine of radians |
| `np.cos(x)` | `π` | approximately `-1` | Cosine of radians |
| `np.round(x)` | `1.6` | `2` | Nearest integer |
| `np.floor(x)` | `-1.2` | `-2` | Greatest integer at most input |
| `np.ceil(x)` | `-1.2` | `-1` | Smallest integer at least input |

## Guided lab

Download [Universal functions lab](QAI.02.02.21_Universal_Functions_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python universal_functions.py
python check_universal_functions.py
```

The program displays each function on controlled inputs. The checker verifies shapes, element coordinates, approximate floating-point results, and invalid-input handling; it prints `All checks passed.`

**Trace before running:** `differences[0, 0]` is `-3`. Predict the corresponding absolute value `3` and square `9`. For `measurements[1] == -1.2`, predict floor `-2`, ceiling `-1`, and round `-1`.

**Controlled variation:** copy `differences`, replace its `[0, 0]` value with `-6`, then calculate `abs` and `square`. The new corresponding outputs are `6` and `36`; the original remains `-3`.

**Debug:** Before `sqrt` on real data, check for negative values; before `log`, check for values at or below zero. A warning and `nan`/infinity do not by themselves explain the data problem. If `sin(90)` seems wrong for a quarter turn, convert 90 degrees to radians. For floating results, compare within a small tolerance rather than demanding exact binary equality.

## Independent mini-project: measurement report

Use signed deviations `deviations = np.array([-3.2, 0.0, 2.7, -1.5])` and nonnegative counts `counts = np.array([0.0, 1.0, 4.0, 9.0])`. Print the absolute deviations, their squares, their floor, ceiling and rounded values, and square roots of the counts. Then evaluate sine and cosine at `0`, `π/2`, and `π`, displaying six decimal places. A complete solution is in `mini_project_reference.py`.

Expected output:

```text
magnitude [3.2, 0.0, 2.7, 1.5]
square [10.24, 0.0, 7.29, 2.25]
floor [-4.0, 0.0, 2.0, -2.0]
ceil [-3.0, 0.0, 3.0, -1.0]
round [-3.0, 0.0, 3.0, -2.0]
roots [0.0, 1.0, 2.0, 3.0]
sine [0.0, 1.0, 0.0]
cosine [1.0, 0.0, -1.0]
```

Full reference solution:

```python
import numpy as np

deviations = np.array([-3.2, 0.0, 2.7, -1.5])
counts = np.array([0.0, 1.0, 4.0, 9.0])
angles = np.array([0.0, np.pi / 2, np.pi])
print("magnitude", np.abs(deviations).tolist())
print("square", np.round(np.square(deviations), 2).tolist())
print("floor", np.floor(deviations).tolist())
print("ceil", np.ceil(deviations).tolist())
print("round", np.round(deviations).tolist())
print("roots", np.sqrt(counts).tolist())
print("sine", np.round(np.sin(angles), 6).tolist())
print("cosine", np.round(np.cos(angles), 6).tolist())
```

## Check your understanding

1. **What makes `np.abs()` a unary ufunc?** One input value produces one output value at each array position.
2. **What is `np.log(np.exp(1))` approximately?** `1`, for a valid small real input.
3. **Which inputs do real `sqrt` and `log` require?** `sqrt` needs nonnegative values; `log` needs strictly positive values.
4. **Why is `np.floor(-1.2)` equal to `-2`?** `-2` is the greatest integer that does not exceed `-1.2`.
5. **Is `np.round()` itself a ufunc?** No. It is an element-wise NumPy array function included here alongside ufuncs.

Remember: choose a function with a valid input domain, retain the meaning of each element, and distinguish displayed rounding from the calculated value.

## Further reading

- [NumPy: universal functions](https://numpy.org/doc/stable/reference/ufuncs.html)
- [NumPy: mathematical functions](https://numpy.org/doc/stable/reference/routines.math.html)
- [NumPy: round](https://numpy.org/doc/stable/reference/generated/numpy.round.html)
