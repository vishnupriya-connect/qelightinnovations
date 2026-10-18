# QAI.01.17 — Tuples

> QAI.01.16 Lists → **QAI.01.17 Tuples** → QAI.01.18 Dictionaries

## 1. Destination: keep a fixed ordered group

A lesson can have a code, a title, and a level: `("QAI.01.17", "Tuples", "Beginner")`. These three positions have a specific meaning. When a particular group of values should stay together and the **positions themselves should not be reassigned**, a Python **tuple** can represent that group. This lesson shows how to construct, read, and unpack tuples, and exactly what tuple immutability does and does not guarantee.

You will produce `tuple_records.py`, a short executable exercise with an intentionally diagnosed unpacking error. A tuple does not replace a list of changing lessons; choosing the right collection for a course record is part of the later QAI.01.15–01.19 cluster project.

## 2. Tuple, tuple literal, item, and empty tuple

A **tuple** is an ordered sequence whose positions cannot be reassigned after it is created. A **tuple literal** usually shows comma-separated values inside parentheses. Each value is a **tuple item**:

```python
lesson = ("QAI.01.17", "Tuples", "Beginner")
empty = ()
print(lesson)                 # ('QAI.01.17', 'Tuples', 'Beginner')
print(len(lesson))            # 3
print(empty)                  # ()
print(type(lesson))           # <class 'tuple'>
```

The empty tuple has zero items. Items may have different types, and duplicates are allowed:

```python
checkpoints = ("draft", "review", "review")
print(len(checkpoints))       # 3: duplicates occupy positions
print("review" in checkpoints)  # True
```

**Mental model:** a list is a row of positions whose entries you can update; a tuple is a row of positions whose entries cannot be replaced. Both preserve item order. Neither verifies that a code, title, and level have been entered correctly.

## 3. One item needs a comma

**Single-item tuple:** `("Python",)` contains one item. The comma makes it a tuple; parentheses around a value alone do not:

```python
one = ("Python",)
grouped_string = ("Python")
empty = ()
print(one, type(one))             # ('Python',) <class 'tuple'>
print(grouped_string, type(grouped_string))  # Python <class 'str'>
print(len(one))                   # 1
print(len(empty))                 # 0
```

For several items, commas also create the tuple even without parentheses: `"ML", "GenAI"` is a tuple. Use parentheses when they make the intended grouping clearer. Do not mistake the comma printed in `('Python',)` for part of the string: its item is `"Python"`.

## 4. Tuple index and slice

A **tuple index** selects one item starting at index 0; a negative index counts from the end. A **tuple slice** selects a range and produces another tuple. The stop is excluded, just as with lists and strings:

```python
lesson = ("QAI.01.17", "Tuples", "Beginner")
print(lesson[0])             # QAI.01.17
print(lesson[-1])            # Beginner
print(lesson[0:2])           # ('QAI.01.17', 'Tuples')
print(lesson[:1])            # ('QAI.01.17',)
print(lesson[::-1])          # ('Beginner', 'Tuples', 'QAI.01.17')
```

`lesson[3]` raises `IndexError` because there are only three items at positions 0–2. `lesson[3:]` returns `()`. The result of `lesson[:1]` is a **one-item tuple**, so its displayed form retains the comma.

You can visit items in order as with any sequence:

```python
for part in ("QAI.01.17", "Tuples"):
    print("Part:", part)
```

```text
Part: QAI.01.17
Part: Tuples
```

The `for` syntax was previewed in QAI.01.15; full loop design comes in QAI.01.21.

## 5. Immutable sequence: what cannot change

An **immutable sequence** does not allow replacing an item at an existing index or using list-changing methods:

```python
lesson = ("QAI.01.17", "Tuples", "Beginner")
# lesson[1] = "Lists"        # TypeError: tuple does not support item assignment
# lesson.append("Example")   # AttributeError: tuple has no append method
print(lesson)                 # still the same tuple
```

If you want a different tuple, create one and bind the name to it:

```python
lesson = ("QAI.01.17", "Tuples", "Beginner")
revised = (lesson[0], lesson[1], "Foundation")
print(revised)                # ('QAI.01.17', 'Tuples', 'Foundation')
print(lesson)                 # original remains unchanged
```

`lesson = revised` would make the name `lesson` refer to the new tuple; it would **not** edit the former tuple. Tuple concatenation works the same way: `("ML",) + ("GenAI",)` returns a new tuple `("ML", "GenAI")`.

**Important limit:** a tuple can hold a **mutable item** such as a list. You cannot replace that tuple position, but you can change the list stored there:

```python
record = ("QAI.01.17", ["draft"])
record[1].append("review")
print(record)                 # ('QAI.01.17', ['draft', 'review'])
# record[1] = ["final"]      # TypeError if executed
```

Thus, “tuple is immutable” means the tuple's **own slots** are fixed; it does not make every object reachable through those slots immutable. This connects to the shallow-copy and alias discussion in QAI.01.09 and QAI.01.16.

## 6. Tuple unpacking and multiple assignment

**Tuple unpacking** assigns its items to separate names in their stored order. **Multiple assignment** means placing values into several names in one statement:

```python
lesson = ("QAI.01.17", "Tuples", "Beginner")
code, title, level = lesson
print(code)                   # QAI.01.17
print(title)                  # Tuples
print(level)                  # Beginner
```

Read the assignment as “first item → `code`, second → `title`, third → `level`.” Exactly three target names are used for exactly three values here. Multiple assignment also works directly with comma-separated values:

```python
first, second = "ML", "GenAI"
print(first, second)          # ML GenAI
first, second = second, first
print(first, second)          # GenAI ML
```

The swap prepares the values on the right before binding the names on the left; no temporary name is needed. The comma-separated pair on the right is tuple-like packing; unpacking also works with some other sequences, including a two-item list.

**Mismatch error:**

```python
pair = ("QAI.01.17", "Tuples")
# code, title, level = pair  # ValueError: not enough values to unpack
code, title = pair
print(code, title)            # QAI.01.17 Tuples
```

Too many values for too few target names also raises `ValueError`. When the expected shape of external data may vary, validate the number of values before unpacking or use an explicit record with named fields. Ignoring a shape mismatch silently would risk assigning the wrong meaning to a position.

## 7. Guided implementation: inspect a fixed lesson record

Create `tuple_records.py` in `qai-path-lab/code-lab/`:

```python
# tuple_records.py
lesson = ("QAI.01.17", "Tuples", "Beginner")
code, title, level = lesson

print("Tuple:", lesson)
print("Length:", len(lesson))
print("First item:", lesson[0])
print("Last item:", lesson[-1])
print("First two:", lesson[:2])
print("Code:", code)
print("Title:", title)
print("Level:", level)

revised = (code, title, "Foundation")
print("Revised tuple:", revised)
print("Original tuple:", lesson)

for part in lesson:
    print("Visit:", part)
```

Run from `code-lab` with `py .\tuple_records.py` in Windows PowerShell (or your verified `python` command), or `python3 tuple_records.py` in Bash/Zsh.

**Expected output:**

```text
Tuple: ('QAI.01.17', 'Tuples', 'Beginner')
Length: 3
First item: QAI.01.17
Last item: Beginner
First two: ('QAI.01.17', 'Tuples')
Code: QAI.01.17
Title: Tuples
Level: Beginner
Revised tuple: ('QAI.01.17', 'Tuples', 'Foundation')
Original tuple: ('QAI.01.17', 'Tuples', 'Beginner')
Visit: QAI.01.17
Visit: Tuples
Visit: Beginner
```

**Controlled change A:** replace the tuple with `("QAI.01.17", "Tuples")`. The line `code, title, level = lesson` now raises `ValueError`. Explain why before running: three target names but only two items. To complete this variation successfully, restore a third value such as `"Foundation"`.

**Controlled change B:** leave the original tuple in place and uncomment a new line `lesson[1] = "Lists"` after creation. Python raises `TypeError`. Restore the working script and create a separate revised tuple instead, as above. These two failures are distinct: the first is an **unpacking shape** error; the second is an attempted **tuple mutation**.

## 8. Common errors and exact fixes

| Symptom | Why | Fix |
|---|---|---|
| `("Python")` behaves like text | parentheses alone group an expression | write `("Python",)` |
| `lesson[3]` gives `IndexError` | indexes for three items end at 2 | inspect `len(lesson)`; use an existing position |
| `lesson[1] = "ML"` gives `TypeError` | tuple slots cannot be reassigned | create a revised tuple; use a list when regular item updates are needed |
| `lesson.append("RAG")` gives `AttributeError` | tuple lacks list mutation methods | use a list for a changing sequence |
| unpacking raises `ValueError` | number of variables differs from number of items | inspect the shape; match counts or validate variable input |
| inner list changed despite tuple immutability | contained list is still mutable | keep immutable items if full value immutability is required |
| course record fields are confused | positional meanings were not stated | document positions or later use a dictionary with named fields |

**Debug routine:** print the tuple with `repr(lesson)`, check `len(lesson)`, number its positions, count the unpacking targets, then decide whether the requirement calls for a fixed tuple or a mutable list. Do not catch an unpacking exception and continue with incomplete field assignments.

## 9. Independent micro-lab and full solution

**Task:** represent a fixed two-field evaluation result with lesson code `"QAI.01.17"` and status `"passed"`. Unpack it, print a formatted result, show the first-item slice, and make a **new** tuple whose status is `"review"` without changing the original. Demonstrate how to represent a one-field tuple containing only the code.

**Complete solution:**

```python
result = ("QAI.01.17", "passed")
code, status = result
print(f"{code}: {status}")
print(result[:1])
revised = (code, "review")
print("Revised:", revised)
print("Original:", result)
single = (code,)
print("One item:", single)
print("One-item length:", len(single))
```

**Expected output:**

```text
QAI.01.17: passed
('QAI.01.17',)
Revised: ('QAI.01.17', 'review')
Original: ('QAI.01.17', 'passed')
One item: ('QAI.01.17',)
One-item length: 1
```

**Reasoning:** `result[:1]` is a one-item tuple because slicing a tuple returns a tuple. `revised` is a new value; `result` still reports `"passed"`. The comma in `(code,)` ensures the one-field record is a tuple.

## 10. What to remember and retain

- A tuple is ordered. Use indexes, slices, membership, and iteration as for other sequences.
- `()` is empty; `("Python",)` has one item; `("Python")` is a string.
- The tuple's positions cannot be reassigned. A mutable object stored as an item can still change.
- Unpacking binds tuple positions to names in order; normal unpacking needs matching counts.
- Multiple assignment supports concise unpacking and swapping.
- Keep `tuple_records.py`, its expected-versus-observed output, the two controlled-error observations, and a one-paragraph list-versus-tuple choice: a changing curriculum path → list; a fixed-position record → tuple when positional fields are clear.

**Next:** QAI.01.18 introduces dictionaries, where named keys such as `"code"` and `"title"` make record fields explicit.

---

**Node contract (S90):** `C | L3 | H1–H2 | E2–E3 | A1–A3 | P0`. This note covers all ten S86 tuple items, provides worked traces, a runnable guided script, a fully solved micro-lab, and two controlled error diagnoses. Learner evidence comes from executing and explaining them.
