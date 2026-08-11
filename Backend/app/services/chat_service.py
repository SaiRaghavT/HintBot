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
    
    #Retriveing the previous conversation history
    history = get_history(session_id)
    
    #Appending the first system prompt to messages
    messages = [
        {
            "role": "system",
            "content": general_chat_prompt,
        }
    ]
    #Appending the previous conversation history to the messages 
    messages.extend(history)
    
    #Appending the latest user query to the messages 
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