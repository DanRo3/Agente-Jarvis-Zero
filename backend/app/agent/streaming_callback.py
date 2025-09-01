# backend/app/agent/streaming_callback.py
from typing import Any, Dict, List
from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema.agent import AgentFinish
from starlette.websockets import WebSocketState

class StreamMessage(Dict):
    type: str
    content: Any

class StreamingCallbackHandler(AsyncCallbackHandler):
    """
    Callback handler que transmite los pasos del agente y los tokens del LLM
    a través de un WebSocket.
    """
    # --- ¡LA CORRECCIÓN CLAVE ESTÁ AQUÍ! ---
    # Hacemos que 'websocket' sea opcional en el constructor.
    # Si LangChain lo instancia internamente sin argumentos, no fallará.
    # Lo asignaremos más tarde en el endpoint del WebSocket.
    def __init__(self, websocket: WebSocket = None):
        self.websocket = websocket

    def set_websocket(self, websocket: WebSocket):
        """Método para asignar el websocket después de la instanciación."""
        self.websocket = websocket

    async def send_stream_message(self, data: StreamMessage):
        """Envía un mensaje estructurado, manejando desconexiones."""
        if self.websocket and self.websocket.client_state == WebSocketState.CONNECTED:
            try:
                await self.websocket.send_json(data)
            except Exception as e:
                print(f"Error en callback al enviar: {e}. El cliente probablemente se desconectó.")
        else:
            # Es normal que esto ocurra si la conexión se cierra a mitad de un stream.
            # No es necesario imprimir un warning ruidoso.
            pass

    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        await self.send_stream_message({"type": "thought", "content": "🧠 Pensando..."})

    async def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        tool_name = serialized.get("name", "Herramienta Desconocida")
        await self.send_stream_message({"type": "tool_start", "content": f"🛠️ Usando Herramienta: `{tool_name}`"})

    async def on_tool_end(self, output: str, **kwargs: Any) -> None:
        await self.send_stream_message({"type": "tool_end", "content": f"👀 Observación: `{output}`"})
    
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        await self.send_stream_message({"type": "stream_token", "content": token})

    async def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        await self.send_stream_message({"type": "stream_end", "content": ""})