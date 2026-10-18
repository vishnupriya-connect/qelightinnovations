# QAI.01.09 — Objects, References, Aliases, and Copies

> `QAI.01.08 Data types` → **`QAI.01.09 Objects, references, aliases, and copies`** → `QAI.01.10 Operators and operands`

## 1. Why this matters for AI work

Imagine preparing a list of course documents. You want a second version for an experiment, but changes to that version unexpectedly appear in the original. The cause may be **aliasing**: two names refer to one mutable object. In this lesson you will predict and test aliasing, distinguish equal content from identical objects, and choose between a shallow and a deep copy.

Run examples inside the disposable `qai-path-lab/code-lab/` folder. The only data are fictional titles. Lists are used here as small containers; their complete operations are taught later.

## 2. Name, object, value, identity

An **object** is a value Python manages while a program runs. It has a **type**, a **value/content**, and an **identity**. The identity distinguishes one object from other objects during its lifetime. An object's **value** is the information or contents you work with. Two objects can have equal values and still have different identities.

```python
first = ["intro"]
second = ["intro"]
print(first == second)  # True: same contents
print(first is second)  # False: separate lists
```

| Term | Question it answers | Example |
|---|---|---|
 object value | “What does it contain?” | `["intro"]` |
 object identity | “Is this the very same object?” | `first is second` |
 equality (`==`) | “Do these values compare equal?” | `first == second` |
 identity comparison (`is`) | “Do both names refer to the same object?” | `first is second` |

`==` compares values as defined by that type; `is` compares identity. For ordinary lists, two independently made lists with matching items compare equal, but are not the same object. Use `is None` to test Python's unique missing-value object, as in `QAI.01.08`. Do not use `is` to compare everyday numbers or strings for value equality: Python may reuse some immutable objects, so a particular result can mislead you.

Python's `id(obj)` can display an identity token:

```python
documents = ["intro"]
same_documents = documents
print(id(documents) == id(same_documents))  # True
```

The actual numeric token varies between runs. Do **not** treat it as a guaranteed portable memory address. The Boolean result here is the useful observation.

## 3. Reference, variable reference, and memory reference

A **reference** is the connection Python uses to reach an object. Assignment makes a variable name refer to an object:

```python
documents = ["intro"]
```

`documents` is a **variable reference** to the list object. You can picture a name pointing to an object held in computer memory. We call that conceptual connection a **memory reference**. Python does not require you to know or edit a raw memory address to use it.

```text
name documents  ──refers to──>  list object ["intro"]
```

This picture describes *which object a name reaches*. It does not imply that assigning one name to another automatically creates a new list.

## 4. Shared reference, alias, and aliasing

An **alias** is a second name for the **same** object. **Aliasing** is the situation in which such shared references exist:

```python
original = ["intro"]
working = original
print(original is working)  # True
```

`working = original` does not copy the list. It binds `working` to the original list object. Both names are **shared references** to it.

```text
name original ─┐
               ├──refers to──> one list object ["intro"]
name working  ─┘
```

If your aim was an independent experiment, this assignment alone has **not** achieved it. Python's [copy documentation](https://docs.python.org/3/library/copy.html) explicitly distinguishes assignment from copying.

## 5. Mutation changes a shared mutable object

**Mutation** means changing an existing object's contents in place. A list is a **mutable object**; `append` adds an item to that same list:

```python
original = ["intro"]
working = original
working.append("rules")
print(original)             # ['intro', 'rules']
print(working)              # ['intro', 'rules']
print(original is working)  # True
```

**Trace:** the list began with one title; both names referred to that one list; `append` changed it; both names now display the changed list. No copying happened.

**Reassignment is different:**

```python
original = ["intro"]
working = original
working = ["practice"]
print(original)             # ['intro']
print(working)              # ['practice']
print(original is working)  # False
```

The last assignment made `working` refer to a newly created list. It did not edit the object reached by `original`. Distinguish “change the object” from “change which object this name reaches” before predicting effects.

## 6. Immutable objects: a familiar contrast

An **immutable object** cannot have its value changed in place. Strings and integers from `QAI.01.08` are familiar examples:

```python
original_title = "Gen"
working_title = original_title
working_title = working_title + "AI"
print(original_title)  # Gen
print(working_title)   # GenAI
```

The operation produces a new string value and rebinds `working_title`. It does not edit the original string. This example alone does not prove that assigning an immutable value created two separate objects; identity and immutability are different ideas. The operational rule is: when you need to change an immutable value, compute a new value and assign a name to it.

## 7. Copy an outer container: a shallow copy

A **copy** makes another object from an existing one. For a simple list of strings, `list.copy()` creates a new outer list:

```python
original = ["intro"]
working = original.copy()
print(original == working)  # True: same contents
print(original is working)  # False: separate outer lists
working.append("quiz")
print(original)             # ['intro']
print(working)              # ['intro', 'quiz']
```

The list produced by `copy()` is a **copied object**; `original` still refers to the **original object**. This is a **shallow copy**: it makes a new outer container and keeps references to the objects inside. For this simple list of immutable strings, appending to the new outer list leaves the original list unchanged.

### A nested list reveals the boundary

A **nested list** is a list containing another list. Suppose each inside list holds notes for one course unit:

```python
original = [["orientation"], ["practice"]]
working = original.copy()
print(original is working)        # False: different outer lists
print(original[0] is working[0])  # True: same first inner list
working[0].append("example")
print(original)                   # [['orientation', 'example'], ['practice']]
print(working)                    # [['orientation', 'example'], ['practice']]
```

`[0]` means “first item.” Here it selects the first inner list. **Predict the surprise:** despite different outer lists, both show `"example"` because they still share that inner list. A shallow copy protects changes to the outer list itself, not in-place edits to shared nested mutable values.

Check the different outcome of an outer edit:

```python
original = [["orientation"]]
working = original.copy()
working.append(["quiz"])
print(original)  # [['orientation']]
print(working)   # [['orientation'], ['quiz']]
```

Only the copied outer list received an additional inner list. Ask **which level was changed?** before deciding whether a shallow copy is enough.

## 8. Copy nested mutable values: a deep copy

A **deep copy** creates a new outer object and recursively copies suitable objects inside it. Python provides `copy.deepcopy(...)` in its standard `copy` module. A **module** is a reusable source of Python functions; `import copy` makes that module available.

```python
import copy

original = [["orientation"], ["practice"]]
independent = copy.deepcopy(original)
print(original == independent)          # True: equal contents
print(original is independent)          # False: new outer list
print(original[0] is independent[0])    # False: new inner list
independent[0].append("example")
print(original)                         # [['orientation'], ['practice']]
print(independent)                      # [['orientation', 'example'], ['practice']]
```

The deep copy has separate nested lists in this example, so an edit in the copied course plan does not change the original plan. Deep copying is not automatically the best default: it can cost extra time and memory, and complex objects may have custom copying behavior. Choose the **level of independence** your task needs; verify it with a mutation test. The [official copy reference](https://docs.python.org/3/library/copy.html) describes shallow and deep behavior.

| Operation | New outer list? | Shared inner lists in the nested example? |
|---|---|---|
 `working = original` | no | yes; everything is the same object |
 `working = original.copy()` | yes | yes |
 `working = copy.deepcopy(original)` | yes | no, for these ordinary nested lists |

## 9. Guided lab: predict, run, and compare

Create `references_copies.py` inside `qai-path-lab/code-lab/`. The file uses only fictional lesson names and Python's standard library:

```python
import copy

source = [["intro"], ["practice"]]
alias = source
shallow = source.copy()
deep = copy.deepcopy(source)

print("Alias is source:", alias is source)
print("Shallow is source:", shallow is source)
print("Deep equals source:", deep == source)
print("Shallow first item shared:", shallow[0] is source[0])
print("Deep first item shared:", deep[0] is source[0])

alias[0].append("worked example")
print("After alias edit, source:", source)
print("After alias edit, shallow:", shallow)
print("After alias edit, deep:", deep)

shallow.append(["new unit"])
print("After shallow outer edit, source:", source)
print("After shallow outer edit, shallow:", shallow)
```

Run from `code-lab` with `py .\references_copies.py` in PowerShell, or `python3 references_copies.py` in Bash/Zsh. Use `python` if that was your verified Windows interpreter in `QAI.01.06`.

**Expected output:**

```text
Alias is source: True
Shallow is source: False
Deep equals source: True
Shallow first item shared: True
Deep first item shared: False
After alias edit, source: [['intro', 'worked example'], ['practice']]
After alias edit, shallow: [['intro', 'worked example'], ['practice']]
After alias edit, deep: [['intro'], ['practice']]
After shallow outer edit, source: [['intro', 'worked example'], ['practice']]
After shallow outer edit, shallow: [['intro', 'worked example'], ['practice'], ['new unit']]
```

**Why:** alias and source are one outer list; shallow has a new outer list but shares inner lists; deep has separate inner lists. The first edit targets a shared inner list; the last edit targets the shallow outer list only.

**Controlled variation:** just before the last two prints, add `deep[1].append("quiz")`. Predict: `deep` becomes `[['intro'], ['practice', 'quiz']]`, while `source` and `shallow` are unchanged by that new line. Save and run; inspect all three to verify.

## 10. Diagnose three easy-to-miss mistakes

| Symptom | Cause | Correct action |
|---|---|---|
 “I wrote `backup = source`, but editing backup changed source” | assignment made an alias | for an independent outer list use `source.copy()`; inspect nested values before choosing |
 “I used `source.copy()`, but nested notes changed” | shallow copy still shares inner lists | use `copy.deepcopy(source)` when independent nested mutable data is needed |
 “`a == b` is `True`, so they must be the same list” | equality checks content; identity checks the object | inspect `a is b` with separately constructed lists |

For an AI application, unintentionally editing a shared list of source documents, prompts, or evaluation examples can change what a later run tests. Before modifying a collection that may be reused, decide who owns it and test whether its nested data is shared.

## 11. Independent exercise and full answer

**Task:** an original course outline contains `[["intro"], ["quiz"]]`. Make (1) an alias, (2) a shallow copy, (3) a deep copy. Append `"worked example"` to the first inner list through the alias. Then append a new outer item `["extra"]` only to the shallow copy. Predict all three final lists and the identity checks before running.

**Worked solution:**

```python
import copy

original = [["intro"], ["quiz"]]
alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

alias[0].append("worked example")
shallow.append(["extra"])

print("Original:", original)
print("Shallow:", shallow)
print("Deep:", deep)
print("Alias same object:", alias is original)
print("Shallow same outer object:", shallow is original)
print("Shallow shares first inner object:", shallow[0] is original[0])
print("Deep shares first inner object:", deep[0] is original[0])
```

**Expected:**

```text
Original: [['intro', 'worked example'], ['quiz']]
Shallow: [['intro', 'worked example'], ['quiz'], ['extra']]
Deep: [['intro'], ['quiz']]
Alias same object: True
Shallow same outer object: False
Shallow shares first inner object: True
Deep shares first inner object: False
```

The alias mutated the shared first inner list, so the original and shallow copy reflect that edit. Adding `["extra"]` changes only the shallow **outer** list. The deep copy's contents stay as they were before either change.

## 12. Evidence and recall

Keep `references_copies.py` and a short `copy_trace.md` with your predicted and observed results, the two levels of `is` checks, one controlled variation, and this decision: “I need to change only the outer list” → a shallow copy may suffice; “I need to edit nested mutable lists independently” → make and verify an appropriate deep copy.

**Remember:** an object has value, type, and identity; a variable name refers to an object; assignment can create an alias; mutating a shared mutable object is visible through all aliases; reassignment changes one name's reference; `==` asks about equality, `is` about identity; a shallow copy duplicates the outer container, while a deep copy can duplicate its nested mutable contents.

## 13. Next connection

`QAI.01.10 — Operators and operands` studies how Python combines values into expressions. You have already used `+`, `==`, and `is`; next you will name the parts of those expressions and read more complex ones in the correct order.
