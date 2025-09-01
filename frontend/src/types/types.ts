// frontend/src/types.ts

export interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}

export interface MonitoringStep {
  type: 'thought' | 'tool_start' | 'tool_end' | 'stream_token' | 'stream_end' | 'error';
  content: string;
}

// --- ¡NUEVO TIPO! ---
export interface ChatSession {
  id: number;
  title: string;
  created_at: string; // La API lo enviará como una cadena de texto ISO
}

export interface ChatSessionDetails extends ChatSession {
  messages: {
    role: 'user' | 'ai';
    content: string;
  }[];
}