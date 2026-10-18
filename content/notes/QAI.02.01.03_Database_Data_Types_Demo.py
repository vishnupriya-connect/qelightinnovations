"""Show declared versus actual SQLite types on fixed fictional lesson data."""

import sqlite3


def main():
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute(
            "CREATE TABLE lessons ("
            "code TEXT NOT NULL, minutes INTEGER, fee DECIMAL(8,2), "
            "ratio REAL, published BOOLEAN, updated_at TEXT, image BLOB)"
        )
        ratio = 0.75  # Change to 0.80, run again, then restore.
        connection.execute(
            "INSERT INTO lessons VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "QAI.01.31", 35, "299.50", ratio, True,
                "2026-09-25T10:30:00+05:30", b"example bytes",
            ),
        )
        connection.execute(
            "INSERT INTO lessons VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("QAI.01.32", None, None, None, False, None, None),
        )
        declared = next(
            item[2] for item in connection.execute("PRAGMA table_info(lessons)")
            if item[1] == "fee"
        )
        kinds = connection.execute(
            "SELECT typeof(fee), typeof(published), typeof(updated_at), "
            "typeof(image), ratio FROM lessons WHERE code = ?",
            ("QAI.01.31",),
        ).fetchone()
        count = connection.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
        missing = connection.execute(
            "SELECT COUNT(*) FROM lessons WHERE minutes IS NULL"
        ).fetchone()[0]
        try:
            connection.execute(
                "INSERT INTO lessons (code, minutes) VALUES (?, ?)",
                (None, 20),
            )
            missing_code_rejected = False
        except sqlite3.IntegrityError:
            missing_code_rejected = True
        print("Declared fee type:", declared)
        print("Stored fee kind:", kinds[0])
        print("Stored published kind:", kinds[1])
        print("Stored update-time kind:", kinds[2])
        print("Stored image kind:", kinds[3])
        print("Lesson count:", count)
        print("Lessons with NULL minutes:", missing)
        print("Missing code rejected:", "yes" if missing_code_rejected else "no")
        print("Completion ratio:", kinds[4])
    finally:
        connection.close()


if __name__ == "__main__":
    main()
