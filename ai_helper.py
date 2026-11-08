import os

import requests
from dotenv import load_dotenv

from suggestions import make_suggestions

load_dotenv()

def get_ai_tips(missing, job_title, api_key=None):
    """Ask a free AI model for one tip per missing skill. Return None on any problem."""
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key or not missing:
        return None

    prompt = (
        f"A student is applying for a {job_title} role and is missing these skills: "
        f"{', '.join(missing)}."
        "For each skill, write one practical tip (maximum 20 words) on how to learn it"
        "by building a small project. Reply with exactly one line per skill in the "
        "format 'skill: tip'. No extra text."
    )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model":"openrouter/free",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        if response.status_code !=200:
            return None
        message = response.json()["choices"][0]["message"]
        text = (message.get("content") or "").strip()
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None

    lines = [line.strip().lstrip("-*. ").strip() for line in text.splitlines()]
    lines = [line for line in lines if ":" in line]
    return lines or None


def make_ai_suggestions(missing, job_title, api_key=None):
    """Return (tips, source). Falls back to built-in tips if the AI fails."""
    tips = get_ai_tips(missing, job_title, api_key)
    if tips:
        return tips, "AI"
    return make_suggestions(missing), "built-in tips"


if __name__=="__main__":
    missing = ["numpy", "pandas", "scikit-learn"]
    job_title = "Machine Learning Intern"

    tips, source = make_ai_suggestions(missing, job_title)
    print("Source:", source)
    for tip in tips:
        print("-", tip)


    print()
    print("Fallback test (invalid key):")
    tips, source = make_ai_suggestions(missing, job_title, api_key="invalid-key")
    print("Source:", source)