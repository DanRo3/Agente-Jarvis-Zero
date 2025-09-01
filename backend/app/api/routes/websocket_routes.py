# backend/app/api/routes/websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Tuple
from starlette.websockets import WebSocketState

from ...ws.connection_manager import manager
from ...agent.agent_logic import create_agent_executor
from ...crud import chat_crud
from ...db import models
from ..dependencies import get_db, get_current_user
from ...agent.streaming_callback import StreamingCallbackHandler

router = APIRouter()

async def get_user_from_websocket(token: str = Query(...), db: Session = Depends(get_db)) -> models.User:
    return get_current_user(token=token, db=db)

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    session_id: int,
    user: models.User = Depends(get_user_from_websocket),
    db: Session = Depends(get_db)
):
    db_session = chat_crud.get_chat_session(db, session_id)
    if not db_session or db_session.owner_id != user.id:
        await websocket.close(code=1008, reason="Acceso no autorizado o sesión no encontrada")
        return

    await manager.connect(websocket)
    print(f"Cliente '{user.email}' conectado a la sesión de chat #{session_id}")

    try:
        chat_history: List[Tuple[str, str]] = []
        for msg in db_session.messages:
            if msg.role == "user":
                ai_response = next((m.content for m in db_session.messages if m.id > msg.id and m.role == "ai"), "")
                if ai_response:
                    chat_history.append((msg.content, ai_response))

        agent_executor = create_agent_executor(chat_history)
        
        while True:
            user_message = await websocket.receive_text()
            
            chat_crud.create_chat_message(db, message={"role": "user", "content": user_message}, session_id=session_id)
            
            # --- ¡LA CORRECCIÓN CLAVE ESTÁ AQUÍ! ---
            # 1. Creamos la instancia del handler.
            streaming_callback = StreamingCallbackHandler()
            # 2. Le asignamos el websocket de la conexión actual explícitamente.
            streaming_callback.set_websocket(websocket)
            
            response = await agent_executor.ainvoke(
                {"input": user_message},
                config={"callbacks": [streaming_callback]}
            )
            ai_message = response["output"]
            
            chat_crud.create_chat_message(db, message={"role": "ai", "content": ai_message}, session_id=session_id)

    except WebSocketDisconnect:
        print(f"Cliente '{user.email}' desconectado (WebSocketDisconnect). Limpiando.")
    
    except Exception as e:
        error_message = f"Ha ocurrido un error inesperado en el backend: {e}"
        print(f"\n--- ERROR --- \n{error_message}\n--- END ERROR ---\n")
        if websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_json({"type": "error", "content": error_message})
            except RuntimeError:
                print("No se pudo enviar el mensaje de error, el cliente ya se había desconectado.")

    finally:
        manager.disconnect(websocket)
        print(f"Conexión para la sesión #{session_id} cerrada y limpiada.")