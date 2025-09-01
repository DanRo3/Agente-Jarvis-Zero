// frontend/src/services/chatService.ts
import apiClient from './apiClient';
import type { ChatSession, ChatSessionDetails } from '../types/types';

export const getChatSessions = async (): Promise<ChatSession[]> => {
  const response = await apiClient.get('/api/sessions/');
  return response.data;
};

export const createNewChatSession = async (title: string = "Nueva Conversación"): Promise<ChatSession> => {
  const response = await apiClient.post('/api/sessions/', { title });
  return response.data;
};

export const getChatSessionDetails = async (sessionId: string): Promise<ChatSessionDetails> => {
  const response = await apiClient.get(`/api/sessions/${sessionId}`);
  return response.data;
};