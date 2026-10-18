# Pandas basics

## A table with labels

**Pandas** is a Python library for working with tabular data: values arranged in rows and columns. A classroom score sheet is a table. One row can describe one learner; one column can hold one kind of information, such as a name or a score. A **cell** is the value at the meeting point of one row and one column.

First import the library:

```python
import pandas as pd
```

`import pandas` also works, but then you would write `pandas.DataFrame(...)`. The common **import alias** `pd` is a short name for the same library; it does not change the library.

Pandas gives you two main kinds of **objects**, or values you can keep in variables:

| Object | Picture | Labels |
| --- | --- | --- |
| `Series` | One line of values | An index labels its positions |
| `DataFrame` | A table with rows and columns | An index labels rows; column names label columns |

## One labeled line: Series

```python
import pandas as pd

scores = pd.Series([7, 9, 8], index=["Asha", "Bala", "Charu"])
print(scores)
print(scores["Bala"])  # 9
```

The three numbers are **values**. `"Asha"`, `"Bala"`, and `"Charu"` are **labels** in the **index**. A label identifies a place in this Series. `scores["Bala"]` asks for the value carrying that label. A Series is one-dimensional: it has one labeled axis, its index.

## A labeled table: DataFrame

```python
table = pd.DataFrame(
    {"name": ["Asha", "Bala"], "score": [7, 9]},
    index=["L1", "L2"],
)
print(table)
```

Expected display:

```text
    name  score
L1  Asha      7
L2  Bala      9
```

Here `table` is a **DataFrame**. `"L1"` and `"L2"` are row labels in its index. `"name"` and `"score"` are column labels. The first row contains Asha and 7; the cell for row `"L2"` and column `"score"` holds 9. Pandas prints row and column labels beside the values; the labels help you identify data.

You can inspect those parts without guessing from the display:

```python
print(table.index.tolist())    # ['L1', 'L2']
print(table.columns.tolist())  # ['name', 'score']
print(table.shape)             # (2, 2): two rows, two columns
print(table["score"].tolist()) # [7, 9]
print(type(table["score"]).__name__)  # Series
print(table.loc["L2", "score"])        # 9
```

Selecting one column gives a Series whose index still identifies the rows. `.loc[row_label, column_label]` shows the row-and-column address of one cell. The details of creating and selecting Series and DataFrames are explored in later lessons.

## What does axis mean?

An **axis** is a direction of labels in a Pandas object. A DataFrame has two: `axis=0` refers to its row index, and `axis=1` refers to its columns. For a Series, its index is its single axis. In ordinary reading, say “rows” and “columns”; use axis numbers when an operation asks for them.

```python
print(table.axes[0].tolist())  # ['L1', 'L2']: row axis
print(table.axes[1].tolist())  # ['name', 'score']: column axis
```

If you leave out `index=...` when creating this DataFrame, Pandas supplies default row labels `0` and `1`. These labels are not an automatic `"name"` column or a learner ID. A DataFrame also allows repeated index labels, so do not assume a label uniquely identifies a row unless you checked or designed it that way.

## Guided lab

Download [Pandas basics lab](QAI.02.03.01_Pandas_Basics_Lab.zip), extract it, and run inside the extracted folder:

```bash
python -m pip install -r requirements.txt
python pandas_basics.py
python check_pandas_basics.py
```

**Trace before running:** The lab creates three scores with learner labels and a two-row table. Predict the label of the second table row, the two column names, and the type returned by selecting the `score` column. Run it and compare with the printed trace.

**Controlled variation:** Change Bala's score from 9 to 10 in both examples. Predict which printed values change. Rerun the checker after making the matching change to its expected values, or restore the original score first.

**Debug:** `table["Score"]` raises `KeyError` because the column label is `"score"` with a lowercase `s`. Print `table.columns.tolist()` and use the exact label. If `import pandas as pd` raises `ModuleNotFoundError`, install the lab requirements in the same Python environment used to run the script.

## Independent mini-project: a tiny reading log

Make a table with rows labeled `"D1"` and `"D2"`. Give it two columns: `"book"` with values `"River"` and `"Sky"`, and `"pages"` with values `12` and `15`. Print the row labels, column labels, the `"pages"` column as a list, the type of that column, and the cell at row `"D2"`, column `"pages"`. The lab includes `mini_project_reference.py`.

Expected output:

```text
rows ['D1', 'D2']
columns ['book', 'pages']
pages [12, 15]
column type Series
D2 pages 15
```

Full reference solution:

```python
import pandas as pd

reading = pd.DataFrame(
    {"book": ["River", "Sky"], "pages": [12, 15]},
    index=["D1", "D2"],
)
print("rows", reading.index.tolist())
print("columns", reading.columns.tolist())
print("pages", reading["pages"].tolist())
print("column type", type(reading["pages"]).__name__)
print("D2 pages", reading.loc["D2", "pages"])
```

## Check your understanding

1. **What is Pandas used for here?** Working with a table of labeled rows and columns.
2. **How is a Series different from a DataFrame?** A Series has one labeled axis; a DataFrame has a row index and a column axis.
3. **What does `pd` mean?** It is a short import alias for `pandas`.
4. **In `table.loc["L2", "score"]`, which part names a row?** `"L2"`; `"score"` names the column.
5. **Does `axis=0` refer to the DataFrame's columns?** No. It refers to its row index; `axis=1` refers to columns.

Remember: identify a table's rows, columns, index, and cell labels before working with its values.

## Further reading

- [Pandas: What kind of data does pandas handle?](https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html)
- [Pandas: Package overview](https://pandas.pydata.org/docs/getting_started/overview.html)
