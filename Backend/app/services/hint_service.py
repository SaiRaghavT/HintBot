MAX_HINTS = 4

hint_states: dict[tuple[str, str], dict] = {}


def get_hint_state(session_id: str, problem_id: str) -> dict:
    key = (session_id, problem_id)

    if key not in hint_states:
        hint_states[key] = {
            "problem_id": problem_id,
            "hint_level": 0,
            "hints_used": 0,
            "max_hints": 4,
            "status": "active",
        }

    return hint_states[key]


def can_use_hint(state: dict) -> bool:
    return (
        state["status"] == "active"
        and state["hints_used"] < MAX_HINTS
    )


def consume_hint(state: dict) -> None:
    state["hints_used"] += 1
    state["hint_level"] = state["hints_used"]


def complete_problem(session_id: str, problem_id: str) -> None:
    state = get_hint_state(session_id, problem_id)
    state["status"] = "completed"