# backend/app/api/routes/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# --- IMPORTACIONES CORREGIDAS ---
from ...crud import chat_crud # Importamos directamente el módulo que necesitamos
from ...db import models
from ...schemas import chat as chat_schemas
from ..dependencies import get_db, get_current_active_user

router = APIRouter(
    prefix="/api/sessions",
    tags=["Chat Sessions"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=chat_schemas.ChatSession)
def create_session(
    session: chat_schemas.ChatSessionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_active_user)
):
    # Ahora llamamos directamente a la función desde el módulo importado
    return chat_crud.create_chat_session(db=db, session=session, user_id=current_user.id)

@router.get("/", response_model=List[chat_schemas.ChatSession])
def read_sessions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return chat_crud.get_chat_sessions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=chat_schemas.ChatSession)
def read_session(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_session = chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta sesión")
    return db_session

@router.post("/{session_id}/messages", response_model=chat_schemas.ChatMessage)
def create_message_for_session(
    session_id: int, 
    message: chat_schemas.ChatMessageCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_session = chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta sesión")
    return chat_crud.create_chat_message(db=db, message=message, session_id=session_id)