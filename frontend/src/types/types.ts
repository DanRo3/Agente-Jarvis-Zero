// frontend/src/types.ts

export interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}

export interface MonitoringStep {
  type: 'thought' | 'tool_start' | 'tool_end' | 'final_answer';
  content: string;
}