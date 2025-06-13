import React, { useState, useCallback } from 'react';
import ChatPanel from './components/ChatPanel';
import PreviewPanel from './components/PreviewPanel';
import Header from './components/Header';
import ResizableLayout from './components/ResizableLayout';
import { ChatMessage, VideoData } from './types';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentVideo, setCurrentVideo] = useState<VideoData | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsGenerating(true);

    try {
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          history: messages.slice(-6), // Send last 6 messages for context
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: data.message || 'Animation generated successfully!',
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      if (data.video_url) {
        setCurrentVideo({
          url: data.video_url,
          title: data.title || 'Generated Animation',
          timestamp: new Date(),
        });
      }
    } catch (error) {
      console.error('Error generating animation:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, there was an error generating your animation. Please check if the backend server is running.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsGenerating(false);
    }
  }, [messages]);

  const handleRestart = useCallback(() => {
    setMessages([]);
    setCurrentVideo(null);
    setIsGenerating(false);
  }, []);

  return (
    <div className="h-screen bg-gray-900 text-white flex flex-col font-sans">
      <Header onRestart={handleRestart} />
      <div className="flex-1 overflow-hidden">
        <ResizableLayout
          leftPanel={
            <ChatPanel
              messages={messages}
              onSendMessage={handleSendMessage}
              isGenerating={isGenerating}
              onRestart={handleRestart}
            />
          }
          rightPanel={
            <PreviewPanel
              video={currentVideo}
              isGenerating={isGenerating}
            />
          }
        />
      </div>
    </div>
  );
}

export default App;