from google import genai
from dotenv import load_dotenv
import os
from google.genai import types, errors
from datetime import datetime
import httpx


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

load_dotenv(".env")

file_name = f"./output/result_{file_time}.txt"
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")

client = genai.Client(api_key=api_key)


try:
    prompt = input("Promptu daxil edin: ").strip()
    if not prompt:
        print("Prompt yoxdur.")
        exit()
    if not api_key:
        print("API key yoxdur.")
        exit()
    if not model_name:
        print("Model adı yoxdur.")
        exit()
    if prompt.lower().strip() == "exit":
        exit()
        
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            system_instruction="Mütləq Azərbaycan dilində cavab ver",
            temperature=0.7,
        )
    )

    response_text = f"""
Tarix və vaxt: {current_time}
Model: {model_name}
Prompt: {prompt}

Cavab: {response.text}
"""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(response_text)

    print(response_text)

except KeyboardInterrupt:
    print("\nProses dayandırıldı.\n")
    exit()
except FileNotFoundError as e:
    print(f"\nFayl tapılmadı: \n{e.filename}\n")
except PermissionError:
    print("\nİcazə xətası: faylı oxumaq və ya yazmaq mümkün olmadı.\n")
except httpx.ConnectError:
    print("\nŞəbəkə xətası: Gemini serverinə qoşulmaq mümkün olmadı.\n")
except httpx.TimeoutException:
    print("\nTimeout: Gemini serverindən vaxtında cavab gəlmədi.\n")
except errors.APIError as e:
    print(f"\nGemini API xətası ({e.code}): {e.message}\n")
except RuntimeError as e:
    print(f"\nRuntime xətası: \n{e}\n")
except OSError as e:
    print(f"\nSistem xətası: \n{e}\n")
except Exception as e:
    print(f"\nGözlənilməyən xəta: \n{type(e).__name__}: {e}\n")