from fastapi import APIRouter, HTTPException

from app.schemas.run import RunRequest, RunResponse
from app.services.code_execution_service import execute_code


router = APIRouter(
    prefix="/run",
    tags=["Code Execution"],
)


@router.post("", response_model=RunResponse)
async def run_code(request: RunRequest):

    try:
        output, error = await execute_code(
            language=request.language,
            code=request.code,
        )

        return RunResponse(
            output=output,
            error=error,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )