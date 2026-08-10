from app.models.llm import generate_response
from app.prompts import general_chat_prompt


async def chat_with_llm(message: str) -> str:
    prompt = general_chat_prompt

    response = await generate_response(
        system_prompt=prompt,
        user_message=message,
    )

    return response