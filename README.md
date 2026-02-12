# Enterprise AI Knowledge Assistant

Full-stack app for document upload + Q&A.

- Backend: FastAPI (`backend/`)
- Frontend: React (`frontend/`)
- Backend on Render (`render.yaml`)
- Frontend on Netlify (`netlify.toml`)

## Project Structure

- `backend/app/main.py` FastAPI app entrypoint
- `backend/app/routes/qa.py` Q&A and file upload endpoints
- `backend/app/routes/auth.py` auth endpoints
- `frontend/src/App.js` app UI
- `render.yaml` Render service config
- `netlify.toml` Netlify build/SPA routing config

## Local Run

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Required backend env (`backend/.env`):
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `DATABASE_URL` (for local: `sqlite:///./app.db`)
- `SECRET_KEY`
- `CORS_ORIGINS` (for local: `http://localhost:3000`)

### 2. Frontend

```powershell
cd frontend
npm install
copy .env.example .env
npm start
```

Required frontend env (`frontend/.env`):
- `REACT_APP_API_URL=http://127.0.0.1:8000`

## API Endpoints

- `GET /health` health check
- `POST /ask` body: `{ "question": "..." }`
- `POST /upload` multipart file upload
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

## Production Deploy (Render + Netlify)

## Render (Backend)

Create a Render **Web Service** from this repo.

Use these values:
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`

Set env vars in Render:
- `OPENAI_API_KEY=...`
- `OPENAI_MODEL=gpt-4o-mini`
- `DATABASE_URL=<Render Postgres URL>`
- `SECRET_KEY=<long-random-string>`
- `CORS_ORIGINS=https://<your-netlify-site>.netlify.app`

Expected live backend URL format:
- `https://<render-service-name>.onrender.com`

Quick validation:
- `https://<render-service-name>.onrender.com/health` returns `{"status":"ok"}`

## Netlify (Frontend)

Create a Netlify site from this repo.

Use these values:
- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `build`

Set env vars in Netlify:
- `REACT_APP_API_URL=https://<render-service-name>.onrender.com`

Expected live frontend URL format:
- `https://<your-netlify-site>.netlify.app`

## First-Time Go-Live Flow

1. Deploy backend on Render and wait until `/health` is OK.
2. Copy backend URL and add it to Netlify `REACT_APP_API_URL`.
3. Add Netlify URL to Render `CORS_ORIGINS`.
4. Trigger redeploy on both services.
5. Open frontend URL and upload a file.
6. Ask a question and confirm you get a detailed response.

## Known Runtime Cases

- If OpenAI quota is exhausted, backend returns a safe fallback message from `POST /ask` instead of crashing.
- Upload returns quickly and indexing runs in a background task.

## Troubleshooting

- CORS error in browser: check `CORS_ORIGINS` includes exact Netlify domain.
- Frontend cannot reach API: check `REACT_APP_API_URL` and redeploy Netlify.
- `429 insufficient_quota`: add billing/credits to OpenAI API project, or switch API key to a funded project.
