# Column selection lab and learner report

This local lab teaches single and multiple column selection, ordered selection, attribute-access limits, missing fields, mapping-based rename, and complete header replacement. It uses invented learners and marks; no account, API key, external dataset, or paid service is required.

## Run

Use Python 3.11 or later and Pandas 2.2 or 3.x. From this folder:

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

`lab.py` is the guided demonstration. `project.py` is the complete mini-project reference solution. `test_project.py` supplies 14 meaningful checks. `expected_lab.txt` and `expected_project.txt` contain exact stdout. Nothing is written to a data file by the examples.

## Independent task

Before reading the solution, write `build_report(source)` to require unique fields `student`, `python`, and `sql`, select them in that order, rename them to `learner`, `python_mark`, and `sql_mark`, and preserve source values and row labels. Exclude all extra fields. Reject missing required fields and duplicate source headers. Accept a zero-row table with the correct schema.

The reference deliberately makes no claim to validate mark ranges, data types, learner identities, or missing cell values. These are later validation tasks.

## Expected project stdout

```text
learner,python_mark,sql_mark
Anu,72,80
Bala,85,77
Chitra,91,89
```

The returned DataFrame keeps the row index even though the printed CSV omits it.

## Controlled variation

Replace the report request with `student` and `sql`, then rename `sql` to `database_mark`. The worked solution is in the notes and lab. Expected rows are `Anu,80`, `Bala,77`, `Chitra,89`.

## Debug record

- `Python` raises `KeyError` because the existing label is `python`. Inspect the schema and correct the key.
- A strict rename with old key `Python` raises `KeyError`; the default ignore mode would conceal that typo.
- Assigning one header to three columns raises `ValueError`; provide exactly three correctly ordered labels.
- `df.mean` is a method when a `mean` field exists. Use `df['mean']`.
- Duplicate `mark` labels make scalar selection a DataFrame. Reject duplicates when a report requires one unambiguous field per name.

## Evidence

Save the passing test output, compare stdout with the expected files, and explain why reorder and rename leave each learner's marks attached to the same row. Tests use Pandas equality assertions, exception checks, source immutability, and both empty and malformed input cases. Text column dtype display can differ across Pandas versions; the output checks avoid relying on that display.
