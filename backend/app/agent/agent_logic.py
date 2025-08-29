# backend/app/agent/agent_logic.py
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.memory import ConversationBufferMemory
from typing import List, Tuple

# Carga el prompt estandarizado "ReAct" desde LangChain Hub.
prompt = hub.pull("hwchase17/react-chat")

# --- Herramientas (Simulación de Servidores MCP) ---
tools = [TavilySearchResults(max_results=3)]

def get_llm():
    """
    Abstracción para obtener el LLM. Permite cambiar fácilmente entre
    OpenAI, un LLM local a través de LM Studio, u otros.
    """
    # Si la URL base de OpenAI está definida (apuntando a LM Studio), úsala.
    if os.getenv("OPENAI_API_BASE"):
        return ChatOpenAI(
            temperature=0,
            model="local-model",
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            openai_api_key="not-required",
            streaming=True  # Habilita el streaming de tokens
        )
    # De lo contrario, usa la API oficial de OpenAI
    else:
        return ChatOpenAI(
            temperature=0, 
            model="gpt-4o-mini",
            streaming=True  # Habilita el streaming de tokens
        )

def create_agent_executor(chat_history: List[Tuple[str, str]]):
    """
    Función principal que ensambla y devuelve un Agente de LangChain.
    """
    llm = get_llm()

    # Nivel 1 de Memoria: Memoria Activa de Corto Plazo
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )
    for human_msg, ai_msg in chat_history:
        memory.chat_memory.add_user_message(human_msg)
        memory.chat_memory.add_ai_message(ai_msg)

    # El Agente "ReAct" (Reason + Act)
    agent = create_react_agent(llm, tools, prompt)

    # El Ejecutor del Agente
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor