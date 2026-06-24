from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.gemini_chain import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    history: list[str] = []
    brand: str | None = None
    gender: str | None = None

@router.post("/chat")
def chat(request: ChatRequest):
    response, history = generate_response(request.query, request.history, request.brand, request.gender)
    return {"response": response, "history": history}