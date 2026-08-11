import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent / "data" / "problems.json"
)


def _load_problems() -> list[dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["questions"]


def get_all_problems() -> list[dict]:
    problems = _load_problems()

    return [
        {
            "frontend_id": problem["frontend_id"],
            "title": problem["title"],
            "difficulty": problem["difficulty"],
            "topics": problem["topics"],
        }
        for problem in problems
    ]


def get_problem_by_id(frontend_id: str) -> dict | None:
    problems = _load_problems()

    for problem in problems:
        if problem["frontend_id"] == frontend_id:
            return problem

    return None