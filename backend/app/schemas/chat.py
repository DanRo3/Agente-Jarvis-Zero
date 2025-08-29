# backend/app/schemas/chat.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

# --- Esquemas para Mensajes ---

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    timestamp: datetime

    class Config:
        orm_mode = True # Permite que Pydantic lea datos desde modelos ORM (SQLAlchemy)

# --- Esquemas para Sesiones de Chat ---

class ChatSessionBase(BaseModel):
    title: str

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    created_at: datetime
    messages: List[ChatMessage] = [] # Incluye los mensajes relacionados

    class Config:
        orm_mode = True