# backend/app/api/routes/auth_routes.py
import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# --- IMPORTACIONES CORREGIDAS ---
from ...crud import user_crud # Importamos directamente el módulo que necesitamos
from ...schemas import token as token_schemas
from ...schemas import user as user_schemas
from ...core import security
from ..dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class GoogleToken(BaseModel):
    token: str

@router.post("/google", response_model=token_schemas.Token)
async def login_with_google(google_token: GoogleToken, db: Session = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={google_token.token}"
            )
            response.raise_for_status()
            profile = response.json()

        if profile["aud"] != os.getenv("GOOGLE_CLIENT_ID"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de Google inválido: Audiencia incorrecta.",
            )
        
        user_email = profile["email"]
        user_google_id = profile["sub"]
        user_full_name = profile.get("name")

        # Ahora llamamos directamente a la función desde el módulo importado
        user = user_crud.get_user_by_email(db, email=user_email)
        if not user:
            user_in = user_schemas.UserCreate(
                email=user_email,
                google_id=user_google_id,
                full_name=user_full_name
            )
            user = user_crud.create_user_from_google(db, user=user_in)

        access_token = security.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token de Google inválido: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )