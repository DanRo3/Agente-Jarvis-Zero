// frontend/src/pages/ChatLayout.tsx
import { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import type { ChatSession } from "../types/types";
import { getChatSessions, createNewChatSession } from "../services/chatService";
import { ChatList } from "../components/chat/ChatList";
import { useAuth } from "../context/AuthContext";

export function ChatLayout() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  useEffect(() => {
    // Cargar las sesiones del usuario al montar el componente
    const fetchSessions = async () => {
      try {
        const userSessions = await getChatSessions();
        setSessions(userSessions);
      } catch (error) {
        console.error("Error al cargar las sesiones:", error);
      }
    };
    fetchSessions();
  }, []);

  const handleNewChat = async () => {
    try {
      const newSession = await createNewChatSession();
      setSessions((prev) => [newSession, ...prev]);
      navigate(`/chat/${newSession.id}`);
    } catch (error) {
      console.error("Error al crear un nuevo chat:", error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="h-screen flex flex-col bg-slate-900 text-slate-200">
      <header className="flex items-center justify-between p-2 pl-4 border-b border-slate-700">
        <h1 className="text-xl font-bold text-cyan-400">Atlas</h1>
        <div className="flex items-center gap-4">
          <p className="text-sm text-slate-400">{user?.email}</p>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded-md text-sm font-semibold"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>
      <div className="flex-1 grid grid-cols-[260px_1fr] overflow-hidden">
        <aside className="border-r border-slate-700">
          <ChatList sessions={sessions} onNewChat={handleNewChat} />
        </aside>
        <main className="overflow-hidden">
          <Outlet />{" "}
          {/* Aquí se renderizará el componente de chat específico */}
        </main>
      </div>
    </div>
  );
}
