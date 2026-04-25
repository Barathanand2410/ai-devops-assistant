# AI DevOps Assistant

AI DevOps Assistant is a full-stack application that helps users generate CI/CD pipelines, explain generated scripts, and fix pipeline-related errors using AI.

## Features

- Generate CI/CD pipelines using AI
- Support for multiple tools:
  - GitHub Actions
  - Jenkins
  - GitLab CI
- Explain generated pipeline scripts
- Fix pipeline errors
- Chat-style interface
- Query history
- Download generated scripts
- New chat support
- Deployed frontend and backend on Google Cloud Run

## Tech Stack

### Frontend
- React
- Vite
- Axios
- Tailwind CSS

### Backend
- FastAPI
- OpenAI API
- SQLAlchemy
- SQLite

### Deployment
- Docker
- Google Cloud Run
- Artifact Registry
- Cloud Build

---

## Project Structure

```bash
ai-devops-assistant/
│
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── app.db
│   └── src/
│       ├── api/
│       ├── auth/
│       ├── config/
│       ├── db/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       ├── templates/
│       └── utils/
│
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       └── assets/
│
└── README.md

How It Works
Backend

The backend is built using FastAPI and handles:

pipeline generation
explanation requests
fix error requests
query history
script download
Frontend

The frontend is built using React + Vite and provides:

chat-based interaction
history panel
explain tab
fix error tab
new chat
clean UI for DevOps workflows
API Endpoints
Backend Endpoints
POST /ai/devops-query → Generate pipeline
POST /ai/explain → Explain generated script
POST /ai/fix-error → Fix CI/CD related error
GET /ai/history → Get history
GET /ai/download/{id} → Download generated script
Local Setup
1. Clone the repository
git clone https://github.com/your-username/ai-devops-assistant.git
cd ai-devops-assistant
2. Backend setup
cd backend
python -m venv .venv
Windows
.venv\Scripts\activate
Linux / Mac
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run backend:

uvicorn main:app --reload

Backend will be available at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
3. Frontend setup
cd frontend
npm install
npm run dev

Frontend will be available at:

http://localhost:5173
Environment Variables

Create a .env file inside backend/ and add:

OPENAI_API_KEY=your_openai_api_key

You can also add any other secret/configuration values required by your backend.

Docker Setup
Backend Dockerfile

Used to containerize the FastAPI backend for Cloud Run deployment.

Frontend Dockerfile

Used to containerize the React/Vite frontend for Cloud Run deployment.

Why .dockerignore is used

.dockerignore prevents unnecessary files such as node_modules, dist, and local editor files from being copied into the Docker build context. This makes builds cleaner, smaller, and more reliable.

Example:

node_modules
dist
.git
.vscode
Deployment
Backend Deployment (Cloud Run)

Build and deploy backend:

gcloud run deploy devops-backend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated

If deploying using image:

gcloud run deploy devops-backend \
  --image asia-south1-docker.pkg.dev/PROJECT_ID/devops-repo/devops-backend:v1 \
  --region asia-south1 \
  --allow-unauthenticated
Frontend Deployment (Cloud Run)

Deploy frontend:

gcloud run deploy devops-frontend \
  --image asia-south1-docker.pkg.dev/PROJECT_ID/devops-repo/devops-frontend:v1 \
  --region asia-south1 \
  --allow-unauthenticated
  
Updating the Deployment After Code Changes
If backend code changes
Update backend code
Test locally
Rebuild / redeploy backend

Example:

cd backend
gcloud run deploy devops-backend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
  
If frontend code changes
Update frontend code
Test locally
Rebuild / redeploy frontend

Example:

cd frontend
gcloud run deploy devops-frontend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated

Current Status
Backend deployed on Google Cloud Run
Frontend deployed on Google Cloud Run
OpenAI integration working
Full project live and accessible online
Future Improvements
Move from SQLite to PostgreSQL / Cloud SQL
Add authentication and user management
Add custom domain
Restrict CORS to frontend URL only
Add robust production error handling
Add role-based access
Add CI/CD for self-deployment
Author
Barathanand R

License

This project is for learning, internal development, and deployment practice.

#Home Page

<img width="1919" height="847" alt="homepage" src="https://github.com/user-attachments/assets/997317d7-0823-4b37-87bc-0d814a3b58c4" />
