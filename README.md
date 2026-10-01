# FastFood POS + Bookkeeping System

This repository contains a starter monorepo for a multi-location fast-food POS system with inventory control, accounting, and reporting.

## Structure

- `backend/` - FastAPI backend
- `frontend/` - Next.js POS UI
- `docker-compose.yml` - local orchestration for Postgres + Redis + backend + frontend

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Notes

This is an implementation starter. It includes:
- FastAPI app skeleton
- JWT auth example
- order flow scaffolding
- reporting endpoints
- shift-close reconciliation service
- initial database models
- Next.js POS dashboard shell

## Production next steps

- Add Alembic migrations
- Add full SQLAlchemy models for all tables
- Add database repositories and service layer for all entities
- Add RBAC enforcement per location
- Add file uploads and receipt printing integration
- Add inventory receiving, stock transfer, and financial reconciliation flows
