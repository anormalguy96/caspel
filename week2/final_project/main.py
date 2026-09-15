from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import PromptResponse
from schemas import AskRequest, AskResponse
from gemini_service import generate_answer, MODEL_NAME

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Caspel AI Assistant API")


@app.post("/ask", response_model=AskResponse, status_code=201)
def ask_question(req: AskRequest, db: Session = Depends(get_db)):
    prompt_text = req.prompt.strip()
    if not prompt_text:
        raise HTTPException(
            status_code=400,
            detail="Prompt boş ola bilməz."
        )

    try:
        answer_text = generate_answer(prompt_text)
    except RuntimeError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API xətası: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini çağırış xətası: {str(e)}"
        )

    record = PromptResponse(
        prompt=prompt_text,
        response=answer_text,
        model=MODEL_NAME
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Məlumat bazası xətası: {str(e)}"
        )


@app.get("/history", response_model=list[AskResponse])
def get_history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        statement = (
            select(PromptResponse)
            .order_by(PromptResponse.created_at.desc())
            .limit(limit)
        )
        results = db.scalars(statement).all()
        return results
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Məlumat bazası xətası: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
