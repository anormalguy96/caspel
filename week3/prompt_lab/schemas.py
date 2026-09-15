from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal

# --- REQUEST SCHEMAS (İstifadəçidən gələn sorğular) ---

class AskRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    mode: Literal["factual", "balanced", "creative"] = "balanced"

class CompareRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

class GroundedRequest(BaseModel):
    context: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)

# --- RESPONSE SCHEMAS (İstifadəçiyə qaytarılan cavablar) ---

class ExperimentResponse(BaseModel):
    id: int
    prompt: str
    response: str
    system_prompt: str
    temperature: float
    mode: Optional[str] = None
    experiment_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CompareItem(BaseModel):
    id: int
    temperature: float
    response: str

class CompareResponse(BaseModel):
    prompt: str
    low_temperature: CompareItem
    high_temperature: CompareItem
