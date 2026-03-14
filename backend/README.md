# Backend (Step 1: DB & Migrations)

This folder is the **infrastructure-only** backend scaffold (no API routes yet).

## 1) Setup

Create `backend/.env` based on `.env.example` and set `DATABASE_URL`:

- PostgreSQL example:

  `DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/global_vision"`

Install deps (recommended inside `backend/.venv`):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Create migration (first time)

```bash
cd backend
source .venv/bin/activate
python -m alembic revision --autogenerate -m "init tables"
```

## 3) Apply migration

```bash
cd backend
source .venv/bin/activate
python -m alembic upgrade head
```

When it succeeds, you should see 3 tables created:
`sources`, `articles`, `ai_results`.

