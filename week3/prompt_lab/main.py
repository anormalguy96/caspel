from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from contextlib import asynccontextmanager
import logging

from database import engine, Base, get_db
from models import Experiment
from schemas import (
    AskRequest,
    CompareRequest,
    GroundedRequest,
    ExperimentResponse,
    CompareResponse,
    CompareItem,
)
import prompt_service
import gemini_service


# Server qalxanda DB cədvəllərini avtomatik yaradırıq
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="PromptLab — LLM Behavior Lab",
    description="Week 3 LLM Behavior, Prompt Engineering & Hallucination Experiment API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/ask", response_model=ExperimentResponse, summary="Mode-a uyğun tək prompt sorğusu")
def ask(payload: AskRequest, db: Session = Depends(get_db)):
    temperature = prompt_service.get_temperature(payload.mode)
    system_prompt = prompt_service.get_system_prompt(payload.mode)

    try:
        response_text = gemini_service.generate_answer(
            prompt=payload.prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API xətası: {str(e)}")

    # Nəticəni DB-də saxlayırıq
    exp = Experiment(
        prompt=payload.prompt,
        response=response_text,
        system_prompt=system_prompt,
        temperature=temperature,
        mode=payload.mode.lower(),
        experiment_type="ASK",
    )
    try:
        db.add(exp)
        db.commit()
        db.refresh(exp)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database xətası: {e}")
        raise HTTPException(status_code=500, detail="Database xətası baş verdi.")

    return exp

@app.post("/compare", response_model=CompareResponse, summary="Eyni prompt-un 0.1 və 1.0 temperaturda müqayisəsi")
def compare(payload: CompareRequest, db: Session = Depends(get_db)):
    system_prompt = prompt_service.get_system_prompt("balanced")

    try:
        res_low = gemini_service.generate_answer(
            prompt=payload.prompt,
            system_prompt=system_prompt,
            temperature=0.1,
        )
        res_high = gemini_service.generate_answer(
            prompt=payload.prompt,
            system_prompt=system_prompt,
            temperature=1.0,
        )
    except Exception as e:
        print(f"Gemini API xətası: {e}")
        raise HTTPException(status_code=502, detail="Gemini API xətası baş verdi.")

    exp_low = Experiment(
        prompt=payload.prompt,
        response=res_low,
        system_prompt=system_prompt,
        temperature=0.1,
        mode=None,
        experiment_type="COMPARE",
    )
    exp_high = Experiment(
        prompt=payload.prompt,
        response=res_high,
        system_prompt=system_prompt,
        temperature=1.0,
        mode=None,
        experiment_type="COMPARE",
    )

    try:
        db.add_all([exp_low, exp_high])
        db.commit()
        db.refresh(exp_low)
        db.refresh(exp_high)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database xətası: {e}")
        raise HTTPException(status_code=500, detail="Database xətası baş verdi.")

    return CompareResponse(
        prompt=payload.prompt,
        low_temperature=CompareItem(
            id=exp_low.id,
            temperature=0.1,
            response=res_low,
        ),
        high_temperature=CompareItem(
            id=exp_high.id,
            temperature=1.0,
            response=res_high,
        ),
    )


@app.post("/grounded", response_model=ExperimentResponse, summary="Kontekst əsaslı (hallusinasiyasız) sorğu")
def grounded(payload: GroundedRequest, db: Session = Depends(get_db)):
    system_prompt = prompt_service.get_grounded_system_prompt()
    full_prompt = prompt_service.build_grounded_user_prompt(payload.context, payload.question)
    temperature = 0.1

    try:
        response_text = gemini_service.generate_answer(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API xətası: {str(e)}")

    exp = Experiment(
        prompt=full_prompt,
        response=response_text,
        system_prompt=system_prompt,
        temperature=temperature,
        mode=None,
        experiment_type="GROUNDED",
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp

@app.get("/history", response_model=List[ExperimentResponse], summary="Eksperiment tarixçəsi və filtrləmə")
def get_history(
    mode: Optional[str] = Query(None, description="factual, balanced, creative"),
    experiment_type: Optional[str] = Query(None, description="ASK, COMPARE, GROUNDED"),
    limit: int = Query(20, ge=1, le=100, description="Maksimum qayıdan sətir sayı"),
    db: Session = Depends(get_db),
):
    stmt = select(Experiment)

    if mode:
        stmt = stmt.where(Experiment.mode == mode.lower())
    if experiment_type:
        stmt = stmt.where(Experiment.experiment_type == experiment_type.upper())

    stmt = stmt.order_by(Experiment.id.desc()).limit(limit)
    records = db.scalars(stmt).all()
    return records