# QAI.01.15 — Sequence Basics

> QAI.01.14 String operations → **QAI.01.15 Sequence basics** → QAI.01.16 Lists

## 1. Why this node comes now

The previous lesson turned `"Explain GenAI simply"` into the parts `["Explain", "GenAI", "simply"]`. A course assistant may also hold lesson titles, example prompts, or evaluation results as several items in a known order. Before you change such a collection, learn how to **read** it: order, length, position, slice, membership, and one-item-at-a-time traversal.

By the end, you can explain and predict what Python will read from an ordered collection, run a small inspection script, and diagnose three common mistakes. Building and changing lists belongs to QAI.01.16.

## 2. Collection → sequence → item

A **collection** is a value that contains several items. A **sequence** is a collection whose items have a defined order and numbered positions. A **sequence item** is one value at one of those positions. Familiar sequences include a string of characters and a list of values:

```python
question = "AI"
lessons = ["Python", "ML", "GenAI"]
print(question)                 # AI
print(lessons)                  # ['Python', 'ML', 'GenAI']
```

| Value | One item means | Positions |
|---|---|---|
| `"AI"` | a one-character string such as `"A"` | 0, 1 |
| `["Python", "ML", "GenAI"]` | a whole element such as `"Python"` | 0, 1, 2 |

**Important distinction:** a string and a list are both sequences, but their items differ. `"Python"` is one **list** item, while it contains six **string** items (one character at each position). A sequence can contain duplicates: repeated values occupy separate positions.

## 3. Ordered collection, duplicate item, and length

**Ordered collection** means the position of each item is meaningful. The list below records lesson order; swapping its first and second titles changes the learning order.

**Sequence length** counts items, not unique values. Use `len(sequence)`:

```python
lessons = ["Python", "ML", "ML", "GenAI"]
print(len(lessons))             # 4
print(len("ML"))                # 2
```

The value `"ML"` occurs twice in `lessons`. These are **duplicate items**, at indexes 1 and 2. The list length is still 4. For the string `"ML"`, length 2 counts characters. **Ordered** does not mean sorted alphabetically; the stored order is simply the order of positions.

An empty sequence has length zero:

```python
print(len(""))                 # 0
print(len([]))                 # 0
```

`[]` is an empty list; QAI.01.16 teaches list creation in depth.

## 4. Sequence index: read exactly one item

A **sequence index** identifies one position. Python counts from zero; `-1` reads the last item. An index read does not change the sequence:

```python
lessons = ["Python", "ML", "GenAI"]
print(lessons[0])              # Python
print(lessons[1])              # ML
print(lessons[-1])             # GenAI
print(lessons[-2])             # ML
print(lessons)                 # ['Python', 'ML', 'GenAI']
```

| Index from start | 0 | 1 | 2 |
|---|---|---|---|
| Item | Python | ML | GenAI |
| Index from end | -3 | -2 | -1 |

`lessons[3]` and `lessons[-4]` raise `IndexError`. An empty sequence has no valid index: `[][0]` also raises `IndexError`. A negative index does not reverse the collection; it selects a position relative to the end.

## 5. Sequence slice: read a portion

A **sequence slice** takes a range of positions: `sequence[start:stop:step]`. The **start** is included; the **stop** is excluded; the **step** is the movement between selected positions. You already used this with strings. Now compare the results:

```python
lessons = ["Python", "ML", "GenAI", "RAG"]
print(lessons[1:3])            # ['ML', 'GenAI']
print(lessons[:2])             # ['Python', 'ML']
print(lessons[-2:])            # ['GenAI', 'RAG']
print(lessons[::2])            # ['Python', 'GenAI']
print(lessons[::-1])           # ['RAG', 'GenAI', 'ML', 'Python']
print("GenAI"[1:3])            # en
```

**Worked trace:** `lessons[1:3]` begins at position 1 (`"ML"`), includes position 2 (`"GenAI"`), and stops **before** position 3 (`"RAG"`). The result is another list with two items. A slice of a string is a string; a slice of a list is a list.

`lessons[99:]` gives an empty list, while `lessons[99]` raises `IndexError`. A step of zero raises `ValueError`. A full list slice can produce a **new outer list**, but if its items are mutable nested objects, those objects can still be shared. The alias and copy consequences are taught in QAI.01.16, building on QAI.01.09.

## 6. Membership test: which level is checked?

A **membership test** asks whether the sought item is in a collection. With `in` it gives `True` or `False`:

```python
lessons = ["Python", "ML", "GenAI"]
print("ML" in lessons)          # True: exact top-level item
print("Gen" in lessons)         # False: not a whole list item
print("Gen" in lessons[2])      # True: substring in the string 'GenAI'
print("RAG" not in lessons)     # True
```

**Mental model:** `"Gen" in lessons` checks each top-level element for equality with `"Gen"`; it does not search *inside* each lesson title. `"Gen" in lessons[2]` does search inside that one string. Membership of a string (`"Gen" in "GenAI"`) means substring search; membership of a list means equality with one of its items.

A collection can be nested; `in` still checks its top-level items, not every deeper item. Do not conclude that a missing membership result means the text never occurs anywhere in a nested structure.

## 7. Sequence iteration: one item at a time

**Iteration** means visiting sequence items one at a time, in order. Here is a small preview of a `for` loop; the complete design of loops, including termination and variants, comes in QAI.01.21:

```python
lessons = ["Python", "ML", "GenAI"]
for lesson in lessons:
    print("Study:", lesson)
```

```text
Study: Python
Study: ML
Study: GenAI
```

Read `for lesson in lessons:` as “take each item of `lessons`, one at a time, and refer to the current item as `lesson`.” The indented `print` runs once per item. **Trace:**

| Visit | Current item (`lesson`) | Printed line |
|---:|---|---|
| 1 | Python | Study: Python |
| 2 | ML | Study: ML |
| 3 | GenAI | Study: GenAI |

The loop visits each position, including duplicates; it does not automatically remove them. An empty sequence produces zero visits. The loop does not change the sequence simply by reading each item.

Iterating through a string visits its characters rather than whole words:

```python
for character in "AI":
    print(character)
```

```text
A
I
```

In the previous lesson, `"Explain GenAI".split()` gave a list of two word-like parts; iterating over *that list* would visit `"Explain"` and then `"GenAI"`. These parts are separated by whitespace rules, not by a language-aware word analyser.

## 8. Guided lab: inspect an AI course path

Create `sequence_basics.py` in `qai-path-lab/code-lab/`:

```python
# sequence_basics.py
# Sample course path for learning the behaviour of sequences.
course_path = ["Python", "ML", "ML", "GenAI"]
ai_text = "GenAI"

print("Number of lessons:", len(course_path))
print("First lesson:", course_path[0])
print("Last lesson:", course_path[-1])
print("Middle portion:", course_path[1:3])
print("Every other lesson:", course_path[::2])
print("Has full title ML:", "ML" in course_path)
print("Has full title Gen:", "Gen" in course_path)
print("Gen occurs inside last title:", "Gen" in course_path[-1])
print("Number of text characters:", len(ai_text))
print("First text character:", ai_text[0])

for lesson in course_path:
    print("Visit:", lesson)

print("Original path:", course_path)
```

Run it from `code-lab` with `py .\sequence_basics.py` in PowerShell (or your previously verified `python` command); use `python3 sequence_basics.py` in Bash/Zsh.

**Expected output:**

```text
Number of lessons: 4
First lesson: Python
Last lesson: GenAI
Middle portion: ['ML', 'ML']
Every other lesson: ['Python', 'ML']
Has full title ML: True
Has full title Gen: False
Gen occurs inside last title: True
Number of text characters: 5
First text character: G
Visit: Python
Visit: ML
Visit: ML
Visit: GenAI
Original path: ['Python', 'ML', 'ML', 'GenAI']
```

**Controlled variation A:** replace the path with `["Python", "GenAI"]`. The length becomes 2; the middle slice `[1:3]` is `['GenAI']`, not an error; the last item remains `"GenAI"`; the iteration prints two visits.

**Controlled variation B:** replace the path with `[]`. Length is 0; `course_path[1:3]` gives `[]`; `course_path[-1]` raises `IndexError`. To run this variation without a crash, temporarily comment out the two lines that read `[0]` and `[-1]`, including the `[-1]` in the substring check. The loop prints no `Visit:` lines. Later conditionals let you handle empty data in the program itself.

## 9. Diagnose wrong interpretations before changing code

| Symptom | Likely misconception | Check |
|---|---|---|
| `len(["ML", "ML"])` gives 2 | duplicate values were assumed to count once | count stored positions; both positions contain an item |
| `"Gen" in ["GenAI"]` gives `False` | substring matching was assumed for a list | test membership of the entire list item, or search inside the selected string |
| `lessons[1:2]` contains only item 1 | slice stop was assumed inclusive | write index labels; stop is excluded |
| `lessons[99:]` is empty but `lessons[99]` fails | slice and single-index boundaries were confused | check `len(lessons)` before using an index |
| a duplicate lesson prints twice | iteration was assumed to deduplicate | trace one visit per stored position |
| string iteration prints letters instead of words | string item type was assumed to be a word | use `.split()` only when whitespace-separated parts are intended |
| `len(lessons)` differs from `len(lessons[0])` | outer collection and contained text were confused | say what one item means at each level |

When debugging, first write the exact sequence, number its positions, mark the operation (`index`, `slice`, `in`, or `for`), predict the result, and compare it to Python's output. Test empty and duplicate-containing sequences too.

## 10. Independent micro-lab with complete solution

**Task:** take `labels = ["Input", "Process", "Output", "Output"]`. Print its number of items, the first item, the last two items as a slice, whether the whole item `"Put"` exists, whether `"Put"` occurs inside the second item of the slice `labels[2:]`, and visit every label in order. Predict and then run.

**Predict:** there are four stored items, even though one value is repeated. `"Put"` does not equal the item `"Output"` (case also differs), and `"Put"` is not a case-sensitive substring of `"Output"`; `"put"` is.

**Solution:**

```python
labels = ["Input", "Process", "Output", "Output"]
print(len(labels))
print(labels[0])
print(labels[-2:])
print("Put" in labels)
print("Put" in labels[2:][1])
print("put" in labels[2:][1])
for label in labels:
    print("Visit:", label)
```

**Expected output:**

```text
4
Input
['Output', 'Output']
False
False
True
Visit: Input
Visit: Process
Visit: Output
Visit: Output
```

**Explain the nested selection:** `labels[2:]` creates a two-item list `["Output", "Output"]`; `[1]` reads its second item, the string `"Output"`. `"put" in "Output"` is `True` because its last three letters are lowercase `p`, `u`, `t`. The two `Visit: Output` lines reflect the two separate positions.

## 11. Remember and retain

- A sequence is an ordered collection; `len` counts all items, including duplicates.
- An index retrieves one item; a slice retrieves a portion, excluding its stop.
- For a list, `in` compares top-level items; for a string, it looks for a substring.
- Iteration visits each stored position in order; a string yields characters.
- Check what “one item” means before interpreting length, membership, or iteration.

Save `sequence_basics.py` and record the output for both the original and the two controlled variations. For the empty-sequence variation, record the `IndexError` and which attempted index caused it. This is the node's runnable evidence and debug record.

**Next:** QAI.01.16 teaches how to create, update, copy, and deliberately manage lists rather than only inspect them.

---

**Node contract (S89):** `C | L3 | H0–H2 | E1–E3 | A1–A3 | P0`. This note supplies a positional mental model, traced predictions, a guided executable lab, a solved micro-lab, and a boundary investigation. Learner evidence requires running, changing, and explaining the results; this note alone does not establish that evidence.
