from pydantic import BaseModel, Field


class ResumeData(BaseModel):
    name: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
