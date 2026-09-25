# QAI.00.04 — System and Model Basics

> **Position in the QElight AI path**  
> `QAI.00.03 AI-domain map` → **`QAI.00.04 System and model basics`** → `QAI.00.05 Learning, implementation, and evidence habits`

## 1. Why these words matter

Later lessons will use words such as *model*, *training*, *inference*, and *generalisation* repeatedly. If they are not clear now, ML and GenAI can appear magical.

The central idea is simple:

```text
Data + method → model creation/training → model is used on a new input → output is checked and improved
```

A **model** is not the whole application. A model is one part inside a larger **system**.

## 2. One running example: course-note assistant

| Part | Example |
|---|---|
| System | the full QElight course-note assistant application |
| Data | approved notes, syllabus, learner questions, answer rules |
| Model | language model used to understand/generate text |
| Training | earlier process that created the language model from large data |
| Inference | use the already-trained model to answer one current question |
| Output | answer, citation, or safe “I do not know” response |
| Generalisation | the trained model handles a new but related input; the complete system also needs the right approved notes and checks |

**Distinction to carry forward:** A person may add a new PDF to the assistant's approved document collection. That changes what the **system can look up**; it does not, by itself, retrain the model. This matters whenever a course timetable or policy changes.

## 3. System

- **System:** connected parts that work together to achieve a goal.
- In AI, a system can include people, data, software, models, rules, tools, databases, interfaces, tests, and monitoring.

### Example: complete student-support system

```text
Student question
    ↓
Interface receives question
    ↓
System finds approved notes
    ↓
Language model prepares an answer
    ↓
System checks format/source rules
    ↓
Student sees answer or human-support handoff
```

**Remember:** the language model is a component. The full flow is the system.

## 4. Rule-based system

- **Rule-based system:** a system that applies explicit rules defined by people.
- Rule format often looks like: `IF condition THEN action`.

### Example

```text
IF learner attendance is below 75%
THEN show attendance-shortage notice.
```

### Strengths

- predictable;
- easy to inspect when the rule is simple;
- suitable for stable policies and calculations;
- no training data required for the rule itself.

### Limits

- cannot easily handle a very large number of uncertain variations;
- needs manual updates when policies change;
- may become difficult to manage when there are many interacting rules.

## 5. Learning-based system

- **Learning-based system:** a system that uses a model which learns patterns from data.
- A person does not write every decision rule directly. Instead, the model adjusts itself from examples during training.

### Example

```text
Input: many past emails labelled spam / not spam
Training result: a model that estimates the label for a new email
```

### Strengths

- can find patterns too complex to describe with fixed rules;
- works well with language, images, audio, and large data collections;
- can improve when quality data and evaluation improve.

### Limits

- result depends on data quality and relevance;
- a learned pattern can be wrong, biased, or outdated;
- it needs evaluation and monitoring;
- it may be less directly explainable than a simple rule.

## 6. Data

- **Data:** recorded information used by a system.
- Data can be numbers, rows in a table, text, images, audio, video, documents, labels, logs, or user actions.

### Data has different jobs

| Data use | Purpose | Example |
|---|---|---|
| training data | help a model learn patterns | labelled spam/not-spam emails |
| validation data | help choose/improve a model during development | held-out labelled emails |
| test data | measure final performance on unseen examples | final held-out email set |
| operational data | used while the system is running | current user question |
| reference data | source the system must use for grounded answers | current approved syllabus PDF |
| feedback data | record outcome/quality for improvement | trainer correction of an answer |

**Important:** data is not automatically correct, complete, current, permitted to use, or suitable for a task.

## 7. Model

- **Model:** a mathematical/computational pattern-making component that receives input and produces an output.
- In simple ML, a model may estimate a number or choose a category.
- In GenAI, a model may produce text, code, images, or structured output.

### Model is not a database

| Model | Database / document collection |
|---|---|
| learned behaviour/patterns | stored records/information |
| produces an estimate or generated output | returns stored/retrieved information |
| may be outdated or unsupported for a current fact | can contain current approved facts if maintained |

For reliable current answers, a GenAI application commonly needs both. **Retrieval** here means finding relevant existing documents; the model can then use the retrieved material while preparing an answer:

```text
Approved documents/database + retrieval + model + checks
```

## 8. Training

- **Training:** the development process in which a learning-based model adjusts internal values using data to reduce errors on a task.
- **Internal values:** numbers inside the model that influence how it responds. Later, these will be called *parameters*.

### Simple analogy

Training is like guided practice with many examples and corrections. The learner gradually adjusts how they respond. The model does not understand exactly like a person, but it changes internal values based on examples and an error signal.

### Example: spam model

```text
1. show an email to the model
2. model gives a guessed label
3. compare guess with known label
4. calculate error
5. adjust internal values slightly
6. repeat with many examples
```

### Two training situations in GenAI work

- **Base-model training:** a large organisation trains a foundation model using huge datasets and compute.
- **Adaptation/fine-tuning:** a team further trains an existing model for a narrower task or style.

Later, you will learn when fine-tuning is useful and when prompt design or retrieval is a better choice.

## 9. Inference

- **Inference:** use a trained model to produce an output for a new input.
- Training changes the model. Inference uses the model as it currently exists.

### Example

```text
Trained spam model + new email → spam/not-spam prediction
Trained language model + new prompt → generated answer
```

### Common operational distinction

| Training | Inference |
|---|---|
| model learns/changes | model is used as it is |
| usually needs many examples | usually starts with one current input |
| can take long and use substantial compute | expected to respond within acceptable time |
| evaluated for learning quality | evaluated for response quality, speed, cost, and safety |

**Remember:** asking an already-trained model a question is inference, not training. Changing the question, answer instructions, or attached reference document can change its immediate output without changing the model's learned internal values. We will learn how applications send such requests later.

## 10. Prediction

- **Prediction:** an output that estimates an unknown label, number, probability, or future value.
- It is common in ML.

### Examples

| Input | Prediction |
|---|---|
| house details | estimated house price |
| email | probability that it is spam |
| customer history | likely to renew / not renew |
| sales history | predicted next-month sales |

Prediction is not necessarily about the future. It can estimate an unknown present label too—for example, whether a current image contains a defect.

## 11. Generation

- **Generation:** produce new content, such as text, image, audio, video, code, or structured output.
- It is common in Generative AI.

### Examples

| Input | Generated output |
|---|---|
| “Explain loops to a beginner” | lesson explanation |
| course content + instruction | quiz draft |
| image prompt | new image |
| feature request | draft code |

### Prediction versus generation

| Prediction | Generation |
|---|---|
| usually chooses/estimates a defined output | produces a new content sequence or object |
| spam probability, price, category | paragraph, image, code, summary |
| often evaluated against known target values/labels | evaluated for relevance, accuracy, safety, quality, and format |

Technically, a generative model also predicts pieces of output step by step. Operationally, use the word **generation** when the user wants new content.

**Compare with QAI.00.02:** “What is the approved course fee?” is a **question-answering task**, even if a generative model phrases the answer. “Draft a new invitation to the course” is a **generation task**. The user-facing job and the model's internal method need not have the same name.

## 12. Generalisation

- **Generalisation:** ability to perform well on new, relevant inputs that were not exact copies of training examples.

“New” does not mean any problem in the world. The new case should be related enough to the learned task; a spam model is not expected to estimate house prices. A model that works on new, relevant examples still needs careful checking when the environment changes.

### Why it matters

A model can appear excellent if it remembers familiar examples, but fail on new situations. Useful AI must work on fresh but related cases.

### Example

```text
Training examples: “reset password”, “forgot password”, “password not working”
New input: “I cannot enter my account because I lost my login code.”

Good generalisation: identifies this as an account-access problem.
Poor generalisation: fails because exact words differ.
```

### Not the same as memorisation

| Memorisation | Generalisation |
|---|---|
| repeats familiar examples | handles new relevant variations |
| may look good on old data | is tested on unseen data |
| weak evidence of useful capability | key evidence of useful capability |

### Generalisation can fail when

- new inputs are very different from the original data;
- training data is too small, narrow, biased, or noisy;
- task rules have changed;
- the system receives missing or misleading context;
- evaluation did not represent real usage.

## 13. Complete working picture

### Rule-based fee checker

```text
Current fee data + stated policy rule
            ↓
Rule-based system
            ↓
Eligibility result
```

No model training is required if the rule is clear.

### Learning-based attendance predictor

```text
Past attendance data
            ↓
Training
            ↓
Trained prediction model
            ↓
New schedule/weather/event details
            ↓
Inference
            ↓
Predicted attendance count
```

### GenAI course assistant

```text
Approved notes + learner question + answer rules
            ↓
Retrieval and system checks
            ↓
Trained language model during inference
            ↓
Grounded answer / safe handoff
            ↓
Trainer feedback improves notes, prompts, evaluation, or system design
```

**Read the last line carefully:** fixing an inaccurate approved note improves the reference data; changing answer instructions improves the application; collecting corrected examples *may later* support training. These are different actions. Trainer feedback does not magically update a model after each user question.

## 14. Practical mapping activity

### Situation 1 — institute fee calculation

```text
Policy: 10% discount when a learner meets a stated eligibility condition.
```

- Appropriate starting approach: rule-based system.
- Why: policy is explicit; result must be predictable and auditable.
- Human role: own the policy and handle exceptions.

### Situation 2 — likely course-enrolment count

```text
Need: estimate next month’s enrolments from past data, campaign data, and calendar information.
```

- Appropriate starting approach: learning-based ML prediction, after a baseline analysis.
- Training data: past enrolment and related information.
- Inference input: next month’s campaign/calendar details.
- Output: estimated enrolment number.
- Generalisation check: evaluate on months not used during training.

### Situation 3 — QElight learner question assistant

```text
Need: answer learner questions from approved notes, without inventing course facts.
```

- Appropriate starting approach: GenAI system with approved-note retrieval, answer rules, and human correction path.
- Model role: create a clear response.
- Reference-data role: supply approved current information.
- Inference: each current learner question.
- Generalisation check: test many differently worded questions, including unclear and unsupported questions.

### Independent mental trace — classify actions before reading the solution

An institute has a trained email spam model and a course assistant using an already-trained language model. Label each event as **model training**, **model inference**, **reference-data update**, or **human/system review**. Some events include more than one activity; state the main one.

1. A developer uses 10,000 labelled emails to adjust the spam model's internal values.
2. The spam model labels a fresh email as spam.
3. Staff replace the approved course timetable PDF with the revised version; no model weights are changed.
4. A student asks the course assistant for a deadline and receives a draft answer using the current timetable.
5. The trainer checks the answer and reports that its citation does not support the date.

**Worked solution:**

| Event | Main activity | Why |
|---|---|---|
| 1 | Model training | Labelled examples are used to adjust internal values. |
| 2 | Model inference | The already-trained model processes a new input. |
| 3 | Reference-data update | The source document changed; the model was not retrained. |
| 4 | Model inference within a larger system | The current question and retrieved timetable are used to prepare an answer; whether it is correct still needs checking. |
| 5 | Human/system review | Feedback identifies a support failure; correcting a document or check is separate from changing model weights. |

**Transfer variation, with answer:** Suppose staff only change the assistant's instruction from “be concise” to “include the relevant schedule section.” Is this model training? **No.** It is an application/inference instruction change. It may improve the response, but a test must verify that the cited section genuinely supports the deadline.

### Choosing an approach from the task

| Need | Initial approach | Why and limit |
|---|---|---|
| Apply a fixed fee rule | Ordinary rule-based software | Good when policy is explicit; update it when policy changes. |
| Estimate future enrolments from historical records | Learning-based prediction if a simple comparison method is insufficient | New events or poor data can make the estimate unreliable. |
| Draft varied lesson examples from approved concepts | GenAI application with trainer review | Newly written content may contain unsupported claims. |
| Give the exact current exam date | Look up the current approved source, optionally phrase a checked answer | Generating a plausible date from model memory is unsafe. |

## 15. What to remember

- A **system** is the complete arrangement; a **model** is one component inside it.
- A rule-based system follows explicit rules; a learning-based system uses patterns learned from data.
- **Training** changes a model from examples; **inference** uses it on a current input.
- **Prediction** estimates a label, number, or probability; **generation** creates new content.
- **Generalisation** means working on new relevant cases, not merely repeating familiar examples.
- GenAI production work requires more than a model: approved data, retrieval where needed, checks, evaluation, security, and human responsibility.

## 16. Next connection

The next subsection, `QAI.00.05 — Learning, implementation, and evidence habits`, establishes how we will study and build: concept, worked example, guided implementation, independent practice, project, explanation, notebook, script, package, API, dataset, experiment, artefact, and reproducibility.
