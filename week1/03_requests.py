import requests


url = "https://postman-echo.com/post"

payload = {
    "model": "Qwen",
    "language": "Azerbaijani",
    "prompt": "Azərbaycan dilinin əsas xüsusiyyətləri hansılardır?"
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print(f"Status: {response.status_code}")

    response.raise_for_status()

    data = response.json()
    sent_payload = data["json"]

    print(f"Model: {sent_payload['model']}")
    print(f"Language: {sent_payload['language']}")
    print(f"Prompt: {sent_payload['prompt']}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")