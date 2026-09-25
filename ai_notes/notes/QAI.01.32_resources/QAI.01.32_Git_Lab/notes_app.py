"""Print a short, fictional course topic list from a local JSON file."""

import json
from pathlib import Path

WELCOME_TEXT = "AI study planner"
DATA = Path(__file__).with_name("lessons.json")


def load_lessons(path=DATA):
    lessons = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(lessons, list):
        raise ValueError("lessons.json must contain a list")
    for lesson in lessons:
        if not isinstance(lesson, dict) or not all(
            isinstance(lesson.get(key), str) and lesson[key].strip()
            for key in ("code", "title")
        ):
            raise ValueError("each lesson needs a nonempty code and title")
    return lessons


def main():
    lessons = load_lessons()
    print(WELCOME_TEXT)
    print("Topics available:", len(lessons))
    for lesson in lessons:
        print(f'{lesson["code"]}: {lesson["title"]}')


if __name__ == "__main__":
    main()
