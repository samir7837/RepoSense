from fastapi import APIRouter, Request
from git import Repo, GitCommandError
import os
import shutil
import stat

from app.services.ai_service import generate_readme
from app.services.review_service import review_code, extract_score

from app.db.database import SessionLocal
from app.models.user import User
from app.models.review import Review
from app.models.repository import Repository


router = APIRouter()

BASE_DIR = "repos"


# Fix Windows permission issue
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


@router.post("/github")
async def github_webhook(request: Request):

    payload = await request.json()

    # ----------------------------------------
    # SAFETY CHECK
    # ----------------------------------------

    if "head_commit" not in payload:
        return {"status": "ignored"}

    commit_message = payload["head_commit"]["message"]

    # LOOP PROTECTION
    if "RepoSense AI" in commit_message:
        print("⏭️ Ignoring RepoSense commit to prevent loop")
        return {"status": "ignored"}

    repo_full_name = payload["repository"]["full_name"]
    repo_name = payload["repository"]["name"]
    branch = payload["ref"].split("/")[-1]
    github_id = str(payload["repository"]["owner"]["id"])

    print("\n🔥 Webhook received")
    print("Repo:", repo_full_name)
    print("Branch:", branch)
    print("Message:", commit_message)

    db = SessionLocal()

    try:
        # ----------------------------------------
        # GET USER
        # ----------------------------------------

        user = db.query(User).filter(
            User.github_id == github_id
        ).first()

        if not user:
            print("❌ User not found")
            return {"error": "User not found"}

        token = user.access_token

        # ----------------------------------------
        # ENSURE REPOSITORY EXISTS (NO DUPLICATES)
        # ----------------------------------------

        existing_repo = db.query(Repository).filter(
            Repository.github_id == github_id,
            Repository.repo_name == repo_name
        ).first()

        if not existing_repo:
            new_repo = Repository(
                github_id=github_id,
                repo_name=repo_name,
                full_name=repo_full_name,
                user_id=user.id
            )
            db.add(new_repo)
            db.commit()
            print("📦 Repository saved to DB")

        # ----------------------------------------
        # PREPARE CLONE URL
        # ----------------------------------------

        clone_url = payload["repository"]["clone_url"]
        clone_url = clone_url.replace(
            "https://",
            f"https://{token}@"
        )

        repo_path = os.path.join(BASE_DIR, repo_name)
        os.makedirs(BASE_DIR, exist_ok=True)

        # ----------------------------------------
        # CLONE OR PULL
        # ----------------------------------------

        if os.path.exists(repo_path):
            try:
                print("📂 Pulling latest changes...")
                repo = Repo(repo_path)
                repo.git.checkout(branch)
                repo.remotes.origin.pull(branch)
            except Exception:
                print("⚠️ Repo corrupted, deleting...")
                shutil.rmtree(repo_path, onerror=remove_readonly)
                repo = Repo.clone_from(
                    clone_url,
                    repo_path,
                    branch=branch
                )
        else:
            print("📥 Cloning repo...")
            repo = Repo.clone_from(
                clone_url,
                repo_path,
                branch=branch
            )

        print(f"✅ Repo ready at: {repo_path}")

        # ----------------------------------------
        # README AI IMPROVER
        # ----------------------------------------

        readme_path = os.path.join(repo_path, "README.md")

        if os.path.exists(readme_path):

            print("📄 Sending README to AI...")

            with open(readme_path, "r", encoding="utf-8") as f:
                old_readme = f.read()

            new_readme = generate_readme(old_readme)

            if new_readme.strip() != old_readme.strip():

                print("💾 Updating README...")

                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(new_readme)

                repo.git.add("README.md")
                repo.index.commit(
                    "✨ Improved README using RepoSense AI"
                )
                repo.remotes.origin.push(branch)

                print("🚀 Changes pushed to GitHub")

        # ----------------------------------------
        # AI CODE REVIEW
        # ----------------------------------------

        print("\n🧠 Running AI Code Review...\n")

        for file in os.listdir(repo_path):

            if file.endswith(".py"):

                file_path = os.path.join(repo_path, file)

                print(f"Reviewing {file}...")

                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()

                review = review_code(code)
                score = extract_score(review)

                # Prevent duplicate reviews for same file + repo + commit
                existing_review = db.query(Review).filter(
                    Review.repo_name == repo_name,
                    Review.file_name == file,
                    Review.github_id == github_id
                ).order_by(Review.id.desc()).first()

                new_review = Review(
                    repo_name=repo_name,
                    file_name=file,
                    score=score,
                    review=review,
                    github_id=github_id
                )

                db.add(new_review)
                db.commit()

                print(f"✅ Review saved for {file}")

    except GitCommandError as e:
        print("❌ Git Error:", str(e))

    except Exception as e:
        print("❌ Error:", str(e))

    finally:
        db.close()

    return {"status": "success"}