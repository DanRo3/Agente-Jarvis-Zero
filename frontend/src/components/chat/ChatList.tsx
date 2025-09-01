// frontend/src/components/chat/ChatList.tsx
import { PlusCircle } from "lucide-react";
import type { ChatSession } from "../../types/types";
import { ChatListItem } from "./ChatListItem";

interface ChatListProps {
  sessions: ChatSession[];
  onNewChat: () => void;
}

export function ChatList({ sessions, onNewChat }: ChatListProps) {
  return (
    <div className="h-full flex flex-col bg-slate-800 p-2">
      <button
        onClick={onNewChat}
        className="flex items-center justify-center gap-2 w-full p-2 mb-4 rounded-md text-sm font-semibold bg-cyan-600 hover:bg-cyan-700 transition-colors"
      >
        <PlusCircle size={18} />
        Nuevo Chat
      </button>
      <nav className="flex-1 overflow-y-auto space-y-1 pr-1">
        {sessions
          .sort(
            (a, b) =>
              new Date(b.created_at).getTime() -
              new Date(a.created_at).getTime()
          )
          .map((session) => (
            <ChatListItem key={session.id} session={session} />
          ))}
      </nav>
    </div>
  );
}
