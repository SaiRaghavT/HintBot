from pydantic import BaseModel


class ProblemSummary(BaseModel):
    frontend_id: str
    title: str
    difficulty: str
    topics: list[str]


class Example(BaseModel):
    example_num: int
    example_text: str
    images: list[str] = []


class ProblemDetail(BaseModel):
    frontend_id: str
    title: str
    difficulty: str
    topics: list[str]
    description: str
    examples: list[Example]
    constraints: list[str]
    starter_code: str