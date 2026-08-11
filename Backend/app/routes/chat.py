from fastapi import APIRouter, HTTPException
from app.services.hint_service import get_hint_states

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import chat_with_llm


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:

        response = await chat_with_llm(
            session_id=request.session_id,
            problem_id=request.problem_id,
            message=request.message,
            code=request.code,
            execution_output=request.execution_output,
            execution_error=request.execution_error,
        )

        hint_state = get_hint_state(
            session_id=request.session_id,
            problem_id=request.problem_id,
        )

        return ChatResponse(
            session_id=request.session_id,
            response=response,
            hints_used=hint_state["hints_used"],
            max_hints=hint_state["max_hints"],
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )