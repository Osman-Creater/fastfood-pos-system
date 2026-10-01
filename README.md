# FastFood POS + Bookkeeping System

## Overview

A monorepo starter for a multi-location fast-food POS and bookkeeping platform.

## Stack

- Backend: FastAPI
- Frontend: Next.js
- Database: PostgreSQL
- Cache: Redis
- Containerization: Docker Compose

## Run locally

```bash
docker-compose up --build
```

## Health check

```bash
curl http://localhost:8000/health
```

## Environment variables

Create a `.env` file with:

```bash
SECRET_KEY=your-secret-key
ENVIRONMENT=development
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project structure

- `backend/` — FastAPI API
- `frontend/` — POS dashboard
- `db/` — SQL schema and migration folder
- `docker-compose.yml` — local environment

## Notes

This is a working starter implementation with the core operational flows for orders, inventory, accounting, and manager reporting.
