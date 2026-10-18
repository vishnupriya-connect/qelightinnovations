# QAI.01.13 — String Basics

> `QAI.01.12 Comparison and Boolean logic` → **`QAI.01.13 String basics`** → `QAI.01.14 String operations`

## 1. Destination: read exact parts of text

An AI application receives course titles, questions, file names, and model responses as text. Before cleaning or formatting them, you must know what a Python **string** contains and how to read a character or a portion safely. You will create strings, handle quotes and special characters, calculate length, index from either end, slice with a start/stop/step, and diagnose boundary mistakes.

The hands-on file in this lesson uses fictional course labels inside `qai-path-lab/code-lab/`. Full string transformations, formatting, search, and cleaning belong to `QAI.01.14`.

## 2. Character, string, literal, and empty string

A **character** is a unit of text such as `G`, `3`, or a space. A Python **string** (`str`) is an ordered sequence of text characters. A **string literal** is text written directly in source code between quotation marks:

```python
course = "GenAI"
section = "01"
empty = ""
print(course)          # GenAI
print(type(course))    # <class 'str'>
print(type(empty))     # <class 'str'>
```

`"01"` is text despite its digits. The **empty string** `""` contains no characters and still has type `str`. It differs from `None`, which means no value is available, and from a string containing a space `" "`, which contains one character.

**Mental model:** think of the string `"GenAI"` as five positions in order:

| Position from start | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Character | G | e | n | A | I |

The quotation marks tell Python where the literal starts and ends; they are **not** part of the five-character value.

## 3. Single and double quotation marks

A string literal may use a pair of **single quotes** or a pair of **double quotes**:

```python
print('GenAI')        # GenAI
print("GenAI")        # GenAI
print("It's ready")   # It's ready
print('Say "ready"')  # Say "ready"
```

The outer pair must match. When the text contains one kind of quote, the other kind can surround it. `'It's ready'` fails because the apostrophe appears to end the string too early. Choose suitable outer quotes or use an escape as explained next.

## 4. Escape character, newline, and tab

In an ordinary Python string literal, a backslash `\` introduces an **escape sequence**: source characters that represent a special character or a quote that would otherwise end the literal. The backslash is the **escape character** here.

| Source in a Python literal | Stored meaning | Visible result when printed |
|---|---|---|
 `\"` inside double quotes | literal double-quote character | `"` |
 `\'` inside single quotes | literal apostrophe | `'` |
 `\\` | one backslash | `\` |
 `\n` | newline character | move to next line |
 `\t` | tab character | horizontal tab spacing |

```python
print("She said \"AI\".")     # She said "AI".
print('It\'s ready.')       # It's ready.
print("First\nSecond")      # two displayed lines
print("Field\tValue")       # one line with a tab between words
```

The **newline character** separates lines *within one string*. The **tab character** represents tab spacing; its visible width depends on where the text is displayed. A Windows-style path in a Python literal also needs thought: `"C:\\notes"` stores a single backslash, whereas `"C:\notes"` contains `\n` and does not mean the intended file path. You will learn path-handling tools later; for now recognise the literal hazard rather than blindly replacing backslashes.

**Important:** some strings contain actual line breaks received from a file or user; `\n` is a way to *write* a newline within a Python literal. A printed string is not the same display as its quoted source.

## 5. String length with `len()`

**String length** is the count of Python string positions. `len(text)` reports it:

```python
print(len("GenAI"))    # 5
print(len(""))         # 0
print(len(" "))        # 1
print(len("A\nB"))     # 3: A, newline, B
```

Quotation marks and the backslash spelling in source are not extra characters in the value: `"A\nB"` contains the letter A, one newline character, and the letter B. A **space** is a character too.

**Limit of the mental model:** for everyday simple text, think of the positions as characters. Some visibly single Unicode symbols can use multiple Python string positions; Python's length is not always the count of what a human perceives as one written symbol, and it is not the number of AI model tokens. Later text-processing nodes treat that distinction explicitly. The indexing and slicing calculations in this lesson use simple letters, digits, spaces, newlines, and tabs so the result is unambiguous.

## 6. String index: read one position

An **index** is a numbered position. Python starts at zero. A **positive index** counts from the beginning; a **negative index** counts back from the end:

```python
course = "GenAI"
print(course[0])   # G: first
print(course[2])   # n: third
print(course[4])   # I: fifth
print(course[-1])  # I: last
print(course[-2])  # A: second from end
print(course[-5])  # G: first, counted backward
```

| Character | G | e | n | A | I |
|---|---:|---:|---:|---:|---:|
| Positive index | 0 | 1 | 2 | 3 | 4 |
| Negative index | -5 | -4 | -3 | -2 | -1 |

For a five-position string, valid positive indexes are 0 through 4; valid negative indexes are -5 through -1. `course[5]` or `course[-6]` raises `IndexError`. An empty string has **no valid single-character index**, so `""[0]` also raises `IndexError`.

Indexing produces a one-character string; it does not modify the original. Strings are immutable, as introduced in `QAI.01.08`.

## 7. String slice: read a range of positions

A **slice** selects a portion of a string. Its general form is `text[start:stop:step]`:

- **slice start:** where selection begins, inclusive;
- **slice stop:** where selection ends, **exclusive**; the character at that index is not included;
- **slice step:** how far to move between selected positions.

Start with an omitted step, which defaults to 1:

```python
course = "GenAI"
print(course[1:4])  # enA: indexes 1, 2, 3; stop 4 excluded
print(course[0:3])  # Gen
print(course[:3])   # Gen: omitted start means from beginning
print(course[3:])   # AI: omitted stop means through end
print(course[:])    # GenAI: full sequence of characters
```

**Worked trace of `course[1:4]`:** start at 1 → e; move to 2 → n; move to 3 → A; stop before 4 → no I. Result `"enA"`. An omitted start or stop uses the appropriate end for the direction of the slice.

### Negative start or stop

```python
course = "GenAI"
print(course[-2:])    # AI: last two characters
print(course[-4:-1])  # enA: from e through A, excluding final I
```

Negative positions are still positions of this same string. `-1` identifies the last character when **indexing**; as a slice stop with a positive step, `-1` excludes that last character.

### Step and reverse

```python
course = "GenAI"
print(course[::2])    # GnI: positions 0, 2, 4
print(course[1:5:2])  # eA: positions 1, 3
print(course[::-1])   # IAneG: reverse order
```

The `step` is 2 in the first two examples: skip every other position. A step of -1 moves backward, so omitting both bounds in `course[::-1]` traverses the whole string in reverse. **Step zero is invalid**: `course[::0]` raises `ValueError`.

### Indexing and slicing fail differently

```python
course = "GenAI"
print(course[:100])   # GenAI: slice safely stops at available end
print(course[100:])   # empty string
# print(course[100])  # IndexError if executed
```

A slice beyond an available boundary normally returns the available part or an empty string; a single out-of-range **index** raises an error. Do not infer from a safe slice that the requested positions actually existed. If a particular length is required, check `len(course)` before relying on it.

## 8. Guided lab: inspect a course label and a question

Create `string_basics.py` in `qai-path-lab/code-lab/`:

```python
# Fictional text used only to practise positions.
course = "GenAI"
question = "Explain GenAI"

print("Course length:", len(course))
print("First:", course[0])
print("Last:", course[-1])
print("First three:", course[:3])
print("Last two:", course[-2:])
print("Every second:", course[::2])
print("Question length:", len(question))
print("Question action:", question[:7])
print("Question subject:", question[8:])
```

**Predict before running:** `"Explain"` has seven positions, then one space, then `"GenAI"` has five. The total question length is 13; its subject begins at index 8.

```text
Course length: 5
First: G
Last: I
First three: Gen
Last two: AI
Every second: GnI
Question length: 13
Question action: Explain
Question subject: GenAI
```

Run from `code-lab` with `py .\string_basics.py` in Windows PowerShell, or `python3 string_basics.py` in Bash/Zsh. Use `python` if that was your verified Windows interpreter. Compare **each** observed line with the prediction.

**Controlled variation:** replace only `question = "Explain GenAI"` with `question = "Explore GenAI"`. The title part still begins at index 8 because `Explore` also has seven characters. The question length remains 13; the action becomes `Explore`. Then replace with `"Learn GenAI"`: the fixed slice positions are now wrong, even though the code still runs. `Learn` has five characters and the subject starts at index 6. This is a **silent design error** caused by assuming every action word has the same length. Dynamic separation of words is taught under string operations in `QAI.01.14`.

## 9. Debug common boundary and escape mistakes

| Symptom | Cause | Exact check and repair |
|---|---|---|
 `IndexError` from `course[5]` | five-character string ends at index 4 | inspect `len(course)`; use `course[-1]` for last character |
 `IndexError` from `""[0]` | empty string has no position 0 | establish what to do with empty input before indexing |
 `"GenAI"[1:4]` gives `"enA"` rather than `"enAI"` | stop 4 is exclusive | use `[1:5]` or `[1:]` |
 `"GenAI"[::0]` gives `ValueError` | step cannot be zero | choose a nonzero step |
 `"C:\notes"` appears split over lines | `\n` interpreted as a newline in the literal | write `"C:\\notes"` for one literal backslash |
 a renamed question produces wrong subject | fixed index assumed a fixed prefix length | check actual length; use appropriate text parsing later |
 `course[0] = "g"` gives `TypeError` | strings do not support in-place character replacement | build a new string in `QAI.01.14` |

**Debug sequence:** show the source literal and the actual value with `repr(text)` when escapes may be involved; inspect `len(text)`; mark each index from 0; label the slice start, exclusive stop, and step; predict output; rerun. `repr` makes special characters visible as escape spellings in many simple cases.

## 10. Independent exercise with full solution

**Task:** a fictional lesson code is `"QAI.01.13"`. Create `lesson_code_parts.py` that prints the full string length, the first three characters, the two digits after `QAI.`, the final two digits, and the final two digits in reverse order. Predict the result before running. Then safely demonstrate an oversize slice and an invalid single index on a *separate disposable test*.

**Worked solution:**

```python
code = "QAI.01.13"
print("Length:", len(code))
print("Domain:", code[:3])
print("Section:", code[4:6])
print("Node:", code[-2:])
print("Reversed node:", code[-2:][::-1])
print("Large slice:", code[:100])
```

**Expected output:**

```text
Length: 9
Domain: QAI
Section: 01
Node: 13
Reversed node: 31
Large slice: QAI.01.13
```

**Trace:** `QAI` occupies indexes 0–2; dot at 3; `01` at 4–5; dot at 6; `13` at 7–8. `code[4:6]` includes 4 and 5, excludes 6. `code[-2:]` picks 7–8. Reversing only this two-character slice yields `31`. An oversize slice stops at the actual end.

**Safe error test:** in `lesson_code_error.py` put `print("QAI.01.13"[9])` and run. The string has length 9 but its last valid positive index is 8, so the expected result is `IndexError`. Repair with `[-1]` for the last character or `[8]` when the length is known. Keep the good solution file unchanged.

## 11. Evidence and technical recall

Keep `string_basics.py`, `lesson_code_parts.py`, and a short `string_index_trace.md` with a drawn 0-to-4 index row for `GenAI`, the predicted and observed output of both programs, the two changed-question results, and one repaired `IndexError` or escape mistake. This satisfies the hands-on, test, and debug requirements for this node.

**Remember:** quotes delimit a string literal; escapes such as `\n` represent special characters; `len()` counts string positions; indexing starts at zero and negative indexes count from the end; a slice includes its start and excludes its stop; a step controls spacing/direction; an invalid index raises `IndexError`, while an oversize slice usually returns available text.

## 12. Next connection

`QAI.01.14 — String operations` uses these foundations to join, search, clean, replace, and format text while preserving the original string when required.
