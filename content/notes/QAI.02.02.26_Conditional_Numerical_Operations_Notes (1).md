# Conditional numerical operations

## Choose a value at each position

Suppose readings are arranged by learner and task. We want to keep readings of at least 50 and show 0 for the rest:

```python
import numpy as np

readings = np.array([[-5, 45, 110], [20, 75, 95]])
condition = readings >= 50
selected = np.where(condition, readings, 0)
print(condition.tolist())
# [[False, False, True], [False, True, True]]
print(selected.tolist())
# [[0, 0, 110], [0, 75, 95]]
```

A **condition** asks whether each value meets a rule. Here the **condition array** has Boolean values at the same coordinates as `readings`. **Conditional selection** with the three-argument `np.where(condition, true_value, false_value)` makes one **conditional value** at each position. The **true-value argument** is `readings`: use that entry when its condition is true. The **false-value argument** is `0`: use zero otherwise. At `[0, 2]`, the reading 110 is kept; at `[0, 1]`, 45 is replaced by 0 in the result. The original remains unchanged.

The previous lesson used one-argument `np.where(condition)` to find *positions*. The three-argument form here constructs a new *array of values*. Scalar and array value arguments can be used together when their shapes are compatible for broadcasting.

## Put values between two bounds

`np.clip()` limits each input to an interval:

```python
bounded = np.clip(readings, 0, 100)
print(bounded.tolist())
# [[0, 45, 100], [20, 75, 95]]
```

Here 0 is the **lower bound** and 100 is the **upper bound**. A **clip value** below 0 becomes 0; one above 100 becomes 100; a value already inside the interval stays the same. In the example, `-5` becomes 0 and 110 becomes 100. `readings.clip(0, 100)` gives the same result. Clipping can be useful for display or a specified operational limit, but if `-5` and 110 are invalid measurements, inspect and report the source issue rather than treating the clipped values as genuine observations.

## Compare two candidate values at each position

`np.maximum()` gives the greater of two corresponding inputs. `np.minimum()` gives the smaller. With a scalar as one input:

```python
lowered = np.maximum(readings, 0)
raised = np.minimum(readings, 100)
print(lowered.tolist()) # [[0, 45, 110], [20, 75, 95]]
print(raised.tolist())  # [[-5, 45, 100], [20, 75, 95]]
print(np.minimum(np.maximum(readings, 0), 100).tolist())
# [[0, 45, 100], [20, 75, 95]]
```

The first call supplies a minimum allowed output of 0 by taking the greater candidate; the second supplies a maximum allowed output of 100 by taking the smaller candidate. Applying both recreates clipping when lower bound is no greater than upper bound. These are **element-wise maximum value** and **element-wise minimum value** operations. They differ from `np.max(readings)` and `np.min(readings)`, which reduce the entire array to one number.

The second candidate can itself be an array:

```python
thresholds = np.array([[0, 50, 100], [10, 80, 90]])
print(np.maximum(readings, thresholds).tolist())
# [[0, 50, 110], [20, 80, 95]]
```

At `[1, 1]`, `max(75, 80)` contributes 80. The input arrays have matching shapes; broadcasting rules from the previous lesson also apply to compatible scalar, vector, or matrix inputs. For ordinary numeric inputs, `np.clip(readings, 0, 100)` matches `np.minimum(np.maximum(readings, 0), 100)`.

| Goal | Expression | Result at input `-5` | Result at input `110` |
| --- | --- | --- | --- |
| Keep only readings `>= 50`, otherwise 0 | `np.where(readings >= 50, readings, 0)` | `0` | `110` |
| Limit to `[0, 100]` | `np.clip(readings, 0, 100)` | `0` | `100` |
| Enforce lower bound 0 | `np.maximum(readings, 0)` | `0` | `110` |
| Enforce upper bound 100 | `np.minimum(readings, 100)` | `-5` | `100` |

For arrays containing NaN, `np.maximum()` and `np.minimum()` propagate it at the corresponding position. Address missing values according to the data rule before interpreting a bounded or selected result.

## Guided lab

Download [Conditional numerical operations lab](QAI.02.02.26_Conditional_Numerical_Operations_Lab.zip), extract it, and run in the folder:

```bash
python -m pip install -r requirements.txt
python conditional_numerical_operations.py
python check_conditional_numerical_operations.py
```

The program prints the condition, selected values, clipped readings, and element-wise bounds. The checker verifies every result and reports `All checks passed.`

**Trace before running:** at `[0, 0]`, `-5 >= 50` is false; `where` gives 0, `maximum(-5, 0)` gives 0, and `minimum(-5, 100)` gives -5. At `[0, 2]`, `where` retains 110 while `clip` gives 100.

**Controlled variation:** copy `readings` and change `[0, 1]` from 45 to 55. At that position the condition becomes true, `where` returns 55, and `clip` also returns 55. The source array remains at 45.

**Debug:** If you call `np.where(condition)` and receive positions rather than selected values, supply the true- and false-value arguments. If `np.max()` returns one number when you need one per element, use `np.maximum()` with the second candidate. Check that the lower bound is no greater than the upper bound before clipping; reversed bounds do not represent the intended interval.

## Independent mini-project: reading display

Use `temperatures = np.array([[-3, 18, 42], [5, 31, 12]])`. (1) Clip readings to `[0, 35]` for a bounded display. (2) Create a condition marking readings outside that interval and use three-argument `np.where()` to make a 1/0 alert array. (3) Keep bounded readings of at least 20 and show 0 for the others. (4) Separately calculate element-wise maximum with 10 and minimum with 30 on the *original* readings. Print all results. The lab contains `mini_project_reference.py`.

Expected output:

```text
bounded [[0, 18, 35], [5, 31, 12]]
alerts [[1, 0, 1], [0, 0, 0]]
warm [[0, 0, 35], [0, 31, 0]]
lower at 10 [[10, 18, 42], [10, 31, 12]]
upper at 30 [[-3, 18, 30], [5, 30, 12]]
original [[-3, 18, 42], [5, 31, 12]]
```

The bounded output is a display transformation; the alert array preserves evidence of out-of-range readings. Full reference solution:

```python
import numpy as np

temperatures = np.array([[-3, 18, 42], [5, 31, 12]])
bounded = np.clip(temperatures, 0, 35)
outside = (temperatures < 0) | (temperatures > 35)
alerts = np.where(outside, 1, 0)
warm = np.where(bounded >= 20, bounded, 0)
print("bounded", bounded.tolist())
print("alerts", alerts.tolist())
print("warm", warm.tolist())
print("lower at 10", np.maximum(temperatures, 10).tolist())
print("upper at 30", np.minimum(temperatures, 30).tolist())
print("original", temperatures.tolist())
```

## Check your understanding

1. **What does each argument of `np.where(condition, x, y)` do?** The condition decides per position; `x` supplies the result when true and `y` when false.
2. **Does `np.where(readings >= 50, readings, 0)` enforce an upper bound of 100?** No. It keeps 110; `clip` would limit it to 100.
3. **How does `np.maximum(readings, 0)` differ from `np.max(readings)`?** The former returns one value per position; the latter returns one whole-array maximum by default.
4. **Why retain the original after clipping?** To distinguish the bounded display from actual out-of-range measurements.

Remember: `where` chooses between alternatives, `clip` enforces an interval, and `maximum`/`minimum` compare candidates at each position.

## Further reading

- [NumPy: where](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
- [NumPy: clip](https://numpy.org/doc/stable/reference/generated/numpy.clip.html)
- [NumPy: maximum](https://numpy.org/doc/stable/reference/generated/numpy.maximum.html) and [minimum](https://numpy.org/doc/stable/reference/generated/numpy.minimum.html)
