# QAI.01.14 — String Operations

> QAI.01.13 String basics → **QAI.01.14 String operations** → QAI.01.15 Sequence basics

## 1. Destination: turn received text into useful text

A learner types `"  Explain   GenAI  "`. A course assistant needs a clean question to show, store, or pass to a later AI component. In this lesson you will combine, search, compare, format, and clean text using ordinary Python strings.

**What you will produce:** `text_cleaning_basics.py`, a runnable script that prints the original input, the cleaned input, and a formatted assistant request. This is basic text handling; deciding linguistic meaning and model tokenisation come later.

## 2. Joining and repeating strings with operators

**Concatenation** joins strings end to end with `+`. You must supply the separator you actually want:

```python
topic = "GenAI"
action = "Explain"
question = action + " " + topic
print(question)             # Explain GenAI
print(action + topic)        # ExplainGenAI
```

**String repetition** with `*` repeats the entire string a chosen number of times:

```python
print("AI" * 3)              # AIAIAI
print("AI " * 3)             # AI AI AI 
print("-" * 8)               # --------
print("AI" * 0)              # empty string
```

`"AI " * 3` has a trailing space. Repetition is useful for small display elements, not for multiplying numeric values: `"3" * 2` gives `"33"`, whereas `3 * 2` gives `6`. `"AI" + 3` raises `TypeError`; convert deliberately only when the application needs text, such as `"AI" + str(3)`.

## 3. Substrings, membership, and comparison

A **substring** is a continuous piece of text inside a larger string. `"AI"` is a substring of `"GenAI"`. **Membership** asks whether that piece occurs anywhere:

```python
title = "GenAI Basics"
print("GenAI" in title)      # True
print("genai" in title)      # False
print("ML" not in title)     # True
print("" in title)           # True
```

Membership is **case-sensitive**: uppercase `G` and lowercase `g` are different. The empty string is found in every string, so validate a search term before treating membership as evidence of a meaningful match. For ordinary whole-word detection, `"AI" in "TRAIL"` is also `True`: substring matching is not word matching.

**String comparison** uses `==` and `!=` to ask whether complete strings are equal or different. `<` and `>` compare text in lexicographic order using the underlying character order; they do **not** measure meaning or course difficulty:

```python
print("GenAI" == "genai")    # False
print("GenAI" != "genai")    # True
print("AI" < "ML")           # True
print("10" < "2")            # True: text comparison, not number comparison
```

To compare a numeric value supplied as text, first validate and convert it at the appropriate boundary, as practised in QAI.01.08. Do not assume that text ordering is natural-language or numerical sorting.

## 4. Put values into messages: placeholders, interpolation, f-strings

A **placeholder** is a marked position to be filled with a value. **String interpolation** means producing a string by inserting values at those positions. An **f-string** is a Python string literal with `f` before its opening quote; an expression inside `{...}` is evaluated and displayed:

```python
student = "Asha"
lesson = "GenAI"
prompt = f"Explain {lesson} to {student}."
print(prompt)                # Explain GenAI to Asha.
```

`{lesson}` and `{student}` are placeholders in this f-string. `f"..."` creates a new string; it does not change either variable. Another **formatting** option is `.format()`, where `{}` placeholders are filled in order:

```python
message = "Explain {} to {}.".format("GenAI", "Asha")
print(message)               # Explain GenAI to Asha.
```

For a value that should appear with a fixed number of decimal places:

```python
score = 0.875
print(f"Evaluation score: {score:.2f}")  # Evaluation score: 0.88
```

Formatting controls display; it does not make a measurement accurate or change the stored value of `score`. When inserting untrusted text into an AI prompt, formatting alone does not make that text safe or authoritative: the AI application's later input-trust rules still apply.

## 5. A string method returns a result

A **method** is an operation called on a value with the form `value.method(...)`. For string operations, the input string does not change in place: use the returned string if you want the transformation.

```python
raw = "  GenAI  "
raw.strip()                  # calculates "GenAI" and discards the result
print(repr(raw))             # '  GenAI  '
clean = raw.strip()
print(repr(clean))           # 'GenAI'
```

**Mental model:** `raw` and `clean` refer to different string values. An assignment such as `raw = raw.strip()` makes the *name* `raw` refer to the new value; it has not modified the old string. `repr(...)` displays quotes and hidden characters in a way useful for these examples.

## 6. Trim, change case, replace

**Trim whitespace** from both ends with `.strip()`. `.lstrip()` trims only the beginning and `.rstrip()` only the end. Without an argument, these remove surrounding whitespace such as spaces, tabs, and newlines; they do not remove spaces *between* words:

```python
raw = "  Explain   GenAI  \n"
print(repr(raw.strip()))     # 'Explain   GenAI'
print(repr(raw.lstrip()))    # 'Explain   GenAI  \n'
print(repr(raw.rstrip()))    # '  Explain   GenAI'
```

**Uppercase** and **lowercase conversion** create new strings:

```python
label = "GenAI"
print(label.upper())         # GENAI
print(label.lower())         # genai
print(label)                 # GenAI
print("  GenAI ".strip().lower())  # genai
```

Use `.replace(old, new)` to create text with every matching occurrence replaced:

```python
title = "Intro to AI and AI tools"
print(title.replace("AI", "GenAI"))  # Intro to GenAI and GenAI tools
print(title)                        # Intro to AI and AI tools
print("GenAI".replace("ML", "DL"))    # GenAI: no match, unchanged content
```

Replacement is literal and case-sensitive. `"AI"` inside a larger word would also be replaced. Check the intended scope before changing externally supplied text. `.strip("!")` removes matching edge characters, not a fixed substring; for a fixed prefix/suffix use a deliberate check and later `removeprefix`/`removesuffix` when appropriate.

## 7. Split into parts; join parts into text

`.split()` separates on runs of whitespace and returns an ordered **list** of parts. A list is a Python collection introduced fully in QAI.01.16. You can read its elements by index, as with the ordered strings from QAI.01.13:

```python
raw = "  Explain   GenAI \n simply  "
parts = raw.split()
print(parts)                 # ['Explain', 'GenAI', 'simply']
print(parts[0])              # Explain
```

`.split(" ")` has a different rule: it separates at each *literal space*, so repeated spaces produce empty parts; tabs and newlines are not treated as that space. Use plain `.split()` when you intend whitespace-separated words:

```python
print("A  B".split())        # ['A', 'B']
print("A  B".split(" "))     # ['A', '', 'B']
print("A,B".split(","))      # ['A', 'B']: explicit comma separator
```

`separator.join(parts)` produces one string with that separator **between** the strings. The list must contain strings:

```python
parts = ["Explain", "GenAI", "simply"]
print(" ".join(parts))       # Explain GenAI simply
print(" | ".join(parts))     # Explain | GenAI | simply
print("".join(parts))        # ExplainGenAIsimply
```

Together, `" ".join(raw.split())` trims surrounding whitespace **and** collapses internal whitespace to one ordinary space. This is often useful for a simple display label, but it intentionally changes line breaks and spacing. Do not apply it automatically to code blocks, addresses, transcripts needing timestamps, or text where exact spacing matters. Splitting on whitespace does not understand grammar or AI model tokens.

## 8. Check the beginning, end, and position of text

`.startswith(prefix)` and `.endswith(suffix)` answer whether a string begins or ends with exact text:

```python
name = "lesson_notes.md"
print(name.startswith("lesson"))   # True
print(name.endswith(".md"))        # True
print(name.endswith(".pdf"))       # False
```

A **character search** with `.find(substring)` returns the index of the first match, or `-1` if it cannot find one:

```python
question = "Explain GenAI"
print(question.find("GenAI"))      # 8
print(question.find("ML"))         # -1
print(question.find("a"))          # 4: first lowercase 'a' in Explain
```

Index 0 is a valid find result. **Wrong check:** `if question.find("Explain"):` treats 0 as false and -1 as true; branches are taught later, but the rule matters now. Use `"Explain" in question` when only existence matters, or explicitly compare the result with `-1` when you need the position. Prefix/suffix and find are case-sensitive. A filename suffix check is only a text check; it does not prove that a file actually exists or that its contents match the suffix.

## 9. Guided implementation: clean a small course question

Create `text_cleaning_basics.py` in your `qai-path-lab/code-lab/` folder. Replace the sample `raw_question` with a sentence typed by a learner when practising. This script uses only operations introduced so far.

```python
# text_cleaning_basics.py
# Fictional sample. Do not paste private student questions into public demos.
raw_question = "  Explain   GenAI  to me.  "
course = "GenAI"

clean_question = " ".join(raw_question.split())
display_name = course.upper()
request = f"Course: {display_name} | Question: {clean_question}"

print("Raw:", repr(raw_question))
print("Clean:", repr(clean_question))
print("Raw length:", len(raw_question))
print("Clean length:", len(clean_question))
print("Contains course title:", course.lower() in clean_question.lower())
print("Begins with Explain:", clean_question.startswith("Explain"))
print("First period position:", clean_question.find("."))
print("Request:", request)
print("Original unchanged:", repr(raw_question))
```

Run from the `code-lab` folder:

- Windows PowerShell: `py .\text_cleaning_basics.py` (or the verified `python` command).
- Bash/Zsh: `python3 text_cleaning_basics.py`.

**Expected output:**

```text
Raw: '  Explain   GenAI  to me.  '
Clean: 'Explain GenAI to me.'
Raw length: 27
Clean length: 20
Contains course title: True
Begins with Explain: True
First period position: 19
Request: Course: GENAI | Question: Explain GenAI to me.
Original unchanged: '  Explain   GenAI  to me.  '
```

**Trace:** `.split()` produces `['Explain', 'GenAI', 'to', 'me.']`; `" ".join(...)` puts one space between adjacent parts; the old value remains in `raw_question`. If a learner typed only spaces, `.split()` gives an empty list and `" ".join(...)` gives an empty string. That does **not** mean a valid question was supplied. Handling that input deliberately with a conditional is practised in QAI.01.20.

**Controlled change 1:** change the input to `"  What is   ML? "`. Expected clean text: `'What is ML?'`; `Contains course title` becomes `False`; `Begins with Explain` becomes `False`; `First period position` becomes `-1`.

**Controlled change 2:** change the input to `"GenAI\nexamples"`. Expected clean text: `'GenAI examples'`. Notice that the newline was intentionally removed: use this transformation only when the content is meant to be a one-line question.

## 10. Diagnose and fix typical mistakes

| Observed issue | Reason | Exact repair |
|---|---|---|
| `raw.strip()` appears to do nothing | result was discarded | assign `clean = raw.strip()` and inspect `repr(clean)` |
| `"GenAI"` is absent from `"genai"` | case-sensitive search | use `course.lower() in question.lower()` if simple case-insensitive matching is wanted |
| `"A  B".split(" ")` contains `''` | literal separator leaves an empty part | use `.split()` to separate on runs of whitespace |
| `"AI" in "TRAIL"` is `True` | substring is not a whole word | choose a word-aware rule later; avoid asserting whole-word detection |
| `text.find("x")` gives `-1` | no match, not an index to read | check `position != -1` before indexing |
| `text.find("x")` gives `0` | match at start, a valid index | do not use the integer alone as a truth test |
| `"  ".split()` produces no parts | input contains no non-whitespace text | treat as missing question in a later validation step |
| Replacing `"AI"` changes more places than intended | `.replace` operates on all matching substrings by default | check match scope or specify a carefully chosen count/operation |
| “Cleaned” answer loses paragraphs | `split/join` collapses whitespace, including newlines | preserve raw formatting when paragraphs matter |

**Debug routine:** inspect original and transformed values with `repr`, state the exact expected string, compare with the actual string, find the first difference, then adjust **one** operation at a time. Never replace original user text permanently without a clear requirement.

## 11. Independent micro-lab, followed by complete solution

**Task:** for `raw = "  Learn   Python  for GenAI  "`, produce `"Learn Python for GenAI"` without changing `raw`. Display the cleaned phrase in `"Lesson: <cleaned>"`; check whether it ends in `"GenAI"`; find the first `"Python"` position; make a lowercase comparison against `"learn python for genai"`. Record exact outputs.

**Predict:** the cleaned text has one space between words. `Python` begins at index 6, because `Learn` has five characters followed by one space. The suffix check and lowercase comparison are `True`.

**Full solution:**

```python
raw = "  Learn   Python  for GenAI  "
cleaned = " ".join(raw.split())
print(repr(raw))
print(repr(cleaned))
print(f"Lesson: {cleaned}")
print(cleaned.endswith("GenAI"))
print(cleaned.find("Python"))
print(cleaned.lower() == "learn python for genai")
```

**Expected output:**

```text
'  Learn   Python  for GenAI  '
'Learn Python for GenAI'
Lesson: Learn Python for GenAI
True
6
True
```

**Additional boundary check:** change `raw` to `"   "`. `cleaned` becomes `""`; `endswith("GenAI")` becomes `False`; `find("Python")` becomes `-1`; and the lowercase comparison becomes `False`. In an application, this must be rejected as an empty question in the later input-validation lesson, rather than sent to a model.

## 12. What to remember and what to retain as evidence

- `+` joins strings; `*` repeats; `in` finds a substring; comparisons examine text, not meaning.
- f-strings insert values into placeholders; `.format()` is another formatting option.
- `strip`, `lower`, `upper`, `replace`, `split`, `join`, `startswith`, `endswith`, and `find` each have a different purpose.
- A string operation creates a result; keep that result if needed. The original string is not modified.
- Plain `split()` and literal `split(" ")` do not behave the same for repeated spaces.
- `find` returns `0` for a match at the beginning and `-1` for no match.
- Keep `text_cleaning_basics.py`, its expected-versus-actual output, and the micro-lab result. Explain one input for which collapsing whitespace would be wrong (for example, a multiline answer).

**Next connection:** splitting creates a list of parts. QAI.01.15 introduces sequences; QAI.01.16 shows how to manage those lists deliberately.

---

**Node contract (S89):** `C | L3 | H1–H3 | E2–E4 | A1–A3 | P0`. This note supplies explanations, runnable guided code, controlled changes, diagnostics, a solved micro-lab, and expected output. Learner mastery requires running and modifying the script and recording the observed results.
