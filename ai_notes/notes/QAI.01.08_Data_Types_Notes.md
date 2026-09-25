# QAI.01.08 — Data Types

> `QAI.01.07 Values and variables` → **`QAI.01.08 Data types`** → `QAI.01.09 Objects, references, aliases, and copies`

## 1. Destination: use values according to their meaning

A course assistant keeps a document count, a course title, a yes/no readiness result, and sometimes a missing answer. All are **values**. A **data type** tells Python what kind of value it has and which operations make sense. At the end of this node you can inspect types, convert suitable user input, diagnose invalid input, distinguish `None` from `False` and zero, and demonstrate mutation versus reassignment.

Work in the disposable `qai-path-lab/code-lab/` folder. Terms are introduced before their code examples. Python references and copies receive their own detailed treatment in `QAI.01.09`.

## 2. First observation: printing does not show the type

```python
count = 2
entered_count = "2"
print(count)            # 2
print(entered_count)    # 2
print(type(count))      # <class 'int'>
print(type(entered_count))  # <class 'str'>
```

The displayed values look alike, but `2` is an **integer** for arithmetic while `"2"` is a **string** of text. **Type checking** means asking Python what type a value has; `type(value)` does that. Read `<class 'int'>` as “Python reports type `int`.” The full meaning of Python classes comes later.

| Written value | Type | Typical course assistant role |
|---|---|---|
| `2` | `int` | count of documents |
| `2.5` | `float` | hours of study |
| `"GenAI"` | `str` | course title |
| `True` | `bool` | result of a yes/no check |
| `None` | `NoneType` | an answer has not been supplied |

A variable is a name referring to a value; its name does not permanently determine its type. `item = 2` followed by `item = "two"` makes `item` refer to a different kind of value. Avoid that kind of change when a clearer new name would prevent confusion.

## 3. Numeric values: integer and float

An **integer** (`int`) is a whole number: `-1`, `0`, `3`. A **floating-point number** (`float`) can represent numbers with fractional parts: `2.5`, `0.5`; `2.0` is also a float.

```python
documents = 2
added = 3
print(documents + added)  # 5
print(type(documents))    # <class 'int'>
print(type(2.0))          # <class 'float'>
print(type(2 / 1))        # <class 'float'>
```

A **numeric value** is one used as a number for arithmetic. Both `int` and `float` are numeric here. Text that merely looks numeric is not a numeric value:

```python
print(2 + 3)      # 5: arithmetic
print("2" + "3")  # 23: text joined together
```

An identifier like `"003"` should often remain a string: converting it to integer 3 would discard meaningful leading zeroes. Decide what the field *means* before converting it.

**Precision boundary:** floats commonly store approximate representations of decimal fractions. On ordinary Python installations, `0.1 + 0.2` displays `0.30000000000000004`. Do not use that expression as proof that every decimal is exact, nor assume a float alone is suitable for exact money calculations. [Python's floating-point tutorial](https://docs.python.org/3/tutorial/floatingpoint.html) explains why.

## 4. Text and strings

A **text value** in our Python examples is a **string** (`str`): characters between quotes. The empty string `""` is still a string, just with no characters.

```python
course_name = "GenAI"
learner_code = "003"
print(course_name)          # GenAI
print(learner_code)         # 003
print(type(learner_code))   # <class 'str'>
print("Gen" + "AI")         # GenAI
```

The `+` sign combines two strings, but `"5" + 2` raises `TypeError` because it tries to combine text and an integer without choosing an interpretation. `TypeError` means an operation was attempted on incompatible kinds of values.

## 5. Boolean: actual yes/no, not the word “False”

A **Boolean value** (`bool`) is `True` or `False`, with capital first letters. It is useful for a yes/no result:

```python
has_documents = True
print(type(has_documents))  # <class 'bool'>
print(type("False"))        # <class 'str'>
print(bool("False"))        # True
print(bool(""))             # False
```

**Truthiness** means how Python interprets a value in a yes/no context. `bool()` checks truthiness; it does not read the English meaning of the text. Nonempty `"False"` is therefore truthy. Never parse a person's typed “no” by simply calling `bool(input(...))`. Explicit yes/no interpretation comes with input validation later.

## 6. Null value: `None` is distinct from zero and false

`None` is Python's **null value**: a special value indicating that a value is absent or not yet available. Its type is `NoneType`.

```python
retrieved_answer = None
print(retrieved_answer)         # None
print(type(retrieved_answer))   # <class 'NoneType'>
print(retrieved_answer is None) # True
```

| Value | What it could mean in a course assistant |
|---|---|
| `None` | no answer was provided or generated |
| `0` | a measured count is zero |
| `False` | a yes/no check returned no |
| `""` | a string was provided but has no characters |
| `"None"` | the four-letter text, not the null value |

Use `is None` to check the special absent value. `is` tests identity; `QAI.01.09` explains that broader concept. For now remember: a missing answer, a failed check, an empty string, and zero matches are different situations, even though all may be treated as false in some conditions.

## 7. Type conversion: interpret only suitable input

**Type conversion** produces a value of another type when a sensible interpretation exists:

```python
print(int("5") + 2)      # 7
print(float("2.5") + 1)  # 3.5
print(str(5) + " docs")  # 5 docs
```

Converting does not automatically alter a previously assigned name:

```python
entered = "5"
number = int(entered)
print(type(entered))    # <class 'str'>
print(type(number))     # <class 'int'>
```

`input()` always returns text in this example, even if the person types digits:

```python
entered = input("New documents: ")
print(type(entered))  # <class 'str'>
number = int(entered)
print(type(number))   # <class 'int'> for input 3
```

| Attempt | Result | Explanation |
|---|---|---|
| `int("3")` | integer 3 | whole-number text |
| `float("2.5")` | float 2.5 | decimal-form text |
| `str(3)` | text `"3"` | number represented as text |
| `int("three")` | `ValueError` | cannot interpret that word as an integer |
| `int("2.5")` | `ValueError` | decimal-form string is not integer-form text |
| `int(2.9)` | integer 2 | drops the fractional part; does **not** round |

`ValueError` means a conversion was given an unsuitable value. An invalid answer should not quietly become zero: zero is a real, meaningful count.

## 8. Guided lab: count documents from typed input

Create `types_and_conversion.py` in `code-lab`. First **predict** outputs for inputs `3` and `three`, then run both:

```python
# Fictional practice values. No files or APIs are used.
course_name = "GenAI"
existing_documents = 2
entered_new = input("New document count: ")

print("Course:", course_name)
print("Input type:", type(entered_new))

try:
    new_documents = int(entered_new)
except ValueError:
    print("Enter a whole number, such as 3.")
else:
    total_documents = existing_documents + new_documents
    print("Total documents:", total_documents)
    print("Total type:", type(total_documents))
```

`try` means “attempt the conversion.” An `except ValueError` block handles a conversion failure; the `else` block runs only if conversion succeeded. Four spaces show which instructions belong to each block. Full control flow is taught later; this small example prevents an invalid count from being silently accepted.

From `code-lab`, run `py .\types_and_conversion.py` in Windows PowerShell, using `python` instead of `py` if that was the interpreter verified in `QAI.01.06`. On macOS/Linux run `python3 types_and_conversion.py`.

**Expected, input `3`:**

```text
New document count: 3
Course: GenAI
Input type: <class 'str'>
Total documents: 5
Total type: <class 'int'>
```

**Expected, input `three`:**

```text
New document count: three
Course: GenAI
Input type: <class 'str'>
Enter a whole number, such as 3.
```

No total is printed on the invalid run. **Controlled variation:** change only `existing_documents = 2` to `existing_documents = 4` and type `3`. Predicted total: 7, still an `int`. Restore 2 after observing the result.

## 9. Mutable and immutable: can the value change in place?

**Immutable** means an existing value cannot be changed in place. Strings, integers, and floats have this property in Python:

```python
course = "Gen"
course = course + "AI"
print(course)  # GenAI
```

The old string `"Gen"` was not edited; Python formed a new string and **reassigned the name**. Likewise `count = count + 1` associates the name with a new numerical result.

**Mutable** means an existing value can change in place. A **list** is an ordered group of values written within square brackets; full list operations come later:

```python
titles = ["intro"]
titles.append("rules")
print(titles)  # ['intro', 'rules']
```

`append` changed the list itself. This is different from assigning a new value to `titles`. The important consequences when two names refer to the same mutable list come in `QAI.01.09`.

## 10. Diagnose the type and intended meaning

| Attempt | What happens | Repair |
|---|---|---|
| `"5" + 2` | `TypeError` | numerical 7: `int("5") + 2`; textual `"52"`: `"5" + str(2)` |
| `int("abc")` | `ValueError` | ask for valid whole-number text |
| `bool("False")` | `True` | explicitly parse intended yes/no words |
| `None + 2` | `TypeError` | check `is None`; decide whether to stop or use justified default |
| `int(2.9)` | `2` | conversion truncates; do not assume rounding |

Debug in this order: print the actual value with `repr(value)` (which shows quotes around strings), inspect `type(value)`, state what the value should mean, convert only when justified, and test a good input plus a bad input.

## 11. Independent exercise with complete solution

**Task:** a fictional lesson already has 2 hours. Ask for extra hours, accept whole-number text, and show the total. If conversion fails, display guidance instead of a false total. Show that the user input was initially a string. Test `3` and `two`.

**Solution — save as `lesson_duration.py`:**

```python
existing_hours = 2
entered_extra = input("Extra hours: ")
print("Input is text:", type(entered_extra) is str)

try:
    extra_hours = int(entered_extra)
except ValueError:
    print("Use a whole number, for example 3.")
else:
    total_hours = existing_hours + extra_hours
    print("Total hours:", total_hours)
```

For input `3` the type check prints `True` and the total prints `5`. For input `two` the type check still prints `True`; the explanatory message prints and there is no total. `type(entered_extra) is str` checks its exact type; more general object/type relationships follow later.

**Solved classification:** `False` has type `bool`; `"False"` has `str`; `0` has `int`; `0.0` has `float`; `None` has `NoneType`. Similar-looking printed values do not prove equal meaning or equal type.

## 12. Evidence and recall

Keep `types_and_conversion.py` and `lesson_duration.py` in `code-lab`. Record predicted and observed output for good and bad input, one conversion error and its repair, and these two answers: “Why is `bool("False")` true?” (Nonempty text is truthy.) “Why is `None` not zero?” (Absence differs from a measured count of zero.)

**Remember:** a value's type controls possible operations; `input()` provides text; conversion can fail; `None`, `False`, `0`, and `""` are different; reassignment changes what a name refers to, while mutation changes a mutable value in place.

## 13. Next connection

`QAI.01.09 — Objects, references, aliases, and copies` shows exactly what it means for two names to refer to one value and why copying mutable collections changes how later edits behave.
