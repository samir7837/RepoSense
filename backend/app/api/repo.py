from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.db.database import get_db
from app.models.user import User
from app.models.repository import Repository


router = APIRouter(
    prefix="/api/repo",
    tags=["Repositories"]
)


# -----------------------------
# CREATE WEBHOOK FUNCTION
# -----------------------------

def create_webhook(full_name: str, access_token: str):

    url = f"https://api.github.com/repos/{full_name}/hooks"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "name": "web",
        "active": True,
        "events": ["push"],
        "config": {
            # CHANGE THIS IN PRODUCTION
            "url": "https://insistingly-ethnohistorical-jessenia.ngrok-free.dev/api/webhook/github",
            "content_type": "json"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code not in [200, 201]:
        print("Webhook creation failed:", response.text)
        raise HTTPException(
            status_code=400,
            detail="Webhook creation failed"
        )

    print("Webhook created successfully")


# -----------------------------
# CONNECT REPO ENDPOINT
# -----------------------------

@router.post("/connect")
def connect_repo(
    github_id: str,
    repo_name: str,
    full_name: str,
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.github_id == github_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    # Check if repo already exists
    existing = db.query(Repository).filter(
        Repository.full_name == full_name
    ).first()

    if existing:
        return {
            "message": "Repository already connected"
        }


    # Save repo
    repo = Repository(
        github_id=github_id,
        name=repo_name,
        full_name=full_name,
        user_id=user.id
    )

    db.add(repo)
    db.commit()


    # CREATE WEBHOOK AUTOMATICALLY
    create_webhook(
        full_name,
        user.access_token
    )


    return {
        "message": "Repository connected successfully",
        "repo": full_name
    }


# -----------------------------
# GET USER REPOS FROM DB
# -----------------------------

@router.get("/list/{github_id}")
def list_repos(
    github_id: str,
    db: Session = Depends(get_db)
):

    repos = db.query(Repository).filter(
        Repository.github_id == github_id
    ).all()

    return repos