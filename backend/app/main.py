from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.auth import router as auth_router
from app.api.repo import router as repo_router
from app.api.webhook import router as webhook_router
from app.api.dashboard import router as dashboard_router

# Models (important for DB table creation)
from app.models.user import User
from app.models.repository import Repository
from app.models.review import Review

from app.db.database import Base, engine


# -------------------------
# CREATE TABLES
# -------------------------

Base.metadata.create_all(bind=engine)


# -------------------------
# CREATE APP
# -------------------------

app = FastAPI()


# -------------------------
# CORS CONFIGURATION
# -------------------------

origins = [

    "http://localhost:5173",   # Lovable / Vite
    "http://localhost:3000",   # React alternative
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",

]


app.add_middleware(
    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# -------------------------
# ROUTES
# -------------------------

app.include_router(auth_router, prefix="/api/auth")

app.include_router(repo_router, prefix="/api/repo")

app.include_router(webhook_router, prefix="/api/webhook")

app.include_router(dashboard_router, prefix="/api/dashboard")


# -------------------------
# ROOT TEST
# -------------------------

@app.get("/")
def root():
    return {"message": "RepoSense Backend Running"}