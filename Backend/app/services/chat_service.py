from app.models.llm import generate_response
from app.prompts import hint_prompt

from app.services.conversation_service import (
    get_history,
    add_message,
)

from app.services.problem_service import (
    get_problem_by_id,
)

from app.services.hint_service import (
    get_hint_state,
    can_use_hint,
    consume_hint,
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
    hint_state = get_hint_state(
        session_id=session_id,
        problem_id=problem_id,
    )

    if request_type == RequestType.SOLUTION_REQUEST:

        response = (
            "I can't give you the complete solution. "
            "I can give you a hint to help you figure it out."
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

    if not can_use_hint(hint_state):

        response = (
            "You've used all 4 hints for this problem. "
            "Try implementing the approach and running your code."
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

    hint_context = f"""
HINTBOT STATE:

Hints already used: {hint_state["hints_used"]}
Maximum hints: 4
Current hint level: {current_hint_level}

Generate ONLY Hint Level {current_hint_level}.
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
You are HintBot, a coding assessment hint assistant.

Your ONLY purpose is to give the candidate hints about
the coding problem they are currently solving.

The candidate is already working on the problem provided
below. NEVER ask what problem they are solving.

You have access to:

1. The complete problem statement visible to the candidate.
2. The examples visible to the candidate.
3. The constraints visible to the candidate.
4. The candidate's current code.
5. The latest execution output/error.
6. The previous hint conversation.

{hint_context}

HINT RULES:

Hint Level 1:
Give a very small conceptual nudge.
Do not reveal the algorithm or data structure.

Hint Level 2:
Point toward the correct technique or data structure.
Do not explain the complete approach.

Hint Level 3:
Explain the core algorithmic idea.
The candidate should still implement it themselves.

Hint Level 4:
Give concise pseudocode-level guidance.
Do not provide actual implementation code.

CRITICAL RULES:

- NEVER provide the complete solution.
- NEVER provide complete code.
- NEVER write a long explanation.
- NEVER restate the problem.
- NEVER ask what problem the candidate is solving.
- NEVER start a generic conversation.
- NEVER ask what topic they want to discuss.
- ALWAYS respond specifically about the current problem.
- Use the candidate's code when giving the hint.
- Use the latest execution output/error when relevant.
- Keep hints to 1-3 sentences.
- Give ONLY the amount of information appropriate for the current hint level.

CURRENT PROBLEM:

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