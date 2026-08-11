# from fastapi import APIRouter, HTTPException

# from app.schemas.problem import ProblemSummary, ProblemDetail
# from app.services.problem_service import (
#     get_all_problems,
#     get_problem_by_id,
# )


# router = APIRouter(
#     prefix="/problems",
#     tags=["Problems"],
# )


# @router.get("", response_model=list[ProblemSummary])
# async def get_problems():
#     return get_all_problems()


# @router.get("/{frontend_id}", response_model=ProblemDetail)
# async def get_problem(frontend_id: str):

#     problem = get_problem_by_id(frontend_id)

#     if problem is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Problem not found",
#         )

#     return ProblemDetail(
#         frontend_id=problem["frontend_id"],
#         title=problem["title"],
#         difficulty=problem["difficulty"],
#         topics=problem["topics"],
#         description=problem["description"],
#         examples=problem["examples"],
#         constraints=problem["constraints"],
#         starter_code=problem["code_snippets"]["python3"],
#     )

from fastapi import APIRouter, HTTPException

from app.services.problem_service import get_problem_by_id


router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
)


@router.get("/current")
async def get_current_problem():

    # Temporary: hardcoded problem for frontend development
    problem = get_problem_by_id("2")

    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found",
        )

    return {
        "frontend_id": problem["frontend_id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "topics": problem["topics"],
        "description": problem["description"],
        "examples": problem["examples"],
        "constraints": problem["constraints"],
        "starter_code": problem["code_snippets"]["python3"],
    }