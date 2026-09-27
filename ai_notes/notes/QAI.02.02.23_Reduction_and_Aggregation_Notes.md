# Reduction and aggregation

## Turn many values into a summary

Suppose a table records counts for two learners across three tasks:

```python
import numpy as np

counts = np.array([[1, 2, 3], [4, 5, 6]])
print(counts.shape)     # (2, 3)
print(np.sum(counts))   # 21
print(np.mean(counts))  # 3.5
```

A **reduction** combines multiple array values into fewer values. **Aggregation** is the act of summarizing a collection; an **aggregate function** such as `sum()` or `mean()` produces an **aggregate value**. The **whole-array reduction** above uses all six entries and returns one value. The input table stays unchanged. You can also write `counts.sum()` and `counts.mean()`; the examples use `np.sum(counts)` to make the function and input clear.

## Choose a reduction axis

The **reduction axis** tells NumPy which positions to combine:

```python
print(np.sum(counts, axis=1).tolist())  # [6, 15]
print(np.sum(counts, axis=0).tolist())  # [5, 7, 9]
print(np.mean(counts, axis=1).tolist()) # [2.0, 5.0]
print(np.mean(counts, axis=0).tolist()) # [2.5, 3.5, 4.5]
```

For a **row-wise reduction**, `axis=1` combines the three task columns within each learner row. The row axis remains, giving one result per learner: `[1 + 2 + 3, 4 + 5 + 6]`. For a **column-wise reduction**, `axis=0` combines the two learner rows, giving one result per task: `[1 + 4, 2 + 5, 3 + 6]`. With no axis, NumPy combines the whole array for these aggregate functions.

| Question | Expression | Output shape | Values |
| --- | --- | --- | --- |
| Total over everything? | `np.sum(counts)` | scalar | `21` |
| Total per learner? | `np.sum(counts, axis=1)` | `(2,)` | `[6, 15]` |
| Total per task? | `np.sum(counts, axis=0)` | `(3,)` | `[5, 7, 9]` |
| Average per learner? | `np.mean(counts, axis=1)` | `(2,)` | `[2.0, 5.0]` |

## Minimum, maximum, and median

`np.min()` gives the smallest value; `np.max()` gives the largest. `np.median()` gives the middle value after sorting, or the mean of the two middle values if there are an even number of entries:

```python
print(np.min(counts), np.max(counts), np.median(counts)) # 1 6 3.5
print(np.min(counts, axis=1).tolist())    # [1, 4]
print(np.max(counts, axis=0).tolist())    # [4, 5, 6]
print(np.median(counts, axis=1).tolist()) # [2.0, 5.0]
```

The whole array's sorted values are `1, 2, 3, 4, 5, 6`; its middle pair 3 and 4 gives median 3.5. These summaries preserve the meaning of the selected axis: a row median describes one learner, while a column median describes one task.

## Spread: variance and standard deviation

`np.var()` measures average squared distance from the mean; `np.std()` is the square root of variance, so it is in the original unit. For the first row `[1, 2, 3]`, the mean is 2; squared distances are `[1, 0, 1]`. NumPy's default `ddof=0` divides their sum by 3:

```python
print(np.var(counts, axis=1).tolist()) # [0.6666666666666666, 0.6666666666666666]
print(np.round(np.std(counts, axis=1), 3).tolist()) # [0.816, 0.816]
print(np.round(np.var(counts), 3), np.round(np.std(counts), 3))
# 2.917 1.708
```

The whole-array variance is `35/12`, about 2.917; its standard deviation is about 1.708. Rounding here is for display. A different statistical question may call for `ddof=1`, which divides by one fewer observation; that changes the result. State which definition you use when comparing reports.

## Find the position of a minimum or maximum

`np.argmin()` and `np.argmax()` return **indices**, not the minimum and maximum values:

```python
print(np.argmin(counts), np.argmax(counts)) # 0 5
print(np.argmin(counts, axis=1).tolist())  # [0, 0]
print(np.argmax(counts, axis=1).tolist())  # [2, 2]
print(counts[1, np.argmax(counts[1])])     # 6
```

With no axis, NumPy treats this array as a row-by-row flat sequence: the smallest value 1 is at flat index 0 and largest value 6 at flat index 5. With `axis=1`, each index is a *column position within a row*. With `axis=0`, each index is a *row position within a column*. If the extreme value occurs more than once in a selected group, the first occurrence is returned.

## Running totals and products keep the steps

`np.cumsum()` gives a **cumulative sum** at every successive position; `np.cumprod()` gives a **cumulative product**. Unlike one-value reductions, these keep an output for each input along the chosen axis:

```python
print(np.cumsum(counts, axis=1).tolist())
# [[1, 3, 6], [4, 9, 15]]
print(np.cumprod(counts, axis=1).tolist())
# [[1, 2, 6], [4, 20, 120]]
print(np.cumsum(counts, axis=0).tolist())
# [[1, 2, 3], [5, 7, 9]]
```

For each learner, the first cumulative sum is the first task; the next adds the second; the last adds the third. The cumulative product multiplies in that order. Specify an axis when the table's row/column meaning matters: without `axis`, both functions first flatten the array and return one `(6,)` sequence, so the running calculation crosses the boundary between learners.

## Guided lab

Download [Reduction and aggregation lab](QAI.02.02.23_Reduction_and_Aggregation_Lab.zip), extract it, and run in that folder:

```bash
python -m pip install -r requirements.txt
python reduction_and_aggregation.py
python check_reduction_and_aggregation.py
```

The program displays whole-table, learner, task, and running summaries. The checker verifies values, shapes, the default variance definition, and index meaning; it prints `All checks passed.`

**Trace before running:** predict row 1's sum `4 + 5 + 6 = 15`, column 2's sum `3 + 6 = 9`, row 1's `argmax` column index 2, and row 1's cumulative sum `[4, 9, 15]`.

**Controlled variation:** copy `counts`, change `[1, 2]` from 6 to 9, and recompute. Row 1's total becomes 18, column 2's total becomes 12, and row 1's maximum becomes 9 at column 2. The original table stays unchanged.

**Debug:** If you need totals per learner but receive three numbers, check whether you used `axis=0`; use `axis=1` to combine the task columns. If an `argmax` result 2 is mistaken for a maximum value, use it as a coordinate (`counts[1, 2]`) or call `max()`. A running sum without an axis flattens the array, so add `axis=1` for a separate progression per learner.

## Independent mini-project: learner task summary

Use `tasks = np.array([[2, 4, 6], [1, 3, 5]])`. Report total and mean per learner, total per task, whole-table median, row-wise minimum and maximum positions, row-wise variance and standard deviation (rounded to three decimals), and row-wise cumulative sum and product. A complete solution is in `mini_project_reference.py`.

Expected output:

```text
learner totals [12, 9]
learner means [4.0, 3.0]
task totals [3, 7, 11]
median 3.5
min positions [0, 0]
max positions [2, 2]
variance [2.667, 2.667]
std [1.633, 1.633]
running sum [[2, 6, 12], [1, 4, 9]]
running product [[2, 8, 48], [1, 3, 15]]
```

Full reference solution:

```python
import numpy as np

tasks = np.array([[2, 4, 6], [1, 3, 5]])
print("learner totals", np.sum(tasks, axis=1).tolist())
print("learner means", np.mean(tasks, axis=1).tolist())
print("task totals", np.sum(tasks, axis=0).tolist())
print("median", np.median(tasks))
print("min positions", np.argmin(tasks, axis=1).tolist())
print("max positions", np.argmax(tasks, axis=1).tolist())
print("variance", np.round(np.var(tasks, axis=1), 3).tolist())
print("std", np.round(np.std(tasks, axis=1), 3).tolist())
print("running sum", np.cumsum(tasks, axis=1).tolist())
print("running product", np.cumprod(tasks, axis=1).tolist())
```

## Check your understanding

1. **Which axis gives one sum per learner?** `axis=1`, reducing the task columns in each row.
2. **What does `np.argmax(counts, axis=1)[1] == 2` represent?** Column position 2 in learner row 1, not a value of 2.
3. **How is standard deviation related to variance?** It is the square root of variance, returning to the input unit.
4. **Why specify `axis=1` for `cumsum()`?** Each learner's running sequence then starts anew at the first task.

Remember: decide which values form each group, then choose its reduction axis and inspect the output shape.

## Further reading

- [NumPy: statistical functions](https://numpy.org/doc/stable/reference/routines.statistics.html)
- [NumPy: sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html), [argmax](https://numpy.org/doc/stable/reference/generated/numpy.argmax.html), [cumsum](https://numpy.org/doc/stable/reference/generated/numpy.cumsum.html), and [cumprod](https://numpy.org/doc/stable/reference/generated/numpy.cumprod.html)
