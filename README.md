# SatsScore — Bitcoin Financial Intelligence

> CUBO+ Hackathon 2026 | "Don't trust, verify"

## Team

| Name | Role | GitHub |
|------|------|--------|
| | Tech Lead | @wkatir |
| | Tech | |
| | Non-Tech Lead | |
| | Non-Tech | |

## Tech Stack

- **Backend**: FastAPI (Python 3.11+) — Dockerized
- **Database**: PostgreSQL 16 — Dockerized
- **Frontend**: Flutter Web — Deployed on Cloudflare Pages
- **ORM**: SQLAlchemy + Alembic (migrations)
- **Validation**: Pydantic

## Repository Structure

```
/src         → Backend Python (FastAPI) + Dockerfile
/frontend    → Flutter app (Cloudflare Pages)
/strategy    → Business model & documentation (Non-Tech)
```

## Quick Start

### Backend + Database (Docker)

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

### Frontend (Flutter)

```bash
cd frontend
flutter pub get
flutter run -d chrome --dart-define=API_URL=http://localhost:8000
```

### Deploy Frontend to Cloudflare Pages

```bash
cd frontend
flutter build web --release --dart-define=API_URL=https://your-api-domain.com
# Output: frontend/build/web/ → deploy this folder
```

## Submission

**Deadline**: April 21, 2026
