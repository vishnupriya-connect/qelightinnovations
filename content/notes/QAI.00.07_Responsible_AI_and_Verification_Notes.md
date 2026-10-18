# QAI.00.07 — Responsible AI and Verification

> **Position in the QElight AI path**  
> `QAI.00.06 Working environment` → **`QAI.00.07 Responsible AI and verification`** → `QAI.00.08 AI limitations and output judgement`

## 1. Core idea

Responsible AI means designing and using AI so that people, data, rights, and decisions are treated with appropriate care.

Verification means checking whether an AI output, code result, source, or decision is good enough for its intended use.

```text
Useful AI = capable output + appropriate data use + safety controls + verification + accountability
```

An answer that sounds confident but is unsupported is not a reliable answer. A system that works technically but misuses learner data or copied material is not a responsible system.

## 2. Responsibility begins before the model call

Before giving data to an AI system or building an AI feature, ask:

1. What is the user problem and expected benefit?
2. What data is needed? Is all of it truly necessary?
3. Who owns or controls the data/content?
4. What can go wrong?
5. What harm could follow from a wrong output?
6. What checks, limits, and human responsibilities are required?
7. How will the system record and improve failures?

## 3. Privacy

- **Privacy:** appropriate control over personal or sensitive information and how it is collected, used, stored, shared, and deleted.
- **Personal information:** information that identifies or can reasonably be linked to a person.
- **Sensitive information:** information needing higher protection because misuse can cause serious harm; examples may include health, financial, identity, location, children’s, or confidential organisation information.

### Practical rule

Collect and use only the information genuinely needed for the task.

| Unsafe pattern | Better pattern |
|---|---|
| upload entire student database to a public tool for a simple lesson draft | use non-sensitive sample data or only the minimum approved fields |
| paste a learner’s personal details into a chatbot | remove identifiers; use authorised tools/processes only |
| keep every conversation forever | define retention and deletion rules appropriate to the purpose |

### For a course assistant

- do not expose one learner’s information to another learner;
- do not use private student submissions for unrelated purposes without permission;
- do not upload confidential institute/client documents to an unapproved service;
- protect logs, exports, backups, and screenshots too.

## 4. Consent

- **Consent:** meaningful agreement by a person to a stated collection or use of their information/content.
- Good consent is informed, specific to the purpose, voluntary where required, and recorded/managed appropriately.

**Do not confuse consent with every kind of permission.** A particular use may depend on authorisation from the data owner, an organisational policy, a contract, a licence, and applicable law; the correct requirements depend on the place and the purpose. Nor does a learner agreeing to recording automatically permit that recording to be uploaded to any AI provider or reused to train a model. Identify the intended use and check the applicable permission before using the data; do not assume a general “yes” covers a new purpose.

### Distinguish two questions

| Question | Meaning |
|---|---|
| Can we technically use this data? | a tool may allow upload/access |
| Do we have the right/permission to use it this way? | legal, policy, contractual, ethical, and consent question |

### Example

If recorded learner voice is to be used to improve a speech-learning feature, the use, storage, access, and purpose must be clear and authorised. Being able to copy the audio file does not establish permission to use it for model development.

## 5. Copyright and licence

- **Copyright:** legal protection commonly given to original creative works, such as text, images, music, video, code, and course material.
- **Licence:** permission/terms that state how a work, software package, dataset, model, or API may be used.

A licence can permit **some uses but not others**; possession of a copy or paid access to a course does not itself say what you may redistribute. For teaching, write your own explanation and examples, keep a record of any external material used, and check the actual terms before reproducing another person's slides, code, images, or recordings. Applicable exceptions or permissions can vary by place and use; resolve specific rights questions against the actual terms and applicable rules.

### Important distinction

| Copyright | Licence |
|---|---|
| addresses ownership/protection of a work | gives terms/permission for use |
| “Who has rights over this work?” | “What am I allowed to do with it?” |

### Practical rules

- do not copy and republish paid course material as your own;
- do not assume content found online is free to use commercially;
- check licence terms for datasets, models, code libraries, images, and APIs;
- preserve required attribution/notices where applicable;
- record source and licence in project documentation;
- use your own examples, approved material, or properly licensed material for teaching and products.

### GenAI-specific caution

Generated output can resemble protected work or contain material you should not claim as original. Review important outputs, especially for commercial, public, or client use.

## 6. Fairness

- **Fairness:** people or groups are not treated inappropriately or unjustifiably because of irrelevant or protected characteristics, or because the system design creates unequal outcomes without justification.
- Fairness depends on context. There is no single universal metric that solves every situation.

### Example risk

A screening model trained mainly on successful candidates from one past hiring pattern may unfairly disadvantage qualified people who differ from that past pattern.

### Practical controls

- define the decision purpose clearly;
- avoid using irrelevant sensitive attributes when not justified;
- inspect data coverage and missing groups;
- compare outcomes across relevant groups where appropriate and lawful;
- use human review and appeal paths for consequential decisions;
- document the intended use, limits, and known risks.

## 7. Bias

- **Bias:** a systematic tendency that can produce distorted, unfair, or consistently inaccurate outcomes.
- Bias can enter through data, labels, measurement, modelling choices, prompts, product design, or human interpretation.

### Common sources

| Source | Example |
|---|---|
| data bias | training examples underrepresent a language/accent/group |
| label bias | historical human decisions reflect unfair past practice |
| measurement bias | a score measures something different from the intended quality |
| prompt/context bias | instructions lead the model toward one-sided output |
| deployment bias | system is used for a purpose different from its tested purpose |

**Remember:** bias is not solved merely by removing one obvious column from a dataset. Relationships and historical patterns can remain.

## 8. Safety

- **Safety:** prevent or reduce unacceptable harm from an AI system’s outputs, actions, failures, or misuse.
- Safety is wider than content filtering. It includes data safety, software safety, operational safety, and decision safety.

### Safety controls for a GenAI application

Here **prompt injection** means instructions planted in lower-trust material, such as a retrieved document or message, that try to make an assistant ignore its higher-priority task rules. A document used as *evidence* must not gain authority to change who may access student records.

```text
Clear purpose and boundaries
        +
Approved data and access control
        +
Input validation and prompt-injection defence
        +
Output checks and safe fallback
        +
Human approval for consequential actions
        +
Logs, monitoring, and incident response
```

### Safe fallback

A safe fallback is a controlled response when the system lacks evidence, confidence, permission, or a valid action.

Example:

> “I do not have verified information for this question. Please check the current official notice or contact the institute office.”

This is safer than inventing an answer.

## 9. Accountability

- **Accountability:** clear ownership of decisions, actions, review, and correction when a system causes an error or harm.
- AI does not remove human or organisational responsibility.

### Questions an accountable system can answer

- Who owns this system?
- Who approved the data and purpose?
- Who can change prompts/rules/models?
- Who reviews high-impact outputs?
- How can a user report a problem?
- Who investigates incidents and fixes them?
- What record shows what the system did?

### Example roles

| Role | Responsibility |
|---|---|
| trainer/content owner | approves learning material and corrections |
| developer | implements controls, testing, logging, and fixes |
| organisation owner | defines permitted use, policies, and escalation |
| end user | uses the system within stated boundaries and reports issues |

One person may hold several roles in a small project, but the responsibilities must still be explicit.

## 10. Verification

- **Verification:** check whether something meets a stated requirement.
- Verification asks: *Does this output/system behave as expected for the stated conditions?*

### What may need verification

| Item | Example check |
|---|---|
| factual answer | compare with approved current source |
| calculation | execute calculation and test known values |
| generated code | run it in a controlled environment and test behaviour |
| retrieval result | check whether returned documents actually support the answer |
| model output format | validate required fields/schema |
| AI action | confirm permission and require approval where needed |

## 11. Source checking

- **Source checking:** inspect where information came from and whether it is authoritative, current, relevant, and correctly represented.

### Source-checking questions

1. Who created/published this source?
2. Is it primary/official or a secondary interpretation?
3. Is it current enough for the question?
4. Does it actually support the claim being made?
5. Is the source authorised for this use?
6. Can a learner/user inspect the source or citation when needed?

### Example

For current course fees, dates, eligibility, or policy, use the current official source. Do not treat a model’s general response, old screenshot, or informal message as sufficient evidence.

## 12. Code execution

- **Code execution:** run program instructions so the computer performs the specified work.
- AI-generated code is a draft, not proof that it is safe or correct.

### Never run unknown code blindly

Before executing code, inspect:

- what files it reads, writes, deletes, or uploads;
- what network/API calls it makes;
- whether it uses secrets;
- whether it installs packages or changes environment settings;
- whether it can trigger costs or external actions;
- whether it requests elevated permissions.

### Safe execution pattern

```text
Read code
   ↓
Understand intended input/output and side effects
   ↓
Run with non-sensitive sample data in a controlled environment
   ↓
Check logs/output/errors
   ↓
Add tests and limits
   ↓
Use real data/action only when authorised and necessary
```

## 13. Test case

- **Test case:** a defined input, expected behaviour/output, and result check used to verify software or an AI system.

The expected result must be determined **independently** from an approved source or requirement. Copying an AI system's answer into the “expected” column and then declaring a match does not verify truth.

### Example: course assistant test cases

| Input condition | Expected behaviour |
|---|---|
| clear question covered by approved notes | accurate answer with supporting citation |
| question not covered by notes | safe uncertainty/handoff; no invented fact |
| prompt asks to ignore source rules | keep source rules; do not reveal restricted information |
| sensitive personal information appears | avoid exposing it; follow access/privacy rule |
| malformed request | show helpful error rather than crash |

### Why test cases matter for GenAI

The same prompt can give variable output, and real users ask unexpected questions. Test cases make expected behaviour visible and allow improvement over time.

## 14. Human review

- **Human review:** a responsible person checks, approves, corrects, or rejects an AI output/action.
- Human review is especially important where error impact is high, policy is unclear, personal data is involved, or the system takes an external action.

### Human review is not “look at everything forever”

Design it proportionally.

| Situation | Appropriate review level |
|---|---|
| draft teaching example | trainer checks before sharing as official material |
| current institute policy answer | source-based check; escalate uncertainty |
| medical/legal/financial individual advice | qualified professional review; do not rely on general AI answer |
| agent wants to send email or change records | human approval before action |
| low-risk internal formatting task | automated checks plus occasional review may be enough |

## 15. One responsible GenAI workflow

### Example: QElight course-note assistant

```text
Define purpose: answer course questions from approved QElight notes
        ↓
Use minimum permitted content; record source and version
        ↓
Retrieve relevant approved material
        ↓
Generate answer within stated rules
        ↓
Validate format, citations, access, and known risk cases
        ↓
Show safe fallback when evidence is missing
        ↓
Log non-sensitive operational evidence and collect corrections
        ↓
Content owner reviews improvements and changes
```

### Responsibility table

| Concern | Practical control |
|---|---|
| privacy | use minimum data; restrict access; avoid unnecessary uploads/logging |
| consent | make intended use clear; obtain/record permission where required |
| copyright/licence | use approved/licensed sources; keep source/licence record |
| fairness/bias | inspect data/prompt/outcomes; do not use untested system for consequential judgement |
| safety | boundaries, validation, fallback, approvals, incident path |
| accountability | named owner, change record, feedback/correction path |
| verification | citation/source check, test cases, code/output checks, human review |

## 16. Reusable responsible-use record

Complete this before sharing, deploying, or relying on an AI-assisted result.

```text
System / task:
Intended user and allowed use:
Decision impact: low / medium / high
Input data: what is used; whether it contains personal, confidential, or copyrighted material
Permission / licence basis:
Likely harm if wrong, unfair, exposed, or misused:
Controls: source restriction, redaction, access control, human approval, refusal, fallback
Verification method: source check / test case / calculation / human review
Named accountable person:
Known limitation and user-facing warning:
```

### Minimum risk decision

| Situation | Minimum action |
|---|---|
| public, low-impact draft | label as draft; review before publishing |
| personal/confidential input | remove or mask it unless use is authorised and protected |
| factual or policy answer | use approved current source and record it |
| code that changes data or service | test safely before use; retain a rollback path |
| health, legal, financial, employment, education-selection, or safety decision | qualified human owns the final decision; AI output is supporting material only |

### Important distinction

A disclaimer does not make an unsafe system responsible. Responsibility means changing the design, data, access, review, and release decision before harm occurs.

## 17. Guided verification lab — a claim, a source, a check

This lab uses **fictional course information** and the simple dictionary lookup introduced in QAI.00.05. It demonstrates an applied check; it is not a deployed safety system. A learner who has not yet opened Python can predict outputs now and run the cell after setting up the notebook in QAI.00.06/QAI.01.06.

### 17.1 Define the trusted exercise source and test cases

The fictional, approved source `course_schedule_v1` contains exactly one fact:

```text
Assignment 1 due? → Friday, 5:00 p.m.
```

The task is to answer a learner's deadline question. Do not add real learner names, marks, recordings, or private messages. A **test case** pairs a question with an expected answer based on this source; `PASS` means the software matches that expectation, not that the source itself is guaranteed correct in real life.

| Test case | Question | Expected result | Reason |
|---|---|---|---|
| known | `Assignment 1 due?` | `Friday, 5:00 p.m.` | approved exercise source contains answer |
| absent | `What is the exam date?` | `I cannot verify this from approved facts.` | exercise source has no exam date |
| changed wording | `When is Assignment 1 due?` | same fallback | exact-match program cannot infer synonyms |

### 17.2 Run one check and predict a variation

Copy this block into one Python code cell and run it. `==` compares two values and produces `True` or `False`.

```python
# Fictional, approved exercise source. No personal data or model-provider key.
approved_answers = {"Assignment 1 due?": "Friday, 5:00 p.m."}
source_version = "course_schedule_v1"

question = "Assignment 1 due?"
expected = "Friday, 5:00 p.m."
actual = approved_answers.get(question, "I cannot verify this from approved facts.")

print("Source:", source_version)
print("Expected:", expected)
print("Actual:", actual)
print("Pass:", actual == expected)
```

**Expected output:**

```text
Source: course_schedule_v1
Expected: Friday, 5:00 p.m.
Actual: Friday, 5:00 p.m.
Pass: True
```

For the *absent* test, change only `question` to `"What is the exam date?"` and `expected` to `"I cannot verify this from approved facts."`. Predict `Pass: True`, then run the cell. This tests the safe fallback, not a fabricated exam date. For the *changed wording* case, ask `"When is Assignment 1 due?"`; the expected answer for this exact-match implementation is the fallback. Its limitation should be recorded, not hidden.

**Deliberate failed check:** leave the approved source as Friday but set `expected = "Saturday, 5:00 p.m."`. The result is `Pass: False`. Investigate which item is wrong before changing anything: in this fictional case the expected value is unsupported, so correct the test expectation from the source. Never edit the approved source to make a bad expectation pass. For a real project, the content owner would resolve any disagreement about the source itself.

### 17.3 Complete the responsible-use record

```text
System / task: fictional course-deadline helper
Intended user and allowed use: answer one course question from an approved exercise schedule
Decision impact: limited classroom exercise; a real deadline error could still mislead learners
Input data: question and one fictional deadline; no real personal data
Permission / licence basis: original exercise facts made for this lab; no external material uploaded
Likely harm if wrong, unfair, exposed, or misused: learner may miss a real deadline if demo content is presented as current fact
Controls: mark facts as fictional; check against course_schedule_v1; return fallback on missing answer
Verification method: known, missing, and changed-wording test cases; compare expected with actual
Named accountable person: trainer/content owner for any real institute adaptation
Known limitation and user-facing warning: exact question match only; this is not a real timetable
```

**Your evidence:** record your observed output for the three tests, the deliberate failure and its cause, the source version, and the completed risk record. If the environment is unavailable, label the code run pending and perform the trace with the shown expected answers; do not present predictions as executed results.

**What this does and does not show:** the exercise demonstrates source checking, test cases, code execution, and human ownership at a small scale. Later production work must add access control, privacy review, broader evaluation, monitoring, incident response, and review of actual rights and policies.

## 18. What to remember

- Responsible AI is part of system design, not a final disclaimer.
- Privacy: use the minimum permitted data and protect it through its full lifecycle.
- Consent: technical access is not the same as permission to use data/content.
- Copyright and licence: check rights and terms before using, publishing, or commercialising material.
- Fairness and bias: inspect data, context, outcome, and use—not only the model.
- Safety: define limits, checks, fallback, approvals, and incident handling.
- Accountability: people/organisations remain responsible for the system.
- Verify important outputs with sources, code execution, test cases, and appropriate human review.

## 19. Next connection

The next subsection, `QAI.00.08 — AI limitations and output judgement`, explains why verification is necessary: hallucination, outdated knowledge, missing context, prompt sensitivity, uncertainty, fact, evidence, inference, assumption, recommendation, and high-impact decisions.
