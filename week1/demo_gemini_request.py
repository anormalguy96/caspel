import os
import sys
from google import genai
from dotenv import load_dotenv

from google.genai import types

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

client = genai.Client(api_key=api_key)

prompt = input("Prompt: ")

config = types.GenerateContentConfig(
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

response = client.models.generate_content(
    model=model_name,
    contents=prompt,
    config=config,
)

print(response.text)