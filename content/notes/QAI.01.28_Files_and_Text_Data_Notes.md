# QAI.01.28 — Files and Text Data

> QAI.01.27 Python environments → **QAI.01.28 Files and text data** → QAI.01.29 Structured data formats

## 1. Destination: read a source without destroying it

An AI project may receive lesson text from a file and generate a cleaned text file. The source is evidence: it should remain available after processing. Your job in this node is to open a UTF-8 text file, read its lines, write cleaned output to a **different** file, inspect the result, and recognise missing-input and already-existing-output errors.

You will create `make_sample.py`, `data_io.py`, and `test_data_io.py`. This is a small local text-file lab, not an NLP tokenizer: removing whitespace can change meaning when exact layout matters. CSV and JSON follow in QAI.01.29.

## 2. Text file, encoding, UTF-8, and binary mode

A **text file** stores bytes representing characters. A **character encoding** describes how text characters become bytes and are decoded again. **UTF-8** is an encoding that can represent English, Telugu, and many other scripts. Write `encoding="utf-8"` explicitly for project text so a different machine's default encoding does not silently change interpretation. [Python documentation: file input and output](https://docs.python.org/3.12/tutorial/inputoutput.html).

**Binary mode** reads or writes bytes (`bytes`), without text decoding. Compare:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "sample.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("AI and తెలుగు")
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    with open(path, "rb") as handle:
        data = handle.read()
    print(text)                       # AI and తెలుగు
    print(type(text).__name__)         # str
    print(type(data).__name__)         # bytes
    print(data.decode("utf-8") == text)  # True
```

The byte sequence is **not** interchangeable with human-readable text without a deliberate decode step. If bytes are not valid in the chosen UTF-8 encoding, reading them as UTF-8 can raise `UnicodeDecodeError`. Do not silently replace undecodable bytes and assume the source was interpreted correctly. Later data pipelines decide how to diagnose and quarantine such inputs.

## 3. Open file → file handle → close file

`open(path, mode, encoding=...)` opens a file and returns a **file handle**: an object through which Python reads or writes that file. `close()` closes it and releases its resources. Python's `with` syntax makes closing automatic when execution leaves the block:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "one.txt"
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("GenAI\n")
        print("Inside, closed:", handle.closed)  # False
    print("After with, closed:", handle.closed)   # True
```

A **context manager** is an object used by `with` to manage entry and cleanup around a block. A file handle is a context manager. `with open(...) as handle:` binds the handle only for the work you want to perform and closes it on leaving the block, including when an exception occurs. If you open manually without `with`, you must close explicitly; prefer `with` for this project. Attempting I/O on the closed handle raises `ValueError`.

## 4. File mode: choose the intended operation

A **file mode** tells `open` what operation is intended. The commonly needed modes are:

| Mode | Name | What happens if file already exists? | If missing? |
|---|---|---|---|
| `"r"` | **read mode** | read existing text | `FileNotFoundError` |
| `"w"` | **write mode** | **truncate and overwrite** | create file |
| `"a"` | **append mode** | write at end | create file |
| `"x"` | exclusive creation | `FileExistsError`; preserves existing file | create file |
| `"rb"` / `"wb"` | **binary mode** | read bytes / overwrite bytes, respectively | `rb` fails; `wb` creates |

`"w"` can destroy previous contents as soon as it opens the file; `"x"` is a helpful choice when accidental overwrite is unacceptable. File creation still requires an existing parent directory. `encoding` applies to **text** modes; binary mode handles bytes and does not take text encoding for the file operation. [Python `open` documentation](https://docs.python.org/3.12/library/functions.html#open).

**Controlled demonstration in a temporary folder, never with a real source file:**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "mode_demo.txt"
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("First\n")
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("Second\n")
    print(repr(path.read_text(encoding="utf-8")))  # 'First\nSecond\n'
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("Replaced\n")
    print(repr(path.read_text(encoding="utf-8")))  # 'Replaced\n'
```

The second `"w"` **replaces** the earlier two lines. You cannot recover their content from this file merely by reading it again. Write output to a new path and preserve your source.

## 5. Read a file, read one line, iterate lines

**Read file:** `handle.read()` returns all remaining text as one string. **Read line:** `handle.readline()` returns the next line (often including its ending newline). File iteration visits successive lines without first requesting one huge string:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "questions.txt"
    path.write_text("AI\nML\n", encoding="utf-8")
    with open(path, "r", encoding="utf-8") as handle:
        first = handle.readline()
        second = handle.readline()
        end = handle.readline()
    print(repr(first))         # 'AI\n'
    print(repr(second))        # 'ML\n'
    print(repr(end))           # '': end of file

    with open(path, "r", encoding="utf-8") as handle:
        print([line.strip() for line in handle])  # ['AI', 'ML']
    with open(path, "r", encoding="utf-8") as handle:
        print(repr(handle.read()))   # 'AI\nML\n'
```

After `readline()`, the handle is at a later position. Do not expect `read()` on the **same** handle to start over without deliberately repositioning it; this demonstration opens a fresh handle for each reading pattern. Reading everything at once may not fit a large file in memory; iterate lines when that suits the data.

## 6. Write file and preserve intended line endings

**Write file:** `handle.write(text)` writes a string to a text-mode file and returns the number of characters written. It does **not** automatically add a newline:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "output.txt"
    with open(path, "x", encoding="utf-8", newline="\n") as handle:
        count = handle.write("AI\nGenAI\n")
    print(count)                         # 9 Python string positions
    print(repr(path.read_text(encoding="utf-8")))  # 'AI\nGenAI\n'
```

`newline="\n"` requests a consistent LF line separator for this lab. The number returned by `write` counts text positions written, **not bytes on disk**, so Unicode text may use a different number of encoded bytes. For this simple example, `"AI\nGenAI\n"` has 9 string positions.

## 7. File-not-found error and missing parent directory

A **file-not-found error** (`FileNotFoundError`) is an expected failure when `"r"` tries to open a path that does not exist:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    missing = Path(folder) / "not_here.txt"
    try:
        with open(missing, "r", encoding="utf-8") as handle:
            handle.read()
    except FileNotFoundError:
        print("Source text file is missing.")
```

```text
Source text file is missing.
```

Decide whether missing input is recoverable; do **not** create an empty source and quietly produce an empty output when a required dataset is absent. If the **parent directory** for a new output file is missing, opening it for write may also raise `FileNotFoundError`. Create the intended output directory explicitly; do not change paths until an import happens to work.

## 8. Guided P1 lab: prepare a fictional UTF-8 source

Create `qai-path-lab/data-lab/`. Put the following script in `make_sample.py`. It creates a small *fictional* sample once and refuses to overwrite it:

```python
# make_sample.py
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / "data" / "lessons.txt"
source.parent.mkdir(parents=True, exist_ok=True)
with open(source, "x", encoding="utf-8", newline="\n") as handle:
    handle.write("  AI  \n\n  GenAI  \n  తెలుగు  \n")
print("Created fictional sample:", source.name)
```

Run `py .\make_sample.py` on Windows or `python3 make_sample.py` in Bash/Zsh from `data-lab`. **Expected:** `Created fictional sample: lessons.txt`. If `data/lessons.txt` already exists, `"x"` raises `FileExistsError`; keep the existing file, inspect it, and remove or rename only the sample you deliberately created if you really want a new run. Do not run this on a real source file.

`Path(__file__).resolve().parent` means “the folder containing this script,” so it works even if the shell's current folder differs. `mkdir(..., exist_ok=True)` ensures the intended `data/` directory exists; it does not overwrite the text file.

## 9. Guided P1 lab: `data_io.py`

Save this alongside `make_sample.py`:

```python
# data_io.py
from pathlib import Path


def cleaned_labels(lines):
    """Return nonblank, edge-trimmed labels from text lines."""
    result = []
    for raw_line in lines:
        label = raw_line.strip()
        if label != "":
            result.append(label)
    return result


def copy_cleaned_labels(source, destination):
    """Read UTF-8 source; exclusively create separate UTF-8 output.

    Return number of resulting labels. Do not edit or overwrite the source.
    Raise FileNotFoundError, UnicodeDecodeError, or FileExistsError as relevant.
    """
    with open(source, "r", encoding="utf-8") as handle:
        labels = cleaned_labels(handle)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "x", encoding="utf-8", newline="\n") as handle:
        if labels:
            handle.write("\n".join(labels) + "\n")
    return len(labels)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    source = root / "data" / "lessons.txt"
    destination = root / "output" / "lesson_labels.txt"
    count = copy_cleaned_labels(source, destination)
    print("Cleaned labels:", count)
    with open(destination, "r", encoding="utf-8") as handle:
        print("Output:", repr(handle.read()))
    with open(source, "rb") as handle:
        print("Original bytes retained:", len(handle.read()) > 0)
```

Run `py .\data_io.py` on Windows or `python3 data_io.py` in Bash/Zsh. **Expected** with the fictional sample:

```text
Cleaned labels: 3
Output: 'AI\nGenAI\nతెలుగు\n'
Original bytes retained: True
```

**Trace:** the input has four lines including a blank one → `cleaned_labels` keeps three labels → `destination` is a **different** path → `"x"` creates it only if absent → the program reads output and confirms the source still contains bytes. Checking source bytes are present is weaker than checking every byte unchanged; the test below checks exact equality for its sample.

**Controlled rerun:** run `data_io.py` again without changing anything. It raises `FileExistsError` when opening the existing output with `"x"`; **the earlier output is not overwritten**. Inspect the result before deciding whether a rerun should produce a new named output or replace an explicitly approved disposable output. Reproducible pipelines later design an explicit overwrite or versioning policy.

**Exact-text limitation:** `strip()` removes leading/trailing whitespace. That is appropriate for this toy **label** file, not automatically for code, poems, quotations, indentation-sensitive material, or transcripts where line spacing matters.

## 10. Test file: normal, missing, existing, Unicode

Put `test_data_io.py` beside `data_io.py`. The tests make temporary files; they never touch the main sample:

```python
# test_data_io.py
import tempfile
import unittest
from pathlib import Path
from data_io import copy_cleaned_labels


class DataIoTests(unittest.TestCase):
    def test_source_preserved_and_utf8_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.txt"
            destination = Path(folder) / "out" / "labels.txt"
            original = "  AI  \n\n  తెలుగు  \n".encode("utf-8")
            source.write_bytes(original)
            self.assertEqual(copy_cleaned_labels(source, destination), 2)
            self.assertEqual(destination.read_text(encoding="utf-8"),
                             "AI\nతెలుగు\n")
            self.assertEqual(source.read_bytes(), original)

    def test_missing_input_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "missing.txt"
            destination = Path(folder) / "out.txt"
            with self.assertRaises(FileNotFoundError):
                copy_cleaned_labels(source, destination)
            self.assertFalse(destination.exists())

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.txt"
            destination = Path(folder) / "out.txt"
            source.write_text("AI\n", encoding="utf-8")
            destination.write_text("KEEP\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                copy_cleaned_labels(source, destination)
            self.assertEqual(destination.read_text(encoding="utf-8"), "KEEP\n")

    def test_invalid_utf8_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.txt"
            destination = Path(folder) / "out.txt"
            source.write_bytes(b"\xff")  # deliberately invalid UTF-8 sample
            with self.assertRaises(UnicodeDecodeError):
                copy_cleaned_labels(source, destination)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
```

Run `py -m unittest -v test_data_io` on Windows or `python3 -m unittest -v test_data_io` in Bash/Zsh from `data-lab`. **Expected:** 4 tests, OK. The test of existing output is an actual preservation test, not just a check that an exception was raised.

## 11. Diagnose text-file mistakes

| Observation | Likely cause | Concrete repair |
|---|---|---|
| `FileNotFoundError` on input | wrong relative path or source absent | print/inspect intended path; verify file exists before processing |
| `FileNotFoundError` while creating output | parent directory missing | create only the intended parent directory |
| `FileExistsError` on output | `"x"` refused overwrite | inspect existing output; choose new filename or explicit approved replacement |
| original contents vanished | source opened with `"w"` | stop, recover from backup if available, and separate input/output paths |
| unreadable characters or `UnicodeDecodeError` | encoding mismatch or invalid bytes | verify source encoding; read with the correct declared encoding |
| `write` count differs from file's byte size | characters were mistaken for encoded bytes | distinguish text character count from UTF-8 bytes |
| second `read()` returns empty | handle already advanced to end | reopen or deliberately reposition for a new read |
| file remains open after a failure | manual `open` had no dependable cleanup | use `with` to manage the file handle |
| blank lines disappear unexpectedly | `strip` and nonblank filter intentionally changed data | decide whether layout is part of the source's meaning |

**Debug sequence:** record the exact input and output paths, mode, encoding, expected line count/content, actual result, and first exception. Use fictional text for shared examples. Do not print a private student transcript or file contents merely to diagnose a path or encoding problem.

## 12. Independent micro-lab with complete solution

**Task:** create `append_audit(audit_path, label)`, which appends `"<label>\n"` in UTF-8 to a **disposable** audit file. It must preserve existing lines. Use `with` and test two calls: `"AI"`, then `"ML"`. Explain why you would not use `"w"` for the second call and why a real audit log needs stronger reliability controls than this toy file.

**Complete standalone solution** (safe in a temporary folder):

```python
from pathlib import Path
from tempfile import TemporaryDirectory


def append_audit(audit_path, label):
    """Append one supplied label as a UTF-8 line to a disposable file."""
    with open(audit_path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(label + "\n")


with TemporaryDirectory() as folder:
    audit = Path(folder) / "audit.txt"
    append_audit(audit, "AI")
    append_audit(audit, "ML")
    observed = audit.read_text(encoding="utf-8")
    print(repr(observed))
    assert observed == "AI\nML\n"
    print("Append check passed")
```

**Expected output:**

```text
'AI\nML\n'
Append check passed
```

`"a"` preserves and extends the existing text. A second `"w"` would truncate the earlier `AI` line. This toy does not address concurrent writers, crashes, access control, logging format, or tamper evidence; it is **not** a production audit trail.

## 13. What to remember and retain

- A file handle connects the program to an opened file; `with` closes it reliably on leaving the block.
- `"r"` reads; `"w"` overwrites; `"a"` appends; `"x"` creates only if absent; `"rb"`/`"wb"` handle bytes.
- `read()` reads remaining text; `readline()` takes the next line; file iteration visits lines.
- Write text with an explicit UTF-8 encoding when that is the source contract; choose how line endings are handled.
- A missing required input should be reported; never manufacture an empty source silently.
- Keep `make_sample.py`, `data_io.py`, `test_data_io.py`, the exact sample/derived files, a four-test success report, and the controlled rerun failure. The source/output preservation rule carries into CSV and JSON next.

**Next:** QAI.01.29 uses the same safe file practices with structured CSV and JSON and validates the expected fields.

---

**Node contract (S90):** `C | L3 | H1–H3 | E3–E5 | A2–A4 | P0–P1`. All seventeen S86 text-file items are covered through worked modes, a UTF-8 mini-project, normal/missing/overwrite/encoding tests, and a solved append exercise. Learner evidence requires running the scripts and recording the observed source and output files.

## Reference documentation

- [Python `open`: modes, encodings, and newline handling](https://docs.python.org/3.12/library/functions.html#open).
- [Python tutorial: reading and writing files](https://docs.python.org/3.12/tutorial/inputoutput.html#reading-and-writing-files).
