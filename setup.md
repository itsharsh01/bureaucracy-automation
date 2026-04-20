# Project Setup Guide

This guide explains how to set up and run the backend locally.

## 1) Prerequisites

- Python 3.9+ installed
- PostgreSQL database (or Supabase Postgres URL)
- Terminal with access to project root

## 2) Clone and move to project

```bash
git clone <your-repo-url>
cd bureaucracy-automation
```

## 3) Create and activate virtual environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4) Install dependencies

```bash
pip install -r requirements.txt
```

## 5) Configure environment variables

Create a `.env` file in the project root and copy values from `.env.example`.

Required variables:

```env
DB_HOST=aws-1-ap-southeast-2.pooler.supabase.com
DB_PORT=5432
DB_DATABASE=postgres
DB_USER=postgres.scnspawdpoxpdiqcyyez
DB_PASSWORD=your_password_here
DB_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

Notes:

- `DB_URL` is the value actively used by the app for SQLAlchemy connection.
- Ensure your DB is reachable from your machine before starting the app.

## 6) Run the backend

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

- Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Expected response:

```json
{"message":"Chatbot Service is running."}
```

## 7) Useful API endpoints

- Auth:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
- Chatbot:
  - `POST /chatbot/`
  - `GET /chatbot/customer/query?customer_id=<id>`
  - `GET /chatbot/admin/queries`
  - `GET /chatbot/operator/queries`
  - `GET /chatbot/company/queries`

## 8) Common issues

- `**DB_URL is not set**`
  - Confirm `.env` exists in project root and contains `DB_URL`.
- `**ModuleNotFoundError: No module named 'src'` (for scripts)**
  - Use `PYTHONPATH=.` when running scripts.
- **Schema column missing errors**
  - Restart app so startup schema updates run.

