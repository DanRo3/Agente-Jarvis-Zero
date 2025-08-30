# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import user as user_schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user_from_google(db: Session, user: user_schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        google_id=user.google_id,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user