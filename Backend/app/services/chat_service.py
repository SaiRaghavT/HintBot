from app.models.llm import generate_response
from app.prompts import general_chat_prompt

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

    hint_instructions = f"""
REQUEST TYPE:
{request_type.value}

HINT STATE:
Hints used: {hint_state["hints_used"]}
Maximum hints: {hint_state["max_hints"]}
Current hint level: {hint_state["hint_level"]}

If this is a HINT request:

Generate Hint Level {current_hint_level}.

Level 1:
Give a broad conceptual direction.
Do not reveal the specific technique immediately.

Level 2:
Point the candidate toward the relevant technique
or data structure.

Level 3:
Explain the algorithmic approach more specifically.

Level 4:
Give pseudocode-level guidance, but do not provide
the complete implementation.

Never provide the complete solution or complete code
as part of a hint.

If this is DEBUG:
Focus on the candidate's code and execution result.
Do NOT consume a hint.

If this is CONCEPT:
Explain the requested concept.
Do NOT consume a hint.

If this is GENERAL:
Answer normally while remaining aware of the problem.

If this is SOLUTION_REQUEST:
Do not reveal the complete solution.
Encourage the candidate to use the available hints first.
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

{hint_instructions}

You are currently helping the candidate solve the coding
problem provided below.

IMPORTANT TUTORING RULES:

1. You MUST use the problem context when answering.
2. You MUST consider the candidate's current code.
3. You MUST consider the latest execution output/error.
4. Do NOT give the complete solution immediately.
5. Prefer guiding questions and incremental hints.
6. If the candidate's code has a mistake, explain the
   relevant issue without simply dumping the corrected solution.
7. If the code has not been executed yet, reason from the
   code itself and the problem requirements.
8. Keep the candidate's current approach in mind before
   suggesting a different approach.
9. Do not invent requirements that are not present in the
   problem statement.
10. The goal is to help the candidate discover the solution.

{problem_context}
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