import asyncio
import json
import logging
from typing import List, Optional
import httpx
from models import ChatMessage

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "deepseek-coder-v2:latest"
        
    async def check_connection(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json()
                    available_models = [model["name"] for model in models.get("models", [])]
                    return self.model in available_models
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
        return False
    
    def _format_chat_history(self, messages: List[ChatMessage]) -> str:
        """Format chat history for LLM context"""
        if not messages:
            return "No previous conversation."
        
        formatted = []
        for msg in messages:
            role = "User" if msg.sender == "user" else "Assistant"
            formatted.append(f"{role}: {msg.content}")
        
        return "\n".join(formatted)
    
    def _create_prompt(self, user_input: str, chat_history: List[ChatMessage]) -> str:
        """Create the complete prompt for the LLM"""
        
        history_text = self._format_chat_history(chat_history[:-1])  # Exclude current message
        
        prompt = f"""You are an expert Python developer and Manim (Community Edition) animator specialized in creating educational physics and mathematics visualizations.

You will be given a conversation history and a user request. Generate a complete, valid Manim script that creates the requested animation.

IMPORTANT RULES:
1. Return ONLY valid Python code - no markdown, explanations, or extra text
2. Use proper Manim syntax and imports
3. Create a class that inherits from Scene
4. Include appropriate animations for the concept
5. Use descriptive variable names and comments in the code
6. Focus on educational clarity - make concepts visually obvious
7. Use appropriate colors, labels, and scales
8. Call self.wait(0.5) as the last line inside the construct method to ensure a video file is produced

Previous conversation:
{history_text}

Current user request: {user_input}

Generate a complete Manim script now:"""

        return prompt
    
    def _sanitize_script(self, script: str) -> str:
        """Remove markdown fences and language hints from the LLM output"""
        # Fast-path: nothing to clean
        if "```" not in script:
            return script.strip()

        # Typical pattern: ```python\n<code>\n``` or ```\n<code>\n```.
        parts = script.split("```")

        # If there are at least three parts, the code is between the first and the last fence.
        if len(parts) >= 3:
            # parts[1] could be 'python\n<code>' or directly the code.
            code_block = parts[1]

            # Remove a leading language marker (e.g. 'python').
            code_lines = code_block.splitlines()
            if code_lines and code_lines[0].strip().lower().startswith("python"):
                code_block = "\n".join(code_lines[1:])

            return code_block.strip()

        # Fallback – remove all back-ticks if pattern is unexpected.
        return script.replace("```", "").strip()
    
    async def generate_manim_script(self, user_input: str, chat_history: List[ChatMessage]) -> Optional[str]:
        """Generate Manim script using Ollama"""
        try:
            prompt = self._create_prompt(user_input, chat_history)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "num_ctx": 4096
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    raw_script = result.get("response", "")

                    # Clean up markdown artefacts produced by the LLM
                    script = self._sanitize_script(raw_script)

                    # Basic validation of the generated script
                    if self._validate_script(script):
                        logger.info("Generated valid Manim script")
                        return script
                    else:
                        logger.error("Generated script failed validation")
                        return None
                else:
                    logger.error(f"Ollama API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            return None
    
    def _validate_script(self, script: str) -> bool:
        """Basic validation of generated Manim script"""
        required_elements = [
            "from manim import *",
            "class",
            "Scene",
            "def construct"
        ]
        
        return all(element in script for element in required_elements)