// frontend/src/components/chat/ChatListItem.tsx
import { MessageSquare } from "lucide-react";
import type { ChatSession } from "../../types/types";
import { NavLink } from "react-router-dom";

interface ChatListItemProps {
  session: ChatSession;
}

export function ChatListItem({ session }: ChatListItemProps) {
  return (
    <NavLink
      to={`/chat/${session.id}`}
      className={({ isActive }) =>
        `flex items-center gap-3 p-2 rounded-md text-sm transition-colors ${
          isActive
            ? "bg-cyan-500/20 text-cyan-300"
            : "text-slate-400 hover:bg-slate-700/50"
        }`
      }
    >
      <MessageSquare size={18} />
      <span className="flex-grow truncate">{session.title}</span>
    </NavLink>
  );
}
