import os

from groq import AsyncGroq
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set in the environment."
    )


client = AsyncGroq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "llama-3.1-8b-instant"


async def generate_response(
    system_prompt: str,
    user_message: str,
) -> str:

    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content