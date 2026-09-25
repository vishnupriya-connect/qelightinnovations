# QAI.01.25 — Modules and Imports

> QAI.01.24 Debugging and testing → **QAI.01.25 Modules and imports** → QAI.01.26 Packages and dependencies

## 1. Destination: reuse the same function from a demo and tests

The previous project placed `prepare_request` in one Python file and its tests in another. This node explains why that arrangement works. A **module** holds definitions that another program can import. You will build a small `src/` folder with a reusable module, a main program, and tests. Running the main program should display results; importing the reusable module should **not** unexpectedly start a demo.

The node's P1 evidence is a working three-file mini-project with both a direct run and an imported test run. Installation, dependency versions, and environment recreation are addressed in QAI.01.26–01.27.

## 2. Module, module file, and import

A **module** is a unit of Python code with its own names. A Python **module file** commonly has a `.py` suffix. An **import** makes a module available to another module; the code that asks for it contains an **import statement**:

```text
src/
├── text_utils.py          reusable definitions
├── demo.py                main program that uses them
└── test_text_utils.py     checks those definitions
```

Here `text_utils.py` is a **custom module** because you wrote it. `demo.py` is a **main program** when you run it to do an action. A module may be imported by more than one consumer: the demo and the tests can share one cleaning function instead of copying it.

**Important:** importing a module normally executes its top-level statements during its first import in a Python process. Therefore a reusable file should put demo printing or network/file actions behind an intentional entry point rather than run them unconditionally during import. Function *definitions* become available when the module loads; their bodies run when called.

## 3. `import` and the module namespace

A **namespace** maps names to objects. The **module namespace** of `text_utils` contains its functions. A **qualified name** uses the module name plus a dot:

```python
# Once text_utils.py exists in the project folder:
import text_utils
print(text_utils.clean_question("  Explain   AI  "))  # Explain AI
```

`text_utils.clean_question` is a qualified name: “look for `clean_question` inside the `text_utils` module.” It helps identify the source of the function. `import text_utils` by itself binds the name `text_utils` in the caller; it does not bind an unqualified `clean_question` there.

An **imported name** is a name made available by an import. Use `from` to import a specific name:

```python
from text_utils import clean_question
print(clean_question(" Explain ML "))             # Explain ML
```

`from text_utils import clean_question` binds `clean_question` directly in the caller's namespace. Both forms can be correct; keep the source clear when two modules define a similarly named function.

## 4. `as` and import alias

`as` gives an **import alias**, an alternate local name:

```python
import text_utils as tu
from text_utils import clean_question as tidy

print(tu.clean_question("  GenAI "))  # GenAI
print(tidy("  RAG  "))                # RAG
```

`tu` and `tidy` are names in this caller. The module file is still `text_utils.py`; an alias does not rename the module on disk. Use aliases sparingly and make them understandable. `import *` hides where names came from and can cause collisions; prefer named imports for course projects.

## 5. `__name__` and `__main__`: tell a run from an import

Python supplies each module a special `__name__` variable. When a file runs as the top-level program, its `__name__` is `"__main__"`. When it is imported normally as `text_utils`, its `__name__` is `"text_utils"`:

```python
# In text_utils.py:
def clean_question(raw):
    return " ".join(raw.split())

if __name__ == "__main__":
    print("Demo:", clean_question("  Explain   AI "))
```

Direct command `python text_utils.py` prints `Demo: Explain AI`. An import `import text_utils` does **not** print the demo line: the `if` condition is false during import. This is the **main guard**. It allows the same file to contain callable definitions and a deliberate direct-run demonstration.

**Scope of this rule:** the main guard prevents only the statements inside that guard from running on import. An unconditional `print(...)` at top level outside the guard would still run when imported. Avoid expensive or sensitive work at import time.

## 6. Guided mini-project: three files in `src/`

Create `qai-path-lab/module-lab/src/`. Save the next three blocks as **separate files with these exact names**. The code uses only Python's standard library.

### `src/text_utils.py` — reusable module

```python
# src/text_utils.py
def clean_question(raw):
    """Return a single line with surrounding and repeated whitespace removed."""
    return " ".join(raw.split())


def display_request(course_title, raw_question):
    """Return a labelled request from two strings without printing."""
    clean = clean_question(raw_question)
    if clean == "":
        return "REJECT: empty question"
    return f"Course: {course_title.strip()} | Question: {clean}"


if __name__ == "__main__":
    print("Demo:", display_request(" GenAI ", "  Explain   AI  "))
```

The module exposes two reusable functions. Its direct-run demo is inside the guard, so a successful import alone has no visible output. The sample expects string inputs; validation of arbitrary external types was covered in QAI.01.23 and can be added when needed.

### `src/demo.py` — main program

```python
# src/demo.py
import text_utils
from text_utils import clean_question as tidy

print("Module name:", text_utils.__name__)
print("Module file recognised:", text_utils.__file__.endswith("text_utils.py"))
print(text_utils.display_request("GenAI", "  Explain    models "))
print("Aliased cleaner:", tidy("  What is   RAG? "))
```

`text_utils.__file__` points to the module file Python loaded; the printed boolean avoids assuming a particular machine path. `tidy` is the caller's alias for the same cleaning function. The main program calls the functions explicitly; importing does not run the module's guarded demo.

**Expected `demo.py` output:**

```text
Module name: text_utils
Module file recognised: True
Course: GenAI | Question: Explain models
Aliased cleaner: What is RAG?
```

### `src/test_text_utils.py` — test consumer

```python
# src/test_text_utils.py
import unittest
import text_utils


class TextUtilsTests(unittest.TestCase):
    def test_cleaning(self):
        self.assertEqual(text_utils.clean_question("  Explain  AI "), "Explain AI")

    def test_display(self):
        self.assertEqual(
            text_utils.display_request(" GenAI ", " Explain AI "),
            "Course: GenAI | Question: Explain AI",
        )

    def test_blank(self):
        self.assertEqual(
            text_utils.display_request("GenAI", "   "),
            "REJECT: empty question",
        )


if __name__ == "__main__":
    unittest.main()
```

From inside `src/`, run:

- Windows PowerShell: `py .\demo.py`; `py -m unittest -v test_text_utils` (or your verified `python` command).
- Bash/Zsh: `python3 demo.py`; `python3 -m unittest -v test_text_utils`.
- Direct reusable-module demo: `py .\text_utils.py` or `python3 text_utils.py`, respectively.

The test command should report **3 tests, OK**. Running `text_utils.py` directly should print **Demo: Course: GenAI | Question: Explain AI**. Running `demo.py` or importing `text_utils` in the test runner should **not** print a separate `Demo:` line. The three files belong in the same folder for these commands.

**Run from the project root when desired:** `python3 src/demo.py` uses the script's `src` directory for its sibling import in an ordinary script launch. For the precise test command above, first change into `src`; QAI.01.26–01.27 show how packages and project setup make multi-folder work clearer.

## 7. Trace exactly what happens on import

When `demo.py` executes `import text_utils`:

1. Python looks for a resolvable module called `text_utils` (the nearby `text_utils.py` is available in this project).
2. During its first import in this process, Python runs the module's top-level statements and creates its function objects.
3. In the imported module, `__name__ == "text_utils"`, so the `if __name__ == "__main__"` demo body does not run.
4. The caller gets a name `text_utils` for that module and then calls `text_utils.display_request(...)`.

Importing the same module again in the **same process** usually reuses the already-loaded module object rather than rerunning its top-level code. Do not build the program around relying on import side effects; explicit function calls make work easier to reason about and test.

## 8. Diagnose import and namespace errors

| Observation | Likely cause | Check and repair |
|---|---|---|
| `ModuleNotFoundError: No module named 'text_utils'` | expected module is not in importable locations | confirm filename, folder, command, and active interpreter |
| `AttributeError: module 'text_utils' has no attribute 'clean_question'` | wrong module loaded or name misspelled | inspect `text_utils.__file__` and module's definitions |
| `NameError: clean_question` after `import text_utils` | only module name is bound locally | use `text_utils.clean_question` or explicit `from` import |
| demo prints during a test import | unconditional top-level print or missing main guard | put demonstration code under `if __name__ == "__main__":` |
| local `json.py` or `unittest.py` causes confusing imports | project file shadows a standard module | rename local file and verify loaded module path |
| importing `src/text_utils.py` is confused with installing a package | module files and installed packages are different concepts | use this local-module lab first; package setup is next |
| two functions have the same short name in a caller | imported names collide | use qualified names or clear aliases |

**Debug routine:** confirm the Python interpreter that executes the command, the exact working location, filename, traceback, and (when import succeeds) `module.__file__`. Do not append arbitrary directories or install random packages to hide a wrong local file path. A wrong interpreter/package setup is examined in QAI.01.26–01.27.

## 9. Independent micro-lab with complete solution

**Task:** create `course_labels.py` with a reusable `format_label(title)` function that returns `"Lesson: <trimmed title>"`. A direct run of this file must print a demo. Create `use_labels.py` that imports `course_labels` using an alias and prints a label for `"  Functions  "` **without** printing the module's guarded demo. Show outputs for both commands.

**File `course_labels.py`:**

```python
# course_labels.py
def format_label(title):
    """Format a string title as a single course label."""
    return f"Lesson: {title.strip()}"


if __name__ == "__main__":
    print("Demo:", format_label(" Tuples "))
```

**File `use_labels.py`:**

```python
# use_labels.py
import course_labels as labels

print(labels.format_label("  Functions  "))
```

**Expected direct run:** `python3 course_labels.py` prints `Demo: Lesson: Tuples`. **Expected consumer run:** `python3 use_labels.py` prints only `Lesson: Functions`. On Windows use `py .\course_labels.py` and `py .\use_labels.py`. Place both files in one folder, run both, and explain that imported `course_labels.__name__` is `"course_labels"` rather than `"__main__"`.

## 10. Remember and retain

- A `.py` module owns a namespace; import provides access to its definitions.
- `import module` then `module.function` is a qualified call; `from module import name` binds a name in the caller; `as` gives a local alias.
- An import can execute **top-level statements**. Put runnable demonstration actions under `if __name__ == "__main__":` so import does not run them.
- `__name__` is `"__main__"` for the directly run file and normally the module name for a normal import.
- Verify the actual file loaded via `module.__file__` when a name resolves to an unexpected module.
- Retain the three-file `src/` project, demo and three-test outputs, and the independent two-file solution. Write a short README-style record with folder layout, commands, expected output, and one import failure you diagnosed.

**Next:** QAI.01.26 adds project packages, dependencies, versions, and reproducible installation; QAI.01.27 builds the isolated Python environment that uses them.

---

**Node contract (S90):** `C | L3 | H1–H3 | E3–E5 | A2–A4 | P0–P1`. All sixteen S86 module/import topics are taught through a runnable three-file mini-project, direct/imported execution checks, failure diagnosis, and a solved independent build. Learner evidence requires running both entry modes and recording the results.
