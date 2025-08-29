# backend/app/agent/streaming_callback.py
from typing import Any, Dict, List
from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema.agent import AgentFinish

# Define los tipos de mensajes que enviaremos al frontend
class StreamMessage(Dict):
    type: str
    content: Any

class StreamingCallbackHandler(AsyncCallbackHandler):
    """
    Callback handler que transmite los pasos del agente y los tokens del LLM
    a través de un WebSocket.
    """
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def send_stream_message(self, data: StreamMessage):
        """Envía un mensaje estructurado al cliente WebSocket."""
        await self.websocket.send_json(data)

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Se ejecuta cuando el LLM empieza a 'pensar'."""
        await self.send_stream_message({
            "type": "thought",
            "content": "🧠 Pensando..."
        })

    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Se ejecuta cuando el agente va a usar una herramienta."""
        tool_name = serialized.get("name", "Herramienta Desconocida")
        await self.send_stream_message({
            "type": "tool_start",
            "content": f"🛠️ Usando Herramienta: `{tool_name}` con entrada: `{input_str}`"
        })

    async def on_tool_end(
        self, output: str, **kwargs: Any
    ) -> None:
        """Se ejecuta cuando la herramienta termina y devuelve una observación."""
        await self.send_stream_message({
            "type": "tool_end",
            "content": f"👀 Observación: `{output}`"
        })
    
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Se ejecuta cada vez que el LLM genera un nuevo token."""
        await self.send_stream_message({
            "type": "stream_token", 
            "content": token
        })

    async def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Se ejecuta cuando el agente ha terminado su razonamiento."""
        await self.send_stream_message({
            "type": "stream_end",
            "content": ""
        })