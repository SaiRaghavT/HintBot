from enum import Enum


MAX_HINTS = 4


class RequestType(str, Enum):
    HINT = "hint"
    DEBUG = "debug"
    CONCEPT = "concept"
    GENERAL = "general"
    SOLUTION_REQUEST = "solution_request"


# Temporary in-memory hint state.
# Later this will move to the assessment session/database.
hint_states: dict[tuple[str, str], dict] = {}


def get_hint_state(session_id: str, problem_id: str) -> dict:
    key = (session_id, problem_id)

    if key not in hint_states:
        hint_states[key] = {
            "problem_id": problem_id,
            "hint_level": 0,
            "hints_used": 0,
            "max_hints": MAX_HINTS,
            "status": "active",
        }

    return hint_states[key]


def can_use_hint(state: dict) -> bool:
    return (
        state["status"] == "active"
        and state["hints_used"] < state["max_hints"]
    )


def consume_hint(state: dict) -> None:
    state["hints_used"] += 1
    state["hint_level"] = state["hints_used"]


def complete_problem(session_id: str, problem_id: str) -> None:
    state = get_hint_state(session_id, problem_id)
    state["status"] = "completed"

def classify_request(message: str) -> RequestType:
    text = message.lower().strip()

    hint_phrases = [
        "give me a hint",
        "give me another hint",
        "need a hint",
        "can i get a hint",
        "hint please",
        "help me with this",
        "what should i do",
        "how do i approach",
        "how should i approach",
    ]

    debug_phrases = [
        "why am i getting",
        "why do i get",
        "what is wrong with my code",
        "what's wrong with my code",
        "why does my code",
        "why isn't my code",
        "error",
        "exception",
        "traceback",
        "bug",
    ]

    concept_phrases = [
        "what is a hashmap",
        "what is a hash map",
        "what is a dictionary",
        "what is recursion",
        "what is binary search",
        "explain this concept",
        "what does this mean",
        "can you explain",
    ]

    solution_phrases = [
        "give me the solution",
        "show me the solution",
        "give me the answer",
        "show me the answer",
        "give me the code",
        "show me the code",
        "what is the complete solution",
    ]

    if any(phrase in text for phrase in solution_phrases):
        return RequestType.SOLUTION_REQUEST

    if any(phrase in text for phrase in debug_phrases):
        return RequestType.DEBUG

    if any(phrase in text for phrase in concept_phrases):
        return RequestType.CONCEPT

    if any(phrase in text for phrase in hint_phrases):
        return RequestType.HINT

    return RequestType.GENERAL