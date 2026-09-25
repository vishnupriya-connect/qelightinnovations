# QAI.01.16 — Lists

> QAI.01.15 Sequence basics → **QAI.01.16 Lists** → QAI.01.17 Tuples

## 1. Destination: manage a changing course path

A QElight course path begins with Python, then ML, then GenAI. As the teaching plan changes, you need to add a lesson, correct an item, remove a duplicate, reorder lessons, and produce a filtered view without damaging the original. A Python **list** gives you an ordered, changeable collection of items.

You will implement `course_records_collections.py`, predict each change, run it, and explain exactly when two names refer to the **same list**. This node focuses on list operations; tuples, dictionaries, and sets follow in QAI.01.17–01.19.

## 2. List, list literal, item, and empty list

A **list literal** is written with square brackets and comma-separated items. A **list item** is one value inside it. An **empty list** contains no items:

```python
path = ["Python", "ML", "GenAI"]
empty = []
print(path)                    # ['Python', 'ML', 'GenAI']
print(len(path))               # 3 items
print(empty)                   # []
print(type(path))              # <class 'list'>
```

Order is stored, duplicates are allowed, and items may have different types. For a course path, consistent types such as lesson-title strings are easier to reason about. `["ML", "ML"]` has two items; `"ML"` alone is a string with two characters. Later you will put related fields into records rather than infer their meaning from an item's position.

**Nested list:** a list can itself contain other lists:

```python
weeks = [["Python", "Data"], ["ML", "GenAI"]]
print(weeks[0])                # ['Python', 'Data']: first inner list
print(weeks[1][0])             # ML: first item in second inner list
print(len(weeks))              # 2 outer items, not 4 lessons
```

Read `weeks[1][0]` from left to right: select the second outer item, then select its first inner item.

## 3. Index and slice: first read without changing

A **list index** chooses one item. A **list slice** returns a new outer list containing items from the selected positions. As in QAI.01.15, start is inclusive and stop is exclusive:

```python
path = ["Python", "Data", "ML", "GenAI"]
print(path[0])                 # Python
print(path[-1])                # GenAI
print(path[1:3])               # ['Data', 'ML']
print(path[:2])                # ['Python', 'Data']
print(path[99:])               # []
# print(path[99])              # IndexError if executed
```

A slice is useful for a small selection or an outer copy. It is **not** a deep copy of nested lists; see Section 9. Check `len(path)` before using an index whose existence is uncertain. An empty list `[]` has no valid index.

## 4. List mutation: change an existing item

**Mutation** changes an existing object. Unlike strings, lists are mutable. Assigning to an existing position changes the list:

```python
path = ["Python", "Maths", "GenAI"]
path[1] = "ML"
print(path)                    # ['Python', 'ML', 'GenAI']
```

An index assignment cannot create a missing distant position:

```python
path = ["Python"]
# path[1] = "ML"              # IndexError: index 1 does not yet exist
path.append("ML")
print(path)                    # ['Python', 'ML']
```

If another name refers to the same list, that other name sees the mutation. That matters whenever you “save” an original before experimenting.

## 5. Add one item, many items, or an item at a position

`.append(item)` adds **one item** at the end. `.extend(iterable)` adds each item from an iterable; here we give it another list. `.insert(index, item)` puts one item before the specified position:

```python
path = ["Python"]
path.append("ML")
print(path)                    # ['Python', 'ML']
path.extend(["NLP", "GenAI"])
print(path)                    # ['Python', 'ML', 'NLP', 'GenAI']
path.insert(1, "Data")
print(path)                    # ['Python', 'Data', 'ML', 'NLP', 'GenAI']
```

`.append(["NLP", "GenAI"])` would add **one nested list**, giving `["Python", ["NLP", "GenAI"]]`. Choose `extend` when you mean two separate lessons. `insert(1, "Data")` does not overwrite `"ML"`; it shifts `"ML"` and later items one place right.

**Predict before trying:** `path.insert(100, "Projects")` inserts at the end if the position exceeds the list length; it does not create 95 blank slots.

## 6. Remove by value, remove by index, and return a removed item

`.remove(value)` removes the **first equal value**; it raises `ValueError` if no match exists. `del path[index]` removes the item at an index; `.pop(index)` removes **and returns** it. `.pop()` without an index removes and returns the last item:

```python
path = ["Python", "ML", "ML", "GenAI"]
path.remove("ML")
print(path)                    # ['Python', 'ML', 'GenAI']
del path[0]
print(path)                    # ['ML', 'GenAI']
removed = path.pop(0)
print(removed)                 # ML
print(path)                    # ['GenAI']
print(path.pop())              # GenAI
print(path)                    # []
```

**Choose precisely:**

| Need | Operation | What you get |
|---|---|---|
| remove the first matching item | `path.remove("ML")` | list changes; method returns `None` |
| remove item at a known position | `del path[0]` | list changes; no returned item |
| remove and keep item at a position | `removed = path.pop(0)` | item returned and list changes |
| remove and keep last item | `removed = path.pop()` | last item returned and list changes |

`path.remove("Missing")` raises `ValueError`. `path.pop()` on an empty list raises `IndexError`. Check the requirement and the actual contents before deleting; use later conditional logic to handle a missing value or an empty list as an expected case.

`.clear()` removes **all items** from the same list object:

```python
path = ["Python", "ML"]
path.clear()
print(path)                    # []
```

If another name aliases this list, it also sees the empty list. `path = []` instead binds only the name `path` to a *different* empty list; an earlier alias still points to the old list.

## 7. Sort and reverse: order, meaning, and side effects

`.sort()` sorts a list **in place**. `.reverse()` reverses its **current order in place**. Neither means “make a new sorted/reversed list.” Both methods return `None`:

```python
titles = ["GenAI", "Python", "ML"]
result = titles.sort()
print(titles)                  # ['GenAI', 'ML', 'Python']
print(result)                  # None
titles.reverse()
print(titles)                  # ['Python', 'ML', 'GenAI']
```

This alphabetical sorting changes an intended **prerequisite order**. Do not sort a curriculum merely because its titles are text. If you need a sorted copy without modifying the original outer list, `sorted(titles)` returns a new list:

```python
path = ["Python", "ML", "GenAI"]
alphabetical = sorted(path)
print(alphabetical)            # ['GenAI', 'ML', 'Python']
print(path)                    # ['Python', 'ML', 'GenAI']
```

`.reverse()` changes the current order; `.sort(reverse=True)` sorts in descending order. They are different operations. Sorting a list containing incompatible values such as `["ML", 2]` raises `TypeError` in Python 3; meaningful sorting needs a deliberate ordering rule and compatible comparison values.

## 8. Alias versus copied list

A **list alias** is another name pointing to the same list. A **copied list** is a new outer list. Predict both traces:

```python
original = ["Python", "ML"]
alias = original
alias.append("GenAI")
print(original)                # ['Python', 'ML', 'GenAI']
print(alias is original)       # True: one list, two names

copy = original.copy()
copy.append("RAG")
print(copy)                    # ['Python', 'ML', 'GenAI', 'RAG']
print(original)                # ['Python', 'ML', 'GenAI']
print(copy is original)        # False: different outer lists
```

`original[:]` and `list(original)` also make a new **outer** list. `==` compares content; `is` checks whether two names refer to the same object. With equal content after copying, `copy == original` can be `True` while `copy is original` is `False`. This revisits QAI.01.09 with a concrete mutation.

### Nested-list limit: a shallow copy

`.copy()` copies the outer list, but inner mutable lists remain shared:

```python
original = [["Python"], ["ML"]]
shallow = original.copy()
shallow[0].append("Data")
print(original)                # [['Python', 'Data'], ['ML']]
print(shallow)                 # [['Python', 'Data'], ['ML']]
shallow.append(["GenAI"])
print(original)                # [['Python', 'Data'], ['ML']]
print(shallow)                 # [['Python', 'Data'], ['ML'], ['GenAI']]
```

The first mutation changes a shared **inner** list. The final append changes only the **outer** `shallow` list. For genuinely independent nested data, make an appropriate deep copy after deciding what should be independent; QAI.01.09 introduces the deep-copy operation. A copy is not automatically a privacy or isolation boundary.

## 9. Why removing inside iteration can skip an item

Recall that iteration visits positions in sequence. If you remove an earlier item while iterating over the **same** list, later items shift left while the iteration continues to its next position:

```python
path = ["ML", "ML", "GenAI"]
for title in path:
    if title == "ML":
        path.remove(title)
print(path)                    # ['ML', 'GenAI']: one ML was skipped
```

**Trace:** visit first `"ML"` at index 0 → remove it → remaining `["ML", "GenAI"]` shifts left → iteration advances to index 1 and visits `"GenAI"`. The second `"ML"`, now at index 0, is missed.

For a filtered **new** list, a list comprehension below is clear. For a very small fixed example, you can also iterate over a copy, `for title in path.copy():`, while mutating `path`; then each original item is visited once. Check whether keeping or removing duplicates is the actual goal.

## 10. List comprehension: produce a new list

A **list comprehension** builds a new list from an existing iterable. Its **comprehension expression** says what to put in the result. Read `[title for title in path]` as “take each `title` from `path` and put it in a new list”:

```python
path = ["Python", "ML", "GenAI"]
copied_titles = [title for title in path]
labels = [f"Study: {title}" for title in path]
print(copied_titles)           # ['Python', 'ML', 'GenAI']
print(labels)                  # ['Study: Python', 'Study: ML', 'Study: GenAI']
print(path)                    # original unchanged
```

The expression `f"Study: {title}"` transforms each item using the f-string from QAI.01.14. A **comprehension condition** after `if` keeps only the items meeting a test. This is a small preview of `if`; QAI.01.20 explains conditionals fully:

```python
path = ["ML", "ML", "GenAI"]
without_ml = [title for title in path if title != "ML"]
ai_titles = [title for title in path if "AI" in title]
print(without_ml)              # ['GenAI']
print(ai_titles)               # ['GenAI']
print(path)                    # ['ML', 'ML', 'GenAI']: original unchanged
```

Read the first as “for each title, include it only when the title is not `'ML'`.” The condition is a Boolean expression from QAI.01.12. In this particular example, the comprehension makes a new filtered list and avoids removing from the list being traversed. A comprehension is not automatically faster or more appropriate for every operation; choose it when the goal is an understandable **new** list.

## 11. Guided implementation: manage a course path

Create `course_records_collections.py` in `qai-path-lab/code-lab/`:

```python
# course_records_collections.py
course_path = ["Python", "ML", "ML", "GenAI"]
original_path = course_path.copy()        # independent outer list of strings
same_list = course_path                   # alias: same list object

course_path.insert(1, "Data")
course_path.append("RAG")
course_path.extend(["Agents", "Evaluation"])
course_path.remove("ML")                  # removes first matching ML only
removed_last = course_path.pop()          # keeps removed Evaluation

filtered = [title for title in course_path if title != "ML"]
print("Original snapshot:", original_path)
print("Changed path:", course_path)
print("Alias sees changes:", same_list)
print("Removed last:", removed_last)
print("Filtered copy:", filtered)
print("Same outer list:", same_list is course_path)
print("Snapshot separate:", original_path is not course_path)
print("ML still in path:", "ML" in course_path)
print("ML in filtered copy:", "ML" in filtered)
```

Run from `code-lab` with `py .\course_records_collections.py` in Windows PowerShell (or the verified `python` command), or `python3 course_records_collections.py` in Bash/Zsh.

**Expected output:**

```text
Original snapshot: ['Python', 'ML', 'ML', 'GenAI']
Changed path: ['Python', 'Data', 'ML', 'GenAI', 'RAG', 'Agents']
Alias sees changes: ['Python', 'Data', 'ML', 'GenAI', 'RAG', 'Agents']
Removed last: Evaluation
Filtered copy: ['Python', 'Data', 'GenAI', 'RAG', 'Agents']
Same outer list: True
Snapshot separate: True
ML still in path: True
ML in filtered copy: False
```

**Trace the middle:** after `insert` the path is `['Python', 'Data', 'ML', 'ML', 'GenAI']`. After `append` and `extend`, `'RAG'`, `'Agents'`, and `'Evaluation'` follow. `remove("ML")` removes only the first `ML`. `pop()` removes `Evaluation` and returns it. The comprehension removes the **remaining** `ML` only from a new list. `original_path` is safe as an independent outer list here because each item is a string; Section 8 warns about nested mutable items.

**Controlled change:** replace the initial list with `["Python", "GenAI"]`. `course_path.remove("ML")` now raises `ValueError`. This is a deliberate test of an invalid operation; change `remove("ML")` to `remove("GenAI")` to complete a successful run and predict the changed order. For code that accepts arbitrary paths, explicitly decide whether a missing item should be ignored, reported, or treated as an error before adding conditional or exception-handling logic in later nodes.

## 12. Diagnose list mistakes

| Symptom | Actual mechanism | Repair |
|---|---|---|
| `path = path.append("ML")` makes `path` become `None` | `append` mutates in place and returns `None` | call `path.append("ML")` on its own line |
| `append(["ML", "GenAI"])` adds one nested item | `append` takes one item | use `extend(["ML", "GenAI"])` for two top-level items |
| “backup” changed when current list changed | `backup = current` made an alias | use `current.copy()` when an independent outer list is required |
| inner list changed in both original and copy | `copy()` is shallow | deliberately copy inner lists or use deep copy when needed |
| `remove("ML")` leaves another `"ML"` | only first matching value is removed | create a new filtered list when all matches must go |
| one duplicate escapes removal in a loop | list shifts while it is being iterated | build a new list or iterate over a separate copy |
| `pop()` fails on `[]` | no last item exists | decide how to handle an empty list first |
| sorted curriculum is in the wrong learning order | alphabetical order differs from dependency order | retain the intentional order; use `sorted` only for an actual sorting requirement |
| `path.sort()` assigned to a variable produces `None` | `sort` mutates and returns `None` | call method separately or use `sorted(path)` for a new outer list |

For an unexpected result, write the list contents after **each** mutation. Mark each name as “same object” or “new outer list.” Re-run with an empty list, one item, and duplicates when those inputs matter.

## 13. Independent micro-lab with full solution

**Task:** start with `units = ["Python", "ML", "ML", "GenAI"]`. Keep an unchanged original snapshot. Add `"Data"` before the first `"ML"`; remove **all** `"ML"` items without mutating the list during iteration; append `"RAG"` to the filtered copy; print all three lists and demonstrate that the snapshot and working list are different objects. Predict the results first.

**Complete solution:**

```python
units = ["Python", "ML", "ML", "GenAI"]
snapshot = units.copy()
units.insert(1, "Data")
filtered = [unit for unit in units if unit != "ML"]
filtered.append("RAG")
print("Snapshot:", snapshot)
print("Working:", units)
print("Filtered:", filtered)
print("Independent outer lists:", snapshot is not units)
```

**Expected output:**

```text
Snapshot: ['Python', 'ML', 'ML', 'GenAI']
Working: ['Python', 'Data', 'ML', 'ML', 'GenAI']
Filtered: ['Python', 'Data', 'GenAI', 'RAG']
Independent outer lists: True
```

**Why this meets the task:** `snapshot = units.copy()` captures a separate outer list before editing; `insert` changes the working list; the comprehension creates yet another list without `ML`; `append` adds `RAG` only there. These items are immutable strings, so a shallow snapshot suffices for this lab. **Extra test:** replace `units` with `[]`; `insert(1, "Data")` adds `"Data"` at the end, and the resulting `filtered` becomes `["Data", "RAG"]`, while `snapshot` stays empty.

## 14. Remember and retain

- A list is ordered and mutable. Read with an index/slice; change with indexed assignment or methods.
- `append` adds one item; `extend` adds items from another iterable; `insert` places one before an index.
- `remove` uses a **value** and removes the first match; `del` and `pop` use an **index**; `pop` returns the removed item; `clear` empties the list.
- `sort` and `reverse` change the list; `sorted` returns a new outer list. Dependency order is a separate decision from alphabetical order.
- `alias = original` shares the list. `copy = original.copy()` makes a new **outer** list, while nested mutable items can remain shared.
- List comprehensions make new lists; the expression transforms an item, and an optional condition filters items.
- Save `course_records_collections.py`, the original and controlled-change output, and your short explanation of the intentional `ValueError`. This is the P0 micro-lab evidence; a later cluster project joins it to tuples, dictionaries, and sets.

**Next:** QAI.01.17 introduces tuples when a fixed ordered group should not have its elements reassigned.

---

**Node contract (S89):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. This note supplies definitions, worked traces, a runnable guided build, controlled modification and failure diagnosis, and an independent solved build. Learner implementation and debugging are evidenced by running and changing the script, not by reading it alone.
