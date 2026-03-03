# RepoSense 🔍

> AI-Powered GitHub Code Review System — Automated. Intelligent. Insightful.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 📌 Overview

**RepoSense** is a full-stack, SaaS-style AI code review platform that integrates directly with GitHub to deliver automated, intelligent code analysis every time you push. It combines GitHub OAuth authentication, real-time webhook event processing, OpenAI-powered code review, and a beautiful analytics dashboard — all wired together in a production-ready architecture.

Whether you're a solo developer looking for immediate code feedback or a team wanting automated review pipelines, RepoSense turns every `git push` into a structured, scored, and stored code review.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 GitHub OAuth Login | Authenticate securely using your GitHub account |
| 📡 Webhook Listener | Automatically receives GitHub push events in real time |
| 🤖 AI Code Review | OpenAI analyzes your Python files and generates detailed structured feedback |
| 📝 README Enhancement | AI rewrites and improves your repository's README on every push |
| 🏆 Review Scoring | Every review is assigned a quality score from 0–100 |
| 🗄️ Persistent Storage | All reviews and metadata stored in PostgreSQL via Supabase |
| 📊 Analytics Dashboard | View scores, review history, and repository stats at a glance |
| 🔄 Auto Clone / Pull | Backend automatically clones new repos or pulls updates on push |
| 🌐 ngrok Integration | Tunnel your local backend to receive live GitHub webhooks during development |

---

## 📸 Screenshots

### 🏠 Homepage
![Homepage](/homepage.png)

### 📊 Dashboard
![Dashboard](/dashboard.png)

### ⚡ Features
![Features](/features.png)

---

## 🏗️ Architecture

RepoSense is composed of three core layers — a React frontend, a FastAPI backend, and a PostgreSQL database hosted on Supabase — along with a GitHub webhook integration pipeline powered by ngrok and OpenAI.

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
│                   React + TypeScript + Tailwind             │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP / Axios
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                         │
│   OAuth Handler │ Webhook Listener │ AI Service │ REST API  │
└──────┬──────────────────────┬──────────────────────┬────────┘
       │                      │                      │
       ▼                      ▼                      ▼
┌─────────────┐   ┌───────────────────┐   ┌──────────────────┐
│  Supabase   │   │   OpenAI API      │   │   GitHub API     │
│  PostgreSQL │   │  GPT-4 / GPT-3.5  │   │  OAuth + Webhooks│
└─────────────┘   └───────────────────┘   └──────────────────┘

GitHub Push Event → ngrok → FastAPI Webhook Endpoint
                          → Clone / Pull Repo
                          → AI Reviews Code Files
                          → AI Improves README
                          → Stores Review + Score in DB
                          → Dashboard fetches & displays
```

**Data Flow Summary:**

1. User authenticates via GitHub OAuth → token stored securely in DB
2. User configures a webhook on their GitHub repository pointing to the ngrok-forwarded FastAPI endpoint
3. On every `git push`, GitHub sends a POST payload to the backend
4. The backend clones or pulls the repository, then sends Python files to OpenAI for structured review
5. OpenAI returns feedback and a score (0–100) — both stored in PostgreSQL
6. The React dashboard polls the REST API to display up-to-date analytics and per-file review breakdowns

---

## 🧱 Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **FastAPI** | High-performance async REST API framework |
| **SQLAlchemy** | ORM for database modeling and queries |
| **GitPython** | Programmatic git clone/pull operations |
| **OpenAI API** | GPT-powered code review and README improvement |
| **PostgreSQL** | Relational database for users, repos, and reviews |
| **Supabase** | Managed Postgres hosting with connection pooling |
| **Uvicorn** | ASGI server for running FastAPI |
| **Python 3.11+** | Core runtime |

### Frontend

| Technology | Purpose |
|---|---|
| **React** | Component-based UI library |
| **TypeScript** | Static typing for maintainable frontend code |
| **TailwindCSS** | Utility-first CSS framework for rapid styling |
| **Framer Motion** | Smooth animations and transitions |
| **Axios** | HTTP client for API communication |

### DevOps & Integrations

| Tool | Purpose |
|---|---|
| **ngrok** | Secure tunneling for local webhook development |
| **GitHub OAuth App** | User authentication and repo access |
| **Supabase** | Postgres database with a cloud-hosted dashboard |

---

## 📁 Project Structure

```
reposense/
│
├── backend/
│   ├── app/
│   │   ├── api/                  # Route handlers (auth, webhook, dashboard)
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── services/             # Business logic (AI review, git ops)
│   │   ├── db/                   # Database session and connection setup
│   │   └── main.py               # FastAPI app entry point, CORS, router registration
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables (excluded from git)
│
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Page-level views (Home, Dashboard, Login)
│   │   ├── hooks/                # Custom React hooks
│   │   ├── api/                  # Axios API client wrappers
│   │   └── App.tsx               # Root component and routing
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── assets/
│   ├── homepage.png
│   ├── dashboard.png
│   └── features.png
│
└── README.md
```

---

## ⚙️ Setup Instructions

> **Prerequisites:** Python 3.11+, Node.js 18+, a GitHub account, a Supabase account, and an OpenAI API key.

---

### 1️⃣ Backend Setup

**Step 1 — Navigate to the backend directory:**

```bash
cd reposense/backend
```

**Step 2 — Create and activate a virtual environment:**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**Step 3 — Install Python dependencies:**

```bash
pip install -r requirements.txt
```

**Step 4 — Create the `.env` file:**

```bash
touch .env
```

Add the following environment variables to `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# OpenAI
OPENAI_API_KEY=sk-...

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

**Step 5 — Start the backend server:**

```bash
uvicorn app.main:app --reload
```

The FastAPI server will be live at `http://localhost:8000`.  
The interactive API docs are available at `http://localhost:8000/docs`.

---

### 2️⃣ Frontend Setup

**Step 1 — Navigate to the frontend directory:**

```bash
cd reposense/frontend
```

**Step 2 — Install Node dependencies:**

```bash
npm install
```

**Step 3 — Start the development server:**

```bash
npm run dev
```

The React app will be served at `http://localhost:8080`.

---

### 3️⃣ GitHub OAuth App Setup

RepoSense uses GitHub OAuth to authenticate users and access their repository metadata.

**Step 1 — Go to GitHub Developer Settings:**

Navigate to: `https://github.com/settings/developers` → **OAuth Apps** → **New OAuth App**

**Step 2 — Fill in the application details:**

| Field | Value |
|---|---|
| Application name | `RepoSense` |
| Homepage URL | `http://localhost:8080` |
| Authorization callback URL | `http://localhost:8000/api/auth/github/callback` |

**Step 3 — Generate a client secret:**

After creating the app, click **Generate a new client secret**.

**Step 4 — Add credentials to `.env`:**

```env
GITHUB_CLIENT_ID=<your_client_id>
GITHUB_CLIENT_SECRET=<your_client_secret>
```

> When deploying to production, update the callback URL to match your deployed backend domain.

---

### 4️⃣ ngrok Webhook Tunneling Setup

GitHub webhooks require a publicly accessible HTTPS URL. During local development, ngrok provides a secure tunnel from the internet to your local server.

**Step 1 — Install ngrok:**

Download from [https://ngrok.com/download](https://ngrok.com/download) or install via Homebrew:

```bash
brew install ngrok/ngrok/ngrok
```

**Step 2 — Authenticate ngrok (first time only):**

```bash
ngrok config add-authtoken <your_ngrok_authtoken>
```

**Step 3 — Start the tunnel on port 8000:**

```bash
ngrok http 8000
```

You will see output similar to:

```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

Copy the `https://` forwarding URL.

**Step 4 — Add the webhook to your GitHub repository:**

1. Go to your target repository on GitHub
2. Navigate to **Settings → Webhooks → Add webhook**
3. Set the following:

| Field | Value |
|---|---|
| Payload URL | `https://<your-ngrok-url>/api/webhook/github` |
| Content type | `application/json` |
| Which events? | `Just the push event` |
| Active | ✅ Checked |

**Step 5 — Test the webhook:**

Make a commit and push to the repository. GitHub will send a push event to your ngrok URL, which proxies it to your local FastAPI backend. The backend will then clone/pull the repo, run AI review, and store results.

> ⚠️ The ngrok URL changes on every restart unless you have a paid plan. Remember to update the webhook payload URL each time.

---

### 5️⃣ Supabase (PostgreSQL) Setup

RepoSense uses Supabase as a managed PostgreSQL database host.

**Step 1 — Create a Supabase project:**

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Click **New Project**, fill in the project name, set a strong database password, and select a region

**Step 2 — Get your connection string:**

1. In your Supabase project dashboard, go to **Settings → Database**
2. Scroll to **Connection String** and select the **URI** format
3. It will look like:

```
postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
```

**Step 3 — Add to backend `.env`:**

```env
DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
```

**Step 4 — Initialize the database:**

SQLAlchemy will automatically create tables on first run when `Base.metadata.create_all()` is called in `main.py`. Ensure this is present before starting the server.

---

## 🔄 How It Works — End-to-End Flow

```
1. User visits the frontend and clicks "Login with GitHub"
   └─► GitHub OAuth flow begins → user grants permissions
       └─► Backend receives access token and stores GitHub ID + token in DB

2. User navigates to Settings and copies the webhook URL:
   └─► https://<ngrok-url>/api/webhook/github
       └─► User adds this as a webhook in their GitHub repo settings

3. User pushes code to their repository
   └─► GitHub detects the push event and POSTs payload to webhook URL
       └─► ngrok forwards the POST to FastAPI backend

4. Backend processes the push event:
   ├─► Extracts repository URL and owner info from payload
   ├─► Clones repo (first time) or pulls latest changes (subsequent pushes)
   ├─► Identifies Python (.py) files for review
   ├─► Sends each file to OpenAI with a structured code review prompt
   ├─► Parses AI response to extract feedback and numeric score (0–100)
   ├─► Sends README.md to OpenAI for enhancement and rewrites the file
   └─► Stores all review data, scores, and metadata in PostgreSQL

5. Frontend dashboard polls the REST API:
   ├─► GET /api/dashboard/repos/{github_id}   → list of tracked repositories
   └─► GET /api/dashboard/reviews/{github_id} → all review records with scores

6. Dashboard renders:
   ├─► Total repositories tracked
   ├─► Total reviews performed
   ├─► Average review score across all files
   └─► Per-file breakdown with individual feedback and scores
```

---

## 🔐 Security Notes

**OAuth Token Handling:**  
GitHub access tokens are stored server-side in the database and are never exposed to the frontend. All authenticated API requests are made from the backend using the stored token.

**Environment Variables:**  
All sensitive credentials (API keys, database URLs, OAuth secrets) are stored in a `.env` file which is explicitly excluded from version control via `.gitignore`. Never push `.env` to a public repository.

**Webhook Loop Prevention:**  
The webhook handler includes logic to prevent recursive loops. When the backend modifies a repository's README and commits the change, the resulting push event is detected and skipped to avoid triggering another review cycle.

**CORS Configuration:**  
CORS is configured in `main.py` using FastAPI's `CORSMiddleware`. In development, the allowed origin is restricted to `http://localhost:8080`. For production deployments, this should be updated to the specific frontend domain.

**Webhook Payload Validation:**  
The webhook endpoint validates incoming payloads to ensure they originate from expected GitHub events before triggering any processing logic.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/auth/github` | Redirects user to GitHub OAuth |
| `GET` | `/api/auth/github/callback` | Handles OAuth callback, stores user |
| `POST` | `/api/webhook/github` | Receives GitHub push events |
| `GET` | `/api/dashboard/repos/{github_id}` | Returns tracked repositories for user |
| `GET` | `/api/dashboard/reviews/{github_id}` | Returns all code reviews for user |

---

## 🚀 Future Improvements

RepoSense is built with extensibility in mind. Planned enhancements include:

**Multi-language Support**  
Expand AI review beyond Python to support JavaScript, TypeScript, Java, Go, and other languages based on file extension detection.

**GitHub App (replacing OAuth)**  
Migrate from OAuth Apps to a GitHub App for finer-grained permission scopes, organization-level access, and webhook management without manual configuration.

**Pull Request Reviews**  
Trigger AI reviews on pull request events in addition to push events, with the option to post review comments directly on the PR via the GitHub API.

**Score Trend Charts**  
Add time-series charts to the dashboard showing how a repository's average code quality score evolves over time, commit by commit.

**Deployment — Vercel + Render**  
Deploy the React frontend to Vercel and the FastAPI backend to Render for a zero-infrastructure production setup with automatic CI/CD on push.

**CI/CD Integration**  
Add a GitHub Actions workflow that runs RepoSense review checks as part of the CI pipeline, optionally blocking merges below a configurable score threshold.

**Multi-repo Dashboard Views**  
Support filtering and comparing metrics across multiple repositories simultaneously on the dashboard.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a pull request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using FastAPI, React, and OpenAI &nbsp;|&nbsp; RepoSense © 2024
</p>
