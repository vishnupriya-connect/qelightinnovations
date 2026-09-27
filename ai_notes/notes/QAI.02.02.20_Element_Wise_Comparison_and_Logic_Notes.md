# Element-wise comparison and logic

## Compare corresponding values

Suppose rows are learners and columns are tasks. A score and its target at the same coordinate form one comparison:

```python
import numpy as np

scores = np.array([[72, 48, 90], [55, 75, 60]])
targets = np.array([[70, 50, 90], [60, 70, 65]])
print((scores > targets).tolist())
# [[True, False, False], [False, True, False]]
print((scores < targets).tolist())
# [[False, True, False], [True, False, True]]
```

A **comparison operator** asks a question and returns `True` or `False`. These are **element-wise comparisons**: `scores[0, 0] == 72` is compared with `targets[0, 0] == 70`, so the first greater-than result is `True`. The **Boolean result array** has the same `(2, 3)` shape as these equal-shaped inputs. It contains truth values, not the original scores.

| Operation | Operator | Result for score 90 and target 90 |
| --- | --- | --- |
| **Equality comparison** | `==` | `True` |
| **Inequality comparison** | `!=` | `False` |
| **Greater-than comparison** | `>` | `False` |
| **Less-than comparison** | `<` | `False` |
| Greater than or equal | `>=` | `True` |
| Less than or equal | `<=` | `True` |

`=` assigns a value to a name; `==` compares values. For the whole arrays:

```python
print((scores == targets).tolist())
# [[False, False, True], [False, False, False]]
print((scores != targets).tolist())
# [[True, True, False], [True, True, True]]
```

Comparison with one number applies that question to each element: `scores >= 70` has shape `(2, 3)` and marks every score of at least 70.

## Combine conditions at each coordinate

Suppose a qualifying score is at least 70 but below 90. **Element-wise logical and** requires both conditions to be true *at the same position*:

```python
high = scores >= 70
below_ninety = scores < 90
qualifies = np.logical_and(high, below_ninety)
print(high.tolist())
# [[True, False, True], [False, True, False]]
print(qualifies.tolist())
# [[True, False, False], [False, True, False]]
```

At `[0, 2]`, score 90 passes `>= 70` but fails `< 90`, so `True AND False` is `False`. **Element-wise logical or** needs at least one condition. **Element-wise logical not** reverses each truth value:

```python
low = scores < 50
at_max = scores == 90
attention = np.logical_or(low, at_max)
print(attention.tolist())
# [[False, True, True], [False, False, False]]
print(np.logical_not(high).tolist())
# [[False, True, False], [True, False, True]]
```

The functions `np.logical_and()`, `np.logical_or()`, and `np.logical_not()` return Boolean results. On Boolean arrays, `high & below_ninety`, `low | at_max`, and `~high` are concise element-wise forms. Use parentheses around comparisons, for example `(scores >= 70) & (scores < 90)`, because Python gives `&` its own operator precedence. Python's words `and`, `or`, and `not` ask for one truth value for the entire expression and cannot combine a multi-element Boolean array this way. They can raise a “truth value of an array is ambiguous” error.

| `A` | `B` | `A AND B` | `A OR B` | `NOT A` |
| --- | --- | --- | --- | --- |
| `False` | `False` | `False` | `False` | `True` |
| `False` | `True` | `False` | `True` | `True` |
| `True` | `False` | `False` | `True` | `False` |
| `True` | `True` | `True` | `True` | `False` |

## Ask whether any or all positions pass

`np.any()` answers whether **at least one** value is true. `np.all()` answers whether **every** value is true:

```python
print(np.any(scores < 50))       # True
print(np.all(scores >= 50))      # False
print(np.any(scores < 50, axis=1).tolist())  # [True, False]
print(np.all(scores >= 50, axis=1).tolist()) # [False, True]
```

Without an `axis`, each produces one Boolean answer for the entire array. With `axis=1`, each evaluates across the columns in each row, producing one answer per learner. With `axis=0`, it evaluates down the rows, producing one answer per task. Unlike `np.logical_and()` and `np.logical_or()`, which retain positions, `any()` and `all()` summarize selected positions.

## Guided lab

Download [Comparison and logic lab](QAI.02.02.20_Element_Wise_Comparison_and_Logic_Lab.zip), extract it, and run in that folder:

```bash
python -m pip install -r requirements.txt
python element_wise_comparison_and_logic.py
python check_element_wise_comparison_and_logic.py
```

The program prints comparison arrays, combined conditions, and per-learner summaries. The checker verifies their positions and reports `All checks passed.`

**Trace before running:** at `[0, 2]`, the score and target are both 90. Predict `==` is `True`, `!=` and `>` are `False`, `high` is `True`, and `qualifies` is `False`.

**Controlled variation:** copy `scores`, change `[0, 2]` from 90 to 85, then repeat the comparisons. It becomes less than its target, `qualifies` becomes `True`, and `attention` becomes `False` at that position. The original score stays 90.

**Debug:** `scores >= 70 and scores < 90` cannot decide one truth value from several entries. Use `np.logical_and(scores >= 70, scores < 90)` or `(scores >= 70) & (scores < 90)`. If `np.any()` gives one answer when you need one per learner, add `axis=1`; do not confuse `axis=0` (one answer per task) with `axis=1` (one per learner).

## Independent mini-project: review task results

Use `results = np.array([[80, 45, 100], [60, 75, 50]])` and a same-shaped `attended = np.array([[True, True, False], [True, False, True]])`. A result is eligible when its score is at least 70 **and** the learner attended. It needs review if its score is below 50 **or** attendance is false. Print both Boolean arrays; then print whether any task needs review for each learner, whether each learner attended all tasks, and whether any eligible task exists for each learner. The lab contains `mini_project_reference.py`.

Expected output:

```text
eligible [[True, False, False], [False, False, False]]
review [[False, True, True], [False, True, False]]
any review [True, True]
all attended [False, False]
any eligible [True, False]
```

Full reference solution:

```python
import numpy as np

results = np.array([[80, 45, 100], [60, 75, 50]])
attended = np.array([[True, True, False], [True, False, True]])
eligible = np.logical_and(results >= 70, attended)
review = np.logical_or(results < 50, np.logical_not(attended))
print("eligible", eligible.tolist())
print("review", review.tolist())
print("any review", np.any(review, axis=1).tolist())
print("all attended", np.all(attended, axis=1).tolist())
print("any eligible", np.any(eligible, axis=1).tolist())
```

## Check your understanding

1. **At equal values, is `>` true?** No. `==`, `>=`, and `<=` are true; strict `>` and `<` are false.
2. **What does logical AND require?** Both conditions true at the same position.
3. **How do you get one “any low score?” answer per learner?** `np.any(scores < 50, axis=1)`.
4. **Why does plain Python `and` fail between two Boolean arrays?** It expects one truth value per operand, but each array contains several.

Remember: comparisons create a Boolean array; logical functions combine its positions; `any()` and `all()` summarize them.

## Further reading

- [NumPy: comparison functions](https://numpy.org/doc/stable/reference/routines.logic.html)
- [NumPy: logical_and](https://numpy.org/doc/stable/reference/generated/numpy.logical_and.html), [logical_or](https://numpy.org/doc/stable/reference/generated/numpy.logical_or.html), and [logical_not](https://numpy.org/doc/stable/reference/generated/numpy.logical_not.html)
- [NumPy: any](https://numpy.org/doc/stable/reference/generated/numpy.any.html) and [all](https://numpy.org/doc/stable/reference/generated/numpy.all.html)
