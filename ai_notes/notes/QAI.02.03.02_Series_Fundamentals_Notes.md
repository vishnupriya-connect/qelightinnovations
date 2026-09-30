# Series fundamentals

## One value for each label

A Pandas **Series** is a one-dimensional sequence of values with an **index**. The index contains **labels** that identify entries. Think of a small record of study minutes: each day label points to one number.

```python
import pandas as pd

minutes = pd.Series(
    [15, 25, 20],
    index=["Mon", "Tue", "Wed"],
    name="study_minutes",
)
print(minutes)
```

Expected display:

```text
Mon    15
Tue    25
Wed    20
Name: study_minutes, dtype: int64
```

The left side shows labels; the right side shows **Series values**. `name` describes the Series. `dtype` describes the type of its values; the exact integer width can depend on the environment. The **length** is the number of entries:

```python
print(minutes.index.tolist())  # ['Mon', 'Tue', 'Wed']
print(minutes.tolist())        # [15, 25, 20]
print(minutes.name)            # study_minutes
print(len(minutes))            # 3
print(minutes.dtype)           # integer dtype, such as int64
```

A label can be text or a number. A numeric label is still a label, so use an explicit selection method when you mean a position.

## Create a Series in three ways

`pd.Series()` is the **Series creation** function. A list supplies values; you can supply matching labels or let Pandas use `0, 1, 2, ...`:

```python
from_list = pd.Series([15, 25, 20], index=["Mon", "Tue", "Wed"])
default_index = pd.Series([15, 25, 20])
print(default_index.index.tolist())  # [0, 1, 2]
```

A dictionary supplies both keys and values. Its keys become labels:

```python
from_dict = pd.Series({"Mon": 15, "Tue": 25, "Wed": 20})
print(from_dict.index.tolist())  # ['Mon', 'Tue', 'Wed']
print(from_dict.tolist())        # [15, 25, 20]
```

A single **scalar** value can be repeated over labels that you provide:

```python
targets = pd.Series(30, index=["Mon", "Tue", "Wed"], name="target_minutes")
print(targets.tolist())  # [30, 30, 30]
```

The list needs as many values as labels. The scalar is one value repeated to match the index length.

## Select by label or position

```python
print(minutes.loc["Tue"])  # 25: label selection
print(minutes.iloc[1])     # 25: position selection, starting at zero
```

`.loc` looks up an index **label**; `.iloc` looks up a numbered **position**. If the label is an integer, `minutes.loc[1]` means label `1`, while `minutes.iloc[1]` means the second entry. A missing label raises `KeyError`; an out-of-range position raises `IndexError`.

## Slice a range

A **slice** asks for a consecutive part of the Series:

```python
print(minutes.loc["Mon":"Tue"].tolist())  # [15, 25]
print(minutes.iloc[0:2].tolist())          # [15, 25]
```

In this simple ordered index, a `.loc` label slice includes both named endpoints. An `.iloc` position slice stops before its end position, as in Python lists. Label slicing can be more involved when labels are unordered or repeated; begin with a known, ordered index.

## Filter with a condition

A comparison produces one Boolean value (`True` or `False`) for each entry. Use that mask to keep the entries whose condition is true:

```python
mask = minutes >= 20
print(mask.tolist())                 # [False, True, True]
long_days = minutes[mask]
print(long_days.index.tolist())     # ['Tue', 'Wed']
print(long_days.tolist())           # [25, 20]
```

This is a **Series Boolean filter**. The retained entries keep their original labels. The condition `>= 20` includes 20. The mask has one Boolean value per Series entry.

## Guided lab

Download [Series fundamentals lab](QAI.02.03.02_Series_Fundamentals_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python series_fundamentals.py
python check_series_fundamentals.py
```

**Trace before running:** Predict the result of `minutes.loc["Tue"]`, the labels in `minutes.iloc[0:2]`, and the labels retained by `minutes >= 20`. Compare each prediction with the printed trace.

**Controlled variation:** Change Wednesday's value from 20 to 19. Predict how the Boolean mask and filtered labels change; run again to check. Restore 20 before running the checker.

**Debug:** A misspelled `.loc` label raises `KeyError`: print `minutes.index.tolist()` and use an existing label. `minutes.iloc[3]` fails because this three-entry Series has positions `0`, `1`, and `2`. If a `.loc` slice has one more entry than expected, remember that its ending label is included in this ordered example.

## Independent mini-project: reading pages

Create a Series named `"pages"` from the dictionary `{"Mon": 8, "Tue": 12, "Wed": 10, "Thu": 15}`. Print its name, length, Tuesday's value by label, the first two values by position, and the labels and values for days with at least 10 pages. The lab contains `mini_project_reference.py`.

Expected output:

```text
name pages
length 4
Tue 12
first two [8, 12]
at least 10 labels ['Tue', 'Wed', 'Thu']
at least 10 values [12, 10, 15]
```

Full reference solution:

```python
import pandas as pd

pages = pd.Series(
    {"Mon": 8, "Tue": 12, "Wed": 10, "Thu": 15},
    name="pages",
)
selected = pages[pages >= 10]
print("name", pages.name)
print("length", len(pages))
print("Tue", pages.loc["Tue"])
print("first two", pages.iloc[:2].tolist())
print("at least 10 labels", selected.index.tolist())
print("at least 10 values", selected.tolist())
```

## Check your understanding

1. **What pairs each Series value with an identifier?** Its index labels.
2. **How is a dictionary converted to a Series?** `pd.Series(dictionary)` uses its keys as labels and values as Series values.
3. **What does `pd.Series(30, index=["Mon", "Tue"])` produce?** Two entries, each with value 30.
4. **Which method selects the second position?** `.iloc[1]`.
5. **Does `.loc["Mon":"Tue"]` include Tuesday here?** Yes, with this ordered index.
6. **What does `minutes[minutes >= 20]` retain?** Entries whose values are 20 or more, with their labels.

Remember: distinguish a label from a position, then check which values a slice or filter actually retains.

## Further reading

- [Pandas: Intro to data structures](https://pandas.pydata.org/docs/user_guide/dsintro.html)
- [Pandas: Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html)
