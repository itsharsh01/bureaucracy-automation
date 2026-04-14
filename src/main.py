from fastapi import FastAPI
try:
    from src.auth.router import router as auth_router
    from src.chatbot.router import router as chatbot_router
    from src.dashboard.router import router as dashboard_router
except ModuleNotFoundError:
    from auth.router import router as auth_router
    from chatbot.router import router as chatbot_router
    from dashboard.router import router as dashboard_router

from src.db.database import engine
from src.db.base import Base

# Automatically create all gathered tables on server startup (no Alembic needed)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complaint Chatbot API")

app.include_router(auth_router)
app.include_router(chatbot_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Chatbot Service is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

