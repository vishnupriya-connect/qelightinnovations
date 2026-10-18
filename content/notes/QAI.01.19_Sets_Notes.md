# QAI.01.19 — Sets

> QAI.01.18 Dictionaries → **QAI.01.19 Sets** → QAI.01.20 Conditional execution

## 1. Destination: work with distinct course topics

Suppose course A covers Python, ML, and ML again in its raw lesson list. Course B covers ML and GenAI. To answer “Which distinct topics occur in both?” or “Which topics occur only in A?”, Python **sets** are useful. A set records distinct items and supports operations such as intersection and difference.

You will run `course_topic_sets.py`, compare two topic collections, and explain when preserving the original lesson order requires a list instead. Set output order is not predictable; lab output uses `sorted(...)` solely to make displayed results stable.

## 2. Set, literal, empty set, unique item

A **set** is a mutable collection of **unique items**. A nonempty **set literal** uses braces with comma-separated items; duplicates collapse into one:

```python
topics = {"Python", "ML", "ML", "GenAI"}
print(len(topics))                   # 3 distinct items
print("ML" in topics)               # True
print(sorted(topics))               # ['GenAI', 'ML', 'Python']
```

`{"ML", "ML"}` has one item, `"ML"`. `sorted(topics)` produces a **new sorted list** for display; it does not sort the set itself. Since a set has no meaningful positional order, do not rely on how `print(topics)` happens to arrange its elements.

An **empty set** is `set()`. The literal `{}` is an empty **dictionary** (QAI.01.18):

```python
empty_topics = set()
empty_record = {}
print(type(empty_topics))            # <class 'set'>
print(type(empty_record))            # <class 'dict'>
print(len(empty_topics))             # 0
```

You can make a set from an existing list:

```python
ordered_lessons = ["Python", "ML", "ML", "GenAI"]
unique_topics = set(ordered_lessons)
print(len(ordered_lessons))          # 4 lesson occurrences
print(len(unique_topics))            # 3 distinct topics
print(ordered_lessons)               # original list still ordered and unchanged
```

**Mental model:** a list can answer “What was the second lesson?”; a set can answer “Is ML present?” and “Which distinct topics are shared?” Converting a lesson list to a set loses both duplicates and lesson order. If repeated lessons carry meaning, keep the list.

## 3. Unordered collection and membership

A set is an **unordered collection**: there is no `topics[0]` or `topics[1:3]`. Attempting either gives `TypeError`. Iterating over a set visits its items, but you must not use the visit order as a learning or display order.

**Set membership** with `in` checks whether an equal complete item is present:

```python
topics = {"Python", "ML", "GenAI"}
print("ML" in topics)                # True
print("Gen" in topics)               # False
print("Gen" in "GenAI")              # True: substring in a string
print("RAG" not in topics)           # True
```

`"Gen" in topics` does not search inside the item `"GenAI"`. Similarly, `"ml"` differs from `"ML"`. Decide whether case differences represent different labels before normalising input.

Set items must be **hashable**. Strings and immutable tuples of strings can be items; mutable lists and dictionaries cannot:

```python
topics = {"Python"}
topics.add(("ML", "Beginner"))
print(("ML", "Beginner") in topics)  # True
# topics.add(["GenAI"])             # TypeError: list is unhashable
```

Not every tuple is hashable: a tuple **containing a list** cannot be added as a set item. To represent a mutable record, use a separate data structure and place a stable, hashable identifier (such as a course code) in the set when appropriate.

## 4. Add, remove, discard

`.add(item)` adds one item; adding one that is already present has no further effect:

```python
topics = {"Python", "ML"}
topics.add("GenAI")
topics.add("ML")
print(sorted(topics))               # ['GenAI', 'ML', 'Python']
```

`.remove(item)` removes a present item and raises `KeyError` if it is absent. `.discard(item)` removes a present item but does **nothing** if it is absent:

```python
topics = {"Python", "ML"}
topics.remove("ML")
print(sorted(topics))               # ['Python']
topics.discard("RAG")               # no error: RAG is absent
print(sorted(topics))               # ['Python']
# topics.remove("RAG")              # KeyError if executed
```

Use `remove` when an absent item indicates a broken expectation; use `discard` when “already absent” is a valid outcome. Both mutate the original set. `.add`, `.remove`, and `.discard` return `None`, not the revised set; do **not** write `topics = topics.add("RAG")`.

## 5. Union: all distinct items from both

The **union** `A | B` contains every item appearing in A or B, once:

```python
a = {"Python", "ML"}
b = {"ML", "GenAI"}
print(sorted(a | b))                # ['GenAI', 'ML', 'Python']
print(sorted(a.union(b)))           # same result using a method
```

This returns a new set; `a` and `b` are unchanged. In the course example, union means “distinct topics taught anywhere across both courses.”

## 6. Intersection: common distinct items

The **intersection** `A & B` contains only items appearing in **both**:

```python
a = {"Python", "ML"}
b = {"ML", "GenAI"}
print(sorted(a & b))                # ['ML']
print(sorted(a.intersection(b)))    # ['ML']
```

**Worked trace:** `Python` is only in A; `ML` is in A and B; `GenAI` is only in B. Therefore the shared topic is `ML`.

## 7. Difference: items present on one side only

The **difference** `A - B` contains items in A that are **not** in B. Direction matters:

```python
a = {"Python", "ML"}
b = {"ML", "GenAI"}
print(sorted(a - b))                # ['Python']: only A
print(sorted(b - a))                # ['GenAI']: only B
print(sorted(a.difference(b)))      # ['Python']
```

Do not reverse the operands when mapping a capability gap: “missing in B compared with A” is `A - B`.

## 8. Symmetric difference: exclusive to either side

The **symmetric difference** `A ^ B` contains items in exactly **one** of the two sets, excluding common items:

```python
a = {"Python", "ML"}
b = {"ML", "GenAI"}
print(sorted(a ^ b))                # ['GenAI', 'Python']
print(sorted(a.symmetric_difference(b)))  # ['GenAI', 'Python']
```

**Comparison:**

| Question | Expression | Result for example |
|---|---|---|
| all distinct topics | `a \| b` | Python, ML, GenAI |
| topics in both | `a & b` | ML |
| topics only in A | `a - b` | Python |
| topics only in B | `b - a` | GenAI |
| topics in exactly one | `a ^ b` | Python, GenAI |

These are **set comparisons of names**, not proof that the content taught under a matching name is equivalent.

## 9. Subset and superset: containment of items

A **subset** contains no item absent from the other set: `a <= b`. A **superset** contains all the other's items: `a >= b`.

```python
required = {"Python", "ML"}
completed = {"Python", "ML", "GenAI"}
print(required <= completed)        # True: every required topic is present
print(completed >= required)        # True: completed covers required
print(completed <= required)        # False
print(required.issubset(completed)) # True
print(completed.issuperset(required))  # True
```

Every set is a subset and superset of **itself** using `<=` and `>=`. The empty set is a subset of every set, including another empty set. `<` and `>` test **proper** subset/superset, requiring inequality as well. A topic label present in `completed` is not, by itself, evidence of actual mastery; use assessment evidence later to make that claim.

## 10. Set comprehension: derive distinct items

A **set comprehension** creates a set from an iterable: `{expression for item in source}`. The expression can transform each item; duplicates in the resulting values collapse:

```python
raw_topics = [" ML ", "ML", "GenAI", "genai"]
cleaned = {topic.strip().lower() for topic in raw_topics}
print(sorted(cleaned))             # ['genai', 'ml']
print(raw_topics)                  # original list unchanged
```

`topic.strip().lower()` is the **comprehension expression**; `for topic in raw_topics` supplies one item at a time. If selection is needed, an optional `if` can filter:

```python
topics = ["ML", "GenAI", "NLP", "AI Ethics"]
ai_only = {topic for topic in topics if "AI" in topic}
print(sorted(ai_only))             # ['AI Ethics', 'GenAI']
```

This condition does simple substring matching, not subject classification. Normalisation such as `lower()` deliberately merges labels differing only in case; keep original labels if distinctions matter.

## 11. Guided lab: compare two course topic lists

Create `course_topic_sets.py` in `qai-path-lab/code-lab/`:

```python
# course_topic_sets.py
path_a = ["Python", "ML", "ML", "GenAI"]
path_b = ["ML", "NLP", "GenAI"]
a = set(path_a)
b = set(path_b)

print("A lesson order:", path_a)
print("A distinct topics:", sorted(a))
print("B distinct topics:", sorted(b))
print("All distinct:", sorted(a | b))
print("Shared:", sorted(a & b))
print("Only A:", sorted(a - b))
print("Only B:", sorted(b - a))
print("Exactly one:", sorted(a ^ b))
print("B contains ML and GenAI:", {"ML", "GenAI"} <= b)

a.add("RAG")
a.discard("Not present")
print("A after edit:", sorted(a))
print("Original ordered A still intact:", path_a)
```

Run from `code-lab` with `py .\course_topic_sets.py` in Windows PowerShell (or your verified `python` command), or `python3 course_topic_sets.py` in Bash/Zsh.

**Expected output:**

```text
A lesson order: ['Python', 'ML', 'ML', 'GenAI']
A distinct topics: ['GenAI', 'ML', 'Python']
B distinct topics: ['GenAI', 'ML', 'NLP']
All distinct: ['GenAI', 'ML', 'NLP', 'Python']
Shared: ['GenAI', 'ML']
Only A: ['Python']
Only B: ['NLP']
Exactly one: ['NLP', 'Python']
B contains ML and GenAI: True
A after edit: ['GenAI', 'ML', 'Python', 'RAG']
Original ordered A still intact: ['Python', 'ML', 'ML', 'GenAI']
```

**Trace:** converting `path_a` to `a` removes the second `ML` and does not preserve a learning order. `a & b` keeps `GenAI` and `ML`; `a - b` keeps `Python`. Adding `RAG` changes `a` but not `path_a`; these are separate collections.

**Controlled change 1:** replace `path_b` with `[]`. Union becomes A's distinct topics, intersection becomes empty, `a - b` becomes all of A, and `b - a` is empty. The subset test `{"ML", "GenAI"} <= b` becomes `False`. With `sorted(...)`, empty set results display as `[]`.

**Controlled change 2:** replace `path_b` with `["ml", "GenAI"]`. Lowercase `"ml"` is distinct from `"ML"`. Shared becomes only `['GenAI']`. Decide **before comparison** whether normalising both data sources to lowercase is appropriate; do not silently assume a case-insensitive match.

## 12. Choose a collection for the actual question

| Requirement | Suitable starting point | Why |
|---|---|---|
| keep lesson order and allow repeats | list | positions and duplicates matter |
| keep a small fixed-position result | tuple | positions cannot be reassigned |
| look up a course field by name | dictionary | `"title"` maps to one value |
| know distinct topics or compare topic groups | set | unique items and set operations |

**Shared project scenario:** a course catalog can use a dictionary for each course record, a list for its ordered lessons, tuples for certain fixed-position results, and sets to compare distinct topic codes. Choosing a set never proves two similarly named topics teach the same skill; that needs evidence beyond these collections.

## 13. Debugging: expected mistakes

| Symptom | Cause | Exact action |
|---|---|---|
| `{}` behaves like a dictionary | it *is* an empty dictionary | create an empty set with `set()` |
| `topics[0]` gives `TypeError` | set has no position 0 | keep a list for ordered access |
| different run shows a different printed set order | set display order is not a contract | use `sorted(topics)` for a defined display order |
| number of set items is smaller than number of source list items | duplicates collapsed | preserve the original list if occurrences matter |
| `"ml" in {"ML"}` is false | case differs | define and apply a consistent normalisation rule if suitable |
| `topics.remove("RAG")` raises `KeyError` | item absent | choose `discard` only if absence is acceptable |
| `topics = topics.add("RAG")` makes `topics` become `None` | `add` mutates and returns `None` | call `topics.add("RAG")` separately |
| adding a list raises `TypeError` | a list is unhashable | use a suitable hashable identifier or immutable item |
| `a - b` differs from `b - a` | difference is directional | say aloud which side's missing items you seek |
| “subset = mastered” is a wrong conclusion | item membership says only that labels match | require actual skill evidence before asserting mastery |

**Debug routine:** show the original list, `len` of the list, `len` of the set, and `sorted(set_value)` for inspection; verify item type and exact spelling; then state which mathematical set operation answers the real question. Avoid checking expected set content by printing raw set braces in a fixed order.

## 14. Independent micro-lab with complete solution

**Task:** from `learner_a = ["Python", "ML", "ML"]` and `learner_b = ["ML", "RAG"]`, print the shared topic, the topics exclusive to each, and whether the required topics `{"Python", "ML"}` are included in learner A's recorded labels. Preserve both input lists. Add `"GenAI"` only to the set derived from learner B and print B's original list plus its new distinct-topic display.

**Complete solution:**

```python
learner_a = ["Python", "ML", "ML"]
learner_b = ["ML", "RAG"]
a = set(learner_a)
b = set(learner_b)
print("Shared:", sorted(a & b))
print("Only A:", sorted(a - b))
print("Only B:", sorted(b - a))
print("Required labels recorded:", {"Python", "ML"} <= a)
b.add("GenAI")
print("B original:", learner_b)
print("B distinct after edit:", sorted(b))
```

**Expected output:**

```text
Shared: ['ML']
Only A: ['Python']
Only B: ['RAG']
Required labels recorded: True
B original: ['ML', 'RAG']
B distinct after edit: ['GenAI', 'ML', 'RAG']
```

**Why:** converting to a set removes duplicate `ML` in A. Intersection keeps `ML`, differences keep each exclusive topic, and the subset operation checks **recorded labels**. `b.add` changes only the set; `learner_b` remains an ordered two-item list. A label recorded for a learner is not proof the learner passed an assessment.

## 15. What to remember and retain

- Set = unique hashable items without positional order; nonempty literal `{"ML"}`; empty set `set()`.
- `add` adds; `remove` errors on absence; `discard` tolerates absence; `in` tests complete items.
- `a | b` union; `a & b` intersection; `a - b` directional difference; `a ^ b` symmetric difference.
- `a <= b` asks if a is a subset of b; `a >= b` asks if a is a superset of b.
- A set comprehension transforms or filters items, producing unique results.
- Retain `course_topic_sets.py`, both controlled-change outputs, and the collection-choice table with a sentence explaining why an ordered curriculum remains a list. These form the P0 node evidence and the final part of the QAI.01.15–01.19 collection-choice cluster.

**Next:** QAI.01.20 teaches `if`, `elif`, and `else` for deliberate choices such as “missing required record” versus “optional field absent.”

---

**Node contract (S90):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. All sixteen S86 set items are addressed through traced operations, runnable code, controlled changes, a solved exercise, and a collection-choice table. Learner evidence requires running and explaining the results.
