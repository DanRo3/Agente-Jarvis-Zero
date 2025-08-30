# backend/app/api/routes/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ... import crud, schemas, models
from ..dependencies import get_db, get_current_active_user

router = APIRouter(
    prefix="/api/sessions",
    tags=["Chat Sessions"],
    dependencies=[Depends(get_current_active_user)] # ¡Seguridad a nivel de router!
)

@router.post("/", response_model=schemas.ChatSession)
def create_session(
    session: schemas.ChatSessionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.chat_crud.create_chat_session(db=db, session=session, user_id=current_user.id)

@router.get("/", response_model=List[schemas.ChatSession])
def read_sessions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.chat_crud.get_chat_sessions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=schemas.ChatSession)
def read_session(
    session_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_session = crud.chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    # ¡VERIFICACIÓN DE PROPIEDAD CRUCIAL!
    if db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta sesión")
    return db_session

@router.post("/{session_id}/messages", response_model=schemas.ChatMessage)
def create_message_for_session(
    session_id: int, 
    message: schemas.ChatMessageCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_session = crud.chat_crud.get_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    # ¡VERIFICACIÓN DE PROPIEDAD CRUCIAL!
    if db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta sesión")
    return crud.chat_crud.create_chat_message(db=db, message=message, session_id=session_id)