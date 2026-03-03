from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import requests

from sqlalchemy.orm import Session

from app.core.config import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET
)

from app.db.database import SessionLocal
from app.models.user import User


# ❗ REMOVE prefix here
router = APIRouter(
    tags=["Auth"]
)


# =========================================================
# GitHub Login
# =========================================================

@router.get("/github/login")
def github_login():

    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        "&scope=read:user user:email repo"
    )

    return RedirectResponse(github_url)



# =========================================================
# GitHub Callback
# =========================================================

@router.get("/github/callback")
def github_callback(code: str):

    # STEP 1: Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"

    token_response = requests.post(
        token_url,
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    access_token = token_response.json().get("access_token")

    # STEP 2: Get GitHub user info
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    user_data = user_response.json()

    github_id = str(user_data["id"])
    email = user_data.get("email")
    login = user_data.get("login")

    # STEP 3: Save user
    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.github_id == github_id
    ).first()

    if not existing_user:
        new_user = User(
            github_id=github_id,
            email=email,
            access_token=access_token
        )
        db.add(new_user)
    else:
        existing_user.access_token = access_token

    db.commit()
    db.close()

    # STEP 4: Redirect to frontend
    return RedirectResponse(
        url=f"http://localhost:8080/auth/callback?github_id={github_id}&login={login}"
    )