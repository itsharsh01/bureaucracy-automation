# Development Guide

This guide covers the basic instructions on how to run the project locally and how to add new API routes to the FastAPI backend.

## How to Run the Project

### 1. Set Up a Virtual Environment (venv)
It is highly recommended to use a virtual environment to manage dependencies securely.

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

*Note: If you run into Execution Policy errors on Windows, run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` as administrator.*

### 2. Install Dependencies
Make sure your virtual environment is activated (you will see `(venv)` prefixing your terminal prompt), then install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Starting the Server
To run the FastAPI server locally in development mode (with auto-reload enabled), execute exactly this command from the root of your project:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
- Your API will be running at [http://localhost:8000](http://localhost:8000)
- The interactive API documentation (Swagger UI) is automatically available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## How to Create a New Route (Feature Module)

We follow a feature-based folder structure. If you need to build a new set of API endpoints (for example, "billing"), follow these steps:

### 1. Create a Feature Folder
Create a new directory inside `src` for your feature:
```text
src/
└── billing/
```

### 2. Create a `router.py`
Inside your new feature folder, create a `router.py` file. Set up an `APIRouter` specifically for this domain:

```python
# src/billing/router.py
from fastapi import APIRouter

# Setting a prefix so all routes in this file will automatically start with /billing
router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/")
def get_billing_info():
    return {"message": "Billing data"}

@router.post("/")
def create_invoice():
    return {"message": "Invoice created"}
```

### 3. Register the Router in `main.py`
Once your router is ready, you must connect it to the main FastAPI application so it actually gets exposed.

Open `src/main.py` and modify it to include your new router:

```python
# src/main.py
from fastapi import FastAPI
try:
    from src.auth.router import router as auth_router
    from src.chatbot.router import router as chatbot_router
    from src.dashboard.router import router as dashboard_router
    # 1. Import your new router
    from src.billing.router import router as billing_router
except ModuleNotFoundError:
    from auth.router import router as auth_router
    from chatbot.router import router as chatbot_router
    from dashboard.router import router as dashboard_router
    # 1. Provide the fallback import
    from billing.router import router as billing_router

app = FastAPI(title="Complaint Chatbot API")

app.include_router(auth_router)
app.include_router(chatbot_router)
app.include_router(dashboard_router)
# 2. Include the router in the app
app.include_router(billing_router)
```

Now, when you visit `/docs`, you will see your new `Billing` endpoints categorized and ready to be tested!
