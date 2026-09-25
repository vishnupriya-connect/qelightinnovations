# QAI.02.01.03 — Database data types

> QAI.02.01.02 table structure → **QAI.02.01.03 database data types** → QAI.02.01.04 entities and attributes

## 1. Destination: choose the kind of value before storing a lesson

One lesson record might contain a code, duration, fee, completion ratio, publication flag, calendar date, scheduled time, update time, and an image file. These values answer different questions. A database **data type** tells the system how a value is represented and which operations make sense for it. A column's declared type should match what that field *means*, not merely what characters were typed in one example.

In this node you will classify examples, run a small database demo, change one input, and explain the important limitation: **data type behaviour depends on the database engine**. Detailed SQL table design and constraints follow later.

## 2. Numbers: counts, exact decimals, measurements

A **numeric data type** represents a number intended for numeric operations. For example, “35 minutes” may be added to another duration; the code `"035"` is an identifier and may need to stay *text*, even though its characters look numeric.

| Type | Example and suitable use | Important distinction |
|---|---|---|
| **Integer data type** | `35` minutes; `120` enrolled learners | Whole numbers, with no fractional part |
| **Decimal data type** | `299.50` rupees | For decimal quantities that require specified decimal precision, **when the chosen DBMS provides an exact decimal type** |
| **Floating-point data type** | `0.75` approximate completion ratio | Efficient approximation for real-valued measurements; many decimal fractions cannot be represented exactly in binary |

**Reason to care:** adding 10 paise and 20 paise requires an exact money rule. A system with a genuine exact-decimal database type can represent `0.10 + 0.20 = 0.30` as intended, subject to its scale/rounding rules. Binary floating-point can produce a nearby approximation. For many measured values, a small approximation is acceptable; for financial totals, decide precision, rounding, and representation deliberately.

**SQLite exception:** SQLite's ordinary `DECIMAL(8,2)` declaration has numeric *affinity*; it is **not** a promise that a value will be stored as an exact fixed-scale decimal. The micro-lab inspects its actual storage kind. For accurate money in a SQLite design, use an intentional approach such as **integer minor units** (paise) with explicit conversion, or another validated strategy. Python's `Decimal` supports decimal arithmetic, but putting a `Decimal` into SQLite does not automatically make SQLite's storage exact decimal. PostgreSQL's `NUMERIC`/`DECIMAL` is an example of an exact-decimal database type. See the product documentation at the end.

### Worked choice

For `learner_count = 42` choose integer. For a course fee of ₹299.50, choose an **exact money representation**: e.g., `29950` integer paise with a documented scale; in a DBMS with appropriate exact decimal support, a suitable exact decimal column is another option. For a rough image-quality measure, floating point may be fine. A lesson identifier such as `"0012"` is text so its leading zeros remain.

## 3. Text, characters, and binary content

A **text data type** holds characters intended to be read as words or identifiers. Examples: lesson title `"Git fundamentals"` and code `"QAI.01.32"`. **Character data types** are a family of text-column types: `CHAR(n)` commonly means a fixed-length character field, while `VARCHAR(n)` commonly means **variable-length text** up to a specified limit. Exact size rules and padding differ across database products.

Keep a phone number or postal code as text if you are not going to perform arithmetic with it; numeric-looking characters are not always numbers.

A **binary data type** holds bytes rather than ordinary readable text, for example bytes of a small image or other file. A common SQL name is `BLOB`; PostgreSQL uses `BYTEA` for binary strings. A path or URL *pointing to* an image is text, not the image's bytes. Choosing to store full media inside or outside the database involves later scale and access decisions; this node only distinguishes the value kinds.

## 4. Boolean, date, time, datetime, timestamp

A **Boolean data type** represents a yes/no state such as `published = true` or `false`. A nullable Boolean can additionally be unknown; `NULL` is not the same as false. SQLite does not have a separate Boolean storage class and commonly stores true/false as integer `1`/`0`, so its behaviour must not be assumed universal.

| Term | Example | Meaning in this lesson |
|---|---|---|
| **Date data type** | `2026-09-25` | Calendar day, without a clock time |
| **Time data type** | `10:30:00` | Clock time, without a calendar day |
| **Datetime data type** | `2026-09-25 10:30:00` | Calendar date **and** time of day |
| **Timestamp** | “Updated at 2026-09-25 10:30:00+05:30” | Commonly a recorded event time; the exact type and time-zone interpretation depend on the DBMS and column definition |

**Think about location:** 10:30 in Bengaluru and 10:30 in another time zone need not describe the same instant. An event log should state whether its timestamps include an offset or represent a time zone, and use an explicit convention such as storing instants in UTC and converting for display. A local class timetable may instead be specified as a local date/time plus time-zone rules. A text value that *looks like* a timestamp is not automatically a DBMS-enforced timestamp.

SQLite ordinarily stores date/time information using text, real, or integer values together with conventions and date/time functions; it has no separate date/time storage class. The demo stores a timestamp-like string as **TEXT**. PostgreSQL has dedicated date and time types; `timestamp without time zone` does not carry a time zone, whereas `timestamp with time zone` represents an instant interpreted with time-zone rules. Learn a provider's semantics before migrating or comparing results.

## 5. Nullability: is absence allowed?

**Nullability** is the rule about whether a column may hold `NULL`, the database marker for missing/unknown/not-applicable information. A **nullable column** permits it; a **non-null column** rejects it with a rule such as `NOT NULL`.

| Column | Proposed rule | Reason |
|---|---|---|
| `code` | Non-null | Every stored lesson must have an identifying code for this example |
| `minutes` | Nullable | The lesson exists even if duration has not been entered yet |
| `published` | Prefer non-null when the business rule requires explicit yes/no | Prevent “unknown” being silently treated as “no” |

A non-null rule merely forbids `NULL`. It does not prove that a text value is meaningful: an empty string may still pass unless separately rejected. Also, `0` is not `NULL`, and `false` is not `NULL`. In this node's demo, `code` has `NOT NULL` and a missing code is deliberately rejected; `minutes` accepts `NULL`.

## 6. Run and interpret one micro-lab

Download [the demo](QAI.02.01.03_Database_Data_Types_Demo.py) and run `python QAI.02.01.03_Database_Data_Types_Demo.py` (or `python3` on systems using that command). It uses only the Python standard library and a temporary SQLite database.

Expected output:

```text
Declared fee type: DECIMAL(8,2)
Stored fee kind: real
Stored published kind: integer
Stored update-time kind: text
Stored image kind: blob
Lesson count: 2
Lessons with NULL minutes: 1
Missing code rejected: yes
Completion ratio: 0.75
```

**Read the output in order:** the schema says `DECIMAL(8,2)`, but SQLite stored this sample fee using its `real` storage class. `BOOLEAN` was stored as `integer`; the update time was text; image bytes were a blob. Two rows exist, one missing duration is allowed, and a third row without a code was rejected. The demo shows *this inserted data under SQLite*, not a guarantee that every input value will have those storage kinds.

### One controlled variation

Change `ratio = 0.75` in the script to `ratio = 0.80`. Predict before running: all eight earlier output lines remain the same; the last line becomes `Completion ratio: 0.8` because Python's normal printed float representation does not preserve the trailing zero. Restore the value afterward. This does **not** change the declared column types.

## 7. Solved decisions and misconceptions

| Prompt | Answer |
|---|---|
| Is `"005"` suitable for an integer lesson code? | Usually no: integer conversion loses leading zeros. Keep an identifier as text. |
| Should a fee be stored in a floating-point column because it contains a decimal point? | No. A decimal point in the written value does not justify approximation for money. Choose an exact representation and rounding policy. |
| Is `NULL` in `published` the same as `false`? | No. Unknown/unset is different from an explicit false decision. |
| Does `NOT NULL` reject `""`? | No. It rejects the SQL null marker; an empty string needs a separate check if disallowed. |
| Does the word `DECIMAL` in an SQLite column guarantee exact decimal arithmetic? | No. SQLite uses storage classes and affinity; inspect/document the selected representation. |
| Is a text string `2026-09-25T10:30:00+05:30` automatically a native timestamp? | No. It can encode a time and offset, but whether a DBMS validates and interprets it as a native temporal value depends on the schema and product. |

## Remember

- Integer = whole-number count; exact decimal = deliberate decimal precision where supported; floating point = approximation.
- Text holds words and identifiers; `CHAR` and `VARCHAR` are character type families; binary holds bytes.
- Boolean = true/false; `NULL` represents absence, not false or zero.
- Date = day; time = clock; datetime = both; timestamp semantics require a time-zone convention.
- Nullable allows `NULL`; non-null rejects it but does not guarantee useful content.
- **Check the DBMS:** SQLite's declared type names can differ from the actual storage kind and from PostgreSQL's type semantics.

## Primary references

- [SQLite: data types, affinity, Booleans, and dates](https://sqlite.org/datatype3.html)
- [PostgreSQL: data types](https://www.postgresql.org/docs/current/datatype.html)
- [Python: decimal arithmetic](https://docs.python.org/3/library/decimal.html)
