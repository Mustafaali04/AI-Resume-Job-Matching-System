import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("No OPENROUTER_API_KEY found in.env")
    raise SystemExit

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": "Give one short tip to learn pandas. Max 20 words."}
        ],
    },
    timeout=60,
)

print("Status code:", response.status_code)
data = response.json()

if response.status_code ==200:
    print("Model used:", data.get("model"))
    print("Reply:", data["choices"][0]["message"]["content"])
else:
    print("Error:", data)