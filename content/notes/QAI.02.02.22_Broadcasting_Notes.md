# Broadcasting

## Apply one value at several positions

Suppose a table has rows for learners and columns for tasks:

```python
import numpy as np

minutes = np.array([[10, 20, 30], [40, 50, 60]])
with_break = minutes + 5
print(minutes.shape, with_break.shape) # (2, 3) (2, 3)
print(with_break.tolist()) # [[15, 25, 35], [45, 55, 65]]
```

**Broadcasting** lets a NumPy operation use an input at multiple corresponding positions when its shape is **compatible** with the other input. Here **scalar broadcasting** uses the single number 5 for every element. The **broadcast result** has shape `(2, 3)` and the original array is unchanged. NumPy need not build a full `(2, 3)` array of fives just to perform the addition.

## A vector lines up with the rightmost axis

A one-dimensional vector of three task adjustments aligns with the table's three columns:

```python
task_bonus = np.array([1, 2, 3])
adjusted = minutes + task_bonus
print(minutes.shape, task_bonus.shape, adjusted.shape)
# (2, 3) (3,) (2, 3)
print(adjusted.tolist()) # [[11, 22, 33], [41, 52, 63]]
```

This is **vector broadcasting**. Think of shape `(3,)` as temporarily aligned with `(1, 3)`; the length-one row axis is used across both learners. At `[1, 2]`, `minutes[1, 2] + task_bonus[2]` is `60 + 3 == 63`. The imagined `(1, 3)` has a **singleton dimension**: an axis of length one.

For a different bonus per learner, the two-value vector `(2,)` does *not* automatically align with the two rows. It is right-aligned against the *three columns*, so `(2, 3) + (2,)` is an **incompatible shape** and raises a broadcasting error. Give the learner adjustment an explicit length-one column axis:

```python
learner_bonus = np.array([100, 200]).reshape(2, 1)
per_learner = minutes + learner_bonus
print(learner_bonus.shape, per_learner.shape) # (2, 1) (2, 3)
print(per_learner.tolist()) # [[110, 120, 130], [240, 250, 260]]
```

At `[1, 2]`, the second learner's 200 is reused across the task axis: `60 + learner_bonus[1, 0] == 260`. The task axis is the **broadcast axis** for this input.

## Check compatibility from the right

For **array compatibility**, align shape entries from the rightmost end. Two lengths at the same position are compatible if they are equal or one of them is 1. Missing leading entries act like 1. The resulting length at each position is the larger one. This yields a **compatible shape** for the calculation:

| First shape | Second shape, right aligned | Compatible? | Result shape |
| --- | --- | --- | --- |
| `(2, 3)` | scalar `()` | yes | `(2, 3)` |
| `(2, 3)` | `(3,)` → `(1, 3)` | yes | `(2, 3)` |
| `(2, 3)` | `(2, 1)` | yes | `(2, 3)` |
| `(2, 3)` | `(2,)` → `(1, 2)` | no: `3` versus `2` | error |
| `(2, 3, 4)` | `(3, 4)` → `(1, 3, 4)` | yes | `(2, 3, 4)` |

Shape compatibility is only a numeric rule. It cannot tell whether a three-value vector truly represents tasks. Check the labels before relying on a broadcast result.

## A matrix can repeat across a leading axis

**Matrix broadcasting** can apply one two-dimensional `(learner, task)` correction table to each week in a three-dimensional `(week, learner, task)` array:

```python
weekly = np.arange(24).reshape(2, 3, 4)
correction = np.array([[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12]])
result = weekly + correction
print(weekly.shape, correction.shape, result.shape)
# (2, 3, 4) (3, 4) (2, 3, 4)
print(weekly[1, 2, 3], correction[2, 3], result[1, 2, 3])
# 23 12 35
```

The matrix aligns as though it had shape `(1, 3, 4)`. Its leading singleton week axis is used for both weeks. A two-dimensional `(2, 3)` matrix would be incompatible with `(2, 3, 4)` because its rightmost length 3 would meet 4. In general, operations such as addition use compatible shapes to determine the broadcast result; broadcasting does not permanently reshape either input.

## Guided lab

Download [Broadcasting lab](QAI.02.02.22_Broadcasting_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python broadcasting.py
python check_broadcasting.py
```

The program shows scalar, vector, column, and matrix broadcasting and prints a coordinate trace. The checker verifies the compatible results and the incompatible error; it reports `All checks passed.`

**Trace before running:** predict `minutes[1, 2] + task_bonus[2] == 63`, `minutes[1, 2] + learner_bonus[1, 0] == 260`, and `weekly[1, 2, 3] + correction[2, 3] == 35`.

**Controlled variation:** create a copy of `task_bonus`, change its third value from 3 to 9, and add it to `minutes`. The last column of *both rows* increases by six compared with `adjusted`. The original bonus and original minutes remain unchanged.

**Debug a broadcasting error:** `minutes + np.array([100, 200])` raises `ValueError` because `(2,)` aligns with the table's rightmost length 3, not its row count 2. If the values represent learners, reshape to `(2, 1)`. If they represent tasks, supply three task values. Do not reshape just to silence an error without confirming the intended axis meaning.

## Independent mini-project: adjust task minutes

Use `base = np.array([[20, 30, 40], [25, 35, 45]])`, task bonuses `[1, 2, 3]`, and learner bonuses `[10, 20]`. Add 5 to every base value; separately add the task vector to each row; then add both task and learner bonuses to the base table. Print the shapes and results and trace the last element of the combined result. The lab contains `mini_project_reference.py`.

Expected output:

```text
scalar (2, 3) [[25, 35, 45], [30, 40, 50]]
tasks (2, 3) [[21, 32, 43], [26, 37, 48]]
combined (2, 3) [[31, 42, 53], [46, 57, 68]]
trace 45 3 20 68
```

Full reference solution:

```python
import numpy as np

base = np.array([[20, 30, 40], [25, 35, 45]])
task_bonus = np.array([1, 2, 3])
learner_bonus = np.array([10, 20]).reshape(2, 1)
scalar = base + 5
tasks = base + task_bonus
combined = base + task_bonus + learner_bonus
print("scalar", scalar.shape, scalar.tolist())
print("tasks", tasks.shape, tasks.tolist())
print("combined", combined.shape, combined.tolist())
print("trace", base[1, 2], task_bonus[2], learner_bonus[1, 0], combined[1, 2])
```

## Check your understanding

1. **Why does `(2, 3) + (3,)` work?** The rightmost lengths match, and the missing leading length acts like one.
2. **Why does `(2, 3) + (2,)` fail?** Right alignment compares 3 and 2; neither is one.
3. **What shape should two learner bonuses have to apply across three tasks?** `(2, 1)`.
4. **What is the result shape for `(2, 3, 4) + (3, 4)`?** `(2, 3, 4)`, with the matrix used across the leading axis.

Remember: align shapes from the right, check each pair of lengths, then trace a value with meaningful axis labels.

## Further reading

- [NumPy: broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy: broadcasting rules for universal functions](https://numpy.org/doc/stable/reference/ufuncs.html)
