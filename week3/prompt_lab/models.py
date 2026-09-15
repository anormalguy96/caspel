from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Float, func
from datetime import datetime
from typing import Optional

class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    mode: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    experiment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # ASK, COMPARE, GROUNDED
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
