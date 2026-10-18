# DataFrame structure inspection

## Inspect before changing a table

**Inspection** means looking at a table's structure and values before deciding what to do with it. After creating or loading a DataFrame, check its row count, column names, data types, and missing values. A printed preview alone can hide important problems.

Use this small practice-session table throughout the lesson:

```python
import pandas as pd

sessions = pd.DataFrame(
    {
        "topic": ["Python", "SQL", "Arrays", "Pandas", "Charts", "Review"],
        "minutes": [10, 20, None, 40, 50, 60],
    },
    index=["R1", "R2", "R3", "R4", "R5", "R6"],
)
print(sessions)
```

`None` marks an unknown duration in row `"R3"`. Pandas represents it as `NaN` in this numeric column. It is a **null**, or missing value; it does not mean zero minutes.

Expected display:

```text
     topic  minutes
R1  Python     10.0
R2     SQL     20.0
R3  Arrays      NaN
R4  Pandas     40.0
R5  Charts     50.0
R6  Review     60.0
```

## See the beginning, end, and a sample

`head(n)` returns the first `n` rows in the table's current order. `tail(n)` returns the last `n` rows. Both return DataFrames; even `head(1)` is a one-row table.

```python
print(sessions.head(1).index.tolist())  # ['R1']
print(sessions.tail(1).index.tolist())  # ['R6']
print(sessions.head(2).index.tolist())  # ['R1', 'R2']
print(sessions.tail(2).index.tolist())  # ['R5', 'R6']
```

Calling `head()` or `tail()` with no argument uses five rows. If the table has fewer than five, all available rows are returned. A first row is the first row in the present order; it is not necessarily the earliest date or the smallest value.

A **random row sample** selects rows from different positions:

```python
preview = sessions.sample(n=2, random_state=42)
print(len(preview))  # 2
```

`sample()` selects rows by default. Here sampling is without replacement, so a row is not selected twice. `random_state=42` makes this example repeatable for the same input and environment. A sample can help reveal patterns beyond the first rows, but two sampled rows do not prove that the whole table is correct.

## Inspect shape, columns, index, and types

```python
print(sessions.shape)              # (6, 2)
print(sessions.columns.tolist())   # ['topic', 'minutes']
print(sessions.index.tolist())     # ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
print(sessions.dtypes)
```

`shape` means `(rows, columns)`. `columns` holds column names; `index` holds row labels. `dtypes` gives the data type of each column. These are **attributes**, information read without parentheses. `head()`, `tail()`, and `sample()` are **methods**, operations called with parentheses.

The `minutes` dtype is `float64` here: ordinary floating-point storage can represent `NaN` alongside the numbers. The inferred text dtype for `topic` can differ between Pandas versions. Always inspect it rather than assuming its name.

## Read DataFrame information

`info()` prints a compact structural report: the index, columns, **non-null counts**, column types, and **memory usage**:

```python
sessions.info(show_counts=True, memory_usage="deep")
print(sessions.count().to_dict())  # {'topic': 6, 'minutes': 5}
```

A non-null count is the number of cells with an available value in that column. There are six rows but only five known minute values. `show_counts=True` explicitly requests counts. `info()` prints its report and returns `None`; assigning its return value does not store the report.

**Memory usage** estimates how much computer memory the DataFrame uses. You can inspect byte counts directly:

```python
usage = sessions.memory_usage(index=True, deep=True)
print(usage)
print("estimated bytes", int(usage.sum()))
```

`index=True` includes the index; `deep=True` asks Pandas to inspect stored objects more fully. The exact byte total depends on the environment and stored data. It is a useful estimate, not the complete memory use of the Python process or the size of a CSV file.

## Read descriptive statistics

**Descriptive statistics** summarize existing values. `describe()` returns a summary table. For this mixed DataFrame, its default result describes the numeric column:

```python
summary = sessions.describe()
print(summary.loc[["count", "mean", "min", "50%", "max"], "minutes"])
```

Expected values:

| Statistic | Meaning here | Result |
| --- | --- | --- |
| `count` | Number of known minute values | 5 |
| `mean` | Their average: `(10 + 20 + 40 + 50 + 60) / 5` | 36 |
| `std` | Sample standard deviation, a measure of spread | About 20.736 |
| `min` | Smallest known value | 10 |
| `25%` | Lower quartile for these ordered values | 20 |
| `50%` | Median, or middle known value | 40 |
| `75%` | Upper quartile for these ordered values | 50 |
| `max` | Largest known value | 60 |

`describe()` excludes missing values when calculating these statistics. The average is 36 over five known sessions, not 30 over six sessions. Statistics for known values do not establish what happened in the missing session.

```python
print(sessions.describe(include="all"))
```

`include="all"` also summarizes text columns. For text, `count` is the number of known values, `unique` is the number of distinct values, `top` is a most frequent value, and `freq` is its frequency. If several text values tie for `top`, do not rely on a particular tied value being chosen.

## Choose an inspection method

| Question | Start with | Limit |
| --- | --- | --- |
| What do rows look like? | `head()`, `tail()` | A preview may miss problems elsewhere |
| What appears away from the ends? | `sample()` | Random sampling is not complete validation |
| How many rows and columns exist? | `shape` | Does not count known values |
| What are labels and types? | `columns`, `index`, `dtypes` | Labels/types alone do not prove value correctness |
| Which columns have missing cells? | `info()` or `count()` | Does not explain why values are missing |
| How are numeric values distributed? | `describe()` | Summaries can hide unusual individual rows |
| What memory does this table use? | `memory_usage(deep=True)` | Does not measure all process memory |

For this six-row example, a manual baseline is easy: count rows, list the five known durations, and compute `180 / 5 = 36`. Use that independent calculation to check the library result. For a large table, combine previews with structural checks and later data-quality checks.

## Guided lab

Download [DataFrame structure inspection lab](QAI.02.03.04_DataFrame_Structure_Inspection_Lab.zip), extract it, and run:

```bash
python -m pip install -r requirements.txt
python dataframe_structure_inspection.py
python check_dataframe_structure_inspection.py
python mini_project_reference.py
```

The source scripts are also available in [practice resources](QAI.02.03.04_resources/README.md).

**Trace, with solution:** Predict shape, first and last labels, the known `minutes` count, and its mean. The answers are `(6, 2)`, `"R1"`, `"R6"`, `5`, and `36.0`. The missing value affects the count and denominator, but not the row count.

**Build:** Create the supplied table; print the first and last two rows; take a repeatable two-row sample; inspect labels and types; call `info()`; compute the statistics; compare the mean to the manual baseline. The lab is the complete reference implementation.

**Controlled variation, with solution:** Replace the missing duration with `30`. The row count stays six, the non-null count becomes six, and the mean becomes `(10+20+30+40+50+60)/6 = 35`. This is a deliberate input change for practice, not permission to guess missing real data.

**Failure and repair:** `print(sessions.shape())` raises `TypeError` because `shape` is an attribute. Use `print(sessions.shape)`. If `report = sessions.info()` leaves `report` as `None`, call `info()` to view it; use `io.StringIO()` and `info(buf=buffer)` when you need its printed text. The lab demonstrates capture.

## Independent mini-project: inspect workshop attendance

Create a DataFrame with labels `"W1"`–`"W4"` and columns `workshop = ["Python", "SQL", "Pandas", "Charts"]` and `attendees = [12, None, 18, 10]`. Build a short inspection report with shape, first and last labels, non-null counts, and the mean of known attendee counts. Include a repeatable sample and memory estimate. Do the task before opening the reference solution.

Acceptance: preserve the unknown count, report four rows and two columns, count three known attendee values, and calculate `40 / 3`. A sample must contain existing rows; memory usage must be positive. Exact sample rows and bytes are environment-dependent.

Expected core output:

```text
shape (4, 2)
first ['W1']
last ['W4']
non-null {'workshop': 4, 'attendees': 3}
known mean 13.333333
```

Full reference solution:

```python
import pandas as pd

workshops = pd.DataFrame(
    {
        "workshop": ["Python", "SQL", "Pandas", "Charts"],
        "attendees": [12, None, 18, 10],
    },
    index=["W1", "W2", "W3", "W4"],
)
print("shape", workshops.shape)
print("first", workshops.head(1).index.tolist())
print("last", workshops.tail(1).index.tolist())
print("non-null", workshops.count().to_dict())
print("known mean", round(workshops.describe().loc["mean", "attendees"], 6))
print("sample labels", workshops.sample(n=2, random_state=42).index.tolist())
print("estimated bytes", int(workshops.memory_usage(deep=True).sum()))
```

Save the script, actual output, and a short debug record containing the failed expression, error, explanation, and repair. The lab contains the reference, checker, and a debug-record template.

## Solved practice and teach-back

1. **Why can `shape[0]` be six while `describe()` reports count five?** Shape counts rows; numeric count excludes the missing duration.
2. **Does `head(1)` return a Series?** No, it returns a one-row DataFrame.
3. **Fix `sessions.columns()`.** Use `sessions.columns`; it is an attribute.
4. **Choose a first check for unexpected text in a numeric column.** Inspect `dtypes` and sample values; numeric `describe()` might otherwise omit that column. Investigate before conversion.
5. **Would two clean sampled rows justify declaring the table complete?** No. Sampling can miss missing or invalid entries; inspect counts and validate the full table.
6. **Why use a manual calculation here?** It checks the interpretation of the statistic independently of the library call.

Explain to another learner: “A preview shows examples; shape shows table size; counts show available values; statistics summarize those available values.” Demonstrate the six-row/five-value distinction and repair one attribute-versus-method error.

Missing-value treatment is developed in later Pandas lessons. This inspection stage detects the issue before changing the data.

## References

- [Pandas: DataFrame info](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html)
- [Pandas: DataFrame describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
- [Pandas: DataFrame sample](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)
- [Pandas: DataFrame memory usage](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.memory_usage.html)
