# QAI.01.18 — Dictionaries

> QAI.01.17 Tuples → **QAI.01.18 Dictionaries** → QAI.01.19 Sets

## 1. Destination: read a course record by field name

The previous lesson represented a lesson as `("QAI.01.18", "Dictionaries", "Beginner")`. To read the title, you had to remember that position 1 meant “title.” A **dictionary** lets you name that field: `lesson["title"]`. This matters when handling AI dataset rows, course records, application settings, and later JSON or API responses.

In this lesson you will create and update records, handle a missing field without hiding required-data errors, read views and nested fields, and build a small dictionary by comprehension. You will run `dictionary_records.py` and check its exact outputs.

## 2. Mapping, dictionary, key, value, pair

A **mapping** associates a **key** with a **value**. A Python **dictionary** (`dict`) is a mutable mapping. One association is a **key-value pair**:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionaries", "level": "Beginner"}
print(lesson["code"])         # QAI.01.18
print(lesson["title"])        # Dictionaries
print(type(lesson))           # <class 'dict'>
```

Here `"title"` is a key and `"Dictionaries"` is its value. The braces and colon form a **dictionary literal**: `{key: value, ...}`. An **empty dictionary** is `{}`; `[]` is an empty list, not a dictionary:

```python
record = {}
record["code"] = "QAI.01.18"
print(record)                 # {'code': 'QAI.01.18'}
print(len(record))            # 1 pair
```

Dictionary keys must be hashable; strings and integer values are familiar examples. A list cannot serve as a key because it is mutable and unhashable: `{["course"]: "AI"}` raises `TypeError`. Values can be strings, numbers, lists, other dictionaries, and more.

**Choose the structure by the question:** a list answers “what is at index 1?”; a dictionary answers “what is stored under key `'title'`?” A dictionary preserves insertion order in modern Python, but it is a mapping **by keys**, not a sequence indexed by numeric position. `lesson[0]` asks for a key `0`, which is absent here; it does not return the first pair.

## 3. Unique keys; values may repeat

Each key is **unique within one dictionary**. Assigning an existing key updates its value; it does not create a second pair:

```python
lesson = {"title": "Tuples", "title": "Dictionaries"}
print(lesson)                 # {'title': 'Dictionaries'}
print(len(lesson))            # 1
```

An accidentally repeated key in a literal silently keeps the last specified value; review data generation when this would lose information. Values, by contrast, can repeat:

```python
levels = {"python": "Beginner", "genai": "Beginner"}
print(len(levels))            # 2 different keys
```

`"Title"` and `"title"` are different string keys. Decide one spelling for a field and use it consistently.

## 4. Lookup: required field versus optional field

A **dictionary lookup** with square brackets requires the key. A missing key raises `KeyError`:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionaries"}
print(lesson["title"])        # Dictionaries
print("title" in lesson)       # True: membership checks KEYS
print("missing" in lesson)     # False
# print(lesson["level"])      # KeyError if uncommented
```

Use `.get(key)` when absence is an expected, acceptable possibility. It returns `None` by default; `.get(key, fallback)` returns the chosen fallback if the key is absent:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionaries"}
print(lesson.get("level"))               # None
print(lesson.get("level", "Unspecified"))  # Unspecified
print(lesson.get("title", "Unspecified"))  # Dictionaries
```

**Decision:** if `"code"` must always exist in a valid record, let a missing required key be detected and repaired at the input boundary; do not casually substitute `"Unspecified"`. If `"level"` really is optional, `.get("level", "Unspecified")` can be appropriate.

There is a subtle distinction between a **missing key** and a key whose stored value is `None`:

```python
lesson = {"level": None}
print(lesson.get("level"))     # None
print(lesson.get("missing"))   # None
print("level" in lesson)       # True
print("missing" in lesson)     # False
```

Use `key in lesson` when you need to distinguish presence from absence. `"Beginner" in lesson` asks whether it is a **key**, not whether it occurs among the values.

## 5. Update, add, remove

A **dictionary update** with `record[key] = value` changes the value for an existing key; the same syntax **adds a key-value pair** when the key is new:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionary"}
lesson["title"] = "Dictionaries"   # update existing key
lesson["level"] = "Beginner"       # add new pair
print(lesson)                     # {'code': 'QAI.01.18', 'title': 'Dictionaries', 'level': 'Beginner'}
```

`.update({...})` adds or replaces several pairs at once:

```python
lesson = {"code": "QAI.01.18", "level": "Draft"}
lesson.update({"title": "Dictionaries", "level": "Beginner"})
print(lesson)                     # {'code': 'QAI.01.18', 'level': 'Beginner', 'title': 'Dictionaries'}
```

To **remove a key-value pair**, use `del record[key]` or `record.pop(key)`. `pop` also returns the removed value:

```python
lesson = {"code": "QAI.01.18", "status": "draft"}
old_status = lesson.pop("status")
print(old_status)                 # draft
print(lesson)                     # {'code': 'QAI.01.18'}
lesson["temporary"] = "remove me"
del lesson["temporary"]
print(lesson)                     # {'code': 'QAI.01.18'}
```

`del lesson["missing"]` and `lesson.pop("missing")` raise `KeyError`. `lesson.pop("missing", "not found")` instead returns `"not found"`. Use a fallback only when absence is an expected case. These methods mutate the **same dictionary**, so aliases see the update; `lesson.copy()` creates a new *outer* dictionary but still shares nested mutable values.

## 6. Keys, values, and items: three dictionary views

A **dictionary key view** (`.keys()`) represents keys; a **dictionary value view** (`.values()`) represents values; a **dictionary item view** (`.items()`) represents (key, value) pairs:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionaries"}
print(list(lesson.keys()))    # ['code', 'title']
print(list(lesson.values()))  # ['QAI.01.18', 'Dictionaries']
print(list(lesson.items()))   # [('code', 'QAI.01.18'), ('title', 'Dictionaries')]
```

`list(...)` makes a snapshot list suitable for a clear printout. The views themselves **reflect later changes** to the dictionary:

```python
lesson = {"code": "QAI.01.18"}
keys_view = lesson.keys()
lesson["title"] = "Dictionaries"
print(list(keys_view))        # ['code', 'title']
```

Thus a view is not a detached copy. Dictionary iteration maintains the dictionary's insertion order in current Python. The order shown in these examples is the order we inserted the keys; business or learning order must still be chosen deliberately.

## 7. Iterate keys, values, or pairs

**Dictionary iteration** by default visits keys. Use `.items()` to unpack a key and its value together:

```python
lesson = {"code": "QAI.01.18", "title": "Dictionaries"}
for key in lesson:
    print("Key:", key)
for key, value in lesson.items():
    print(f"{key} = {value}")
```

```text
Key: code
Key: title
code = QAI.01.18
title = Dictionaries
```

`for value in lesson.values():` visits values only. If you need both the field name and the value, `items()` is clearer than repeatedly looking up each key. The two target names (`key, value`) unpack each item-view pair as introduced in QAI.01.17. Loops receive full treatment in QAI.01.21.

Do not add or remove keys while iterating directly over the same dictionary; Python may raise `RuntimeError`. First build a separate list of selected keys or a new dictionary when the requirement genuinely calls for structural change during traversal.

## 8. Nested dictionary: choose one level at a time

A **nested dictionary** stores another dictionary as a value. Example: one course code maps to fields for that course:

```python
catalog = {
    "QAI.01.18": {"title": "Dictionaries", "level": "Beginner"},
    "QAI.01.19": {"title": "Sets", "level": "Beginner"},
}
print(catalog["QAI.01.18"]["title"])  # Dictionaries
print(catalog["QAI.01.19"]["level"])  # Beginner
```

Read `catalog["QAI.01.18"]["title"]` in two steps: get the record for the course code, then get the `"title"` field inside that record. If either key is missing, bracket lookup raises `KeyError`. A missing outer record cannot be repaired by pretending its inner field exists; inspect each level deliberately.

**Careful copying:**

```python
original = {"lesson": {"title": "Tuples"}}
shallow = original.copy()
shallow["lesson"]["title"] = "Dictionaries"
print(original["lesson"]["title"])  # Dictionaries: same inner dictionary
```

When original nested records must remain independent, copy their inner dictionaries too, or use an appropriate deep-copy operation after deciding which nested objects should be shared.

## 9. Dictionary comprehension: build a mapping from a list

A **dictionary comprehension** creates a new dictionary: `{key_expression: value_expression for item in source}`. You already met list comprehensions in QAI.01.16. Here the key expression is a title, and the value expression counts its characters:

```python
titles = ["ML", "GenAI", "Python"]
title_lengths = {title: len(title) for title in titles}
print(title_lengths)          # {'ML': 2, 'GenAI': 5, 'Python': 6}
print(titles)                 # original list unchanged
```

An optional condition filters entries:

```python
titles = ["ML", "GenAI", "Python"]
ai_lengths = {title: len(title) for title in titles if "AI" in title}
print(ai_lengths)             # {'GenAI': 5}
```

If the source produces the **same key more than once**, later values replace earlier values under that key; a dictionary does not retain a duplicate key as a second pair. If you need all duplicate observations, decide on an appropriate list or grouped-data design rather than assume a comprehension preserves them.

## 10. Guided lab: manage named lesson fields

Create `dictionary_records.py` in `qai-path-lab/code-lab/`:

```python
# dictionary_records.py
lesson = {"code": "QAI.01.18", "title": "Dictionary", "status": "draft"}
snapshot = lesson.copy()  # separate outer dictionary of string values

lesson["title"] = "Dictionaries"
lesson["level"] = "Beginner"
previous_status = lesson.pop("status")

print("Original snapshot:", snapshot)
print("Current record:", lesson)
print("Removed status:", previous_status)
print("Required code:", lesson["code"])
print("Optional author:", lesson.get("author", "Not provided"))
print("Contains title key:", "title" in lesson)
print("Keys:", list(lesson.keys()))

for key, value in lesson.items():
    print(f"{key}: {value}")

catalog = {lesson["code"]: {"title": lesson["title"], "level": lesson["level"]}}
print("Catalog title:", catalog["QAI.01.18"]["title"])
```

Run from `code-lab` with `py .\dictionary_records.py` in Windows PowerShell (or your verified `python` command); use `python3 dictionary_records.py` in Bash/Zsh.

**Expected output:**

```text
Original snapshot: {'code': 'QAI.01.18', 'title': 'Dictionary', 'status': 'draft'}
Current record: {'code': 'QAI.01.18', 'title': 'Dictionaries', 'level': 'Beginner'}
Removed status: draft
Required code: QAI.01.18
Optional author: Not provided
Contains title key: True
Keys: ['code', 'title', 'level']
code: QAI.01.18
title: Dictionaries
level: Beginner
Catalog title: Dictionaries
```

**Trace:** the existing `"title"` keeps its place when its value changes. Removing `"status"` removes one pair; adding `"level"` appends a new key in insertion order. `snapshot` still has the original strings, because it is a separate outer dictionary and these sample values are strings.

**Controlled change 1:** delete the `"code"` pair from the *initial literal* and rerun. The script now fails at `lesson["code"]`: this is a missing **required** field, not a reason to silently invent a code. Restore it.

**Controlled change 2:** change the author's lookup to `lesson.get("author")`. The printed line becomes `Optional author: None`; the script otherwise works. Explain the difference from a default display label. For a record with `"author": None`, the same lookup gives `None` but `"author" in lesson` is `True`.

## 11. Diagnose mismatches precisely

| Observation | Cause | Repair |
|---|---|---|
| `lesson["missing"]` raises `KeyError` | key absent | validate required data; use `get` only if absence is allowed |
| `lesson.get("x")` gives `None` | either absent key or stored `None` | use `"x" in lesson` if presence matters |
| `"Beginner" in lesson` is `False` | membership checks keys | inspect `lesson.values()` when searching values |
| `lesson[0]` raises `KeyError` | dictionary keys are not sequence indexes | use a named key such as `lesson["code"]` |
| `{"x": 1, "x": 2}` has one pair | duplicate key overwrote earlier value | generate unique keys or use a structure for repeated records |
| `for x in lesson:` prints field names | default iteration visits keys | use `.values()` or `.items()` for needed data |
| an inner record changes in both copies | outer copy retained nested aliases | copy inner data according to required independence |
| key insertion during direct iteration fails | dictionary size changed during traversal | iterate over a separate snapshot or build a new dictionary |
| `lesson.pop("missing")` raises `KeyError` | removal expected a present key | decide whether absence is an error or provide a deliberate fallback |

For debugging, print `repr(record)`, check the **exact** key spelling, list the keys, identify whether the key is optional, then inspect the relevant level. Test normal, missing-key, and stored-`None` cases separately.

## 12. Independent micro-lab and complete solution

**Task:** start with `{"code": "QAI.01.18", "title": "Dictionaries"}`. Add optional `"level": "Beginner"`; keep the original untouched; create a second dictionary whose keys are `"code"` and `"title"` and whose values are the lengths of the corresponding strings. Print the required title, a fallback for missing `"owner"`, the new key-value pairs, and both original and edited records.

**Full solution:**

```python
original = {"code": "QAI.01.18", "title": "Dictionaries"}
edited = original.copy()
edited["level"] = "Beginner"
lengths = {key: len(value) for key, value in original.items()}

print("Required title:", edited["title"])
print("Optional owner:", edited.get("owner", "Not provided"))
print("Lengths:", lengths)
print("Original:", original)
print("Edited:", edited)
```

**Expected output:**

```text
Required title: Dictionaries
Optional owner: Not provided
Lengths: {'code': 9, 'title': 12}
Original: {'code': 'QAI.01.18', 'title': 'Dictionaries'}
Edited: {'code': 'QAI.01.18', 'title': 'Dictionaries', 'level': 'Beginner'}
```

**Why it works:** `original.copy()` creates a separate outer record containing string values. The comprehension iterates over `(key, value)` pairs, keeps each key, and computes the string length as its new value. If the input could include non-string values, validate the data or define what the length should mean before applying this code.

## 13. Remember and retain

- Dictionary = mutable mapping from **unique keys** to values; `{}` is empty.
- Bracket lookup requires a present key; `get` supports genuinely optional fields.
- `key in record` tests keys. Absence differs from an explicitly stored `None`.
- Assignment updates an existing key or adds a new pair; `del` and `pop` remove pairs.
- `keys()`, `values()`, `items()` provide views; `items()` supports key-and-value iteration.
- Read a nested dictionary one level at a time; outer `copy()` does not isolate mutable inner records.
- A comprehension can make a new mapping; duplicate generated keys overwrite earlier values.
- Retain `dictionary_records.py`, its output, and a short missing-required-field debug record. The P0 lesson supplies the dictionary portion of the later collection-choice cluster exercise.

**Next:** QAI.01.19 introduces sets for unique items and set operations; sets are not dictionaries despite both involving braces.

---

**Node contract (S90):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. This note includes all 18 S86 dictionary topics, a guided runnable record, controlled invalid/optional cases, and a complete solved micro-lab. Learner evidence requires executing the script and explaining observed cases.
