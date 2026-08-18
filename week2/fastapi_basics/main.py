from fastapi import FastAPI
from google import genai
import os
from dotenv import load_dotenv

load_dotenv("../week1/env")
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    print("API açarı tapılmadı.")
    exit()

if not model_name:
    print("Model adı tapılmadı.")
    exit()

api = FastAPI(static_files="static", index_file="index.html")
client = genai.Client(api_key=api_key)

# get, post, put, delete

@api.get('/prompt')
def prompt_writing_interface():
    prompt_text = input("Promptu daxil edin: ")
    
    if not prompt_text:
        return "Prompt yoxdur"
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt_text
    )
    return response.text
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="[IP_ADDRESS]", port=8000)