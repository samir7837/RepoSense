from fastapi import APIRouter

from app.db.database import SessionLocal

from app.models.repository import Repository
from app.models.review import Review


router = APIRouter()


# ====================================
# GET USER REPOSITORIES
# ====================================

@router.get("/repos/{github_id}")
def get_user_repos(github_id: str):

    db = SessionLocal()

    repos = db.query(Repository).filter(
        Repository.github_id == github_id
    ).all()

    result = []

    for repo in repos:

        reviews = db.query(Review).filter(
            Review.repo_name == repo.repo_name
        ).all()


        avg_score = 0

        if reviews:

            avg_score = sum(
                r.score for r in reviews
            ) / len(reviews)


        result.append({

            "repo_name": repo.repo_name,

            "full_name": repo.full_name,

            "total_reviews": len(reviews),

            "average_score": round(avg_score, 2)

        })


    db.close()

    return result


# ====================================
# GET ALL REVIEWS FOR USER
# ====================================

@router.get("/reviews/{github_id}")
def get_user_reviews(github_id: str):

    db = SessionLocal()

    reviews = db.query(Review).filter(
        Review.github_id == github_id
    ).all()

    result = []

    for review in reviews:

       result.append({
    "repo_name": review.repo_name,
    "file_name": review.file_name,
    "score": review.score,
    "review": review.review
     })

    db.close()

    return result