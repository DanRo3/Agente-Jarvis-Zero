// frontend/src/components/chat/ChatBubble.tsx
import { User, Bot } from "lucide-react";
import type { ChatMessage } from "../../types/types";

interface ChatBubbleProps {
  message: ChatMessage;
}

export function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.sender === "user";

  return (
    <div className={`flex items-start gap-3 ${isUser ? "justify-end" : ""}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-cyan-900/50 flex items-center justify-center">
          <Bot className="text-cyan-400" size={20} />
        </div>
      )}
      <div
        className={`max-w-xl p-3 rounded-lg whitespace-pre-wrap break-words ${
          isUser
            ? "bg-blue-600 rounded-br-none"
            : "bg-slate-700 rounded-bl-none"
        }`}
      >
        <p>{message.text}</p>
      </div>
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center">
          <User className="text-slate-400" size={20} />
        </div>
      )}
    </div>
  );
}
