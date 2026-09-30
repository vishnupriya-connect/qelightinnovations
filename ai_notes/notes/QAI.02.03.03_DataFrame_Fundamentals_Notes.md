# DataFrame fundamentals

## A table held in one Python object

A Pandas **DataFrame** is a two-dimensional table. Each **row** can describe one item; each **column** holds one kind of information. A **cell** is the value where a row meets a column.

```python
import pandas as pd

learners = pd.DataFrame(
    {
        "name": ["Asha", "Bala"],
        "score": [7, 9],
    },
    index=["L1", "L2"],
)
print(learners)
```

Expected display:

```text
    name  score
L1  Asha      7
L2  Bala      9
```

`pd.DataFrame()` **creates** the DataFrame object. The dictionary keys become **column labels** (`"name"`, `"score"`); each list supplies the cells down one column. Both lists contain two entries, one for each row. The supplied **index** gives row labels (`"L1"`, `"L2"`). Without it, Pandas would use default row labels `0` and `1`.

Trace one cell: row `"L2"` means Bala's row; column `"score"` means scores; their meeting point contains `9`.

## Read its structure

```python
print(learners.index.tolist())     # ['L1', 'L2']
print(learners.columns.tolist())   # ['name', 'score']
print(learners.shape)              # (2, 2)
print(learners.ndim)               # 2
print(learners.loc["L2", "score"])  # 9
```

**Shape** is `(number of rows, number of columns)`. **Dimensions** here means the two axes of a table: the row index and the columns. `ndim` is `2` even if a DataFrame has only one column. `learners.loc["L2", "score"]` uses row and column labels to locate a cell.

## Data types belong to columns

A **data type**, or `dtype`, describes what kind of values a column stores. The `name` column contains text; `score` contains integers. A DataFrame can have different dtypes in different columns:

```python
print(learners.dtypes)
print(learners["score"].dtype)
```

`learners.dtypes` gives one dtype per column. The exact text and integer dtype names can vary by Pandas version and platform. `learners["score"].dtype` gives the **column data type** for `score`. A mixed table does not have one useful single dtype for all its columns; inspect `dtypes` rather than assuming that all cells share a type.

## Four ways to create the same table

The first example used a **dictionary of columns**. Each key names a column and each list gives that column's values. You can also use a **list of dictionaries**, where each dictionary describes a row:

```python
from_rows = pd.DataFrame(
    [
        {"name": "Asha", "score": 7},
        {"name": "Bala", "score": 9},
    ],
    index=["L1", "L2"],
)
```

A **list of lists** supplies rows in order. Because its values do not name columns, supply `columns=`:

```python
from_lists = pd.DataFrame(
    [["Asha", 7], ["Bala", 9]],
    index=["L1", "L2"],
    columns=["name", "score"],
)
```

A two-dimensional **NumPy array** can also become a DataFrame. Here it contains only numeric values, so use numeric column names:

```python
import numpy as np

counts = np.array([[7, 2], [9, 3]], dtype=np.int32)
from_array = pd.DataFrame(
    counts,
    index=["L1", "L2"],
    columns=["score", "tasks"],
)
print(from_array.shape)             # (2, 2)
print(from_array.loc["L2", "tasks"]) # 3
```

For the first three constructions, the same row and column labels lead to the same table. The NumPy example is another table with different columns. Pandas supplies labels around the array's existing rows and columns; the array must have a compatible two-dimensional shape for this example.

| Input | Represents | Name the columns with |
| --- | --- | --- |
| Dictionary of equal-length lists | Each key is one column | Dictionary keys |
| List of dictionaries | Each dictionary is one row | Keys in the row dictionaries |
| List of lists | Each inner list is one row | `columns=[...]` |
| Two-dimensional NumPy array | Rows and columns of array values | `columns=[...]` |

## Guided lab

Download [DataFrame fundamentals lab](QAI.02.03.03_DataFrame_Fundamentals_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python dataframe_fundamentals.py
python check_dataframe_fundamentals.py
```

**Trace before running:** Predict the row and column labels, shape, dimensions, and the value at `"L2"` / `"score"`. Predict whether `from_rows` and `from_lists` represent the same table.

**Controlled variation:** Add `"Charu"` with score `8` and row label `"L3"` to each of the three learner-table constructions. Predict their new shape and the value at `"L3"` / `"score"`. Restore the original examples before running the supplied checker.

**Debug:** A dictionary with a two-name list and a three-score list raises a `ValueError`: one value is needed for every row in each column. A list of lists with two values per row but three column labels also fails. Check lengths and `columns=` before trying to read cells. A misspelled row or column label raises `KeyError`.

## Independent mini-project: practice log

Create a DataFrame from a list of dictionaries. Each row is a practice session: `{"topic": "Python", "minutes": 20}` and `{"topic": "Pandas", "minutes": 30}`. Use index labels `"S1"` and `"S2"`. Print the shape, row and column labels, the dtype of the `minutes` column, and the cell at `"S2"` / `"minutes"`. The lab includes `mini_project_reference.py`.

Expected output (the integer dtype name may vary):

```text
shape (2, 2)
rows ['S1', 'S2']
columns ['topic', 'minutes']
minutes type integer
S2 minutes 30
```

Full reference solution:

```python
import pandas as pd

practice = pd.DataFrame(
    [
        {"topic": "Python", "minutes": 20},
        {"topic": "Pandas", "minutes": 30},
    ],
    index=["S1", "S2"],
)
print("shape", practice.shape)
print("rows", practice.index.tolist())
print("columns", practice.columns.tolist())
print("minutes type", "integer" if pd.api.types.is_integer_dtype(practice["minutes"].dtype) else "other")
print("S2 minutes", practice.loc["S2", "minutes"])
```

## Check your understanding

1. **Which object holds the table?** A DataFrame.
2. **In a dictionary of lists, what becomes a column label?** Each dictionary key.
3. **What does shape `(3, 2)` mean?** Three rows and two columns.
4. **Why supply `columns=` for a list of lists or plain NumPy array?** The values do not carry column names.
5. **Can one DataFrame contain text and integer columns?** Yes; inspect the dtype of each column with `dtypes`.
6. **What does `ndim` report for a one-column DataFrame?** `2`, because it still has row and column axes.

Remember: identify what represents each row and column in the input, then verify the resulting labels, shape, and column dtypes.

## Further reading

- [Pandas: What kind of data does pandas handle?](https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html)
- [Pandas: DataFrame reference](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
