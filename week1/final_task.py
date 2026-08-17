from google import genai
from dotenv import load_dotenv
import os
from google.genai import types, errors
from datetime import datetime
import httpx
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
ENV_PATH = BASE_DIR / ".env"

def main():
    load_dotenv(ENV_PATH)
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("MODEL_NAME")
    if not api_key:
        print("Gemini API açarı yoxdur.")
        return
    if not model_name:
        print("Model adı yoxdur.")
        return
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    client = genai.Client(api_key=api_key)
    
    prompt = input("Promptu daxil edin: ").strip()
    if not prompt:
        print("Prompt yoxdur.")
        return
    if prompt.lower() == "exit":
        return
        
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            system_instruction="Mütləq Azərbaycan dilində cavab ver",
            temperature=0.7,
        )
    )
    # Safely extract text parts from response candidates
    answer_text = "".join(
        part.text for candidate in (response.candidates or [])
        for part in (candidate.content.parts or [])
        if part.text
    ).strip()

    if not answer_text:
        print("cavab yoxdur")
        return
    
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    file_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    file_name = OUTPUT_DIR / f"result_{file_time}.md"

    response_text = f"""
## Tarix və vaxt: {current_time}
## Model: {model_name}
## Prompt: {prompt}

## Cavab: 

{answer_text}
"""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(response_text)

    print(response_text)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProses dayandırıldı.\n")
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