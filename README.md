# auth-react-fastapi

The purpose of this app was to practice setting up auth to get a better understanding of the auth flow.

Basic CRUD funtionality was also added to get an understanding of using FastAPI and NEON Postgres.

## Backend - FastAPI

**Start Application:** `uvicorn src.main:app --reload` from backend folder.

**Install Requirements:** `pip install -r requirements`

**Python Virtual Env:** `python -m venv venv source` then `venv/bin/activate `

**Generate keys use this:** `python -c "import secrets; print(secrets.token_urlsafe(64))"`
