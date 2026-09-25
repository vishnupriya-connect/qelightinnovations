"""Run only after adding this file to the second commit in the lab."""

import subprocess
import sys
from pathlib import Path

from notes_app import load_lessons


def main():
    lessons = load_lessons()
    assert len(lessons) == 2
    print("Check 1: two lesson records load")
    assert [item["code"] for item in lessons] == ["QAI.01.31", "QAI.01.32"]
    print("Check 2: lesson order and codes match")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("notes_app.py"))],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Topics available: 2" in result.stdout
    assert "QAI.01.32: Git fundamentals" in result.stdout
    print("Check 3: command-line app prints expected data")
    print("Checks passed: 3")


if __name__ == "__main__":
    main()
