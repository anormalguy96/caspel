from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class AskResponse(BaseModel):
    id: int
    prompt: str
    response: str
    model: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
