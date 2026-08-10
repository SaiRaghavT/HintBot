from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_with_llm


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await chat_with_llm(
            message=request.message
        )

        return ChatResponse(
            response=response
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )