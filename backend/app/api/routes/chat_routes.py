# backend/app/api/routes/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...schemas import chat as chat_schemas
from ...crud import chat_crud
from ..dependencies import get_db

router = APIRouter(
    prefix="/api/sessions", # Todas las rutas aquí empezarán con /api/sessions
    tags=["Chat Sessions"], # Agrupa estas rutas en la documentación de la API
)

@router.post("/", response_model=chat_schemas.ChatSession)
def create_session(session: chat_schemas.ChatSessionCreate, db: Session = Depends(get_db)):
    return chat_crud.create_chat_session(db=db, session=session)

@router.get("/", response_model=List[chat_schemas.ChatSession])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sessions = chat_crud.get_chat_sessions(db, skip=skip, limit=limit)
    return sessions

@router.get("/{session_id}", response_model=chat_schemas.ChatSession)
def read_session(session_id: int, db: Session = Depends(get_db)):
    db_session = chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.post("/{session_id}/messages", response_model=chat_schemas.ChatMessage)
def create_message_for_session(
    session_id: int, message: chat_schemas.ChatMessageCreate, db: Session = Depends(get_db)
):
    # Verificamos primero que la sesión exista
    db_session = chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return chat_crud.create_chat_message(db=db, message=message, session_id=session_id)