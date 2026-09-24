# QAI.00.02 — Task Types

> **Position in the QElight AI path**  
> `QAI.00.01 Task and system basics` → **`QAI.00.02 Task types`** → `QAI.00.03 AI-domain map`

## 1. Destination of this subsection

After this subsection, you should be able to hear a problem statement and identify its primary task type:

- classification;
- numerical prediction;
- similarity search;
- translation;
- summarisation;
- question answering;
- generation.

This skill matters because **the task type comes before the model, tool, library, or project design.** A wrong task definition produces the wrong solution even when the code works.

## 2. One decision map

Ask **what the user needs the output to do**, then what form it takes. Output form is a useful first clue, not a complete definition: an invoice *total* is a number but ordinarily a calculation, not a prediction; a written *answer* may be question answering even if a generative model writes its words.

```text
Required output?
├─ One label/category              → classification
├─ One number                      → numerical prediction
├─ Most related item(s)            → similarity search
├─ Same meaning in another language→ translation
├─ Shorter faithful version         → summarisation
├─ Answer to a question             → question answering
└─ New content                     → generation
```

Some real systems combine task types. First name the **main task**, then name supporting tasks.

**Prerequisite vocabulary:** A **label** is a name selected for an item, such as `spam`. An **estimate** is an uncertain numerical guess about something not directly known, such as future sales. A **source** is the existing material from which information can be obtained. A **draft** is newly composed content that needs review where factual accuracy matters.

**First filter:** If a fixed rule can calculate an exact result from complete inputs, state *calculation* before selecting any AI task type. The seven types below are a map of common AI/data tasks, not a claim that every real task is one of seven AI tasks.

Example: a course-document assistant may use similarity search to find notes, question answering to respond, and generation to write the answer. Its user-facing main task is usually **question answering**.

## 3. Atomic task types

### 3.1 Classification

- **Classification:** assign an input to one category from a defined set of categories.
- Output is a **label**, not a newly written answer.

| Input | Possible output labels |
|---|---|
| email | spam / not spam |
| customer review | positive / neutral / negative |
| transaction | normal / suspicious |
| image | cat / dog / other |

#### Key idea

The categories are decided before the system runs. The system chooses among them.

#### Example

Task: classify a support ticket.

```text
Input: “I cannot reset my password.”
Output label: account-access
```

#### Misconception guard

- “Write a polite reply to this support ticket” is **generation**, not classification.
- “Is this review positive or negative?” is classification because the labels are fixed.

### 3.2 Numerical prediction

- **Numerical prediction:** estimate a number from available information.
- Output is a measurable quantity.

| Input | Predicted number |
|---|---|
| house details | estimated price |
| past sales and date | next week’s sales |
| study activity | expected score |
| delivery details | expected delivery time in minutes |

#### Key idea

The output can take many numerical values, such as `47.5`, `₹6,25,000`, or `18 minutes`.

#### Example

```text
Input: past three months of course enrolment, campaign status, month
Output: estimated enrolments next month = 82
```

#### Misconception guard

- “Will the customer leave: yes or no?” is classification.
- “How likely is the customer to leave: 0.72?” is a numerical score/probability estimate. A system may use that score to assign a final `likely to leave` / `not likely to leave` label; the final label is classification. A probability score is not the same thing as a predicted amount such as sales revenue.
- A number is not automatically a fact; it is an estimate and must be evaluated.
- “What is 20% of ₹1,000?” returns a number but is an exact calculation, **not** numerical prediction. Its answer is ₹200 when the inputs and rule are correct.

### 3.3 Similarity search

- **Similarity search:** find items that are most related to a given item or query.
- Output is a ranked list of existing items.

| Query | Similarity-search output |
|---|---|
| “How do I reset password?” | most relevant help articles |
| photo of a product | visually similar products |
| student question | most relevant course-note sections |
| song clip | similar songs/audio records |

#### Key idea

When configured for meaning-based matching, the system can find related items even without identical words. Simple keyword matching, by contrast, relies more heavily on overlapping words. Both can be useful retrieval methods. **Similarity is not proof of factual correctness**: a related document can be outdated or irrelevant to the user's exact question.

#### Example

```text
Query: “How can I change my account password?”
Retrieved document: “Password reset and account recovery procedure”
```

#### Misconception guard

- Search retrieves existing information.
- Generation creates new content.
- Retrieving a similar passage is **not yet** answering the question; verify whether the passage actually contains the answer and is an approved/current source.
- A reliable course assistant often performs similarity search first and generation second.

### 3.4 Translation

- **Translation:** express the same meaning in another language.
- Goal: preserve meaning, tone, and important details as far as possible.

| Input | Output |
|---|---|
| English instruction | Telugu instruction with same meaning |
| customer message in Hindi | English version for support staff |
| technical note | Kannada learner-friendly version |

#### Key idea

Translation changes language, not the intended meaning.

#### Example

```text
Input: “Please submit the form before Friday.”
Output: “దయచేసి శుక్రవారం లోపు ఫారమ్ సమర్పించండి.”
```

#### Misconception guard

- Translation is not summarisation: it should not remove important details.
- Translation is not explanation: it should not add new teaching material unless requested.
- “Rewrite this in simpler English” is simplification within one language, not translation into a different language.

### 3.5 Summarisation

- **Summarisation:** create a shorter version that preserves the important content of a larger input.
- Goal: reduce length without changing the essential meaning.

| Input | Output |
|---|---|
| long meeting transcript | decisions, owners, deadlines |
| lengthy policy | short policy brief |
| chapter | key concepts and sequence |

#### Key idea

Summarisation answers: “What are the important points here?”

#### Example

```text
Input: 10-page project meeting notes
Output: “Release delayed by one week. Priya owns testing. API issue needs review by Friday.”
```

#### Misconception guard

- A summary must remain faithful to the source.
- “Write a new proposal based on these notes” is generation, not only summarisation.
- A shorter answer is not always a good summary; omitted decisions can make it useless.
- If a meeting never assigned an owner, the summary must not invent one to fill a neat template.

### 3.6 Question answering

- **Question answering:** provide an answer to a stated question.
- The answer may come from supplied documents, a database, general model knowledge, calculations, or a tool.

**Question answering names the user's job, not the implementation.** A person, a rule-based program, a database lookup, or a generative model may help produce the answer. The system must still define its approved source and how to behave when the source does not support the answer.

| Question | Desired answer |
|---|---|
| “When does the course start?” | start date from approved schedule |
| “What is a vector database?” | clear explanation at learner level |
| “What was last month’s sales?” | value from the authorised data source |

#### Key idea

Question answering is defined by the user’s question. The important design choice is **where the answer is allowed to come from**.

#### Example

```text
Question: “What documents are required for admission?”
Answer source: current approved admissions checklist
Output: list of documents with source reference
```

#### Misconception guard

- A fluent answer can still be unsupported or wrong.
- For institute, company, legal, medical, or current information, define the approved evidence source and the safe fallback: “I do not have verified information; please contact …”

### 3.7 Generation

- **Generation:** create new content from instructions and available context.
- Output may be text, image, audio, video, code, or structured data.

| Instruction/context | Generated output |
|---|---|
| lesson objective + student level | draft lesson explanation |
| product brief | marketing draft |
| prompt + image settings | new image |
| code requirement | draft Python function |

#### Key idea

Generation creates a new candidate output. It can be useful, creative, and fast, but needs checking when accuracy or safety matters.

#### Example

```text
Instruction: “Create three beginner examples of classification for an institute class.”
Output: three drafted examples
```

#### Misconception guard

- Generation is not guaranteed truth.
- Generation is not the best first choice when the required answer already exists in an approved database or document.
- “Generate a summary” uses generation as an implementation method, but the user’s task type is summarisation.
- “Write the official fee deadline” is not permission to invent one. If a definite fact is requested, look up the authorised source; the visible task is question answering, and generated wording is only a possible implementation step.

## 4. Quick comparison table

| Task type | Primary output | Main question it answers | Example |
|---|---|---|---|
| Classification | label/category | “Which group does this belong to?” | spam or not spam |
| Numerical prediction | uncertain numeric estimate | “How much / how many / how long, when the amount is not known yet?” | next month sales |
| Similarity search | ranked existing items | “What is most related?” | relevant course section |
| Translation | same meaning, different language | “How is this said in another language?” | English → Telugu |
| Summarisation | shorter faithful content | “What matters most?” | meeting brief |
| Question answering | answer to a question | “What is the answer?” | eligibility criteria |
| Generation | new content | “Create something fitting this instruction.” | draft lesson note |

## 5. Worked example: a course-learning assistant

### User request

> “I am a beginner. Explain tokenisation using the approved course notes, give one example, and prepare three quiz questions.”

### Task decomposition

| Part | Task type | Why |
|---|---|---|
| locate relevant course notes | similarity search | find existing relevant information |
| explain tokenisation from those notes | question answering | answer the learner’s question with evidence |
| create a beginner-friendly example | generation | create a new example suited to the learner |
| prepare three quiz questions | generation | create new assessment items |
| verify the explanation | human review / evaluation | prevent unsupported or unclear teaching content |

**Important:** one user request can contain several task types. The correct design connects them in the right order.

### One complete input-to-output trace

Suppose the approved notes contain a paragraph explaining that **tokenisation** splits text into smaller pieces for a language-processing system. A learner asks, “What is tokenisation? Give an example and three practice questions.” You need not learn tokenisation yet; watch how we identify the jobs in this request.

1. **Input:** learner question, approved notes, learner level. The learner level changes *how* to explain, not what the note says.
2. **Similarity search (supporting task):** locate the relevant existing paragraph. A related paragraph about *text cleaning* is not enough merely because it shares some words.
3. **Question answering (main task):** prepare an explanation based on the paragraph, retaining its meaning. If the paragraph is absent, disclose that limitation instead of pretending to cite it.
4. **Generation (supporting task):** draft a new illustration—such as splitting “I like tea” into smaller text pieces—and three new practice questions.
5. **Check:** verify the explanation against the source and verify each practice question has a correct answer. The trainer decides whether it is suitable for students.
6. **Output:** supported explanation, clear example, three reviewed questions, and source reference; otherwise an honest uncertainty response.

**Change one input (mental trace):** The question now asks for a course examination date, but no current approved schedule is supplied. The main task is still question answering; the safe result changes to “I cannot verify the date from the available material.” Writing a plausible date is not an acceptable substitute.

### Distinguish a user-facing task from its supporting steps

| User asks for | Main task | Possible supporting step | What to check |
|---|---|---|---|
| “Which queue should receive this complaint?” | Classification | Read ticket text | Label belongs to approved queue list. |
| “What will demand be next month?” | Numerical prediction | Prepare historical records | Estimate compared with observed demand later. |
| “Show related course sections.” | Similarity search | Prepare searchable notes | Returned sections actually concern the topic. |
| “What does the approved timetable say about Monday?” | Question answering | Retrieve timetable | Date/version and cited passage support answer. |
| “Create a first draft of a workshop invitation.” | Generation | Refer to supplied event details | No invented time, price, or speaker. |

## 6. Hands-on micro-lab — identify the task type

For each statement, choose the primary task type. Answers follow immediately below.

1. “Place each incoming ticket into billing, account access, technical issue, or other.”
2. “Estimate how many students will attend tomorrow’s live class.”
3. “Find the five course-note sections closest to this student question.”
4. “Convert this Telugu notice into English without changing its meaning.”
5. “Reduce this 40-minute meeting transcript to decisions and action items.”
6. “Answer: What is the fee-payment deadline in the approved notice?”
7. “Draft a polite reminder message for students who have not submitted the assignment.”

### Solutions

| No. | Primary task type | Reason |
|---|---|---|
| 1 | classification | choose one fixed ticket category |
| 2 | numerical prediction | output is an estimated count |
| 3 | similarity search | retrieve related existing note sections |
| 4 | translation | preserve meaning in another language |
| 5 | summarisation | produce shorter faithful content |
| 6 | question answering | answer a stated question from approved evidence |
| 7 | generation | create a new message |

## 7. Hands-on micro-lab — choose the safer first approach

| Situation | Better first approach | Why |
|---|---|---|
| student asks for the exact current examination date | question answering from official/current schedule | accuracy matters; do not rely on general model memory |
| team wants a first draft of a workshop invitation | generation | new wording is needed; human can review it |
| institute has 10,000 past questions and wants related questions for practice | similarity search | find relevant existing material first |
| finance team wants next-month revenue estimate | numerical prediction | output is a number based on historical data |
| support team wants to route messages quickly | classification | each message must enter a known queue |

## 8. What to remember

- Task type is chosen from the **required output**, not from the tool name.
- Categories → classification.
- Number → numerical prediction.
- Related existing item → similarity search.
- Same meaning in another language → translation.
- Shorter faithful content → summarisation.
- Answer to a stated question → question answering.
- New content → generation.
- Real GenAI systems commonly combine similarity search, question answering, generation, checks, and human review.

## 9. Solved knowledge check

### Question 1

“Find the most relevant policy sections, then write a two-paragraph response to the employee.” What are the two main task types?

**Solution:** similarity search, then generation. If the response must answer a specific policy question, question answering is also part of the system.

### Question 2

Why is “answer from the current approved fee document” not safely solved by generation alone?

**Solution:** the required information already exists and can change. The system should retrieve/check the current approved document; generation may only help phrase the answer.

### Question 3

“Predict whether a student will pass” and “predict the student’s final mark” use different task types. Name them.

**Solution:** pass/not pass is classification. Final mark is numerical prediction.

### Question 4

What is the primary task type of “write a 100-word summary of this article in Telugu”?

**Solution:** summarisation plus translation. The main goal is a shorter faithful version; the output language adds translation.

## 10. Evidence gate before QAI.00.03

Create a one-page **Task-Type Map** for one future QElight/Trishana application.

Use this template:

```text
Application name:
User problem:
Primary task type:
Supporting task types:
Input:
Output:
Approved source / data:
Main error risk:
Human review or approval needed:
```

### Reference answer

```text
Application name: QElight course-note assistant
User problem: learner cannot quickly find a correct explanation in course notes
Primary task type: question answering
Supporting task types: similarity search; generation
Input: learner question; approved notes; learner level
Output: cited explanation, example, and safe uncertainty response
Approved source / data: versioned QElight course notes
Main error risk: unsupported or outdated answer
Human review or approval needed: trainer reviews corrected content and high-impact guidance
```

## 11. Next connection

You now know *what a system may do*. Next, `QAI.00.03 — AI-domain map` shows the major fields used to solve different task types: AI, ML, deep learning, NLP, computer vision, speech/audio AI, Generative AI, and robotics.
