from typing import Dict, List


# Temporary in-memory conversation storage
conversations: Dict[str, List[dict]] = {}


def get_history(session_id: str) -> List[dict]:
    return conversations.get(session_id, [])


def add_message(
    session_id: str,
    role: str,
    content: str,
) -> None:

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_history(session_id: str) -> None:
    conversations.pop(session_id, None)