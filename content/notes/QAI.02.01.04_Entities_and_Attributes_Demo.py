"""Trace learners, courses, enrolments, and one derived count locally."""

import sqlite3


def main():
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE learners (learner_id TEXT, name TEXT, city TEXT)")
        connection.execute("CREATE TABLE courses (course_id TEXT, title TEXT, capacity INTEGER)")
        connection.execute("CREATE TABLE enrolments (learner_id TEXT, course_id TEXT)")
        connection.executemany(
            "INSERT INTO learners VALUES (?, ?, ?)",
            [("L1", "Anu", "Bengaluru"), ("L2", "Ravi", "Mysuru")],
        )
        connection.executemany(
            "INSERT INTO courses VALUES (?, ?, ?)",
            [("C1", "AI Foundations", 3), ("C2", "Git Basics", 2)],
        )
        connection.executemany(
            "INSERT INTO enrolments VALUES (?, ?)",
            [("L1", "C1"), ("L1", "C2"), ("L2", "C1")],
        )
        learner = connection.execute(
            "SELECT learner_id, name, city FROM learners WHERE learner_id = ?",
            ("L1",),
        ).fetchone()
        address = {"city": "Bengaluru", "postal_code": "560001"}
        interests = ["Python", "SQL"]
        enrolled_names = [
            row[0] for row in connection.execute(
                "SELECT learners.name FROM enrolments "
                "JOIN learners ON enrolments.learner_id = learners.learner_id "
                "WHERE enrolments.course_id = ? ORDER BY learners.name",
                ("C1",),
            )
        ]
        capacity = connection.execute(
            "SELECT capacity FROM courses WHERE course_id = ?", ("C1",)
        ).fetchone()[0]
        print("Entity type: Learner")
        print("Entity instance:", " | ".join(learner))
        print("Composite address parts:", address["city"] + ", " + address["postal_code"])
        print("Multiple interests:", ", ".join(interests))
        print("Entity tables: learners, courses")
        print("Relationship table: enrolments")
        print("Enrolled in C1:", ", ".join(enrolled_names))
        print("Available seats in C1:", capacity - len(enrolled_names))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
