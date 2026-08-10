import subprocess
import sys
import tempfile
import os


async def execute_code(
    language: str,
    code: str,
) -> tuple[str, str | None]:

    if language != "python":
        return "", f"Unsupported language: {language}"

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as file:

            file.write(code)
            temp_file = file.name

        process = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5,
        )

        output = process.stdout

        error = process.stderr if process.stderr else None

        return output, error

    except subprocess.TimeoutExpired:
        return "", "Execution timed out."

    except Exception as error:
        return "", str(error)

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)