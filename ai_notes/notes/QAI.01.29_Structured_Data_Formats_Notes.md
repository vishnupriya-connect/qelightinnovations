# QAI.01.29 — Structured Data Formats: CSV and JSON

> QAI.01.28 Files and text data → **QAI.01.29 CSV and JSON** → QAI.01.30 Notebook workflow

## 1. Destination: move course records between files without losing meaning

A CSV file may contain lesson records in rows. An application may need those records as JSON for another program. Reading characters from a file is only the first step: the program must recognise columns, validate required fields, convert text into the intended types, and write a **separate** output file.

In this node you will build a small `data_io.py` project that converts fictional lesson CSV into JSON, validates the result, and preserves the CSV source. CSV and JSON are file/data formats; neither decides whether a lesson is pedagogically correct.

## 2. Delimiter, CSV, header row, data row

A **delimiter** separates fields in a record. **CSV** means **comma-separated values**. One common CSV layout starts with a **header row** naming the columns, followed by **data rows**:

```csv
code,title,active
QAI.01.28,"Files, text data",true
QAI.01.29,Structured data,false
```

The first row names `code`, `title`, and `active`. The second row is one lesson. Its title contains a comma, so quotes keep `"Files, text data"` in **one** field rather than two. Real CSV also has rules for quotes and line breaks inside fields; do not parse it with `line.split(",")`. Use Python's `csv` module. [Python CSV documentation](https://docs.python.org/3.12/library/csv.html).

`csv.DictReader` uses the header row as dictionary keys:

```python
import csv
from io import StringIO

sample = 'code,title,active\nQAI.01.28,"Files, text data",true\n'
reader = csv.DictReader(StringIO(sample))
print(reader.fieldnames)                  # ['code', 'title', 'active']
print(next(reader))                       # {'code': 'QAI.01.28', 'title': 'Files, text data', 'active': 'true'}
```

**Important:** the CSV `active` value is the **string** `"true"`, not Python's Boolean `True`. A column name does not enforce type. Define and check the conversion rule explicitly. An extra or missing column also needs a deliberate policy; the lab requires exactly three known headers.

## 3. JSON values and Python values

**JSON** is a text format for representing data. The main value forms needed here:

| JSON concept | JSON example | Python value after parsing |
|---|---|---|
| **JSON object** | `{"code": "QAI.01.29"}` | dictionary |
| **JSON array** | `["AI", "ML"]` | list |
| **JSON string** | `"GenAI"` | string (`str`) |
| **JSON number** | `0.75` | number (often `float`; integral numbers commonly `int`) |
| **JSON Boolean** | `true` / `false` | `True` / `False` |
| **JSON null** | `null` | `None` |

JSON Boolean words are lowercase; Python Boolean literals are capitalised. JSON uses double quotes for strings and object keys. This is JSON text, **not** Python source code:

```json
{"lessons": [{"code": "QAI.01.29", "active": true, "score": 0.75, "note": null}]}
```

JSON does not automatically verify that each object has the fields your application needs. For external JSON, validate the resulting Python structure after parsing. [Python JSON documentation](https://docs.python.org/3.12/library/json.html).

## 4. Deserialisation and serialisation

**Deserialisation** converts text/bytes in an interchange format into usable program values. **Serialisation** converts program values into a format to store or transmit. Python's `json` module provides both:

```python
import json

text = '{"score": 0.75, "approved": true, "note": null}'
record = json.loads(text)                # parse JSON string → Python dict
print(record)                           # {'score': 0.75, 'approved': True, 'note': None}
encoded = json.dumps(record, ensure_ascii=False)  # Python dict → JSON text
print(encoded)                          # {"score": 0.75, "approved": true, "note": null}
```

`json.loads` means load from a **string**; `json.dumps` means dump to a **string**. For a file handle, `json.load(handle)` parses JSON from the file and `json.dump(value, handle)` writes JSON to it. **Parse JSON** means interpret JSON according to its syntax; `json.JSONDecodeError` signals invalid JSON syntax. **Write JSON** means serialise supported Python values to a file; unsupported values need an explicit conversion policy.

Do not assume a parsed JSON object is valid course data just because its syntax is valid. `{"lessons": "not a list"}` is valid JSON syntax but violates the lab's required data shape.

## 5. UTF-8 and the difference between CSV text and typed JSON

Our input CSV stores three text columns. For `active`, the accepted source spellings are **exactly** `true` and `false`. Convert them to Python `True` and `False` so JSON output contains actual JSON Booleans.

```python
csv_value = "false"
if csv_value not in {"true", "false"}:
    raise ValueError("active field must be true or false")
active = csv_value == "true"
print(active)                          # False
print(type(active).__name__)           # bool
```

`bool("false")` would be `True` because it is a **nonempty string**. That is a common silent bug. Write input and output as UTF-8 so titles such as `తెలుగు` remain meaningful. When opening CSV files in Python, use `newline=""` so the `csv` module handles CSV newlines correctly; use `encoding="utf-8"` for text files. [Python CSV documentation](https://docs.python.org/3.12/library/csv.html).

## 6. Guided lab: build a fictional CSV source

Create `qai-path-lab/structured-lab/`. Save this as `make_sample.py`. It uses `csv.writer` to **write CSV** correctly, including a title containing a comma, and refuses to overwrite an existing source:

```python
# make_sample.py
import csv
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / "data" / "lessons.csv"
source.parent.mkdir(parents=True, exist_ok=True)
with open(source, "x", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["code", "title", "active"])
    writer.writerow(["QAI.01.28", "Files, text data", "true"])
    writer.writerow(["QAI.01.29", "Structured data", "false"])
    writer.writerow(["QAI.01.29-TE", "తెలుగు", "true"])
print("Created fictional CSV:", source.name)
```

Run `py .\make_sample.py` in Windows PowerShell or `python3 make_sample.py` in Bash/Zsh from `structured-lab`. **Expected:** `Created fictional CSV: lessons.csv`. The file's exact quote placement/newline bytes are handled by the CSV writer; inspect parsed rows rather than assuming a hand-typed byte representation.

## 7. Guided lab: `data_io.py` with shape checks

Save this next to `make_sample.py`. It reads from one file, validates rows, exclusively creates **another** file, parses that output, and confirms its shape. It does not overwrite the CSV.

```python
# data_io.py
import csv
import json
from pathlib import Path

FIELDS = ["code", "title", "active"]


def read_lessons_csv(source):
    """Return validated lesson records from an expected UTF-8 CSV schema."""
    records = []
    seen_codes = set()
    with open(source, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV headers must be code,title,active")
        for row in reader:
            if set(row) != set(FIELDS) or any(row[field] is None for field in FIELDS):
                raise ValueError("CSV row has missing or extra fields")
            code = row["code"].strip()
            title = row["title"].strip()
            active_text = row["active"].strip()
            if code == "" or title == "":
                raise ValueError("CSV code and title must be nonblank")
            if code in seen_codes:
                raise ValueError("CSV code must be unique")
            if active_text not in {"true", "false"}:
                raise ValueError("CSV active field must be true or false")
            seen_codes.add(code)
            records.append({
                "code": code,
                "title": title,
                "active": active_text == "true",
            })
    return records


def validate_json_lessons(data):
    """Require an object with a lessons array of typed lesson records."""
    if not isinstance(data, dict) or set(data) != {"lessons"}:
        raise ValueError("JSON root must have exactly a lessons field")
    if not isinstance(data["lessons"], list):
        raise ValueError("JSON lessons must be an array")
    for record in data["lessons"]:
        if not isinstance(record, dict) or set(record) != set(FIELDS):
            raise ValueError("JSON lesson fields are invalid")
        if not isinstance(record["code"], str) or record["code"].strip() == "":
            raise ValueError("JSON code must be nonblank text")
        if not isinstance(record["title"], str) or record["title"].strip() == "":
            raise ValueError("JSON title must be nonblank text")
        if type(record["active"]) is not bool:
            raise ValueError("JSON active must be a Boolean")
    return data


def convert_csv_to_json(source, destination):
    """Read validated CSV, exclusively create JSON output, and return data."""
    records = read_lessons_csv(source)
    data = validate_json_lessons({"lessons": records})
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "x", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    return data


def read_lessons_json(source):
    """Parse UTF-8 JSON and validate this project's expected data shape."""
    with open(source, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return validate_json_lessons(data)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    source = root / "data" / "lessons.csv"
    destination = root / "output" / "lessons.json"
    source_before = source.read_bytes()
    data = convert_csv_to_json(source, destination)
    loaded = read_lessons_json(destination)
    print("CSV -> JSON records:", len(data["lessons"]))
    print("First title:", loaded["lessons"][0]["title"])
    print("Telugu title:", loaded["lessons"][2]["title"])
    print("JSON parsed records:", len(loaded["lessons"]))
    print("Source bytes unchanged:", source.read_bytes() == source_before)
```

**Run:** `py .\data_io.py` on Windows or `python3 data_io.py` in Bash/Zsh.

**Expected output:**

```text
CSV -> JSON records: 3
First title: Files, text data
Telugu title: తెలుగు
JSON parsed records: 3
Source bytes unchanged: True
```

**Data flow:** CSV bytes → UTF-8 text → `csv.DictReader` dictionaries containing **strings** → explicit Boolean conversion and schema checks → Python `{"lessons": [...]}` → `json.dump` in a **different** file → `json.load` → validated Python values.

The output will show `"active": true` or `"active": false` as JSON values, **without quotes**, and Telugu text remains readable because `ensure_ascii=False`. Running the converter again fails with `FileExistsError` rather than overwriting the previously generated output. A crash or disk error during a write may still leave an incomplete new file; later production pipelines use deliberate temporary-file and replacement policies.

## 8. Validate normal, malformed, and dangerous-to-assume shapes

Save `test_structured_data_io.py` beside `data_io.py`. The tests use disposable files:

```python
# test_structured_data_io.py
import csv
import json
import tempfile
import unittest
from pathlib import Path
from data_io import convert_csv_to_json, read_lessons_json


class StructuredDataTests(unittest.TestCase):
    def make_csv(self, folder, headers, rows):
        source = Path(folder) / "lessons.csv"
        with open(source, "x", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)
        return source

    def test_quoted_comma_unicode_boolean_and_source_preservation(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(
                folder, ["code", "title", "active"],
                [["1", "Files, text", "true"], ["2", "తెలుగు", "false"]],
            )
            original = source.read_bytes()
            destination = Path(folder) / "out" / "lessons.json"
            convert_csv_to_json(source, destination)
            data = read_lessons_json(destination)
            self.assertEqual(data["lessons"][0]["title"], "Files, text")
            self.assertIs(data["lessons"][0]["active"], True)
            self.assertIs(data["lessons"][1]["active"], False)
            self.assertEqual(data["lessons"][1]["title"], "తెలుగు")
            self.assertEqual(source.read_bytes(), original)

    def test_missing_header_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(folder, ["code", "title"], [["1", "AI"]])
            destination = Path(folder) / "out.json"
            with self.assertRaisesRegex(ValueError, "headers"):
                convert_csv_to_json(source, destination)
            self.assertFalse(destination.exists())

    def test_missing_row_field_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(
                folder, ["code", "title", "active"], [["1", "AI"]],
            )
            with self.assertRaisesRegex(ValueError, "missing or extra"):
                convert_csv_to_json(source, Path(folder) / "out.json")

    def test_invalid_boolean_text_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(
                folder, ["code", "title", "active"], [["1", "AI", "yes"]],
            )
            with self.assertRaisesRegex(ValueError, "true or false"):
                convert_csv_to_json(source, Path(folder) / "out.json")

    def test_duplicate_codes_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(
                folder, ["code", "title", "active"],
                [["1", "AI", "true"], ["1", "ML", "false"]],
            )
            with self.assertRaisesRegex(ValueError, "unique"):
                convert_csv_to_json(source, Path(folder) / "out.json")

    def test_existing_output_remains_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_csv(
                folder, ["code", "title", "active"], [["1", "AI", "true"]],
            )
            destination = Path(folder) / "out.json"
            destination.write_text("KEEP", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                convert_csv_to_json(source, destination)
            self.assertEqual(destination.read_text(encoding="utf-8"), "KEEP")

    def test_json_syntax_and_shape_fail_separately(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            path.write_text("{broken", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                read_lessons_json(path)
            path.write_text('{"lessons": "wrong type"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "array"):
                read_lessons_json(path)


if __name__ == "__main__":
    unittest.main()
```

Run `py -m unittest -v test_structured_data_io` in PowerShell or `python3 -m unittest -v test_structured_data_io` in Bash/Zsh from `structured-lab`. **Expected:** 7 tests, OK. The last test distinguishes *syntax failure* from *valid JSON of the wrong shape*. A JSON number such as `1` is an `int` after parsing, but a value stored in CSV remains text unless converted.

## 9. Typical mistakes and checks

| Observation | Cause | Check and repair |
|---|---|---|
| comma inside title splits a record | hand-written `split(",")` ignored CSV quoting | use `csv.reader` / `DictReader` |
| extra blank lines appear in CSV output | platform newline handling not delegated to `csv` | open CSV with `newline=""` |
| `"false"` is treated as true | `bool("false")` tests nonempty text | compare accepted spellings explicitly |
| `KeyError` for expected column | header absent or misspelled | validate `reader.fieldnames` before reading rows |
| `None` appears for a CSV column | short row had fewer fields | check every required field before conversion |
| `json.load` raises `JSONDecodeError` | malformed JSON syntax | report file/category, not private payload |
| JSON loads but `lessons` is a string | schema not checked | validate top-level object and array type |
| `json.dumps` cannot handle a custom object | not natively serialisable | convert to explicitly supported data shape |
| output already exists | exclusive `"x"` refused overwrite | inspect existing file before choosing a new destination |
| non-English title becomes unreadable | encoding or output settings mismatch | use UTF-8 and review the receiving application |
| CSV looks valid but values have wrong meaning | all fields initially parse as text | define numeric/Boolean/required-field rules |

**Debug order:** inspect header names → parsed row shape → string-to-type conversions → proposed Python data shape → destination path → JSON round-trip. Report controlled error categories and a fictional minimal example rather than share sensitive dataset rows.

## 10. Independent micro-lab with full solution

**Task:** a short CSV contains `name,completed` records. Convert it to a JSON object with a `"learners"` array. Treat `completed` as true only when CSV text is exactly `"true"`, false only when exactly `"false"`, and reject other values. Preserve the CSV; write UTF-8 JSON to a **new** path; print the parsed JSON result.

**Complete standalone solution** in a temporary folder:

```python
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    source = Path(folder) / "learners.csv"
    destination = Path(folder) / "learners.json"
    with open(source, "x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name", "completed"])
        writer.writerow(["Anu", "true"])
        writer.writerow(["Ravi", "false"])
    original = source.read_bytes()

    learners = []
    with open(source, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["name", "completed"]:
            raise ValueError("CSV headers are invalid")
        for row in reader:
            if set(row) != {"name", "completed"} or any(v is None for v in row.values()):
                raise ValueError("CSV row is incomplete")
            if row["completed"] not in {"true", "false"}:
                raise ValueError("completed must be true or false")
            learners.append({
                "name": row["name"],
                "completed": row["completed"] == "true",
            })

    with open(destination, "x", encoding="utf-8", newline="\n") as handle:
        json.dump({"learners": learners}, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with open(destination, "r", encoding="utf-8") as handle:
        observed = json.load(handle)
    print(observed)
    print("Source preserved:", source.read_bytes() == original)
```

**Expected output:**

```text
{'learners': [{'name': 'Anu', 'completed': True}, {'name': 'Ravi', 'completed': False}]}
Source preserved: True
```

**Reasoning:** CSV fields enter as strings, then the accepted text is converted into Boolean values. `json.dump` writes those values as JSON `true` and `false`. `json.load` reads them back as Python `True` and `False`. The CSV bytes are unchanged and the output path is separate.

## 11. What to remember and retain

- A delimiter separates fields; CSV headers name columns; quoted fields can contain commas.
- CSV reader values are text until you validate and convert them.
- JSON object → dictionary, array → list, string → `str`, number → numeric value, Boolean → `bool`, null → `None`.
- `json.load`/`json.loads` deserialise; `json.dump`/`json.dumps` serialise.
- Valid syntax does not imply valid application shape; check required keys and value types.
- Read UTF-8 with `with`; for CSV use `newline=""`; write to a separate destination and preserve source bytes.
- Retain `make_sample.py`, `data_io.py`, `test_structured_data_io.py`, input/output sample files, seven-test result, and a short note comparing malformed JSON with wrong-shape JSON.

**Next:** QAI.01.30 uses notebooks for exploration while keeping data transformation reproducible when rerun in order.

---

**Node contract (S90):** `C | L3 | H1–H3 | E3–E5 | A2–A4 | P0–P1`. All sixteen S86 structured-data items are covered through file conversion, explicit schema checks, round-trip JSON, seven tests, and a solved standalone task. Learner evidence requires running the project and examining both source and derived data.

## Reference documentation

- [Python `csv` module: reader and writer](https://docs.python.org/3.12/library/csv.html).
- [Python `json` module: encoder and decoder](https://docs.python.org/3.12/library/json.html).
