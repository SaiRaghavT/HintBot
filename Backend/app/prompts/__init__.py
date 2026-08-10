from pathlib import Path


PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    prompt_path = PROMPTS_DIR / filename

    return prompt_path.read_text(
        encoding="utf-8"
    )


general_chat_prompt = load_prompt(
    "general_chat.txt"
)