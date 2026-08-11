from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

general_chat_prompt = (
    PROMPTS_DIR / "general_chat.txt"
).read_text(encoding="utf-8")

hint_prompt = (
    PROMPTS_DIR / "hint_prompt.txt"
).read_text(encoding="utf-8")