# QAI.00.01 — Task and system basics

**Where we are:** QAI.00 Orientation → **QAI.00.01 Task and system basics** → QAI.00.02 Task types → QAI.00.03 AI-domain map.

**Target:** Given a request involving ordinary software, machine learning (ML), or generative AI (GenAI), describe the work clearly enough that another person can build and check a suitable solution. No programming knowledge is assumed here. We will write and run code after the computing and Python foundations.

## 1. The destination: from “use AI” to a checkable job

Suppose an institute says, “We need an AI chatbot.” This names a possible tool, not the job. What problem does it solve? For whom? Where may it get answers? What if it cannot find one?

A more useful request is: “Help enrolled students find answers to course questions using our approved notes. Show the supporting note. If the answer is absent or unclear, tell them and direct them to a trainer.” Now we can discuss information, steps, outputs, checks, and ownership. A chatbot *might* be the right interface, but we have not assumed that.

Our route through this section is:

1. Describe the **task** and its **goal**.
2. Name the **input**, **process**, and **output**.
3. Set a **success condition**; observe **feedback** after use.
4. Separate **human tasks** from **machine tasks**.
5. Trace examples and write one complete task record yourself.

**System**, for now, means the connected arrangement of people, information, steps, and tools that carries out a task. A system is not automatically an AI model. A calculator is a system; so is a course-question service that combines staff, approved documents, and software.

## 2. One mental model

```text
Need → task and goal → input → process → output → check against success condition
                                                ↓
                              feedback from use → possible improvement
```

The goal tells us **why** the work matters; the success condition tells us **what counts as good enough**. Feedback tells us **what happened when we tried it**. These are related but not interchangeable.

We will follow three different systems so the idea does not become “everything is a chatbot”:

| System | How it does the main work | Example of its result |
|---|---|---|
| Salary calculator | Follows an explicit calculation rule | Monthly salary total |
| Sales predictor | Uses a pattern learned from earlier examples | Estimated sales for next month |
| Course-question assistant | Drafts an answer using a question and approved material, with checks | Answer plus supporting reference, or an honest handoff |

Here **model** means a component that uses learned patterns to make a prediction or produce content. You do not need to know its internal mathematics yet. Importantly, a model can be only one component of a larger system.

## 3. The nine building blocks

### 3.1 Task — what work must be done?

A **task** is a bounded piece of work, stated as an action. “Calculate take-home pay,” “estimate next month’s sales,” and “answer a question from course notes” are tasks. “Use AI” is not a task: it says nothing about the work. “Build a chatbot” is mainly a proposed solution; it still does not tell us what the user needs the chatbot to accomplish.

| Statement | Task? | Why |
|---|---|---|
| “Use a large language model.” | No | Names a technology. |
| “Identify duplicate invoice records.” | Yes | Names work and the records involved. |
| “Help learners.” | Not yet | Too broad; we cannot tell what action or result is expected. |
| “Explain an ML term using approved beginner notes.” | Yes | Names a bounded action and source. |

**Remember:** task = what is to be done; technology = one possible way to do it.

### 3.2 Goal — why do that work?

A **goal** is the useful result intended for a person or organisation. It is not just the immediate output. “Produce a sales number” is an output; “help the shop plan next month’s stock” is a goal.

| Task | Goal |
|---|---|
| Calculate take-home pay | Give staff a correct payable amount under the approved rule. |
| Estimate sales | Help a shop plan stock with less uncertainty. |
| Explain an ML term | Help a beginner apply the idea correctly, not just read a fluent sentence. |

An answer can satisfy the task mechanically yet fail the goal: a long, accurate explanation may still be unusable for a learner who needs a small worked example.

### 3.3 Input — what is received?

An **input** is information or material supplied to begin or perform the task. Inputs can include numbers, text, images, audio, files, database records, instructions, and a user's choices.

| System | Possible inputs |
|---|---|
| Salary calculator | Base pay, allowances, deductions, approved calculation rule. |
| Sales predictor | Earlier sales, date, price, promotion details; the month to estimate. |
| Course-question assistant | Student question, approved course notes, learner level, answer rules. |

An **instruction** says what to do (“answer in simple English”). A **source document** supplies information (the syllabus PDF). Both can be inputs, but they play different roles. A **prompt** is an input containing a request or instruction for a GenAI model; not every input is a prompt.

**Failure example:** A student asks “Is the exam tomorrow?” but supplies no course or date, and the system has no current timetable. A confident date would be a guess. Missing inputs may call for a clarifying question rather than an invented answer.

### 3.4 Process — what happens between input and output?

A **process** is the sequence of actions that changes input into output. The actions can be performed by a person, fixed program rules, a learned model, or a combination.

| System | Possible process |
|---|---|
| Salary calculator | Check entries → apply approved formula → display total. |
| Sales predictor | Check supplied details → apply a trained prediction model → return estimate. |
| Course-question assistant | Read question → locate relevant approved notes → draft answer → check support → answer or hand off. |

**Rule** means an explicit instruction, such as “subtract deductions from gross pay.” A **trained model** uses patterns obtained from examples; the model is not the whole process. A course assistant also needs document access, checks, and possibly a human handoff. We will study rules, learning, retrieval, and model details in later nodes.

### 3.5 Output — what comes out?

An **output** is the observable result a process returns, creates, stores, displays, or requests. It can be a number, label, text, image, draft, recommendation, or action request.

| Task | Output |
|---|---|
| Calculate pay | A pay amount and, if needed, a breakdown. |
| Estimate sales | A numerical estimate with the specified period. |
| Identify spam | A label such as `spam` or `not spam`. |
| Answer a course question | An answer with supporting material, or “I cannot verify this from the notes.” |

**Output is not the same as outcome.** The assistant may output a beautifully written answer while the student remains confused. The goal is a useful outcome, not merely an output string.

### 3.6 Success condition — how will we decide “good enough”?

A **success condition** is a checkable standard for an output or its use. Define it before declaring the system successful. It need not be a single number; several checks may apply together.

| Vague wish | Checkable success condition |
|---|---|
| “The calculator should work.” | For supplied test payslips, the total matches the approved calculation rule. |
| “Predict sales well.” | On sales periods held aside for checking, errors are smaller than a simple agreed comparison method. |
| “Answer course questions well.” | Answer uses approved notes, shows the relevant source, and does not invent a timetable when evidence is missing. |

A **test case** is a specific input paired with the expected behaviour, used to check a success condition. A **comparison method**, sometimes called a baseline, is a simple alternative against which a more complex solution can be judged; we will implement these later. Here it is enough to understand why “sounds good” is not a complete test.

### 3.7 Feedback — what did use reveal?

**Feedback** is information received after a result is observed that can guide improvement. It may come from a user, an expert, a test, or recorded system behaviour.

| Output | Feedback |
|---|---|
| Salary total | Payroll reviewer spots a deduction applied twice. |
| Sales estimate | Actual sales later differ substantially from the estimate. |
| Course answer | Learner says the example helped but a cited paragraph does not support the claim. |

**Distinction:** “Must cite the approved syllabus” is a success condition. “Yesterday's answer cited the wrong section” is feedback. Positive feedback is useful too, but user approval alone cannot prove a factual answer was correct.

### 3.8 Human task — what must a person do or own?

A **human task** is work in which a person supplies judgement, action, or responsibility. Humans can use machines without handing over accountability for consequential decisions.

- Salary: payroll staff approve policy exceptions and final payment.
- Sales: the stock manager decides purchasing after considering the estimate and current events.
- Education: a trainer approves the course material and helps a student whose question the system cannot settle.

**Human review** means an authorised person checks and can accept, change, or reject a result. It is especially important when mistakes can seriously affect a person's health, money, rights, or opportunities. The detailed safeguards come in QAI.00.07–00.08.

### 3.9 Machine task — what can a system execute?

A **machine task** is a bounded piece of work executed by a computer, through explicit rules or a learned model.

- Apply a pay formula to valid numbers.
- Produce a sales estimate from supplied features.
- Find relevant course documents and prepare a draft answer.

**Important:** “machine task” does not mean “no human involved.” A system can calculate the pay, but a person remains responsible for approving payment. Equally, not every machine task uses AI: ordinary calculation is often enough.

## 4. Put the pieces together: one worked AI-system trace

An institute receives this question: “When is the next GenAI assignment due?”

**Scenario information:** The approved course schedule supplied to the system says “GenAI Assignment 1 — Friday, 2 October 2026, 5:00 p.m.” A learner asks from the correct course page. These are exercise facts, not a claim about any real institute.

| Part | Completed record |
|---|---|
| Task | Answer the learner's assignment-deadline question. |
| Goal | Learner knows the correct deadline and can act on it. |
| Input | Question, course identity, current approved schedule, answer instructions. |
| Process | Confirm course → find deadline in schedule → draft concise answer → check it against schedule → attach supporting section. |
| Output | “Assignment 1 is due Friday, 2 October 2026 at 5:00 p.m. [course schedule]”. |
| Success condition | Correct course, correct time and date, supported by the current approved schedule; otherwise ask or hand off. |
| Feedback | Trainer reports a mismatch if the schedule changes; learner may report confusion. |
| Machine task | Search schedule, prepare candidate answer, attach reference. |
| Human task | Course staff own schedule updates and resolve conflicts or special cases. |

**Now change one input:** The schedule is missing. What changes? The process cannot check the deadline, so a safe output is “I cannot verify the deadline from the available schedule; please check with the course staff.” The goal stays the same, but the system cannot honestly claim it has met the original answer condition. This is an **H0 mental trace**: predict what happens when an input changes and explain why.

## 5. Contrast: when AI is and is not appropriate

| Request | Reasonable first approach | Human boundary |
|---|---|---|
| Add allowances and subtract deductions | Ordinary rule-based calculation; no generative model needed. | Payroll approval and exceptions. |
| Estimate future stock demand from historical records | Consider a prediction method, then compare with a simple baseline. | Stock manager decides purchase. |
| Help students understand varied questions in course notes | Search approved material and possibly use GenAI to draft a grounded answer. | Trainer owns content and difficult answers. |
| Determine whether a student legally qualifies for a benefit | Do not let an unverified generated answer make the final decision. | Authorised people and current rules required. |

Here **grounded** means an answer is supported by supplied material, not merely plausible. We will build and evaluate document-grounded applications later. For now, focus on choosing the work and defining checks before choosing a tool.

## 6. Your turn: task-record micro-lab, with solutions

### Case A — ordinary software

“Our staff spend time adding each learner's attendance days and calculating a percentage.” Define task, goal, input, process, output, success condition, feedback, and human responsibility **before** reading the example solution.

**Reference solution:** Task: calculate attendance percentage for each learner. Goal: give staff accurate figures for follow-up. Input: approved attendance records and total scheduled sessions. Process: validate counts → divide attended sessions by scheduled sessions → multiply by 100 → display. Output: percentage and underlying counts. Success: matches hand-checked cases; zero scheduled sessions is handled explicitly rather than divided by zero. Feedback: staff correct missing entries. Human: staff maintain records and decide any action based on attendance. AI is not required for the arithmetic.

### Case B — learned prediction

“A shop wants to estimate sales for the coming month.” What is output versus goal? Name one feedback source and one human decision.

**Reference solution:** Output: estimated sales for a specified month (perhaps with a range). Goal: plan stock with fewer shortages or leftovers. Feedback: actual sales once the month ends. Human decision: purchasing manager uses the estimate alongside constraints and judgement. We cannot claim prediction quality until we compare estimates with appropriate past or future observations.

### Case C — GenAI assistance

“A student asks the course assistant to explain overfitting, but the approved notes do not cover it.” Predict a defensible process and output.

**Reference solution:** Check approved notes → establish that a supported explanation is unavailable → disclose the limitation and refer the student to the trainer or an authorised source. Do not create a confident course-specific explanation and pretend it came from those notes. Later, the trainer can add reviewed teaching material; that is feedback leading to improvement.

### Case D — spot the category error

Classify each statement: **task**, **goal**, **input**, **output**, **success condition**, or **feedback**.

1. “Student asks: What is a feature?”
2. “Answer the student's question from approved notes.”
3. “Student can correctly identify a feature in a new example.”
4. “Return a short explanation with one cited example.”
5. “For five checked questions, do not claim unsupported facts.”
6. “Trainer reports that yesterday's example was misleading.”

**Solution:** 1 input; 2 task; 3 goal; 4 output; 5 success condition; 6 feedback. Note that a real solution may specify several success conditions: factual support and evidence of student understanding are different checks.

## 7. Common confusions resolved

| Confusion | Correction |
|---|---|
| “The goal is to use ChatGPT.” | Tool choice is not the user benefit; state the useful outcome. |
| “The model is the whole system.” | People, information, software, checks, and model may all contribute. |
| “The answer was generated, so the task succeeded.” | Compare output with success conditions and real-world outcome. |
| “Feedback and success condition are the same.” | Standard is set for judgement; feedback reports what happened in use. |
| “A machine handled one step, so humans are unnecessary.” | Humans may own inputs, exceptions, policy, and final decisions. |
| “AI is necessary for any task in an AI course.” | Explicit, stable arithmetic or rules often call for ordinary software. |

## 8. What must stay in memory

- Start from **work and desired benefit**, not a product name.
- **Task:** work; **goal:** useful result; **input:** supplied material; **process:** steps; **output:** produced result.
- **Success condition:** a checkable standard; **feedback:** information from an observed result.
- **Machine work** may involve rules, learned prediction, or content generation. Those are different ways to perform tasks.
- A machine can help; a human can remain responsible.
- If necessary input or evidence is absent, an honest clarification or handoff can be better than a confident answer.

## 9. Completion evidence

Make a one-page task record for **one real, low-risk problem** that interests you. Choose a salary or attendance calculator, a small sales estimate, or a question helper. Include all nine building blocks and one “what if the input is missing?” trace. No code is required at this node.

**Self-check with the solved cases above:** Can another person tell (1) exactly what is being done, (2) who benefits, (3) what is supplied and returned, (4) how the result will be checked, and (5) who handles uncertainty and exceptions? If not, revise the record. For a sample complete record, use the assignment-deadline trace in §4.

**Next:** QAI.00.02 names different kinds of tasks—classification, numerical prediction, similarity search, translation, summarisation, question answering, and generation—so you can recognise which kind of solution is relevant.
