# Array input and output

## Save an array, then load it back

An **array file** stores array data outside a running Python program. To **save an array** is to write it to a file; to **load an array** is to read it into a new program or later run. These steps are called **array serialisation** and **array deserialisation**: turn an in-memory array into stored bytes, then reconstruct it.

```python
from pathlib import Path
import numpy as np

scores = np.array([[10, 20, 30], [40, 50, 60]], dtype=np.int32)
folder = Path("array_io_output")
folder.mkdir(exist_ok=True)
path = folder / "scores.npy"
np.save(path, scores)
loaded = np.load(path, allow_pickle=False)
print(loaded.shape, loaded.dtype)   # (2, 3) int32
print(loaded.tolist())             # [[10, 20, 30], [40, 50, 60]]
print(np.array_equal(scores, loaded)) # True
```

A **binary array file** such as `.npy` stores one NumPy array with its shape and data type. `np.save()` writes it, and `np.load()` reads it. Binary bytes are not meant to be read as ordinary text. For these numeric arrays, `allow_pickle=False` keeps loading limited to non-object data. The original array and the newly loaded array contain the same values but are separate objects.

## Save several arrays under names

`np.savez()` places several arrays in one `.npz` archive. Give each one a clear name:

```python
task_ids = np.array([101, 102, 103], dtype=np.int32)
bundle_path = folder / "study_bundle.npz"
np.savez(bundle_path, scores=scores, task_ids=task_ids)
with np.load(bundle_path, allow_pickle=False) as bundle:
    print(sorted(bundle.files))             # ['scores', 'task_ids']
    restored_scores = bundle["scores"].copy()
    restored_ids = bundle["task_ids"].copy()
print(restored_scores.shape, restored_ids.tolist())
# (2, 3) [101, 102, 103]
```

The keyword names `scores` and `task_ids` are keys inside the archive, not separate file paths. The `with` block closes the loaded archive when finished; the explicit copies remain available afterward. `.npz` is useful when related arrays should travel together. `np.save()` and `np.savez()` create NumPy binary formats; use a text format if a person or another simple tool needs to read the numbers directly.

## Write and read comma-delimited text

A **text array file** stores printable numbers. Here each row is one line and a **comma delimiter** separates values within a row:

```python
csv_path = folder / "scores.csv"
np.savetxt(csv_path, scores, fmt="%d", delimiter=",")
print(csv_path.read_text().strip())
# 10,20,30
# 40,50,60
text_loaded = np.loadtxt(csv_path, delimiter=",", dtype=np.int32)
print(text_loaded.shape, text_loaded.dtype) # (2, 3) int32
print(np.array_equal(scores, text_loaded)) # True
```

`np.savetxt()` writes a plain numeric table. `fmt="%d"` writes these integer values without decimals; `delimiter=","` writes commas. `np.loadtxt()` needs the same delimiter. Its default dtype is floating-point, so `dtype=np.int32` explicitly reconstructs the integer type here. For fractional values, choose an appropriate floating-point format and verify the precision you need. Plain text does not carry the same automatic shape and dtype metadata as `.npy`; a single-row text file may load as a one-dimensional array unless you request a minimum dimension.

| Format | Write | Read | What to remember |
| --- | --- | --- | --- |
| One binary array, `.npy` | `np.save()` | `np.load()` | Keeps NumPy shape and dtype |
| Named binary arrays, `.npz` | `np.savez()` | `np.load()` and named keys | Close archive after reading |
| Numeric text table, `.csv` here | `np.savetxt()` | `np.loadtxt()` | Match delimiter and choose dtype/format |

## Check a round trip rather than assuming it

After a file is written, check the loaded array's shape, dtype, and values. `np.array_equal(original, loaded)` tests exact numeric equality for this integer example. For floating-point text with limited printed digits, use a suitable tolerance such as `np.allclose()` when exact binary equality is not expected. Preserve the original file when debugging a load error.

If `np.loadtxt(csv_path)` is used without the comma delimiter, it may raise `ValueError` when it sees a line such as `10,20,30` as one token. The fix is to supply `delimiter=","`; do not edit the data merely to hide the parsing problem. A misspelled path can raise `FileNotFoundError`. Check the directory and name before retrying. Do not enable pickle loading for an ordinary numeric file to work around a format mismatch.

## Guided lab

Download [Array input and output lab](QAI.02.02.31_Array_Input_and_Output_Lab.zip), extract it, and run inside the folder:

```bash
python -m pip install -r requirements.txt
python array_input_and_output.py
python check_array_input_and_output.py
```

The guided program uses a temporary directory for its file round trips and prints their shape, dtype, and equality checks. The checker validates the file content and all three load paths; it reports `All checks passed.`

**Trace before running:** predict that the `.npy` file reconstructs `(2, 3)` and `int32`, the `.npz` archive contains two named arrays, and the CSV text contains two lines of three comma-separated integers.

**Controlled variation:** copy `scores`, change `[1, 2]` from 60 to 99, and save it to a new `.npy` path. Load that new path and check 99 at `[1, 2]`; the first file and original `scores` still contain 60. A new path makes it easy to compare two saved versions.

**Debug:** If a text round trip loads as floats, specify `dtype` when appropriate. If a comma file fails to parse, pass `delimiter=","`. If a `.npz` load gives a container rather than a plain array, choose a named key such as `bundle["scores"]`.

## Independent mini-project: persist a study table

Create `minutes = np.array([[12, 15], [20, 25]], dtype=np.int32)` and `learners = np.array([101, 102], dtype=np.int32)`. In a folder named `study_output`, save the table to `minutes.npy`, both arrays as named entries in `study.npz`, and the table as `minutes.csv` with comma-separated integer text. Load each back and print shapes, dtypes, and equality checks. The lab contains `mini_project_reference.py`; it writes real files in `study_output` so you can inspect them.

Expected output:

```text
npy (2, 2) int32 True
npz keys ['learners', 'minutes']
npz arrays True True
csv (2, 2) int32 True
csv text 12,15 / 20,25
```

Full reference solution:

```python
from pathlib import Path
import numpy as np

minutes = np.array([[12, 15], [20, 25]], dtype=np.int32)
learners = np.array([101, 102], dtype=np.int32)
folder = Path("study_output")
folder.mkdir(exist_ok=True)
npy_path = folder / "minutes.npy"
npz_path = folder / "study.npz"
csv_path = folder / "minutes.csv"
np.save(npy_path, minutes)
np.savez(npz_path, minutes=minutes, learners=learners)
np.savetxt(csv_path, minutes, fmt="%d", delimiter=",")
from_npy = np.load(npy_path, allow_pickle=False)
with np.load(npz_path, allow_pickle=False) as bundle:
    keys = sorted(bundle.files)
    table_ok = np.array_equal(bundle["minutes"], minutes)
    learners_ok = np.array_equal(bundle["learners"], learners)
from_csv = np.loadtxt(csv_path, delimiter=",", dtype=np.int32)
print("npy", from_npy.shape, from_npy.dtype,
      np.array_equal(from_npy, minutes))
print("npz keys", keys)
print("npz arrays", table_ok, learners_ok)
print("csv", from_csv.shape, from_csv.dtype,
      np.array_equal(from_csv, minutes))
print("csv text", " / ".join(csv_path.read_text().strip().splitlines()))
```

## Check your understanding

1. **Which format automatically preserves NumPy shape and dtype for one array?** `.npy` through `np.save()` and `np.load()`.
2. **How do you read one array from a `.npz` archive?** Open it with `np.load()`, then access its named key, for example `bundle["scores"]`.
3. **Why pass `delimiter=","` to `loadtxt()` for this CSV?** So the comma-separated values in each line are parsed as separate columns.
4. **Why specify `dtype=np.int32` when loading this text?** Text lacks the original dtype metadata; `loadtxt()` defaults to floating-point.

Remember: choose the format for the intended reader, save, load, and verify shape, dtype, and values.

## Further reading

- [NumPy: save](https://numpy.org/doc/stable/reference/generated/numpy.save.html), [load](https://numpy.org/doc/stable/reference/generated/numpy.load.html), and [savez](https://numpy.org/doc/stable/reference/generated/numpy.savez.html)
- [NumPy: savetxt](https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html) and [loadtxt](https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html)
