# Numerical-computing basics

## What are we trying to calculate?

Suppose a learner studies for **20**, **30**, and **10** minutes on three days. These numbers are **numerical data**: values on which it makes sense to perform arithmetic. Their total is `20 + 30 + 10 = 60` minutes. Their mean, or ordinary average, is `60 / 3 = 20` minutes per day.

Adding the values and finding their mean are **numerical operations**. **Numerical computing** means using a computer to represent such values and carry out calculations reliably. A simple example may use a short Python list; later lessons work with larger collections and examine how their structure affects operations.

| Item | In this example | Why it matters |
|---|---|---|
| Numerical data | `20, 30, 10` minutes | The values and unit give the calculation meaning |
| Operation | Sum | Answers “How much time altogether?” |
| Operation | Mean | Answers “How much per day on average?” |
| Result | `60` minutes and `20` minutes/day | Check against the arithmetic before trusting the program |

A course ID such as `103` may be written with digits, but adding course IDs normally has no useful meaning. Numerical work starts with an actual question and suitable measured or counted values, not just anything stored as a number. Units and data quality matter: a value in hours mixed with minutes would make the total misleading unless converted first.

## Use a numerical library when it helps

A **library** is reusable code written for common tasks. A **numerical library** provides tools for working with numbers. **NumPy** is a Python library used for numerical computing, with operations such as `sum` and `mean` and, in later lessons, its array data structure.

Python can sum a short list without NumPy:

```python
minutes = [20, 30, 10]
total = sum(minutes)  # 60
```

NumPy gives us a consistent numerical toolkit to learn and reuse as the work becomes more complex:

```python
import numpy

minutes = [20, 30, 10]
total = numpy.sum(minutes)
average = numpy.mean(minutes)
print(total, average)  # 60 20.0
```

`import` tells Python to load the named module and make it available to this program. Here `numpy` is the **imported library** name used to access its functions. `numpy.sum` means “the `sum` provided by NumPy.” `numpy.mean` means “the `mean` provided by NumPy.” The dot separates the module name from a name inside it. NumPy must be installed in the Python environment running the file before the import will succeed.

For this tiny example, the main benefit is a clear first demonstration of the library. Do not infer a speed advantage from adding NumPy to three numbers. In later work, choosing an appropriate data structure and measuring on a real workload matters more than the name of the library alone.

## Name the module with an alias

A **namespace** helps keep names organized: `numpy.sum` identifies NumPy's `sum` even if a program also uses Python's built-in `sum`. An **import alias** is a local shorter name for the imported module:

```python
import numpy as np

minutes = [20, 30, 10]
print(np.sum(minutes))   # 60
print(np.mean(minutes))  # 20.0
```

`np` is the widespread NumPy convention. It does not install another library or create another set of numbers. In this program, `np` refers to the NumPy module. The two styles are alternatives:

| Import line | Name available in that program | Call to find the sum |
|---|---|---|
| `import numpy` | `numpy` | `numpy.sum(minutes)` |
| `import numpy as np` | `np` | `np.sum(minutes)` |

After **only** `import numpy`, writing `np.sum(minutes)` gives `NameError` in a fresh program: the name `np` was never created there. After **only** `import numpy as np`, use `np.sum(minutes)`; do not assume the name `numpy` was also bound in your current namespace. You may import both names in one file, as the lab does solely to compare them; usual NumPy code simply writes `import numpy as np` once.

The alias is a choice in *your program's namespace*. It does not rename the package installed on disk. Reading `np.mean(...)` in another person's code means looking for an earlier `import numpy as np` in the same program or notebook context.

## Trace a controlled change

The initial list `[20, 30, 10]` has total **60** and mean **20.0**. Now replace the last value 10 with 40:

```python
minutes = [20, 30, 40]
print(np.sum(minutes))   # 90
print(np.mean(minutes))  # 30.0
```

The total increases by **30**, from 60 to 90. The number of days stays three, so the mean rises by `30 / 3 = 10`, from 20 to 30 minutes per day. Predict these numbers *before* running the file. If the mean is different, first inspect the input values and the count of days. A mean on an empty collection is not meaningful for this activity; the lab's helper raises a clear `ValueError` for empty input.

## Guided micro-lab

Download the [numerical-computing basics lab](QAI.02.02.01_Numerical_Computing_Basics_Lab.zip), unzip it, and run from its folder:

```sh
python numerical_basics.py
python check_numerical_basics.py
```

Use `python3` if needed. The ZIP includes `requirements.txt`. If NumPy is not installed in the Python environment you are using, install it in that environment with `python -m pip install -r requirements.txt`, then rerun the two files. The main program prints:

```text
NumPy imported: True
Full-name sum: 60
Alias mean: 20.0
Study minutes: [20, 30, 10]
Summary (total, mean): (60, 20.0)
Changed summary: (90, 30.0)
```

The first line is `True` because the lab imports NumPy by both names in the *same program* and checks that both names refer to the same module. The checker also uses a separate namespace to show that `import numpy` alone does not define `np`. It tests the two totals, means, and empty-input error.

**Your steps:**

1. Write the two sums and two means on paper or in a comment before running.
2. Run both files and compare output with your prediction.
3. In a copy, change the middle day's 30 minutes to 60 while leaving the other initial values 20 and 10. Predict the new total **90** and mean **30.0**. Run it and explain that the +30 change to one of three days raises the mean by 10.
4. Restore the supplied file before running the checker, since it checks the original and its supplied controlled change.

**Repair a mistake:** in a fresh scratch file, write `import numpy` and then try `np.sum([20, 30, 10])`. The `NameError` points to the missing local alias. Repair it by calling `numpy.sum(...)` or changing the import to `import numpy as np`. Record the error, the corrected line, and the result **60**. If the import itself raises `ModuleNotFoundError`, check that NumPy was installed for the *same Python interpreter* that runs your script; naming your own file `numpy.py` can also hide the real package.

## Transfer to a second small question

Two practice sessions last **15** and **45** minutes. Find their total and mean without looking at the result first. The reference solution is:

```python
import numpy as np

practice_minutes = [15, 45]
print(np.sum(practice_minutes))   # 60
print(np.mean(practice_minutes))  # 30.0
```

The total is **60 minutes** and the mean is **30 minutes per session**. Check that the denominator is the number of sessions, two, rather than the number of minutes. You can use Python's built-in `sum` for the total as well. Keep the input, hand calculation, code, and observed output so you can explain what each result means.

## Check your understanding

1. Which values are numerical data in the study example, and what unit do they use?
2. What is the difference between a numerical operation and a numerical library?
3. What does `import numpy` make available? What does `import numpy as np` make available?
4. Does the alias `np` install or duplicate NumPy?
5. Why does `np.mean(...)` fail after only `import numpy` in a fresh program?
6. What are the total and mean for `[20, 30, 40]`?
7. Why would summing course IDs not answer a useful study-duration question?

**Answers and reasoning**

1. The values **20, 30, 10**, measured in minutes.
2. An operation is the calculation, such as sum; a library supplies reusable functions for such work.
3. The full-name import binds `numpy`; the alias import binds `np` in the program's namespace.
4. No. It is another local name for the same imported module.
5. `np` is not defined by that import; call `numpy.mean(...)` or import with `as np`.
6. **90** total and **30.0** mean, because `90 / 3 = 30`.
7. IDs label courses; their sum is not a measurement of study time.

## Remember and retain

- Start with a numerical question, appropriate values, their unit, and a hand-checkable expected result.
- Import NumPy before calling its functions. `numpy` and `np` are names determined by the import statement.
- A namespace keeps function names attributable to their module; an alias makes common calls shorter.
- Keep the two import forms, initial and changed calculations, the repaired `NameError`, and the two-session transfer result for later review.

## Further reading

- [NumPy: absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy: installing and verifying](https://numpy.org/install/)
- [Python: modules and imports](https://docs.python.org/3/tutorial/modules.html)
