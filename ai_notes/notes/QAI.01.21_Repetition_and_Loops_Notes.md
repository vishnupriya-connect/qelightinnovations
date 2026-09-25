# QAI.01.21 — Repetition and Loops

> QAI.01.20 Conditional execution → **QAI.01.21 Repetition and loops** → QAI.01.22 Functions

## 1. Destination: validate a collection of learner questions

In QAI.01.20, you decided what to do with **one** learner question. A course application receives many questions. Copying the validation code for each input would make errors likely. A **loop** repeats a group of instructions for each relevant input or while a clear condition remains true.

At the end, you will extend `validation_and_loop_lab.py` to process several questions, record exactly which iterations ran, deliberately skip invalid text, stop a bounded preview, and diagnose an infinite-loop risk. This node establishes the mechanism; packaging the behaviour as a reusable function follows in QAI.01.22.

## 2. Loop, iteration, body, and variable

A **loop** is a construct that repeats code. One execution of its **loop body** is an **iteration**. A **loop variable** refers to the current item in a `for` loop:

```python
questions = ["What is AI?", "What is ML?"]
for question in questions:
    print("Question:", question)
```

```text
Question: What is AI?
Question: What is ML?
```

Read the line as “for each `question` in `questions`, run the indented body.” The body runs twice because there are two items. After the first iteration, the loop variable receives the second item. An empty list makes the body run **zero** times.

**Trace before execution:**

| Iteration | Current `question` | Printed result |
|---:|---|---|
| 1 | What is AI? | Question: What is AI? |
| 2 | What is ML? | Question: What is ML? |

Do not confuse “two items” with “two distinct values”: if the list contains a duplicate, both positions are visited.

## 3. Iterable and iterator: where the next item comes from

An **iterable** is a value from which Python can obtain items for iteration, such as a list, tuple, string, dictionary, or `range`. An **iterator** is an object that keeps track of progress through an iterable and supplies the next item when requested:

```python
topics = ["Python", "ML"]
progress = iter(topics)              # obtain an iterator
print(next(progress))                # Python
print(next(progress))                # ML
print(next(progress, "DONE"))        # DONE: exhausted
```

`iter(topics)` creates an iterator; `next(progress)` consumes its next item. Without a fallback, calling `next(progress)` after exhaustion raises `StopIteration`. A `for` loop requests successive items and ends naturally at exhaustion, without you managing `next` explicitly.

**Strings** provide characters, lists provide items, and **dictionaries** provide keys during default iteration:

```python
for letter in "AI":
    print("Letter:", letter)
for key in {"code": "QAI.01.21", "title": "Loops"}:
    print("Key:", key)
```

```text
Letter: A
Letter: I
Key: code
Key: title
```

Use `record.items()` when you need both dictionary key and value, as in QAI.01.18. A set is also iterable but offers no reliable positional order; never make lesson order depend on it.

## 4. `for` loop over a bounded collection

A **`for` loop** repeats over a given iterable. It is well suited to the questions already stored in a list:

```python
questions = [" Explain AI ", "  ", "Explain ML"]
for raw in questions:
    clean = " ".join(raw.split())
    if clean == "":
        print("SKIP: empty")
    else:
        print("READY:", clean)
```

```text
READY: Explain AI
SKIP: empty
READY: Explain ML
```

For this fixed list, the body executes **three times** even though one question is skipped by its branch. The program does not erase that item from `questions`. The length of a list gives the number of positions to be visited if you do not alter the list during iteration. Recall QAI.01.16: changing the same list's size while iterating can skip items.

## 5. `range()`: start, stop, step

`range()` is an iterable representing an integer progression. Its **start value** is included, its **stop value** is excluded, and its **step value** is the change between successive numbers:

```python
print(list(range(3)))                # [0, 1, 2]
print(list(range(1, 5)))             # [1, 2, 3, 4]
print(list(range(1, 7, 2)))          # [1, 3, 5]
print(list(range(5, 0, -2)))         # [5, 3, 1]
print(list(range(3, 3)))             # []
```

`range(stop)` starts at 0 and steps by 1. `range(start, stop)` steps by 1. `range(start, stop, step)` makes all three choices explicit. A negative step moves downward. `range(1, 5, -1)` gives no items: moving down from 1 will not reach an exclusive upper stop of 5. Step zero raises `ValueError`.

For a numeric count:

```python
for attempt in range(1, 4):
    print("Attempt", attempt)
```

```text
Attempt 1
Attempt 2
Attempt 3
```

Choose `for item in items` when you need the items themselves. Choose `range` when you need a defined numeric progression. Do not create indexes solely to access each list item if direct item iteration suffices.

## 6. `while` loop and loop condition

A **`while` loop** checks its **loop condition** before each iteration. It runs the body while that condition is truthy and stops as soon as it becomes false:

```python
attempt = 1
while attempt <= 3:
    print("Attempt:", attempt)
    attempt += 1
print("Next value:", attempt)
```

```text
Attempt: 1
Attempt: 2
Attempt: 3
Next value: 4
```

| Check | `attempt <= 3` | Print? | New `attempt` |
|---:|---|---|---:|
| 1 | `1 <= 3` → true | Attempt: 1 | 2 |
| 2 | `2 <= 3` → true | Attempt: 2 | 3 |
| 3 | `3 <= 3` → true | Attempt: 3 | 4 |
| 4 | `4 <= 3` → false | none; loop ends | 4 |

If the initial condition is false, `while` runs **zero** iterations. For example, starting with `attempt = 4` in this code prints only `Next value: 4`.

## 7. Infinite-loop risk: prove progress toward stopping

An **infinite loop** keeps repeating without a terminating state. This example would never change its condition; **do not run it**:

```python
# DO NOT RUN: illustration of the bug
# attempt = 1
# while attempt <= 3:
#     print(attempt)
#     # missing: attempt += 1
```

The condition remains true because `attempt` stays 1. The repair is to update it on each intended iteration, as in Section 6. A `for` over a finite list or finite `range` has an inherent end, whereas `while` relies on its condition becoming false or an intentional `break`.

**Before running a `while` loop, write down:** initial state → change in each body execution → condition that eventually becomes false. This catches many accidental infinite loops. An unbounded external stream may need a separate stop or timeout policy in later systems work.

## 8. `break`: stop a loop early

`break` exits the **nearest containing loop** immediately. Use it when a deliberate stopping event occurs:

```python
events = ["Python", "ML", "STOP", "GenAI"]
for event in events:
    if event == "STOP":
        break
    print("Study:", event)
print("Loop ended")
```

```text
Study: Python
Study: ML
Loop ended
```

`GenAI` is never visited. A stop marker in your input is an application rule, not a general Python rule. If you need to report why processing stopped, record that separately before the `break`.

## 9. `continue`: skip the rest of this iteration

`continue` moves to the loop's next iteration; it does **not** stop the entire loop:

```python
questions = ["What is AI?", "  ", "What is ML?"]
for raw in questions:
    clean = raw.strip()
    if clean == "":
        print("Skipped empty question")
        continue
    print("Ready:", clean)
```

```text
Ready: What is AI?
Skipped empty question
Ready: What is ML?
```

The final print is skipped for the blank item. **While-loop hazard:** if `continue` happens before the variable controlling the stopping condition is updated, the loop may never end. Update the progress variable before any possible `continue`:

```python
values = ["valid", "", "valid"]
position = 0
while position < len(values):
    current = values[position]
    position += 1                     # advance BEFORE continue
    if current == "":
        continue
    print("Accepted:", current)
```

```text
Accepted: valid
Accepted: valid
```

The position advances three times even though only two values are printed.

## 10. `pass`: a deliberate no-operation placeholder

`pass` does **nothing**; Python sometimes needs a statement where you have not written an action yet:

```python
course = "GenAI"
if course == "GenAI":
    pass                           # syntactically valid, no action
print("Still running")
```

```text
Still running
```

`pass` does not skip an iteration (`continue` does) and does not exit a loop (`break` does). It also does **not** implement validation. Do not leave a `pass` placeholder in an important branch and assume that case has been handled.

## 11. Nested loop: a loop inside a loop

A **nested loop** runs its inner loop anew for each outer item. For each lesson, display two review modes:

```python
lessons = ["Python", "ML"]
modes = ["notes", "practice"]
for lesson in lessons:
    for mode in modes:
        print(lesson, "->", mode)
```

```text
Python -> notes
Python -> practice
ML -> notes
ML -> practice
```

Two outer visits × two inner visits = four printed lines. An inner `break` exits the inner loop only; the outer loop can continue with its next lesson. Nested loops can do a lot of work: 1,000 lessons × 1,000 modes would mean 10 lakh inner visits, so choose them for a real need and inspect the size of both collections.

## 12. Guided implementation: extend the validation script

Replace the QAI.01.20 stage-1 content of `validation_and_loop_lab.py` with this **stage-2** version. It validates a series of raw questions, skips invalid ones, keeps accepted questions in input order, and shows a preview with a terminating `while` loop.

```python
# validation_and_loop_lab.py — stage 2
lesson = {"code": "QAI.01.21", "title": "Repetition and loops"}
raw_questions = ["  Explain GenAI  ", "   ", "A" * 81, "What is a prompt?"]
max_characters = 80
accepted = []

if "title" not in lesson:
    print("REJECT: missing course title")
else:
    position = 0
    for raw in raw_questions:
        position += 1
        clean = " ".join(raw.split())
        if clean == "":
            print(f"{position}: EMPTY -> skipped")
            continue
        if len(clean) > max_characters:
            print(f"{position}: TOO LONG -> skipped")
            continue
        accepted.append(clean)
        print(f"{position}: READY -> {clean}")

    print("Accepted count:", len(accepted))
    preview_position = 0
    while preview_position < len(accepted) and preview_position < 2:
        print(f"Preview {preview_position + 1}: {accepted[preview_position]}")
        preview_position += 1

print("Original question count:", len(raw_questions))
```

Run from `code-lab` with `py .\validation_and_loop_lab.py` in Windows PowerShell (or your verified `python` command), or `python3 validation_and_loop_lab.py` in Bash/Zsh.

**Expected output:**

```text
1: READY -> Explain GenAI
2: EMPTY -> skipped
3: TOO LONG -> skipped
4: READY -> What is a prompt?
Accepted count: 2
Preview 1: Explain GenAI
Preview 2: What is a prompt?
Original question count: 4
```

**Trace:** `position` advances on **every** question, even one skipped with `continue`. `accepted` receives the first and fourth cleaned questions. The `while` starts at accepted index 0 and stops after two previews because `preview_position` becomes 2. Its two conditions prevent both out-of-range indexing and showing more than two entries.

**Controlled change A:** use `raw_questions = []`. No `for` body executes; accepted count is 0; `while` does not execute; original count is 0. There are no `READY`, `EMPTY`, or `Preview` lines.

**Controlled change B:** keep the original questions and remove `preview_position += 1`. Do **not** run the resulting script without a limit or safe interruption: the preview condition remains true, repeating `Preview 1` indefinitely. Restore the increment and predict the four checks as the loop reaches its stop.

**Controlled change C:** change the record to `{"code": "QAI.01.21"}`. The script prints `REJECT: missing course title` and `Original question count: 4`. It processes no questions because the `for` belongs to the `else` branch. The gate checks **key presence only**; add a blank-title test if that is a requirement, as in QAI.01.20.

## 13. Diagnose common loop faults

| Observation | Mechanism | Fix |
|---|---|---|
| `range(1, 4)` gives 1, 2, 3 | stop is exclusive | adjust stop deliberately |
| `for` over `[]` prints nothing | iterable has no items | decide if empty input deserves an explicit message |
| `while` repeats indefinitely | condition never changes toward false | show state trace; update the control state on all paths |
| `continue` makes `while` loop forever | update was skipped | update before `continue` or restructure loop |
| one skipped input disappears from input count | count only accepted items | track total visits and accepted items separately |
| `break` stops too much or too little | it stops only nearest loop | mark nesting and identify which loop contains it |
| iteration over a set appears shuffled | set has no promised visit order | keep a list when order matters |
| duplicate list item is visited twice | every list position is visited | deduplicate only if that is the explicit task |
| removing from list inside `for` skips entries | indexes shift during iteration | build a separate filtered list |
| `pass` leaves an invalid case unhandled | `pass` is a no-op | replace placeholder with real action and a test |

**Debug routine:** write the initial values, the condition or next item, the body effect, and the next state in a trace table. Test zero, one, and several items, including one invalid item. Set an explicit progress bound before experimenting with uncertain `while` logic.

## 14. Independent micro-lab with full solution

**Task:** process `entries = ["Python", "", "ML", "STOP", "GenAI"]` in order. Ignore the empty entry, stop when `"STOP"` appears, and store only topics processed before the stop. Print one line for each accepted topic, one line for the skipped empty entry, then print the final list. Use `continue` and `break` intentionally.

**Full solution:**

```python
entries = ["Python", "", "ML", "STOP", "GenAI"]
processed = []
for entry in entries:
    if entry == "":
        print("SKIP: empty")
        continue
    if entry == "STOP":
        print("STOP: requested")
        break
    processed.append(entry)
    print("ACCEPT:", entry)
print("Processed:", processed)
```

**Expected output:**

```text
ACCEPT: Python
SKIP: empty
ACCEPT: ML
STOP: requested
Processed: ['Python', 'ML']
```

**Why:** the empty item executes the first branch and continues without adding a value. `STOP` executes the next branch and breaks, so `GenAI` is never visited. Change `entries` to `[]`: the body executes zero times and only `Processed: []` appears. Change the first item to `"STOP"`: the loop prints `STOP: requested` and `Processed: []`.

## 15. Remember and retain

- A loop repeats a body. Each visit is an iteration; the loop variable denotes the current `for` item.
- An iterable provides an iterator; a `for` loop ends when items are exhausted.
- `range(start, stop, step)` includes start and excludes stop; step must not be zero.
- A `while` loop requires a condition that eventually becomes false or an intentional exit.
- `break` ends the nearest loop; `continue` skips to its next iteration; `pass` does nothing.
- Nested loops multiply visits; predict the number and order before running.
- Keep the stage-2 `validation_and_loop_lab.py`, a trace of all four original visits, outputs for empty/missing-title cases, and an explanation of why the deliberately removed `while` increment would never terminate. Do not execute the broken unbounded variant.

**Next:** QAI.01.22 places repeated validation in functions with explicit inputs, outputs, and tests.

---

**Node contract (S90):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. All eighteen S86 loop topics are covered with traces, bounded runnable code, controlled edge cases, and a full solved micro-lab. Learner evidence requires running the safe examples and explaining the unsafe variation without running it.
