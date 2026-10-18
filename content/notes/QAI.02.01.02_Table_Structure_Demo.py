"""Inspect one tiny table's columns, records, nulls, and repeated rows."""

import sqlite3


def main():
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE lessons (code TEXT, title TEXT, minutes INTEGER)")
        rows = [
            ("QAI.01.31", "Configuration and secrets", 35),
            ("QAI.01.32", "Git fundamentals", 55),
            ("QAI.02.01.02", "Table structure", None),
            ("QAI.01.31", "Configuration and secrets", 35),
        ]
        connection.executemany(
            "INSERT INTO lessons (code, title, minutes) VALUES (?, ?, ?)",
            rows,
        )
        columns = [info[1] for info in connection.execute("PRAGMA table_info(lessons)")]
        stored = connection.execute("SELECT code, title, minutes FROM lessons").fetchall()
        repeated = len(stored) - len(set(stored))
        print("Table: lessons")
        print("Columns:", ", ".join(columns))
        print("Column count:", len(columns))
        print("Record count:", len(stored))
        print("NULL durations:", sum(record[2] is None for record in stored))
        print("Repeated full rows:", repeated)
        print("Distinct full rows:", len(set(stored)))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
