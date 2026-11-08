import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")


prompt = (
    "A student is applying for a Machine Learning Intern role and is missing these skills: "
    "numpy, pandas, scikit-learn. "
    "For each skill, write one practical tip (maximum 20 words) on how to learn it "
    "by building a small project. Reply with exactly one line per skill in the "
    "format ' skill: tip'.No extra text."
)

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt}],
    },
    timeout=60,
)

print("Status code:", response.status_code)
data = response.json()

if response.status_code == 200:
    print("Model used:", data.get("model"))
    message = data["choices"][0]["message"]
    print(repr(message.get("content")))
else:
    print("Error:", data)