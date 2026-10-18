"""Tiny data-system demonstration for a beginner; Python standard library only."""

import sqlite3


def main():
    # SQLite runs inside this process; :memory: disappears when it ends.
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute(
            "CREATE TABLE lessons (code TEXT PRIMARY KEY, title TEXT, minutes INTEGER)"
        )
        lessons = [
            ("QAI.01.31", "Configuration and secrets", 35),
            ("QAI.01.32", "Git fundamentals", 55),
        ]
        connection.executemany(
            "INSERT INTO lessons (code, title, minutes) VALUES (?, ?, ?)",
            lessons,
        )
        selected = connection.execute(
            "SELECT code, title, minutes FROM lessons WHERE code = ?",
            ("QAI.01.31",),
        ).fetchall()
        for code, title, minutes in selected:
            print(f"Lesson: {code} | {title} | {minutes} minutes")
        print("Records selected:", len(selected))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
