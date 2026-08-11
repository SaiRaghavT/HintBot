from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    title: str
    description: str | None = None
    duration_minutes: int
    problem_ids: list[str]


class AssessmentProblem(BaseModel):
    frontend_id: str
    title: str
    difficulty: str
    topics: list[str]
    description: str
    examples: list
    constraints: list[str]
    starter_code: str


class AssessmentResponse(BaseModel):
    assessment_id: str
    title: str
    description: str | None
    duration_minutes: int
    problem_ids: list[str]


class AssessmentDetailResponse(BaseModel):
    assessment_id: str
    title: str
    description: str | None
    duration_minutes: int
    problems: list[AssessmentProblem]


class AssessmentStartResponse(BaseModel):
    session_id: str
    assessment_id: str
    title: str
    duration_minutes: int
    problems: list[AssessmentProblem]