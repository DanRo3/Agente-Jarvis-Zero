// frontend/src/App.tsx
import { useState, useRef, useCallback } from "react";
import { SendHorizonal, Plug, PlugZap } from "lucide-react";
import type {
  ChatMessage,
  MonitoringStep as MonitoringStepType,
} from "./types/types";
import { MonitoringStep } from "./components/monitoring/MonitoringStep";
import { ChatBubble } from "./components/chat/ChatBubble";

function App() {
  const [sessionId, setSessionId] = useState("1");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [monitoringSteps, setMonitoringSteps] = useState<MonitoringStepType[]>(
    []
  );
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
    }
    if (!sessionId.trim()) {
      alert("Por favor, introduce un ID de sesión.");
      return;
    }

    const socket = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    ws.current = socket;

    socket.onopen = () => {
      console.log("WebSocket conectado!");
      setIsConnected(true);
    };
    socket.onclose = () => {
      console.log("WebSocket desconectado.");
      setIsConnected(false);
    };
    socket.onerror = (error) => {
      console.error("Error en WebSocket:", error);
      setIsConnected(false);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case "thought":
        case "tool_start":
        case "tool_end":
          setMonitoringSteps((prev) => [...prev, data]);
          break;

        case "stream_token":
          setChatMessages((prevMessages) => {
            const lastMessage = prevMessages[prevMessages.length - 1];
            if (lastMessage && lastMessage.sender === "ai") {
              const updatedMessages = [...prevMessages];
              updatedMessages[prevMessages.length - 1] = {
                ...lastMessage,
                text: lastMessage.text + data.content,
              };
              return updatedMessages;
            } else {
              return [...prevMessages, { sender: "ai", text: data.content }];
            }
          });
          break;

        case "stream_end":
          console.log("Streaming de respuesta finalizado.");
          break;

        case "error":
          console.error("Error desde el backend:", data.content);
          alert(`Error del servidor: ${data.content}`);
          break;
      }
    };
  }, [sessionId]);

  const sendMessage = () => {
    if (
      input.trim() &&
      isConnected &&
      ws.current?.readyState === WebSocket.OPEN
    ) {
      setMonitoringSteps([]);
      ws.current.send(input);
      setChatMessages((prev) => [...prev, { sender: "user", text: input }]);
      setInput("");
    }
  };

  return (
    <div className="bg-slate-900 text-slate-200 font-sans h-screen flex flex-col">
      <header className="flex items-center justify-between p-3 border-b border-slate-700 bg-slate-800/50">
        <h1 className="text-xl font-bold text-cyan-400">Atlas - Agente IA</h1>
        <div className="flex items-center gap-3">
          <input
            type="text"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            placeholder="ID de Sesión"
            className="w-24 bg-slate-700 border border-slate-600 rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500"
          />
          <button
            onClick={connect}
            className="bg-cyan-600 hover:bg-cyan-700 px-3 py-1 rounded-md text-sm font-semibold flex items-center gap-2"
          >
            {isConnected ? <PlugZap size={16} /> : <Plug size={16} />}
            {isConnected ? "Conectado" : "Conectar"}
          </button>
        </div>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-2 flex-1 overflow-hidden">
        {/* Panel Izquierdo: Conversación */}
        <div className="flex flex-col p-4 border-r border-slate-700 overflow-hidden">
          <div className="flex-1 overflow-y-auto pr-2 space-y-4">
            {chatMessages.map((msg, index) => (
              <ChatBubble key={index} message={msg} />
            ))}
          </div>
          <div className="mt-4 flex gap-2">
            <input
              type="text"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 disabled:opacity-50"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && sendMessage()}
              placeholder={
                isConnected
                  ? "Habla con Atlas..."
                  : "Conéctate a una sesión para empezar"
              }
              disabled={!isConnected}
            />
            <button
              onClick={sendMessage}
              className="bg-cyan-600 hover:bg-cyan-700 p-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!isConnected || !input.trim()}
            >
              <SendHorizonal size={24} />
            </button>
          </div>
        </div>

        {/* Panel Derecho: Razonamiento del Agente */}
        <div className="flex flex-col p-4 overflow-hidden">
          <h2 className="text-lg font-bold text-center mb-4 text-purple-400">
            Razonamiento del Agente (Ciclo ReAct)
          </h2>
          <div className="flex-1 overflow-y-auto bg-slate-800/50 rounded-lg p-3 space-y-3">
            {monitoringSteps.length === 0 && (
              <p className="text-slate-500 text-center pt-4">
                Esperando una tarea...
              </p>
            )}
            {monitoringSteps.map((step, index) => (
              <MonitoringStep key={index} step={step} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
