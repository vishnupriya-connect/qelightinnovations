# QAI.02.01.04 — Entities and attributes

> QAI.02.01.03 database data types → **QAI.02.01.04 entities and attributes** → QAI.02.01.05 keys and row identity

## 1. Destination: decide what the course database describes

A QElight enrolment system needs to answer: *Which learners are in which courses? How many places remain?* Before making tables, identify the things worth recording, the facts about each thing, and the connections between things.

The same small example runs through this node:

- Learner `L1`: **Anu**, living in Bengaluru; interests: Python and SQL.
- Learner `L2`: **Ravi**, living in Mysuru.
- Course `C1`: **AI Foundations**, capacity **3**.
- Course `C2`: **Git Basics**, capacity **2**.
- Enrolments: Anu in both courses; Ravi in AI Foundations.

Run the [companion demo](QAI.02.01.04_Entities_and_Attributes_Demo.py) once, change one course capacity, and explain its output. Defining database keys and enforcing relationships comes in the next nodes.

## 2. From a real-world object to an entity

A **real-world object** is something the system cares about: a person, course, product, or event. It need not always be a physical object; a class enrolment is an event or connection we may also need to record.

An **entity** is a distinct thing or occurrence represented in our model. An **entity type** names the kind of thing, such as `Learner` or `Course`. An **entity instance** is one specific example of that type: learner `L1`, Anu; or course `C1`, AI Foundations.

| Question | Answer in this example |
|---|---|
| What kind of thing is being described? | `Learner` is an entity type. |
| Which exact thing? | Anu (`L1`) is an instance of Learner. |
| Is `"Bengaluru"` another learner? | No. It is an attribute value describing Anu's city. |
| Is `Course` the same as `AI Foundations`? | No. `Course` is the type; `AI Foundations` is one instance. |

**Mental model:** entity type = the kind of folder; entity instance = one named item in it; an attribute = a fact recorded about that item. This is a modelling aid, not a requirement to make a separate folder on your computer.

## 3. Attribute and attribute value

An **attribute** is a property of an entity type. For `Learner`, useful attributes could be `learner_id`, `name`, and `city`. An **attribute value** is the specific content for one instance: Anu's `city` has value `Bengaluru`.

For a `Course`, `capacity` is an attribute; its value for AI Foundations is `3`. Saying “capacity” without a course tells you which *kind* of data; saying “3” without the attribute does not tell you whether it is capacity, credits, or days.

Do not collect an attribute simply because it is available. Choose what you need for a stated task, check the source and accuracy, and protect personal information such as a learner's address.

## 4. Five ways to think about attributes

These labels answer different questions; **one attribute can fit more than one label**.

| Term | Small course example | What question does it answer? |
|---|---|---|
| **Simple attribute** | `city = Bengaluru` | Do we treat this value as one unit for this task? |
| **Composite attribute** | `address = {city: Bengaluru, postal_code: 560001}` | Do we need meaningful component parts? |
| **Single-valued attribute** | Anu's `name = Anu` in this simplified model | Do we record one value per instance? |
| **Multi-valued attribute** | Anu's `interests = {Python, SQL}` | Can this instance have several values of this kind? |
| **Derived attribute** | `available_seats = capacity − number_of_enrolments` | Can we calculate the value from other recorded facts? |

**Simple/composite depends on use:** `address` may be treated as one text string for display; if you need city-based reporting, modelling `city` and `postal_code` separately is more useful. Even `name` can be broken down for a particular task; the “simple” label is not an eternal property of a word. Do not assume a person's name can always be split reliably into first and last parts.

**Single/multi-valued is a separate axis:** a simple `city` may be single-valued in this model; interests may be multiple. One person could have multiple addresses if the product really needs that. “Two words in a text value” does **not** automatically mean two separate attribute values.

**Derived value can become stale:** C1 has capacity 3 and two enrolments, so available seats = `3 − 2 = 1`. If you store `1` separately and then enroll someone else, you must update it. Computing it from current enrolment records avoids that inconsistency for this simple model. Real booking needs additional rules for cancellations and concurrent requests, covered later.

## 5. Entity tables and a relationship table

An **entity table** stores instances of one entity type:

**`learners` entity table**

| learner_id | name | city |
|---|---|---|
| L1 | Anu | Bengaluru |
| L2 | Ravi | Mysuru |

**`courses` entity table**

| course_id | title | capacity |
|---|---|---:|
| C1 | AI Foundations | 3 |
| C2 | Git Basics | 2 |

A **relationship table** records an association between entities. Our `enrolments` table says which learner joined which course:

| learner_id | course_id |
|---|---|
| L1 | C1 |
| L1 | C2 |
| L2 | C1 |

Matching `L1` to the learner table and `C1` to the course table lets us say “Anu is enrolled in AI Foundations.” The `enrolments` table should not need to copy Anu's city or the course title into every row just to identify the association. The exact identity, uniqueness, and reference-enforcement rules come in QAI.02.01.05 and QAI.02.01.06.

**Caution:** the demo constructs these three tables and finds matches, but deliberately does **not** claim the database enforces every enrolment rule yet. For example, without an appropriate rule it could admit a learner ID that has no matching learner. That is a design issue addressed when learning keys and constraints.

When a learner has several interests, you can *conceptually* show them as a set in a diagram. In a relational design you may use a separate `learner_interests` table if those interests must be searched and managed individually; putting comma-separated values in one text field would make that harder. The demo displays the conceptual list separately rather than claiming that the `learners` table has a multi-valued column.

## 6. Run a micro-lab and change one fact

Run `python QAI.02.01.04_Entities_and_Attributes_Demo.py`, or `python3` if your computer uses that command. The script creates an in-memory SQLite database and prints:

```text
Entity type: Learner
Entity instance: L1 | Anu | Bengaluru
Composite address parts: Bengaluru, 560001
Multiple interests: Python, SQL
Entity tables: learners, courses
Relationship table: enrolments
Enrolled in C1: Anu, Ravi
Available seats in C1: 1
```

First explain why `Anu` is an instance and `Bengaluru` is an attribute value. Then find the two records in `enrolments` whose `course_id` is `C1`; there are two, so capacity 3 leaves one seat.

### Controlled variation, with answer

Change only the `C1` course-capacity tuple from `3` to `4` in the script and run again. **Expected:** all lines above remain the same except `Available seats in C1: 2`. Neither learner identity nor enrolment count changed. Restore the original number afterward.

## 7. Solved classification

| Prompt | Answer and reason |
|---|---|
| “Ravi” is what? | An attribute value (`name`) for learner instance `L2`. Ravi is also how we refer to that instance in ordinary language. |
| “Course” versus “Git Basics”? | `Course` is an entity type; Git Basics (`C2`) is one course instance. |
| Is `postal_code` a second person? | No. It is a component of a composite address in this design. |
| Can `city` be both simple and single-valued? | Yes; “how many parts?” and “how many values for one learner?” are separate questions. |
| Is `available_seats` derived? | Yes; it can be calculated from the recorded capacity and the number of relevant enrolments. |
| Where should “Anu joined AI Foundations” go? | Into the `enrolments` relationship table as `L1 / C1`; the learner and course descriptions stay in their entity tables. |
| Is an `enrolments` row automatically valid just because its two IDs are present? | No. The IDs must correspond to legitimate instances, and an intended uniqueness rule may be needed; later nodes teach enforcement. |

## Remember

- Entity type names a kind of thing; entity instance identifies one particular thing.
- Attribute names a fact; attribute value supplies it for an instance.
- Simple/composite concerns parts; single/multi-valued concerns how many values; derived means calculated.
- Entity tables describe things; a relationship table records links among things.
- A model is chosen for the task. Recheck privacy, missing information, and rule enforcement before using it as a real enrolment system.

## Primary references

- [PostgreSQL: table relationships and constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Microsoft EF Core: mapping many-to-many relationships with a join table](https://learn.microsoft.com/en-us/ef/core/modeling/relationships/many-to-many)
