# Element-wise arithmetic

## Pair each value with its matching position

Suppose two arrays have the same shape, with rows for learners and columns for tasks:

```python
import numpy as np

a = np.array([[7, 8, 9], [10, 11, 12]], dtype=np.int32)
b = np.array([[2, 3, 4], [3, 4, 5]], dtype=np.int32)
print((a + b).tolist())
# [[9, 11, 13], [13, 15, 17]]
print((a - b).tolist())
# [[5, 5, 5], [7, 7, 7]]
```

An **element-wise operation** applies the same calculation to each pair of **corresponding elements**. For example, `a[0, 1] == 8` and `b[0, 1] == 3` produce `(a + b)[0, 1] == 11`. **Element-wise addition** (`+`) and **element-wise subtraction** (`-`) make an **arithmetic result** at each position. The inputs here remain unchanged. The result has shape `(2, 3)`.

An **arithmetic operator** is a symbol such as `+`, `-`, `*`, `/`, `//`, `%`, or `**`. NumPy also provides named functions. For these arrays, `np.add(a, b)` matches `a + b`, and `np.subtract(a, b)` matches `a - b`.

## Multiplication and division act on pairs

```python
print((a * b).tolist())
# [[14, 24, 36], [30, 44, 60]]
print(np.round(a / b, 2).tolist())
# [[3.5, 2.67, 2.25], [3.33, 2.75, 2.4]]
```

`*` is **element-wise multiplication**: `8 * 3 == 24` at `[0, 1]`. It is not matrix multiplication. `/` is **element-wise division**: `8 / 3` is about 2.67 at the same coordinate. The code rounds only the displayed result to two decimal places; the underlying quotient is not truncated. `np.multiply(a, b)` matches `a * b`; `np.divide(a, b)` matches `a / b` and normally produces floating-point values even from integer inputs.

If the second operand is one number, NumPy applies it to each position:

```python
print((a + 2).tolist()) # [[9, 10, 11], [12, 13, 14]]
```

This is a convenient extension of the same position-by-position idea. When both operands are arrays of different shapes, NumPy may apply broadcasting rules. In this lesson, use equal shapes or a scalar so the meaning of each pair stays clear.

## Whole groups and leftovers

`//` is **element-wise floor division**. It gives the greatest whole number no larger than each quotient. `%` is the **element-wise remainder** after making those whole groups:

```python
print((a // b).tolist())
# [[3, 2, 2], [3, 2, 2]]
print((a % b).tolist())
# [[1, 2, 1], [1, 3, 2]]
print(8 // 3, 8 % 3) # 2 2
```

At position `[0, 1]`, eight items form two complete groups of three, leaving two: `8 == 3 * 2 + 2`. `np.mod(a, b)` matches `a % b`. For negative numbers, floor division rounds toward negative infinity: `-7 // 3 == -3`, and `-7 % 3 == 2`; the relation `-7 == 3 * (-3) + 2` still holds. This is why `//` is not simply “remove decimal digits.”

| Expression | Operation at `a[0, 1] = 8`, `b[0, 1] = 3` | Result |
| --- | --- | --- |
| `a + b` or `np.add(a, b)` | add | `11` |
| `a - b` or `np.subtract(a, b)` | subtract | `5` |
| `a * b` or `np.multiply(a, b)` | multiply | `24` |
| `a / b` or `np.divide(a, b)` | divide | `2.666...` |
| `a // b` | full groups | `2` |
| `a % b` or `np.mod(a, b)` | leftover | `2` |

## Raise each value to a power

`**` performs **element-wise exponentiation**. A power of 2 means multiply each number by itself:

```python
print((a ** 2).tolist())
# [[49, 64, 81], [100, 121, 144]]
print(np.power(a, 2)[0, 1]) # 64
```

`np.power(a, 2)` matches `a ** 2`. With matching array shapes, an exponent array can also specify a different power at each coordinate. A negative integer exponent applied to an integer NumPy array raises `ValueError`; if a reciprocal is intended, use suitable floating-point input after checking that zero bases are handled.

## Check the divisor before calculating

Division by zero does not represent a valid rate or group size. NumPy can warn and produce `inf` or `nan` in floating-point division, so do not accept those values silently. For data that should have no zero divisors, check first:

```python
divisors = np.array([2, 0, 4])
if np.any(divisors == 0):
    print("Fix or exclude zero divisors before dividing.")
else:
    print(np.array([7, 8, 9]) / divisors)
# Fix or exclude zero divisors before dividing.
```

Here `np.any()` asks whether at least one position satisfies the zero condition; comparison and logic are studied in the next lesson. If zero means a genuinely missing or undefined rate, decide how to represent that case explicitly rather than replacing zero with one without justification.

## Guided lab

Download [Element-wise arithmetic lab](QAI.02.02.19_Element_Wise_Arithmetic_Lab.zip), extract it, and run inside the extracted folder:

```bash
python -m pip install -r requirements.txt
python element_wise_arithmetic.py
python check_element_wise_arithmetic.py
```

The program prints the arrays, seven arithmetic results, and one coordinate trace. The checker verifies operators, named functions, shapes, and divisor handling and prints `All checks passed.`

**Trace first:** at `[0, 1]`, the inputs are 8 and 3. Predict addition 11, subtraction 5, multiplication 24, division `8/3`, floor division 2, remainder 2, and `8**2 == 64`.

**Controlled variation:** create `changed = a.copy()` and set `changed[0, 1] = 14`. With the same `b`, the coordinate produces `17`, `11`, `42`, `14/3`, `4`, `2`, and `196` in the same operation order. `a[0, 1]` stays 8.

**Debug:** If `/` gives a warning or an infinite result, inspect the corresponding divisor and the intended meaning of zero. If a calculation with two arrays fails because their shapes cannot be matched, check which rows and columns are meant to correspond; do not reorder measurements merely to silence an error. If the displayed `2.67` is mistaken for the full `8/3` value, remember that `round` changes the display result in this example.

## Independent mini-project: study-time plan

Two learners have planned task minutes `planned = np.array([[12, 15], [20, 22]])` and completed minutes `done = np.array([[5, 7], [8, 10]])`. Calculate remaining minutes, total minutes recorded in both arrays, the ratio completed/planned, complete five-minute groups within the completed time and leftover minutes, and the square of each completed value. Print the results. Compare with `mini_project_reference.py` in the lab.

Expected output:

```text
remaining [[7, 8], [12, 12]]
combined [[17, 22], [28, 32]]
ratio [[0.417, 0.467], [0.4, 0.455]]
groups [[1, 1], [1, 2]]
leftover [[0, 2], [3, 0]]
squared [[25, 49], [64, 100]]
```

The ratio line displays values rounded to three decimal places. The full reference solution is:

```python
import numpy as np

planned = np.array([[12, 15], [20, 22]])
done = np.array([[5, 7], [8, 10]])
remaining = np.subtract(planned, done)
combined = np.add(planned, done)
ratio = np.divide(done, planned)
groups = done // 5
leftover = np.mod(done, 5)
squared = np.power(done, 2)
print("remaining", remaining.tolist())
print("combined", combined.tolist())
print("ratio", np.round(ratio, 3).tolist())
print("groups", groups.tolist())
print("leftover", leftover.tolist())
print("squared", squared.tolist())
```

## Check your understanding

1. **What pairs with `a[1, 2]` in `a + b`?** `b[1, 2]`, at the same row and column.
2. **Does `a * b` multiply matrices?** No. It multiplies corresponding elements; here the output keeps shape `(2, 3)`.
3. **For 8 divided by 3, what are `/`, `//`, and `%`?** About 2.666..., 2, and 2.
4. **What should you do before dividing by observed data?** Check for zero divisors and decide what any undefined result should mean.

Remember: name the quantity represented by each operand, align corresponding positions, and inspect the result at one known coordinate.

## Further reading

- [NumPy: arithmetic functions](https://numpy.org/doc/stable/reference/routines.math.html)
- [NumPy: divide](https://numpy.org/doc/stable/reference/generated/numpy.divide.html), [floor_divide](https://numpy.org/doc/stable/reference/generated/numpy.floor_divide.html), and [mod](https://numpy.org/doc/stable/reference/generated/numpy.mod.html)
- [NumPy: power](https://numpy.org/doc/stable/reference/generated/numpy.power.html)
