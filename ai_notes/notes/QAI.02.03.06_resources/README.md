# Row selection by position and batch mini-project

Use Python 3.11 or later with Pandas 2.2 or 3.x. This local lab requires no account, paid service, or external dataset. It uses invented learners and marks.

```bash
python -m pip install -r requirements.txt
python lab.py
python project.py
python -m unittest -v test_project.py
```

## Files

- `lab.py`: guided scalar, list, slice, step, negative, and two-axis selections; deliberate handled bounds and zero-step errors; controlled variation.
- `project.py`: full reference solution for `select_batch(source, start, batch_size)` and a batch-processing demonstration.
- `test_project.py`: 14 tests with exact expected values and labels, bounds, result dimensions, independent output, and invalid inputs.
- `expected_lab.txt`, `expected_project.txt`: exact standard output from the two scripts.

## Independent task

Implement a batch selector before reading `project.py`. Retain all columns and labels, select consecutive row positions, allow a short final batch and an empty result past the end, and leave the source unchanged when the result is edited. Reject non-Python-integer arguments, negative starts, and non-positive sizes.

The reference uses an exclusive slice stop of `start + batch_size`. It accepts an in-memory DataFrame; it is not a disk-streaming implementation or a way to avoid loading the source into memory. Python Boolean values and third-party integer scalars are intentionally rejected by the argument policy.

## Expected results

With the five sample rows and size-two batches, row labels are `[40, 10]`, `[70, 20]`, and `[60]`. Batch lengths are `2, 2, 1`. Combining the batches reconstructs the source with original labels, values, and order. Starting at position `5` yields shape `(0, 3)`.

The controlled variation selects positions `0, 2, 4` and columns `0, 2`: learner/SQL rows are `Anu,80`, `Chitra,89`, and `Eshan,90`.

## Debug record and solution

- Position `5` and `-6` are outside a five-row table: scalar access raises `IndexError`.
- `iloc[[0, 5]]` also fails; every listed position must exist.
- `iloc[3:99]` clips to the existing final two rows; it does not fabricate rows.
- `iloc[::0]` raises `ValueError`. A step must advance forward or backward.
- Labels are not positions: row label `10` occupies position `1`.
- A slice stop is excluded: `1:4` chooses positions `1, 2, 3`.

Save the test output and explain why a changed source order can change the learner at a saved position. Copy-on-Write behavior differs across Pandas generations; the reference explicitly copies the selected numeric table before independent edits.
