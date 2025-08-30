# backend/app/api/routes/websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Tuple

from ...ws.connection_manager import manager
from ...agent.agent_logic import create_agent_executor
from ... import crud, models
from ..dependencies import get_db
from ..dependencies import get_current_user # Reutilizamos la lógica del guardián

router = APIRouter()

# Dependencia especial para obtener el usuario desde el token en los parámetros del WebSocket
async def get_user_from_websocket(token: str = Query(...), db: Session = Depends(get_db)) -> models.User:
    return get_current_user(token=token, db=db)

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    session_id: int,
    user: models.User = Depends(get_user_from_websocket),
    db: Session = Depends(get_db)
):
    # ¡VERIFICACIÓN DE PROPIEDAD CRUCIAL!
    db_session = crud.chat_crud.get_chat_session(db, session_id)
    if not db_session or db_session.owner_id != user.id:
        await websocket.close(code=1008, reason="Acceso no autorizado o sesión no encontrada")
        return

    await manager.connect(websocket)
    print(f"Cliente '{user.email}' conectado a la sesión de chat #{session_id}")

    # ... (El resto del código de hidratación y del bucle del agente no cambia) ...
    # ... (Pega el resto del código de la función desde la versión anterior aquí) ...

    chat_history: List[Tuple[str, str]] = []
    for msg in db_session.messages:
        if msg.role == "user":
            ai_response = next((m.content for m in db_session.messages if m.id > msg.id and m.role == "ai"), "")
            if ai_response:
                chat_history.append((msg.content, ai_response))

    agent_executor = create_agent_executor(chat_history)
    
    try:
        while True:
            # ... (el bloque try/except para invocar al agente sigue siendo el mismo) ...
            user_message = await websocket.receive_text()
            # ... (el resto del bucle) ...
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Cliente '{user.email}' desconectado de la sesión #{session_id}")