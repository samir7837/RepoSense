import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def review_code(code: str):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {

        "Authorization": f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type": "application/json"

    }


    prompt = f"""
You are a senior code reviewer.

Review this code.

Give:

Score: X/100

Issues

Improvements

Improved Code


Code:

{code}
"""


    data = {

        "model": "openai/gpt-4o-mini",

        "messages": [

            {

                "role": "user",

                "content": prompt

            }

        ]

    }


    response = requests.post(

        url,

        headers=headers,

        json=data

    )


    result = response.json()


    return result["choices"][0]["message"]["content"]


# EXTRACT SCORE


def extract_score(review):

    match = re.search(

        r"Score:\s*(\d+)",

        review

    )

    if match:

        return int(match.group(1))

    return 0