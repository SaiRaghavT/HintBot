import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta, timezone

from app.services.problem_service import get_problem_by_id


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "assessments.json"
)


# Temporary in-memory assessment sessions.
assessment_sessions: dict[str, dict] = {}


def _load_assessments() -> list[dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("assessments", [])


def _save_assessments(assessments: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"assessments": assessments},
            file,
            indent=2,
        )


def create_assessment(
    title: str,
    description: str | None,
    duration_minutes: int,
    problem_ids: list[str],
) -> dict:

    # Validate that every selected problem exists.
    for problem_id in problem_ids:
        problem = get_problem_by_id(problem_id)

        if problem is None:
            raise ValueError(
                f"Problem not found: {problem_id}"
            )

    assessments = _load_assessments()

    assessment = {
        "assessment_id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "duration_minutes": duration_minutes,
        "problem_ids": problem_ids,
    }

    assessments.append(assessment)

    _save_assessments(assessments)

    return assessment


def get_assessment(assessment_id: str) -> dict | None:

    assessments = _load_assessments()

    for assessment in assessments:
        if assessment["assessment_id"] == assessment_id:
            return assessment

    return None


def get_assessment_problems(assessment: dict) -> list[dict]:

    problems = []

    for problem_id in assessment["problem_ids"]:

        problem = get_problem_by_id(problem_id)

        if problem is None:
            continue

        problems.append(
            {
                "frontend_id": problem["frontend_id"],
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "topics": problem["topics"],
                "description": problem["description"],
                "examples": problem["examples"],
                "constraints": problem["constraints"],
                "starter_code": problem["code_snippets"]["python3"],
            }
        )

    return problems


def start_assessment(
    assessment_id: str,
) -> dict | None:

    assessment = get_assessment(assessment_id)

    if assessment is None:
        return None

    session_id = str(uuid.uuid4())

    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=assessment["duration_minutes"]
    )

    session = {
        "session_id": session_id,
        "assessment_id": assessment_id,
        "started_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "status": "active",
        "current_problem_id": (
            assessment["problem_ids"][0]
            if assessment["problem_ids"]
            else None
        ),
    }

    assessment_sessions[session_id] = session

    return {
        "session": session,
        "assessment": assessment,
        "problems": get_assessment_problems(assessment),
    }