# QAI.02.01.01 — Data and data-system basics

> QAI.01.32 Git fundamentals → **QAI.02.01.01 data and data systems** → QAI.02.01.02 table structure

## 1. Destination: describe the data before choosing a tool

Imagine a QElight course catalogue with two lessons:

| code | title | minutes |
|---|---|---:|
| QAI.01.31 | Configuration and secrets | 35 |
| QAI.01.32 | Git fundamentals | 55 |

Your job is to name one value, one field, one complete lesson record, the whole dataset, and its source. Then recognise what changes when those lessons are kept in files or a database. If you can describe these accurately, you are ready to learn table structure and SQL in the following nodes.

## 2. Start with one observation and build upward

**Data** is recorded information that can be stored, communicated, or processed. Its meaning depends on context: `35` alone does not tell you whether it means minutes, rupees, or a score. In this example it means a lesson duration in minutes.

| Smallest to largest | Example | What it means here |
|---|---|---|
| **Data value** | `35` | A particular piece of recorded information |
| **Data field** | `minutes` | A named place for one kind of information |
| **Data item** | The QAI.01.31 lesson | One thing of interest that the data describes; people sometimes use “item” for a smaller piece, so state what your item means |
| **Data record** | `QAI.01.31 / Configuration and secrets / 35` | Related field values describing one item |
| **Dataset** | Both lesson records | A collection of data chosen for a purpose |
| **Data source** | The maintained `lessons.json` file, or a course-admin system that produces it | Where the data came from; distinguish the original system from a copy exported from it |

**Connection:** a value occupies a field in a record; records make a dataset; a source supplies or maintains the data. A dataset can have other forms, such as images with labels, so “dataset” does **not** always mean spreadsheet.

### Trace it aloud

For the first row, the *item* is one lesson. Its *record* has three fields: `code`, `title`, `minutes`. The value of its `minutes` field is `35`. Both rows together form this small course dataset. If someone edits the original catalogue tomorrow, the exported copy may be older; knowing the source helps you assess that.

## 3. Data shape: structured, semi-structured, unstructured

**Structure** means how consistently the parts are organised and named so a program can find them.

| Form | Course example | What a program can locate easily | Important limit |
|---|---|---|---|
| **Structured data** | Rows with a known `code`, `title`, `minutes` layout | A title or minutes value in the agreed field | Correct layout does not guarantee a true or current value |
| **Semi-structured data** | JSON records with named keys, where some records also have `tags` or nested `speaker` details | Named parts after parsing JSON | Keys may be absent or differ; a program must validate the expected shape |
| **Unstructured data** | A free-form lesson transcript, image, or audio recording | The file itself; its meaning may require further processing | “Unstructured” does not mean without any file format, metadata, or information |

These are **descriptions of the organisation of data**, not permanent labels for filename extensions. A JSON file can hold highly regular records; a CSV file can hold inconsistent or incorrectly interpreted values. A transcript may come with structured metadata even though its main text is free form.

**Tabular data** is data laid out in rows and columns. Our table above is tabular. A CSV file is one common way to exchange tabular data. A screenshot *of* a table looks tabular to a person but its pixels do not automatically provide reliable fields to a program. “Tabular” tells you about arrangement; “structured” tells you how predictable the parts are for processing. They commonly overlap.

### Solved classification

1. A table with fields `lesson_code` and `duration` for every row → **tabular and structured**.
2. JSON lesson objects, some with an optional nested `assessment` object → **semi-structured** until you establish a consistent schema; named keys still help a program.
3. An MP3 of a class discussion → **unstructured audio** for this lesson's information task; recorded file metadata may still be structured.
4. A PDF containing a picture of the same two-column table → **visual document**, not immediately a machine-usable table; extraction and checking are needed.

## 4. Database, DBMS, and relational database

A **database** is an organised collection of data that a system can retrieve and update. A **database management system**, abbreviated **DBMS**, is the software that manages storing, retrieving, and changing database content. The *data collection* and the *software that manages it* are related but different things.

A **relational database** organises information in tables with rows and columns and can relate records in different tables using matching identifiers. For example:

| Lesson table | Instructor table | How they connect |
|---|---|---|
| Lesson `QAI.01.31` has `instructor_id = I7` | Instructor `I7` is `Priya` | Matching identifier `I7` links the lesson to its instructor |

An **identifier** is a value chosen to distinguish an item, such as `I7`. The next nodes teach tables, keys, relationships, and SQL precisely; here you only need the purpose of the link. A database can be empty and still be a database; a CSV file with rows is not itself automatically a relational database or DBMS.

**SQL** is a language often used to ask a relational database to create, find, or change data. You need not write SQL independently in this node; the tiny program below lets you see the result before learning its syntax.

## 5. Server, client, and connection

- **Database server:** a program that accepts requests to manage a database, often from other computers over a network. It can control access and serve multiple client programs.
- **Database client:** a program that asks the database system to do work. A Python application and a database administration application can both be clients.
- **Database connection:** the established access path or handle through which a client works with a DBMS. Depending on the product, it can involve a network session or an in-process library handle.

In a typical network setup, a course website's Python application sends a request through a connection to a database server, and the server returns selected records. **SQLite** is an exception to any claim that all databases need a separate server: its database engine runs inside the application process. In the next lab, Python's `sqlite3.connect(":memory:")` opens an *in-memory* relational database and gives Python a connection object. There is no separate database server, login, or network request in that demo. See the SQLite and Python references below.

### Diagnose a common mix-up

“My Python script is the database” is imprecise: the script is the program accessing the data, SQLite is the DBMS library, the in-memory lesson collection is the database contents, and the returned `connection` object is Python's handle for working with it. In a server-based system, the DBMS may be on another machine; do not carry the SQLite serverless assumption over to every relational database.

## 6. Run one micro-lab and interpret the output

Save or open the companion [demo script](QAI.02.01.01_Data_System_Demo.py). From the directory containing it, run:

```text
python QAI.02.01.01_Data_System_Demo.py
```

Use `python3` if your computer uses that command. Expected:

```text
Lesson: QAI.01.31 | Configuration and secrets | 35 minutes
Records selected: 1
```

The program creates the database in memory, inserts the **two** example lesson records, selects only the record whose code is `QAI.01.31`, and displays it. The last line counts **selected results**, not all stored lessons. Run it again: the same records are recreated, because an in-memory database does not survive the process ending.

### Make one controlled change

Change the Python input tuple for `QAI.01.31` from `35` to `40`. Run the program. Expected first line ends in `40 minutes`; the selected-record count stays `1`. That change is in your *input*, not a secret or a request to a remote service.

**What each part is doing:** `sqlite3` is the Python module for working with SQLite. `connect` creates the connection handle; `CREATE TABLE` sets up a table; `executemany` inserts two records; `SELECT` asks for one; `fetchall` retrieves returned rows; `close` closes the connection. You are only tracing this example. The SQL statements and table constraints are taught in later nodes.

## 7. Check your understanding, with answers

| Prompt | Answer and reason |
|---|---|
| What is the data field named `title` in the first example? | A named place for the lesson title. `Configuration and secrets` is its **value** for one record. |
| Are the two lesson records a dataset even if stored in a Python list? | Yes. “Dataset” describes the collection and purpose, not a required storage technology. |
| Are a JSON document and a relational database the same thing? | No. JSON is a data representation; a relational database is a managed collection organised around tables and relationships. |
| Does semi-structured mean unusable? | No. Keys and nested structure can be parsed, but the expected shape needs checking. |
| Does the SQLite demonstration require a database server? | No. SQLite runs inside this Python process; this demo uses an in-memory connection. |
| Did the program store only one lesson because it printed one? | No. It inserted two and **selected** one by code. Selection is different from storage. |

## Remember

- Value → field → record for an item → dataset; identify the source separately.
- A table is rows and columns. Data can be structured, semi-structured, or unstructured according to the question and its usable organisation.
- A database is managed data; a DBMS is the management software; a relational database links table records by identifiers.
- A client uses a connection to work with a database system. A separate server is common, but not universal.
- Never infer a dataset's truth, freshness, or completeness from its format alone.

## Primary references

- [SQLite: about and serverless architecture](https://sqlite.org/about.html)
- [Python: sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
