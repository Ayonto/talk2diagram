export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export interface VideoData {
  url: string;
  title: string;
  timestamp: Date;
}

export interface GenerateRequest {
  message: string;
  history: ChatMessage[];
}

export interface GenerateResponse {
  message: string;
  video_url?: string;
  title?: string;
  error?: string;
}