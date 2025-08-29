# backend/app/api/routes/websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List, Tuple

from ...ws.connection_manager import manager
from ...agent.agent_logic import create_agent_executor
from ...crud import chat_crud
from ..dependencies import get_db
from ...agent.streaming_callback import StreamingCallbackHandler # <-- IMPORTANTE

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    print(f"Cliente conectado a la sesión de chat #{session_id}")

    # 1. Hidratar Memoria (sin cambios)
    chat_history: List[Tuple[str, str]] = []
    db_session = chat_crud.get_chat_session(db, session_id)
    if not db_session:
        print(f"Error: Sesión de chat #{session_id} no encontrada.")
        await websocket.close(code=1011, reason="Session not found")
        return
        
    for msg in db_session.messages:
        if msg.role == "user":
            ai_response = next((m.content for m in db_session.messages if m.id > msg.id and m.role == "ai"), "")
            if ai_response:
                chat_history.append((msg.content, ai_response))

    # 2. Crear instancia del agente (sin cambios)
    agent_executor = create_agent_executor(chat_history)
    
    try:
        while True:
            user_message = await websocket.receive_text()
            print(f"Mensaje de usuario recibido: {user_message}")
            chat_crud.create_chat_message(db, message={"role": "user", "content": user_message}, session_id=session_id)
            
            # --- ¡AQUÍ ESTÁ LA MAGIA! ---
            # 3. Creamos una instancia de nuestro "espía" para esta ejecución específica
            streaming_callback = StreamingCallbackHandler(websocket)
            
            # 4. Invocamos al agente, pasándole el callback
            # El agente ahora transmitirá sus pensamientos a través del callback
            response = await agent_executor.ainvoke(
                {"input": user_message},
                config={"callbacks": [streaming_callback]}
            )
            ai_message = response["output"]
            
            print(f"Respuesta de la IA generada: {ai_message}")

            # Guardamos la respuesta de la IA en la base de datos
            chat_crud.create_chat_message(db, message={"role": "ai", "content": ai_message}, session_id=session_id)

            # La respuesta final ya fue enviada por el callback on_agent_finish
            # por lo que no necesitamos un send_personal_message aquí.

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Cliente desconectado de la sesión de chat #{session_id}")