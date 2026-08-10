from app.models.llm import generate_response
from app.prompts import general_chat_prompt

from app.services.conversation_service import (
    get_history,
    add_message,
)


async def chat_with_llm(
    session_id: str,
    message: str,
) -> str:

    history = get_history(session_id)

    messages = [
        {
            "role": "system",
            "content": general_chat_prompt,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    response = await generate_response(
        messages=messages
    )

    add_message(
        session_id=session_id,
        role="user",
        content=message,
    )

    add_message(
        session_id=session_id,
        role="assistant",
        content=response,
    )

    return response