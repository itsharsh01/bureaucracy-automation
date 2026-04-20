from fastapi import APIRouter
from pydantic import BaseModel
from src.models.service import predict

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class TextRequest(BaseModel):
    text: str

@router.post("/")
def chat_interaction():
    return {"message": "Chatbot response"}

@router.post("/predict")
def predict_api(request: TextRequest):
    result = predict(request.text)
    return {
        "input": request.text,
        "prediction": result
    }
