from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

hint_prompt = (
    PROMPTS_DIR / "hint_prompt.txt"
).read_text(encoding="utf-8")