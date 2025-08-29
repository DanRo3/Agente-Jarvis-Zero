# backend/app/crud/chat_crud.py
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import chat as chat_schemas

# --- Operaciones para ChatSession (sin cambios) ---

def get_chat_session(db: Session, session_id: int):
    return db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()

def get_chat_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChatSession).offset(skip).limit(limit).all()

def create_chat_session(db: Session, session: chat_schemas.ChatSessionCreate):
    db_session = models.ChatSession(title=session.title)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

# --- Operaciones para ChatMessage (¡AQUÍ ESTÁ LA CORRECCIÓN!) ---

def create_chat_message(db: Session, message: chat_schemas.ChatMessageCreate, session_id: int):
    # ANTES, este código esperaba que 'message' siempre fuera un objeto Pydantic
    # db_message = models.ChatMessage(**message.dict(), session_id=session_id)
    
    # AHORA, usamos el método dict() solo si el objeto lo tiene (si es Pydantic).
    # Si es un diccionario normal, lo usamos directamente.
    # Esto hace la función más robusta y reutilizable.
    message_data = message if isinstance(message, dict) else message.dict()
    
    db_message = models.ChatMessage(**message_data, session_id=session_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message