// frontend/src/pages/ChatPage.tsx
import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { SendHorizonal } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import type {
  ChatMessage,
  MonitoringStep as MonitoringStepType,
} from "../types/types";
import { MonitoringStep } from "../components/monitoring/MonitoringStep";
import { ChatBubble } from "../components/chat/ChatBubble";
import { getChatSessionDetails } from "../services/chatService";

export function ChatPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const { token } = useAuth();
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [monitoringSteps, setMonitoringSteps] = useState<MonitoringStepType[]>(
    []
  );
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  useEffect(() => {
    // Scroll al final del chat cuando llegan nuevos mensajes
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  useEffect(() => {
    // Resetea el chat cuando el ID de la sesión cambia
    setChatMessages([]);
    setMonitoringSteps([]);
    setInput("");

    if (!sessionId || !token) return;

    const loadChatHistory = async () => {
      setIsLoadingHistory(true);
      try {
        const sessionDetails = await getChatSessionDetails(sessionId);
        // Transformamos los mensajes de la DB al formato del estado del frontend
        const history = sessionDetails.messages.map((msg) => ({
          sender: msg.role,
          text: msg.content,
        }));
        setChatMessages(history);
      } catch (error) {
        console.error("Error al cargar el historial del chat:", error);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadChatHistory();

    const socket = new WebSocket(
      `ws://localhost:8000/ws/${sessionId}?token=${token}`
    );
    ws.current = socket;

    socket.onopen = () => setIsConnected(true);
    socket.onclose = () => setIsConnected(false);
    socket.onerror = (err) => console.error("WebSocket Error:", err);

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
          // Opcional: mostrar el error en el chat
          setChatMessages((prev) => [
            ...prev,
            { sender: "ai", text: `Error: ${data.content}` },
          ]);
          break;
      }
    };

    return () => {
      socket.close();
    };
  }, [sessionId, token]);

  const sendMessage = () => {
    if (input.trim() && isConnected && ws.current) {
      setMonitoringSteps([]);
      ws.current.send(input);
      setChatMessages((prev) => [...prev, { sender: "user", text: input }]);
      setInput("");
    }
  };

  if (!sessionId) {
    return (
      <div className="h-full grid place-content-center text-slate-500">
        <p>Selecciona o crea una nueva conversación para comenzar.</p>
      </div>
    );
  }

  if (isLoadingHistory) {
    return (
      <div className="h-full grid place-content-center text-slate-500">
        Cargando historial...
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 h-full">
      {/* Panel Izquierdo: Conversación */}
      <div className="flex flex-col p-4 border-r border-slate-700 overflow-hidden">
        <div className="flex-1 overflow-y-auto pr-2 space-y-4">
          {chatMessages.map((msg, index) => (
            <ChatBubble key={index} message={msg} />
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className="mt-4 flex gap-2">
          <input
            type="text"
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 disabled:opacity-50"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
            placeholder={isConnected ? "Habla con Atlas..." : "Conectando..."}
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
          Razonamiento del Agente
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
    </div>
  );
}
