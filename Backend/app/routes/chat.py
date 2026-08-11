from fastapi import APIRouter, HTTPException

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

        return ChatResponse(
            session_id=request.session_id,
            response=response,
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