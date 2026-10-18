# QAI.01.30 — Notebook workflow

> QAI.01.29 CSV and JSON → **QAI.01.30 notebook workflow** → QAI.01.31 configuration and secrets

## 1. Destination: a lesson another person can run

You have a small question cleaner for a course assistant. Your goal is to show the idea, execute the Python, check its result, and give someone else a file that works on their own machine. The companion [notebook](QAI.01.30_Notebook_Workflow_Lab.ipynb) contains the complete guided lab; run it as you read.

A **notebook** is a document containing ordered **cells**: explanation, executable code, and displayed results. The usual notebook file has the extension `.ipynb`. It stores notebook content and metadata in a structured JSON format. A notebook is useful for learning, exploration, and sharing an experiment. A working notebook file is **not** evidence that its code runs correctly from the beginning.

**Practical destination:** restart its Python process, run all cells from top to bottom, get the printed result and passing checks, then extract the essential code into a `.py` script.

## 2. The two cells you will create

| Cell | What you put in it | What happens when you run it |
|---|---|---|
| **Markdown cell** | A heading, objective, assumptions, instructions, or interpretation | Displays formatted text; it does not execute Python |
| **Code cell** | Python statements such as definitions, transformations, and checks | Sends code to the selected Python **kernel** and can display output |

A **kernel** is the Python process that runs notebook code. It remembers values across code cells until restarted. The chosen kernel must use an environment that has the Python packages your code needs. This lab uses only Python's standard library, so no third-party package is needed **inside the cells**; a notebook application still needs its own notebook runtime.

In the companion file, locate the first Markdown cell with the goal and then the first code cell:

```python
raw_questions = ["  Explain   GenAI  ", "   ", "What is RAG?"]
max_characters = 80
print("Questions received:", len(raw_questions))
```

Run that cell. The expected output is `Questions received: 3`. A code cell's **output** is the value or text the notebook displays after running it. Here `print` creates text output. Typing `raw_questions = ...` alone changes the kernel's memory but does not produce a useful display. Outputs saved in a notebook can remain visible after their code or the kernel state changes.

### Try it yourself

1. Open the companion notebook in a notebook editor; select the Python kernel.
2. Add a Markdown cell below the title: `## My prediction` followed by `Three questions were received, including a blank one.`
3. Run the first code cell and compare its printed count with your prediction.
4. Add a code cell at the end: `print(len(raw_questions))`. It should print `3` after the first cell has run.

The count includes the blank entry. Counting inputs and accepting valid questions are different operations.

## 3. Execution order is more important than page position

Clicking Run sends a **cell execution** to the kernel. Many interfaces display an **execution count** such as `[1]`, `[2]`; it counts executions in that kernel session, not the cell's position on the page. Running a lower cell first can give it `[1]` while the top cell remains unexecuted. Re-running a cell increases its count. Counts and saved outputs are clues, not proof of reproducibility.

The kernel's **state** includes variable values, imports, and function definitions currently in memory. Consider these two cells, in page order:

```python
# Cell A
rate = 10
print(rate)

# Cell B
rate = 20
```

Run A: output `10`. Run B, then run A again: A prints `10` and resets `rate` to 10. Reverse the page order or add a third cell `print(rate)` and the answer may differ depending on which cell ran last. The visible text of a notebook does not show its full execution history.

**Stale state failure:** Suppose you run a definition `answer = 3`, later delete that cell, and run `print(answer)`. It may still print `3` in your current session; after restart it raises `NameError`. A learner opening the notebook cannot reconstruct the deleted definition. **Repair:** put every required definition in a cell above its use and restart and run all cells again.

### Reproduce a failure safely

In the companion notebook, **restart the kernel**, then run the last code cell containing `print("Ready questions:", ...)` **before** running the first code cell or the function definition. Expected error: `NameError` because `ready_questions` is not yet defined. Then restart the kernel again and **run all cells** top to bottom. The notebook should finish with `Checks passed: 5`. You have reproduced the failure and its repair without leaving a permanently broken cell in the shared file.

If you ran the last cell after a successful all-cells run, it may succeed; restart first to make the test meaningful.

## 4. The lab's complete data path

The notebook builds one small, self-contained course-question workflow:

1. Define three sample input strings and a maximum length of 80 characters.
2. Define `clean_question(raw)` to trim surrounding spaces and collapse repeated internal spaces.
3. Define `classify_question(raw, max_characters)` to return `"ready"`, `"empty"`, or `"too_long"` plus the cleaned text.
4. Classify every input and keep only ready questions.
5. Check normal and boundary cases with `assert`.
6. Print the ready questions.

The first input becomes `Explain GenAI`; the blank input is rejected; `What is RAG?` remains ready. These are toy data to teach state and execution order, **not** a claim about an AI model's understanding. The checker validates formatting and length, not semantic meaning or safety.

### Why put a definition above its use?

An assignment creates a value in the current Python process; `def` creates a function name. A later cell can use those names only after their defining cells have executed. Notebook state is shared across code cells in one kernel. The companion notebook orders input → functions → processing → checks → display. Running all from the top satisfies these dependencies.

### What do the checks prove?

The lab checks a normal result, a blank input, a length of exactly 80, a length of 81, and the unchanged original input. `assert condition` stops with `AssertionError` when `condition` is false. Passing checks support those five claims only. They do not prove that all possible strings work, and they do not replace production validation or a test suite. The length rule counts Python characters in the cleaned string, not bytes or model tokens.

## 5. The five essential controls

| Action | What it does | When to use it | What it does **not** do |
|---|---|---|---|
| **Run a cell** | Executes that cell in the current kernel | Inspect one change | Does not ensure earlier cells ran |
| **Interrupt kernel** | Requests that the current execution stop | A loop is taking too long | Does not reliably reset state; partly changed values may remain |
| **Restart kernel** | Starts a fresh process and removes in-memory definitions | Check for hidden state; recover from an uncertain session | Does not automatically remove displayed saved outputs |
| **Clear output** | Removes displayed results from cells | Remove old or sensitive displayed content before saving | Does not reset the kernel's variables |
| **Run all cells** | Executes cells in page order | Test the document as another learner will | By itself does not guarantee a fresh kernel |

Notebook editors name or place these commands differently. In JupyterLab, use the **Kernel** and **Edit** menus or the notebook toolbar to locate them. The reliable check is **restart, optionally clear outputs, then run all**. Save after the run if you intend to share the resulting outputs. Before sharing, inspect displayed output for private input, paths, credentials, or other material that should not be distributed.

### Controlled interrupt exercise

Add a temporary code cell containing the following, run it, then interrupt it while it is running:

```python
import time

for item in range(20):
    print(item)
    time.sleep(1)
```

Your notebook may show some numbers and an interruption message. That cell has not finished: its partial output is **not** a completed result. Delete this temporary cell, restart, and run all the original cells. Do not include this loop in the reusable lab.

## 6. Define a reproducible notebook

A **reproducible notebook**, for this lab, is a saved notebook that a classmate can open in a suitable Python notebook environment, restart, and execute from top to bottom without manual hidden setup. This requires:

- all imports, sample inputs, functions, and checks in the file, before their first use;
- a specified input and expected result;
- no dependence on cells you ran earlier but deleted;
- no unexplained local file paths, notebook-only magic commands, or real API keys;
- the same implementation and validation logic when re-run.

The companion file meets those requirements using fixed local example values and standard-library Python. Reproducibility does not mean every computer has identical versions, external data, or APIs. More complex notebooks should record dependencies and versions, fix randomness where needed, and state how the data was obtained. Those practices become operationally important later in the course.

**Evidence exercise:** save a copy; restart the kernel, clear outputs, run all, and confirm that the checks pass and the final output is:

```text
Checks passed: 5
Ready questions: ['Explain GenAI', 'What is RAG?']
```

If the notebook fails only after a restart, locate the first missing import or definition; fix its source cell; repeat the entire clean run. Do not fix it by running a hidden setup cell separately.

## 7. Export and convert the notebook

**Export** means produce a new file from the notebook, such as HTML for reading or a Python script for execution. It does not change the original `.ipynb`. Notebook editors commonly offer an Export command. Select HTML to share a readable, generally non-executable view if your editor supports it; inspect whether sensitive outputs are included. HTML is not a substitute for a runnable notebook.

To **convert essential logic to a script**, copy the code cells in their dependency order into a plain UTF-8 `.py` file. Markdown cells belong in separate documentation or short Python comments. This is a portable conversion procedure that works for this lab:

1. In the same directory as the notebook, create `question_lab.py`.
2. Copy code cell 1 (input), then the function-definition cell, then processing, checks, and display. Do not copy Markdown or stored outputs.
3. Run `python question_lab.py` (or `python3 question_lab.py` on systems that use that command).
4. Confirm that it prints the same check and ready-question lines as a fresh notebook run.

For a repeatable mechanical extraction of **this lab's Python-only code cells**, save the following as `extract_script.py` beside the notebook and run `python extract_script.py`. It creates `question_lab.py` once; `"x"` mode refuses to overwrite an existing file.

```python
import json
from pathlib import Path

directory = Path(__file__).resolve().parent
notebook_path = directory / "QAI.01.30_Notebook_Workflow_Lab.ipynb"
script_path = directory / "question_lab.py"

notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
code_cells = [
    cell for cell in notebook["cells"] if cell["cell_type"] == "code"
]
source_blocks = [
    "".join(cell["source"]) if isinstance(cell["source"], list)
    else cell["source"]
    for cell in code_cells
]
with open(script_path, "x", encoding="utf-8") as handle:
    handle.write("# Generated from the companion notebook's code cells.\n\n")
    handle.write("\n\n".join(source_blocks) + "\n")
print("Created:", script_path.name)
```

Then run `python question_lab.py`. This small extractor assumes ordinary Python code cells and the known local notebook structure. General notebooks can contain cell magics, shell commands, interactive displays, hidden inputs, and side effects that cannot be copied directly into a `.py` file. Inspect and test the converted script; do not equate successful export with working software.

The script runs as a fresh Python process on every invocation, which is useful for finding implicit notebook state. A notebook is an excellent exploratory document; put repeatable program logic in scripts or modules when you need to automate it. Production service architecture comes later.

## 8. Debug and explain the result

| Symptom | Likely cause | Correct action |
|---|---|---|
| `NameError: name 'ready_questions' is not defined` | Processing cell was not run in this kernel | Restart; run all in page order |
| A displayed result contradicts the current code | Output was saved from an older run | Clear output; restart; run all; inspect current results |
| Notebook works but extracted `.py` fails | Notebook depended on hidden state or notebook-only commands | Add missing setup and use standard Python; re-run both cleanly |
| Import fails in a larger notebook | Selected kernel uses a different Python environment | Select the intended environment; document and install required dependencies there |
| Interrupt leaves confusing values | Code executed only partly | Restart and run all to restore a known state |
| Extractor says file exists | `"x"` mode protected an earlier script | Review the old file; choose a new output filename or remove it deliberately |

**Explain it aloud:** “The notebook's page order tells me how code should be read; the kernel remembers the order in which code actually ran. I restart and run all to prove the written order is sufficient. Then I run the extracted script in a new Python process to check the same logic outside the notebook.”

## 9. Practice with worked answer

**Task:** Extend the provided notebook to reject a question containing only spaces and punctuation. Start with `"  ???  "`. Keep the three existing classifications. Decide a simple rule, implement it after the existing normalisation, and add a check. This is a local exercise in notebook changes and fresh runs, not a general text safety filter.

**One valid rule:** require at least one letter or digit. Replace the original `classify_question` definition with this version, keeping the same `clean_question` definition above it:

```python
def classify_question(raw, max_characters):
    cleaned = clean_question(raw)
    if not cleaned or not any(character.isalnum() for character in cleaned):
        return "empty", cleaned
    if len(cleaned) > max_characters:
        return "too_long", cleaned
    return "ready", cleaned
```

Append this check to the check cell:

```python
assert classify_question("  ???  ", max_characters)[0] == "empty"
print("Checks passed: 6")
```

Replace the old `print("Checks passed: 5")` with the new line, **do not leave both**. Restart, clear outputs, and run all. The new final check line should say `Checks passed: 6`; the ready-question list remains unchanged. The simple `isalnum()` policy accepts digits alone; choose a stricter policy in a real application only after stating its user requirement and tests.

## Remember

- `.ipynb` holds cells, metadata, and possibly saved outputs; a kernel runs code and retains state.
- Markdown explains; code executes; outputs and counts can be stale.
- Page order and execution history differ. **Restart → run all** tests the documented order.
- Interrupt stops an operation; clear output hides displayed results; restart resets Python state.
- A notebook is reproducible when its declared setup and source produce the expected result in a fresh run.
- Export for reading; convert tested essential code to `.py` for repeatable execution.

## References

- [Jupyter notebook format specification](https://nbformat.readthedocs.io/en/latest/format_description.html)
- [JupyterLab: notebooks and kernels](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)
