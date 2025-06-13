from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import uuid
import json
import tempfile
import subprocess
import shutil
from pathlib import Path
import logging

from llm_service import LLMService
from manim_service import ManimService
from models import ChatMessage, GenerateRequest, GenerateResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Talk2Diagram API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
manim_service = ManimService()

# Create media directory
MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

# Serve static media files
app.mount("/media", StaticFiles(directory="media"), name="media")

# In-memory session storage (in production, use Redis or database)
sessions: Dict[str, List[ChatMessage]] = {}

@app.get("/")
async def root():
    return {"message": "Talk2Diagram API is running"}

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_animation(request: GenerateRequest):
    """Generate animation from natural language description"""
    try:
        session_id = "default"  # In production, use proper session management
        
        # Get or create session history
        if session_id not in sessions:
            sessions[session_id] = []
        
        # Add user message to session
        user_message = ChatMessage(
            content=request.message,
            sender="user",
            timestamp=None
        )
        sessions[session_id].append(user_message)
        
        # Get recent context for LLM
        recent_messages = sessions[session_id][-6:]  # Last 6 messages
        
        # Generate Manim script using LLM
        logger.info(f"Generating Manim script for: {request.message}")
        manim_script = await llm_service.generate_manim_script(
            user_input=request.message,
            chat_history=recent_messages
        )
        
        if not manim_script:
            raise HTTPException(status_code=500, detail="Failed to generate Manim script")
        
        # Generate video using Manim
        logger.info("Rendering video with Manim")
        video_path = await manim_service.render_video(manim_script)
        
        if not video_path:
            raise HTTPException(status_code=500, detail="Failed to render video")
        
        # Move video to media directory with unique name
        video_id = str(uuid.uuid4())
        video_filename = f"{video_id}.mp4"
        final_video_path = MEDIA_DIR / video_filename
        
        shutil.move(video_path, final_video_path)
        
        # Add assistant response to session
        assistant_message = ChatMessage(
            content="Animation generated successfully! Here's your visualization.",
            sender="assistant",
            timestamp=None
        )
        sessions[session_id].append(assistant_message)
        
        video_url = f"http://localhost:8000/media/{video_filename}"
        
        return GenerateResponse(
            message="Animation generated successfully!",
            video_url=video_url,
            title="Generated Animation"
        )
        
    except Exception as e:
        logger.error(f"Error generating animation: {str(e)}")
        
        # Add error message to session
        if session_id in sessions:
            error_message = ChatMessage(
                content=f"Sorry, I encountered an error: {str(e)}",
                sender="assistant",
                timestamp=None
            )
            sessions[session_id].append(error_message)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    ollama_status = await llm_service.check_connection()
    manim_status = manim_service.check_installation()
    
    return {
        "status": "healthy" if ollama_status and manim_status else "unhealthy",
        "services": {
            "ollama": "connected" if ollama_status else "disconnected",
            "manim": "installed" if manim_status else "not_installed"
        }
    }

@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    if session_id in sessions:
        sessions[session_id] = []
    return {"message": "Session cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)