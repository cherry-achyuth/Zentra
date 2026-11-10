from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.chatbot import get_chat_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    thread_id : str

@app.post('/chat')
def chat_req(request:ChatRequest):
    answer  = get_chat_response(
        request.message,
        request.thread_id
    )

    return {"reply":answer}

app.add_middleware(CORSMiddleware,
                   allow_origins = ["http://localhost:5173"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   allow_methods = ["*"])