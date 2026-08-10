from pydantic import BaseModel


class RunRequest(BaseModel):
    language: str
    code: str


class RunResponse(BaseModel):
    output: str
    error: str | None