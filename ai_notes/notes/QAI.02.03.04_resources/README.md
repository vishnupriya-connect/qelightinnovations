# DataFrame structure inspection

Run from this folder:

```bash
python -m pip install -r requirements.txt
python dataframe_structure_inspection.py
python check_dataframe_structure_inspection.py
python mini_project_reference.py
```

Predict first and last labels, shape, known-value count, and mean before running. Expected core results are six rows, two columns, five known durations, and a mean of 36. Replace the unknown duration with 30 in a practice copy: count becomes six and mean becomes 35. Restore the original data to compare with the checker.

For independent practice, build the workshop report described in the notes. Record your actual output and complete `debug_record.md` before comparing with the reference.

Validated on 2026-09-30 with Python 3 and Pandas 2.2.3. The APIs were checked against current official Pandas documentation. Text dtype names, memory bytes, and sampled row identities may vary by environment; semantic checks avoid depending on them.
