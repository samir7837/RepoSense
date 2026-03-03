import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

REDIS_URL = os.getenv("REDIS_URL")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")

GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")