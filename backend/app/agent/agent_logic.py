# backend/app/agent/agent_logic.py
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.memory import ConversationSummaryBufferMemory
from typing import List, Tuple

# --- ¡NUEVO PROMPT! ---
# Usamos un prompt diseñado específicamente para agentes de "Tool Calling".
# Es mucho más robusto que el prompt de ReAct.
prompt = hub.pull("hwchase17/openai-tools-agent")

tools = [TavilySearchResults(max_results=3)]

def get_llm(streaming: bool = False):
    if os.getenv("OPENAI_API_BASE"):
        # Los agentes de Tool Calling funcionan mejor con modelos que los soportan explícitamente.
        # Puede que los modelos locales no funcionen tan bien con este agente.
        return ChatOpenAI(
            temperature=0,
            model="local-model", # Asegúrate de que este modelo soporte tool calling
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            openai_api_key="not-required",
            streaming=streaming
        )
    else:
        # Los modelos modernos de OpenAI son excelentes para esto.
        return ChatOpenAI(
            temperature=0, 
            model="gpt-4-turbo-preview",
            streaming=streaming
            # Ya no necesitamos el model_kwargs={"stop": None}
        )

def create_agent_executor(chat_history: List[Tuple[str, str]]):
    llm_for_agent = get_llm(streaming=True)
    llm_for_memory = get_llm(streaming=False)

    memory = ConversationSummaryBufferMemory(
        llm=llm_for_memory,
        max_token_limit=3500,
        memory_key="chat_history", 
        return_messages=True
    )
    
    for human_msg, ai_msg in chat_history:
        memory.chat_memory.add_user_message(human_msg)
        memory.chat_memory.add_ai_message(ai_msg)

    # --- ¡NUEVO TIPO DE AGENTE! ---
    # Usamos 'create_openai_tools_agent' en lugar de 'create_react_agent'.
    # Es más fiable porque se basa en funciones estructuradas, no en análisis de texto.
    agent = create_openai_tools_agent(llm_for_agent, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory,
        verbose=True,
        # 'handle_parsing_errors' es menos necesario aquí, pero lo dejamos por seguridad.
        handle_parsing_errors=True 
    )
    
    return agent_executor