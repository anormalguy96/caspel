from fastapi import FastAPI, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile
from pathlib import Path
import os

from schemas import ResumeData
from resume_service import parse_resume_pdf


app = FastAPI(
    title="Resume Parser API",
    version="1.0.0"
)


@app.post("/extract", response_model=ResumeData)
async def extract_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    tmp_path = None

    try:
        with NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:
            tmp_file.write(contents)
            tmp_path = tmp_file.name

        result = parse_resume_pdf(tmp_path)

        return result

    except (ValueError, RuntimeError) as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Resume processing failed."
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)