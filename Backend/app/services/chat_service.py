from app.models.llm import generate_response
from app.prompts import (
    general_chat_prompt,
    hint_prompt,
)

from app.services.conversation_service import (
    get_history,
    add_message,
)

from app.services.problem_service import (
    get_problem_by_id,
)

from app.services.hint_service import (
    RequestType,
    get_hint_state,
    can_use_hint,
    consume_hint,
    classify_request,
)


async def chat_with_llm(
    session_id: str,
    problem_id: str,
    message: str,
    code: str = "",
    execution_output: str = "",
    execution_error: str | None = None,
) -> str:

    # --------------------------------------------------
    # 1. Get the problem from our dataset
    # --------------------------------------------------

    problem = get_problem_by_id(problem_id)

    if problem is None:
        raise ValueError(
            f"Problem not found: {problem_id}"
        )
    request_type = classify_request(message)

    hint_state = get_hint_state(
        session_id=session_id,
        problem_id=problem_id,
    )

    if request_type == RequestType.HINT:

        if not can_use_hint(hint_state):

            response = (
                "I've given you the strongest hint I can "
                "without revealing the solution. "
                "Try implementing the approach and run your code."
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

        current_hint_level = hint_state["hint_level"] + 1

    else:
        current_hint_level = hint_state["hint_level"]

    hint_context = f"""
REQUEST TYPE:
{request_type.value}

HINTS USED:
{hint_state["hints_used"]}

MAX HINTS:
{hint_state["max_hints"]}

CURRENT HINT LEVEL:
{current_hint_level}

{hint_prompt}
"""

    # --------------------------------------------------
    # 2. Get conversation history
    # --------------------------------------------------

    history = get_history(session_id)

    # --------------------------------------------------
    # 3. Build problem context
    # --------------------------------------------------

    examples = "\n\n".join(
        example.get("example_text", "")
        for example in problem.get("examples", [])
    )

    constraints = "\n".join(
        f"- {constraint}"
        for constraint in problem.get("constraints", [])
    )

    problem_context = f"""
CURRENT CODING PROBLEM

Problem ID:
{problem["frontend_id"]}

Title:
{problem["title"]}

Difficulty:
{problem["difficulty"]}

Topics:
{", ".join(problem["topics"])}

Description:
{problem["description"]}

Examples:
{examples}

Constraints:
{constraints}

----------------------------------------

CANDIDATE'S CURRENT CODE:

{code if code else "[No code submitted yet]"}

----------------------------------------

MOST RECENT CODE EXECUTION:

Output:
{execution_output if execution_output else "[No output]"}

Error:
{execution_error if execution_error else "[No execution error]"}

----------------------------------------
"""

    # --------------------------------------------------
    # 4. Tell the LLM how to behave
    # --------------------------------------------------

    context_prompt = f"""
{general_chat_prompt}

{hint_context}

IMPORTANT:
Keep your response concise.
For hints, use 1-2 sentences whenever possible.
Never provide the complete solution.
"""

    # --------------------------------------------------
    # 5. Build messages for Groq
    # --------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": context_prompt,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    # --------------------------------------------------
    # 6. Call LLM
    # --------------------------------------------------

    response = await generate_response(
    messages=messages
)

    if request_type == RequestType.HINT:
        consume_hint(hint_state)

    print(
        f"[HINT DEBUG] "
        f"session={session_id}, "
        f"problem={problem_id}, "
        f"used={hint_state['hints_used']}, "
        f"max={hint_state['max_hints']}"
    )

    # --------------------------------------------------
    # 7. Save conversation
    # --------------------------------------------------

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