# QAI.00.03 — AI-Domain Map

> **Position in the QElight AI path**  
> `QAI.00.01 Task and system basics` → `QAI.00.02 Task types` → **`QAI.00.03 AI-domain map`** → `QAI.00.04 System and model basics`

## 1. Why this map comes before GenAI tools

In practice, people use words such as *AI*, *ML*, *deep learning*, *NLP*, and *GenAI* as though they all mean the same thing. They do not. We will place each word before introducing model names and tools.

This map gives each word a place. Later, when you build a project, you can say:

- what kind of problem it is;
- which AI field is relevant;
- whether a simple rule, ML model, deep-learning model, or Generative AI system is appropriate;
- what depth you need now and what can remain a supporting field.

## 2. The field map: three questions, not one rigid tree

Start with **AI as the broad field**: building systems that carry out abilities such as perception, reasoning, planning, learning, or language use. Within it, ask three different questions about a particular application:

| Question | Possible answer | What that answer tells us |
|---|---|---|
| **How does it work?** | Explicit knowledge/search/planning; machine learning; deep learning | The approach used for part of the task. Deep learning is within machine learning. |
| **What does it work with?** | Language (NLP); images/video (computer vision); sound (speech/audio AI); physical surroundings (robotics) | The input, environment, or specialty involved. |
| **What result is wanted?** | Prediction, decision support, retrieved information, generated content, or physical action | The job; Generative AI is especially relevant when new content is produced. |

**One system can have several labels.** A spoken-question assistant may hear speech (audio AI), process words (NLP), use a deep-learning model (method), and draft an answer (GenAI output). Calling it “GenAI” does not make its speech input or checks disappear.

**Important boundary:** ordinary software can also process text, images, numbers, or audio. A fixed arithmetic rule or a form that checks whether a box is empty is not automatically an AI system. We will often choose ordinary software for well-defined rules and AI methods for tasks that genuinely need them.

## 3. Artificial Intelligence — the umbrella

- **Artificial Intelligence (AI):** methods and systems that perform tasks requiring perception, reasoning, learning, language use, planning, decision support, or action.
- AI is the umbrella term for the AI methods we will study. It includes approaches that learn from data and classical approaches such as representing knowledge, reasoning, search, and planning. Merely following any fixed rule does not by itself make a calculator or form validator an AI system.

| Problem | Possible AI approach |
|---|---|
| find a route subject to constraints | search and planning; ordinary routing software may also be suitable |
| detect spam | machine learning |
| answer a question from documents | NLP + retrieval + Generative AI |
| guide a robot around obstacles | robotics + vision + planning |

**Remember:** AI does not always mean Generative AI, and AI does not always mean machine learning.

## 4. Classical / symbolic AI

- **Classical or symbolic AI:** an AI approach that represents facts, rules, possible states, or goals explicitly and uses them to reason, search, or plan. A lone `if` statement in an ordinary app does not automatically become AI.
- **Rule:** an “if this condition is true, do this action” instruction.
- **Search:** systematically explore possible steps to reach a goal.
- **Planning:** choose a sequence of actions to move from the present state to a desired state.

For a symbolic-AI example, imagine a route planner with possible locations, permitted moves, a destination, and constraints such as “this corridor is closed.” It searches possible moves and selects a permitted route. It did not learn from labelled examples merely by having such rules.

### Example

```text
Rule:
IF attendance < 75%
THEN show “attendance shortage” notice.
```

This rule is not learned from data. A person wrote it.

It illustrates an **explicit rule**. On its own this attendance check is ordinary rule-based software; a richer system that represents many facts and reasons through their implications can be called symbolic AI. Keep the distinction rather than calling every policy check AI.

### When it is a good choice

- policy is clear and stable;
- result must be predictable and explainable;
- data is limited;
- a known workflow must be followed.

### Limit

Rules become difficult to maintain when the real-world pattern is large, uncertain, or impossible to describe exactly—for example, recognising thousands of variations of a handwritten character.

## 5. Machine Learning

- **Machine Learning (ML):** a system learns patterns from examples or data instead of relying only on manually written rules.
- **Data:** recorded information used to learn, test, or operate a system.
- **Pattern:** a repeatable relationship found in data.

### Example: spam detection

Instead of writing every possible spam rule, give a learning system many emails already marked `spam` or `not spam`. It learns patterns that help it classify later emails.

| Input | Learned output |
|---|---|
| new email | spam / not spam |
| customer details | likely to renew / not likely to renew |
| house details | estimated price |

### What ML is good at

- classification;
- numerical prediction;
- anomaly detection;
- ranking and recommendations;
- clustering similar records.

### Limit

ML learns from the data it receives. Poor, biased, incomplete, or outdated data can produce poor results. It does not automatically understand truth, fairness, or business policy.

**Remember:** ML usually predicts, classifies, ranks, or detects patterns. It does not necessarily create a new paragraph, image, or code file.

## 6. Deep Learning

- **Deep Learning (DL):** a part of ML that uses neural networks with many layers to learn complex patterns.
- **Neural network:** a mathematical model made of connected computation units; during training, it adjusts internal numbers to reduce error.
- **Layer:** one stage of transformation inside a neural network.

You do not need the mathematics yet. For now, keep this intuition:

```text
simple input patterns → intermediate representations → useful output
```

Deep learning became especially useful for large, complex, unstructured data:

- language;
- images;
- speech and audio;
- video;
- large mixed datasets.

### Example

An image has many pixels. It is difficult to write enough fixed rules for every possible cat image. A deep-learning model can learn visual patterns from many examples.

### Limit

- needs suitable data, compute, and evaluation;
- can be difficult to explain completely;
- can fail when real inputs differ from training conditions;
- large models need cost, latency, privacy, and safety control.

## 7. Natural Language Processing

- **Natural Language Processing (NLP):** AI methods for working with human language—written text and, in some contexts, spoken language converted to text.
- **Natural language:** everyday human language such as English, Telugu, Hindi, or Kannada; not a programming language.

### Typical NLP tasks

| Task | Example |
|---|---|
| text classification | label a review as positive or negative |
| information extraction | find names, dates, or invoice amounts |
| translation | English ↔ Telugu |
| summarisation | shorten a document faithfully |
| question answering | answer from approved policy notes |
| sentiment analysis | identify positive/negative attitude |

NLP is an **area of AI concerned with language tasks and methods**. It can use rules, traditional ML, deep learning, or Generative AI. NLP describes the language focus; ML describes one way to implement it.

## 8. Computer Vision

- **Computer Vision (CV):** AI methods for understanding or working with images and video.
- **Image:** a grid of picture values called pixels.
- **Video:** a sequence of images over time.

### Typical CV tasks

| Task | Example |
|---|---|
| image classification | identify whether an image is a defective product |
| object detection | locate vehicles in a road image |
| image segmentation | mark the exact region of a tumour in a scan |
| optical character recognition | read text from a scanned document |
| image generation | create a new image from a text instruction; often a multimodal GenAI task linked with visual data |

**Important distinction:** computer vision commonly means *understanding an existing image*. Image generation means *creating a new image* and belongs primarily with generative image modelling; it can share visual methods and data with computer vision. Both can use deep learning.

## 9. Speech and Audio AI

- **Speech and Audio AI:** methods for working with spoken language and other sounds.
- **Speech-to-text:** convert spoken words into written text.
- **Text-to-speech:** create spoken audio from written text.
- **Audio classification:** identify an audio category, such as music, alarm, or background noise.

### Examples

| Input | Output |
|---|---|
| lecture recording | transcript |
| written lesson text | spoken lesson audio |
| customer-call audio | call summary after transcription |
| machine sound | normal / possible fault |

Speech and audio systems often combine audio processing, deep learning, NLP, and Generative AI.

## 10. Generative AI

- **Generative AI (GenAI):** AI that creates new content based on instructions, context, and learned patterns.
- It can generate text, images, audio, video, code, or structured output.
- **Foundation model:** a model trained first on broad data and then usable or adaptable for several tasks. **Pretrained** means this broad training happened before the specific task at hand. We will study what is learned and how to use it later.

### Typical GenAI tasks

| Input | Generated output |
|---|---|
| topic + learner level | lesson draft |
| course notes + question | draft answer with explanation |
| image prompt | generated image |
| requirement | draft code or structured data |
| transcript | summary, quiz, or action list |

### What GenAI is especially useful for

- draft creation;
- adaptation of tone/level/format;
- explanation and ideation;
- multi-step content transformation;
- natural-language interfaces to tools and data.

### What GenAI is not automatically good at

- guaranteed factual truth;
- current private/company information without an approved source;
- accountable high-impact decisions;
- exact calculation without validation;
- following unsafe instructions safely without design controls.

**Remember:** GenAI is a part of AI; contemporary large GenAI systems typically use deep learning. A useful GenAI application can also need ML evaluation, ordinary data systems, rules, retrieval, software engineering, and human judgement.

## 11. Robotics

- **Robotics:** design and operation of machines that sense the environment and take physical actions.
- A robot may use sensors, software, control systems, planning, vision, speech, ML, and AI.
- **Sensor:** device that receives information from the physical world, such as camera, microphone, temperature sensor, or distance sensor.
- **Actuator:** part that creates physical action, such as wheel motor, arm, or gripper.

### Example

```text
Warehouse robot
Input: camera + distance sensor + delivery request
Process: locate package → plan route → avoid obstacles
Output/action: move package to correct location
```

Robotics is included in the AI map so that you can recognise its place. It is not required for the first GenAI operational path.

## 12. One application, many fields: course-learning assistant

| Need | Relevant field/method |
|---|---|
| accept student question in English/Telugu | NLP |
| find relevant note sections | similarity search / information retrieval |
| create a clear explanation | Generative AI |
| check a fixed institute policy | ordinary rule-based software; explicit reasoning methods only if the policy needs them |
| convert lesson to speech | speech and audio AI |
| read text from a scanned handout | computer vision + optical character recognition (OCR): turn visible written characters into machine-readable text |
| monitor answer quality and update notes | data analysis and human review; ML only when a learned quality detector is actually used |

This is why “I am learning GenAI” still requires a supporting understanding of the wider AI field.

## 13. Depth decision for the GenAI path

| Field | Depth for the current GenAI operational path |
|---|---|
| AI overall | working literacy: choose and explain approaches |
| classical AI / rules / planning | working literacy, then deeper for agents/tools |
| ML | implementation depth for data, evaluation, and model workflow |
| deep learning | strong conceptual and implementation depth for neural networks and transformers |
| NLP | strong depth because language models are central to GenAI |
| computer vision | working literacy; deeper for multimodal/image projects |
| speech/audio AI | working literacy; deeper when building voice systems |
| Generative AI | primary operational mastery path |
| robotics | awareness now; specialist path only if chosen later |

## 14. Practical mapping activity

For each application, identify the main field. More than one field can be relevant; choose the primary one first.

| Application | Primary field | Supporting field(s) | Reason |
|---|---|---|---|
| detect whether a product image has a scratch | computer vision | deep learning, ML | input is an image; aim is visual understanding |
| turn a recorded lecture into searchable notes | speech/audio AI | NLP, GenAI | first convert speech to text, then process text |
| draft beginner-friendly Python examples | Generative AI | NLP, human review | creates new instructional content |
| predict attendance count for next class | ML | data analysis | output is an estimated number |
| follow a fixed fee-discount rule | ordinary rule-based software | human policy owner | policy is explicit and needs predictable behaviour; AI is unnecessary |
| answer course questions from uploaded notes | GenAI application | NLP, similarity search, rules, human review | combines retrieved evidence and generated explanation |

### Solved mapping trace: one product, several fields

**Request:** “Let a learner photograph a printed assignment page, ask a spoken question about it, and hear a short answer.”

1. **Page image:** computer vision and OCR can extract printed text; check whether names, numbers, and diagrams were read correctly. OCR means *optical character recognition*: converting visible writing in an image to usable text.
2. **Spoken question:** speech/audio AI converts speech to text; check whether the actual words were heard correctly.
3. **Meaning of question and assignment text:** NLP helps work with the words; finding a relevant approved note may involve similarity search.
4. **New explanation:** GenAI can draft an answer from the verified text and supporting notes. A deep-learning model may implement several of these steps; deep learning is a *method*, not another input type.
5. **Spoken reply:** speech/audio AI can turn checked text into audio. A trainer remains responsible for educational accuracy and for what happens when handwriting or speech is unclear.

**Changed input:** the photographed page is blurry. The first correction is to ask for a clearer image or a typed question. A fluent generated reply cannot repair missing evidence by guessing. There is no physical machine acting in this request, so robotics does not belong in the map.

### Your mapping practice, with answers

**A.** A script computes 10% of ₹500 from an approved fee rule. **Answer:** ordinary rule-based software; ₹50; this alone does not require AI, ML, or GenAI.

**B.** A system examines product photos and identifies which ones have cracks based on examples. **Answer:** computer vision is the visual field; ML is the learned method; deep learning is a possible ML method, not automatically guaranteed by the request; crack/not-crack is classification.

**C.** A student asks for three new examples of a course topic in Telugu. **Answer:** GenAI can draft new examples; NLP is relevant to the language; a trainer checks topic accuracy and Telugu clarity. If the request were to convert a *specified English paragraph* to Telugu without adding examples, translation would be the primary task instead.

**D.** A warehouse machine uses cameras to locate a box and motors to move it. **Answer:** robotics is central because it takes physical action; computer vision helps interpret camera images; planning can choose movements. No GenAI step is implied by the description.

## 15. What to remember

- AI is the umbrella; ML, deep learning, NLP, CV, speech/audio AI, GenAI, robotics, and symbolic methods have different roles.
- ML learns patterns from data; deep learning is a powerful ML approach for complex data.
- NLP works with language; CV works with images/video; speech/audio AI works with sound.
- GenAI creates new candidate content; it still needs sources, evaluation, safety, and human judgement.
- A project may combine several fields. Define the task first, then choose the fields and methods.
- For the planned learning path: understand the full map now; later build deep capability in language models and GenAI applications, supported by model evaluation and reliable operation. We will define each later technique before asking you to use it.

## 16. Next connection

The map shows the fields. Next, `QAI.00.04 — System and model basics` explains the basic working language that appears in all of them: rule-based system, learning-based system, data, model, training, inference, prediction, generation, and generalisation.
