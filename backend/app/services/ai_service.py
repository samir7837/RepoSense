import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_readme(content: str):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional README generator.

Rewrite and improve the following GitHub README.

STRICT RULES:

- Output ONLY the README
- No explanations
- No extra text
- No "Here is the improved version"
- No code blocks
- No ```markdown
- Must start directly with title (# ...)
- Must be clean professional markdown


README:

{content}


Improved README:
"""

    data = {

        "model": "openai/gpt-4o-mini",

        "temperature": 0.3,

        "messages": [

            {
                "role": "user",
                "content": prompt
            }

        ]

    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    output = result["choices"][0]["message"]["content"]

    # Extra safety cleanup
    output = output.replace("```markdown", "")
    output = output.replace("```", "")
    output = output.strip()

    return output