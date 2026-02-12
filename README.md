## Enterprise Assistant Deployment

This repo is configured for:
- Backend on Render (`render.yaml`)
- Frontend on Netlify (`netlify.toml`)

### Backend (Render)

1. Create a new Web Service from this repo.
2. Render will pick up `render.yaml`.
3. Set environment variables from `backend/.env.example`:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional, default is `gpt-4o-mini`)
- `DATABASE_URL` (Render Postgres URL)
- `SECRET_KEY`
- `CORS_ORIGINS` (include your Netlify site URL)

### Frontend (Netlify)

1. Create a new site from this repo.
2. Netlify will pick up `netlify.toml`.
3. Set environment variable from `frontend/.env.example`:
- `REACT_APP_API_URL` (your Render backend URL, for example `https://your-backend.onrender.com`)

### Local Notes

- Backend dependencies: `pip install -r backend/requirements.txt`
- Frontend dependencies: `cd frontend && npm install`
