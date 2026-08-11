from fastapi import APIRouter, HTTPException

from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentDetailResponse,
    AssessmentStartResponse,
)

from app.services.assessment_service import (
    create_assessment,
    get_assessment,
    get_assessment_problems,
    start_assessment,
)


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


# -------------------------
# ADMIN
# -------------------------

@router.post(
    "/admin",
    response_model=AssessmentResponse,
)
async def create_new_assessment(
    request: AssessmentCreate,
):

    try:

        assessment = create_assessment(
            title=request.title,
            description=request.description,
            duration_minutes=request.duration_minutes,
            problem_ids=request.problem_ids,
        )

        return assessment

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.get(
    "/admin/{assessment_id}",
    response_model=AssessmentDetailResponse,
)
async def get_admin_assessment(
    assessment_id: str,
):

    assessment = get_assessment(assessment_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return AssessmentDetailResponse(
        assessment_id=assessment["assessment_id"],
        title=assessment["title"],
        description=assessment["description"],
        duration_minutes=assessment["duration_minutes"],
        problems=get_assessment_problems(assessment),
    )


# -------------------------
# CANDIDATE
# -------------------------

@router.get(
    "/{assessment_id}",
    response_model=AssessmentDetailResponse,
)
async def get_candidate_assessment(
    assessment_id: str,
):

    assessment = get_assessment(assessment_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return AssessmentDetailResponse(
        assessment_id=assessment["assessment_id"],
        title=assessment["title"],
        description=assessment["description"],
        duration_minutes=assessment["duration_minutes"],
        problems=get_assessment_problems(assessment),
    )


@router.post(
    "/{assessment_id}/start",
    response_model=AssessmentStartResponse,
)
async def start_candidate_assessment(
    assessment_id: str,
):

    result = start_assessment(assessment_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    assessment = result["assessment"]

    return AssessmentStartResponse(
        session_id=result["session"]["session_id"],
        assessment_id=assessment["assessment_id"],
        title=assessment["title"],
        duration_minutes=assessment["duration_minutes"],
        problems=result["problems"],
    )