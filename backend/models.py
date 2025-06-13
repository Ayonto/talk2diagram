from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    content: str
    sender: str  # 'user' or 'assistant'
    timestamp: Optional[datetime] = None

class GenerateRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class GenerateResponse(BaseModel):
    message: str
    video_url: Optional[str] = None
    title: Optional[str] = None
    error: Optional[str] = None