# backend/app/crud/chat_crud.py
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import chat as chat_schemas

# --- Operaciones para ChatSession ---

def get_chat_session(db: Session, session_id: int):
    # Esta función no cambia, la verificación de propietario se hace en la API
    return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()

def get_chat_sessions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # ¡NUEVA LÓGICA! Filtra por el propietario
    return db.query(models.ChatSession).filter(models.ChatSession.owner_id == user_id).offset(skip).limit(limit).all()

def create_chat_session(db: Session, session: chat_schemas.ChatSessionCreate, user_id: int):
    # ¡NUEVA LÓGICA! Asigna el propietario al crear
    db_session = models.ChatSession(**session.dict(), owner_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

# --- Operaciones para ChatMessage (sin cambios) ---

def create_chat_message(db: Session, message: chat_schemas.ChatMessageCreate, session_id: int):
    message_data = message if isinstance(message, dict) else message.dict()
    db_message = models.ChatMessage(**message_data, session_id=session_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message