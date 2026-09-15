import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY tapılmadı.")

if not MODEL_NAME:
    raise RuntimeError("MODEL_NAME tapılmadı.")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(prompt: str, temperature: float = 0.7, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Yalnız Azərbaycan dilində cavab ver.",
                    temperature=temperature,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            if not response.text:
                raise RuntimeError("Model boş cavab qaytardı.")

            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                print(f"Rate limit (429). Waiting for 6 seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(6)
            else:
                raise e


if __name__ == "__main__":
    prompt = input("Prompt: ")

    temperatures = [0.1, 0.7, 1.0, 2.0]

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"Prompt: {prompt}\n\n")
        for temp in temperatures:
            print(f"Generating for Temperature = {temp}...")
            try:
                ans = generate_answer(prompt, temperature=temp)
                f.write(f"Temperature = {temp}:\n{ans}\n\n")
            except Exception as e:
                f.write(f"Temperature = {temp}:\nXəta: {e}\n\n")
            time.sleep(2)

    print("Nəticələr output.txt faylına yazıldı!")