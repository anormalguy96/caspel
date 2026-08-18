from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.genai import Client, types, errors
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY tapılmadı.")

if not model_name:
    raise RuntimeError("MODEL_NAME tapılmadı.")

api = FastAPI()

api.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

client = Client(api_key=api_key)

class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)

@api.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@api.get("/suggestions")
def suggestions():
    return {
        "suggestions": [
            "Süni intellekt nədir?",
            "Maşın öyrənməsini sadə dillə izah et.",
            "Transformer arxitekturası necə işləyir?"
        ]
    }

@api.post("/ask")
def ask(req: AskRequest):
    prompt = req.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt boş ola bilməz."
        )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Model boş cavab qaytardı."
            )

        return {
            "response": response.text,
            "model": model_name
        }

    except errors.APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API xətası ({e.code}): {e.message}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:api", port=8000, reload=True)