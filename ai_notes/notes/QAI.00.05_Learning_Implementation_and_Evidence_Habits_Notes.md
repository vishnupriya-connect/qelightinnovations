# QAI.00.05 — Learning, Implementation, and Evidence Habits

> **Position in the QElight AI path**  
> `QAI.00.04 System and model basics` → **`QAI.00.05 Learning, implementation, and evidence habits`** → `QAI.00.06 Working environment`

## 1. Why this subsection exists

AI capability is not formed by watching videos or collecting notes alone.

It is formed by a repeatable cycle:

```text
Concept → Worked example → Guided implementation → Independent practice → Project → Explanation
```

Each step has a different job.

| Step | What it forms |
|---|---|
| Concept | correct meaning and mental model |
| Worked example | see how the idea is used step by step |
| Guided implementation | first successful hands-on execution |
| Independent practice | ability to work without copying every step |
| Project | connect several ideas to solve a real problem |
| Explanation | ability to teach, justify, and retain the idea |

This cycle will be used for every important QElight node. The depth becomes greater as we move from foundations to production GenAI systems.

## 2. Concept

- **Concept:** a basic idea that helps us recognise, reason about, or use something.
- A concept answers: *What is it? Why does it exist? What is it different from?*

### Example

**Concept:** similarity search.

- It finds existing items related to a query.
- It is different from generation, which creates a new answer or content.
- It matters because a GenAI assistant may first find relevant course notes before writing an answer.

A concept is not complete when it is only memorised. It is complete at the current level when you can recognise it in a situation and use the correct words for it.

At this point, some terms below are a **first encounter**. You will learn Python syntax, files, tools, and Git in `QAI.01`. Here you learn what work each item serves, then run one supplied example and record what happened. Do not mistake this first run for full software-engineering proficiency.

## 3. Worked example

- **Worked example:** a complete small problem with the reasoning and solution shown.
- It answers: *How is this concept used in one real situation?*

### Example

```text
Need: Answer “When is Assignment 1 due?” from an approved course schedule.

1. Identify task: question answering.
2. Find related notes: similarity search/retrieval.
3. Use relevant note content as context.
4. Create a simple answer: generation.
5. Check that the answer is supported by the retrieved note.
```

The worked example is not meant for copying forever. It is the bridge between understanding a term and attempting the first implementation.

## 4. Guided implementation

- **Guided implementation:** build or run a small working solution with explicit steps, expected result, and explanation.
- It answers: *Can I make this work once, while the path is clear?*

### Example structure

```text
Goal: Load a small document set and return the most related section for one question.

Step 1: open the starter notebook.
Step 2: load the supplied documents.
Step 3: run the retrieval function.
Step 4: change the question.
Step 5: inspect the returned section.
Step 6: compare the result with the expected answer.
```

At this stage, it is correct to use a provided template. The learner must still understand each changed input, output, and result.

## 5. Independent practice

- **Independent practice:** solve a similar but not identical task without step-by-step copying.
- It answers: *Can I use the concept when the exact example changes?*

### Example

After a guided note-retrieval demo, change:

- the source documents;
- the learner question;
- the required output format;
- one failure case, such as no relevant document.

Then explain:

- why the result is relevant or not relevant;
- what input/context caused the problem;
- what safe behaviour the system should show.

Independent practice is the first evidence of generalisation by the learner.

## 6. Project

- **Project:** a connected piece of work that combines several concepts and implementations to deliver a useful outcome.
- A project has a user problem, inputs, outputs, constraints, implementation, testing, and result.

### Project is different from an exercise

| Exercise | Project |
|---|---|
| practise one narrow skill | combine several skills for a useful result |
| usually small and controlled | has a clear use case and design choices |
| e.g., send one request to a supplied software service | e.g., build a cited question-answering assistant using documents, checks, and evaluation |

### QElight project progression

```text
P0 micro-lab
  ↓
P1 mini-project
  ↓
P2 integrated project
  ↓
P3 major project
  ↓
P4 capstone
```

The scale increases, but every project still needs a complete reference solution, expected result, tests, and explanation of common failures.

## 7. Explanation

- **Explanation:** communicate an idea so another person can understand and use it.
- It answers: *Can I organise my understanding, not merely repeat words?*

### A good technical explanation has four parts

```text
1. What problem does it solve?
2. What is the simple mental model?
3. What happens in the workflow?
4. What can go wrong / when should it not be used?
```

### Example: explain retrieval

> Retrieval finds existing information related to a question. In a course assistant, it finds relevant approved notes before the language model writes an answer. It reduces unsupported answers, but retrieval can still fail if the documents are missing, outdated, or poorly indexed.

Explanation is both a learning tool and a teaching tool. It exposes confusion early.

## 8. Notebook

- **Notebook:** an interactive document that keeps explanatory text, runnable code, output, tables, and images in one ordered file.
- Common notebook format: `.ipynb`.
- A notebook is useful for learning, experimentation, demonstrations, and guided labs.

### Good notebook structure

```text
Title and goal
Prerequisites
Concept explanation
Setup
Small runnable code cells
Expected output
Interpretation
Failure case / modification
Summary
```

### Notebook rule

- Run cells from top to bottom in a clean session.
- Do not trust old saved outputs.
- Record the required package versions and inputs when the result matters.

## 9. Script

- **Script:** a file containing code that is run as a program.
- Common Python script format: `.py`.

### Notebook versus script

| Notebook | Script |
|---|---|
| interactive learning and exploration | repeatable program execution |
| text, code, and visible output together | code-first; output goes to terminal/files/services |
| useful for demos and experiments | useful for automation, jobs, APIs, and production workflows |

### Example

```text
Notebook: explore and test a way to split long documents into searchable pieces.
Script: run the chosen document-splitting approach on a folder of documents every night.
```

## 10. Package

- **Package:** organised reusable code that can be installed or imported into another program.
- A package prevents large projects from becoming one unmanageable notebook or script.

### Simple project structure

```text
project/
├─ notebooks/       learning and experiments
├─ src/             reusable application code
├─ tests/           checks for expected behaviour
├─ data/            controlled sample data or data references
├─ config/          configuration files
├─ README.md        how to run and use the project
└─ requirements.txt package dependencies
```

You will build packages later. For now, remember the purpose: separate reusable code from temporary exploration.

## 11. API

- **API (Application Programming Interface):** an agreed way for one software component to request work from another component.
- An API defines what request to send and what response to expect.

### Everyday analogy

An API is like a clearly defined service counter:

- you submit the required form/input;
- the counter follows its service contract;
- you receive a defined result or error.

### GenAI example

```text
Your application sends: prompt, model choice, and settings.
Model-provider API returns: generated text, structured output, or an error.
```

The API is not the model itself. It is the interface used to access a service or component.

## 12. Dataset

- **Dataset:** a defined collection of related data used for analysis, model development, testing, or evaluation.
- A dataset may be a table, document collection, image collection, audio collection, or structured record set.

**One record** is one individual item in a dataset: for example, a question paired with its approved answer. Two records can form a tiny demonstration dataset; two records are not enough evidence to claim an AI model is accurate.

### Examples

| Dataset | Possible use |
|---|---|
| labelled email collection | train/test spam classifier |
| historical enrolment table | predict enrolment counts |
| course documents and their source names | build/evaluate an assistant that looks up notes before answering |
| prompt and expected-answer set | evaluate a GenAI application |

### Dataset questions to ask

- Who created it?
- What does one record represent?
- Is it permitted to use?
- Is it current and representative?
- What is missing or biased?
- Where is the version recorded?

## 13. Experiment

- **Experiment:** a controlled attempt to test an idea, configuration, model, prompt, or implementation choice.
- An experiment changes one or more chosen variables and observes results.

### Example of a later document-retrieval experiment

```text
Question: When we split source documents into smaller or larger pieces, which choice retrieves the most useful course-note section?

Keep fixed: same documents, same test questions, same method for comparing question and passage.
Change: size of the document pieces.
Measure: whether the correct passage is found; time and cost when later applicable.
Record: configuration and results.
```

We will define *embeddings*, *chunk size*, and retrieval metrics when building document-grounded systems. The only idea needed here is to hold important conditions steady while changing one chosen thing.

**Common mistake:** change documents, prompt, model, chunk size, and evaluation questions at the same time. Then it becomes difficult to know which change caused the result.

## 14. Artefact

- **Artefact:** a saved, inspectable output created during learning or development.
- Artefact is evidence that work happened and can be reviewed or reused.

### Examples of AI artefacts

| Artefact | What it shows |
|---|---|
| notebook | concept, implementation, and output |
| script/package | reusable program logic |
| README | how to run, use, and understand a project |
| dataset card | data source, purpose, limits, permission |
| model card | model purpose, evaluation, limits, risks |
| experiment report | configuration, result, interpretation |
| evaluation set | what quality was tested |
| deployment runbook | how to operate and recover the system |
| teaching note | explanation and examples for learners |

## 15. Reproducibility

- **Reproducibility:** another person—or you at a later time—can run the same work with the same stated inputs and obtain the same result, or understand why a result differs.
- Reproducibility prevents “it worked on my laptop” from becoming the only evidence.

### Minimum reproducibility record

| Item | Why it is recorded |
|---|---|
| code version | know exactly which program was used |
| data version | know exactly which data/documents were used |
| model version | know which model/checkpoint/provider version was used |
| configuration version | know settings such as prompt, temperature, chunk size, and environment values |
| random seed | repeat controlled random behaviour where supported |
| environment/package versions | rerun with compatible software |
| date and result | compare runs over time |

### Random seed

- **Random seed:** a starting value that makes a sequence of pseudo-random choices repeatable in a program.
- It helps controlled experiments, simulations, dataset splits, and some model operations.
- It does not guarantee identical results in every cloud/service/model situation.

### Version

- **Version:** an identifiable state of something at a particular point in time.
- Examples: `dataset v2`, `prompt v5`, `model version 1.3`, `code commit abc123`.

### Configuration

- **Configuration:** chosen settings that control how a program or system runs.
- Examples: model name, temperature, max output length, API endpoint, chunk size, retrieval count, file path.

## 16. One complete learning/build cycle

### Example: create a small cited course-note assistant

| Stage | Work | Resulting artefact |
|---|---|---|
| concept | understand question answering, retrieval, generation, grounding | short note/mind map |
| worked example | inspect a small prepared demo | annotated example |
| guided implementation | run a starter notebook on three documents | runnable notebook |
| independent practice | replace question/documents and handle “no answer” case | modified notebook + notes |
| experiment | compare two chunk sizes | experiment table |
| mini-project | build a small cited Q&A interface | project folder + README |
| explanation | explain design, output, limits, and failure cases | teaching note/demo |
| reproducibility | record data, code, model, prompt, settings, result | run record |

This same cycle later scales to document-grounded answering, AI systems that use tools, adapting models, image generation, deployed applications, and capstone work. Each method will be defined where it is actually built.

## 17. Working habits to keep from today

- Start each note or notebook with a clear task and expected outcome.
- Keep the smallest runnable example before expanding scope.
- Change one important thing at a time during an experiment.
- Save useful output, not only the final code.
- Record source, permission, and version for meaningful data/documents.
- Separate exploration from reusable application code.
- Write the limitation or failure case beside the successful result.
- Explain the work in simple words before claiming mastery.
- Build small evidence continuously; do not wait for a final project to prove capability.

## 18. Reusable minimum project record

Use this record for every lab from now onward. It turns “I tried something” into inspectable evidence.

```text
Project / lab name:
Date:
Goal: one observable result to produce or test
Input: data, prompt, file, API, or other starting material
Method: steps, code, model, or tool used
Environment: local/cloud; important package or model version
Configuration: non-secret settings; random seed if relevant
Expected result: what success should look like
Actual result: observed output, metric, screenshot, file, or link
Check performed: test, source check, comparison, or human review
Limitation / failure observed:
Next change to try:
```

### Minimum project structure

```text
project-name/
├─ README.md                 # purpose and safe run instructions
├─ notebooks/                # exploration and explanation
├─ src/                      # reusable program code, later
├─ data/                     # permitted input/sample data
├─ outputs/                  # generated results; not original source data
├─ tests/                    # checks, later
├─ requirements.txt          # required packages, later
├─ .env.example              # placeholder configuration only
└─ project_record.md         # completed record above
```

Do not create empty folders merely to imitate a professional project. Create an item when the work needs it. Never place a real secret in `README.md`, `.env.example`, notebook output, or Git history.

### Completion rule

Do not call a lab complete merely because code ran once. It is complete when another person can identify the goal, input, method, actual result, check, and limitation.

## 19. Guided operational micro-lab — run, vary, check, record

### 19.1 What you will build

A tiny **rule-based course-answer helper** looks up two approved demonstration answers. It does **not** train a model and does **not** understand varied language. That is useful here: we can inspect every input, result, and version before introducing AI tools.

Use any existing Python notebook that can run a cell. If you are learning with a trainer, the trainer can open the notebook while learners predict results and change one input. A **code cell** is a notebook box containing runnable program instructions; click its Run control to execute it. If no notebook is available yet, save this section and perform the same run immediately after setting up the environment in `QAI.00.06` and `QAI.01.06`. The completed run, not just reading the code, is this node's `H1` evidence.

**Scenario facts used only for this exercise:** In fictional QElight course notes, “Assignment 1 due?” has the answer “Friday, 5:00 p.m.” and “Support contact?” has the answer “Ask your course trainer.” No actual assignment deadline or contact policy is asserted here.

### 19.2 Read these code words before running

- A **variable** is a named place for a value: `question` contains the current question.
- A **dictionary** is a collection that pairs a key with a value: a question is a key, its approved answer is the value.
- `print(...)` shows text in the notebook output.
- `.get(question, fallback)` asks the dictionary for the exact question and supplies the fallback text when the question is absent.
- A **version** is a chosen name for a particular state of source data, code, or settings. `none` means this lab has no learned model.

### 19.3 Run 1: supplied code, expected result, and check

Copy this whole block into **one Python code cell** and run it:

```python
# Fictional approved facts for this exercise only.
approved_answers = {
    "Assignment 1 due?": "Friday, 5:00 p.m.",
    "Support contact?": "Ask your course trainer.",
}

data_version = "course_facts_v1"
code_version = "exact_lookup_v1"
configuration_version = "default_answer_v1"
model_version = "none"  # No trained model is used.
random_seed = "not_applicable"  # No random choice is made.

question = "Assignment 1 due?"
answer = approved_answers.get(question, "I cannot verify this from approved facts.")

print("Question:", question)
print("Answer:", answer)
print("Data version:", data_version)
print("Code version:", code_version)
print("Configuration version:", configuration_version)
print("Model version:", model_version)
print("Random seed:", random_seed)
```

**Expected output:**

```text
Question: Assignment 1 due?
Answer: Friday, 5:00 p.m.
Data version: course_facts_v1
Code version: exact_lookup_v1
Configuration version: default_answer_v1
Model version: none
Random seed: not_applicable
```

Read your **actual** output and compare each line. If the cell fails, report the complete error and the line where it occurs; do not claim the run succeeded on the basis of the expected-output box.

### 19.4 Run 2: controlled input variation

Change **only** this line in the same cell:

```python
question = "Support contact?"
```

**Predict before running:** the answer should become `Ask your course trainer.`; the recorded versions should remain the same. Run the cell. Record prediction and actual output. This is a controlled experiment because one input changed and the rest remained fixed.

**Reference explanation:** `.get(...)` finds the second key in the same two-record dictionary. It returns its paired value. No retraining occurs; `model_version` remains `none`.

### 19.5 Run 3: unsupported question and diagnosis

Now change **only** the question line to:

```python
question = "What is the exam date?"
```

**Expected answer:** `I cannot verify this from approved facts.` The question is absent, so the fallback appears. If an AI-generated guess seemed more helpful, it would still lack an approved source in this exercise.

**Failure investigation:** Change it to `"assignment 1 due?"` using a lowercase initial letter. You will also get the fallback. Why? This deliberately simple lookup needs an **exactly matching key**. You can correct the input to the approved key. Later, we will study methods that handle differently worded questions; those methods need their own checks. Do not silently edit the source facts merely to make an unsupported question appear answered.

### 19.6 Guided implementation to independent variation

Try this bounded variation without copying a completed code cell: add one fictional approved fact, `"Class mode?": "Online."`; change `data_version` to `course_facts_v2`; ask `"Class mode?"`; and predict all output lines. This is `H2` guided modification of supplied code. A fully independent build happens later when Python and project structure have been taught.

**Reference change and expected output:**

```python
approved_answers = {
    "Assignment 1 due?": "Friday, 5:00 p.m.",
    "Support contact?": "Ask your course trainer.",
    "Class mode?": "Online.",
}
data_version = "course_facts_v2"
question = "Class mode?"
```

Retain the other Run 1 lines. The answer becomes `Online.`; data version becomes `course_facts_v2`; code and configuration versions remain `exact_lookup_v1` and `default_answer_v1`. This is **not** a model update: the system's reference data changed, and the same lookup method ran again.

### 19.7 Complete reference project record

Copy the template in §18 and compare your own record to this **example of a completed record**:

```text
Project / lab name: Two-answer course helper
Date: date of my run
Goal: return an approved answer for an exact known question; use an honest fallback otherwise
Input: fictional two-record approved_answers dictionary; question string
Method: exact Python dictionary lookup with a fallback response
Environment: one working Python notebook; Python version recorded from my environment if available
Configuration: default_answer_v1; no random seed needed
Data version: course_facts_v1
Code version: exact_lookup_v1
Model version: none
Expected result: known question → approved answer; missing question → fallback
Actual result: Run 1 due answer; Run 2 trainer answer; Run 3 fallback [replace with my observed outputs]
Check performed: compared expected and actual lines after each run
Limitation / failure observed: lowercase paraphrase does not match the exact key
Next change to try: later, test a method for different wording with approved-answer checks
```

**Reproducibility check:** Another learner can use the exact Run 1 cell and obtain the same output. The record states the data/code/configuration versions and that a model and random seed are not involved. An AI service might generate varied wording across runs; there we would record its model identifier, settings, and actual outputs, then evaluate quality instead of promising identical words.

### 19.8 Completion check

Keep a notebook or script containing your executed cell, Run 1–3 outputs, and the bounded variation. Keep a short project record with expected versus actual results and the exact-match limitation. If you cannot run Python yet, carry this lab into the upcoming environment section; label it **pending execution**, not completed evidence.

## 20. What to remember

- Capability cycle: **concept → worked example → guided implementation → independent practice → project → explanation**.
- A notebook supports learning and experiments; a script supports repeatable execution; a package supports reusable organised code.
- An API is an interface/contract for software communication; it is not the model itself.
- A dataset is a defined data collection; an experiment tests a change under controlled conditions.
- An artefact is inspectable evidence of learning or development.
- Reproducibility needs recorded code, data, model, configuration, environment, and result; random seed helps control repeatable randomness.

## 21. Next connection

The next subsection, `QAI.00.06 — Working environment`, turns these habits into practical setup terms: computer, operating system, browser, terminal, editor, notebook environment, local/cloud environment, account, credential, API key, secret, and environment variable.
