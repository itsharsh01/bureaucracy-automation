from fastapi import APIRouter

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/")
def chat_interaction():
    return {"message": "Chatbot response"}
