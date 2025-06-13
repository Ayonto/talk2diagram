import os
import tempfile
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class ManimService:
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "talk2diagram"
        self.temp_dir.mkdir(exist_ok=True)
        
    def check_installation(self) -> bool:
        """Check if Manim is installed"""
        try:
            result = subprocess.run(
                ["manim", "--version"], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def render_video(self, script: str) -> Optional[str]:
        """Render Manim script to video"""
        try:
            # Create unique directory for this render
            import uuid
            render_id = str(uuid.uuid4())
            render_dir = self.temp_dir / render_id
            render_dir.mkdir()
            
            # Write script to file
            script_path = render_dir / "scene.py"
            with open(script_path, 'w') as f:
                f.write(script)
            
            # Extract scene class name from script
            scene_name = self._extract_scene_name(script)
            if not scene_name:
                logger.error("Could not extract scene name from script")
                return None
            
            # Run Manim
            cmd = [
                "manim",
                "-qm",  # Medium quality
                "--disable_caching",
                "--format=mp4",
                str(script_path),
                scene_name
            ]
            
            logger.info(f"Running Manim command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=render_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Manim failed: {result.stderr}")
                return None
            
            # Find the generated video file
            media_dir = render_dir / "media" / "videos" / "scene" / "720p30"
            if media_dir.exists():
                video_files = list(media_dir.glob("*.mp4"))
                if video_files:
                    return str(video_files[0])
            
            logger.error("No video file generated")
            return None
            
        except subprocess.TimeoutExpired:
            logger.error("Manim rendering timed out")
            return None
        except Exception as e:
            logger.error(f"Error rendering video: {e}")
            return None
    
    def _extract_scene_name(self, script: str) -> Optional[str]:
        """Extract scene class name from Manim script"""
        lines = script.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('class ') and 'Scene' in line:
                # Extract class name
                parts = line.split()
                if len(parts) >= 2:
                    class_name = parts[1].split('(')[0]
                    return class_name
        return None
    
    def cleanup_temp_files(self):
        """Clean up old temporary files"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                self.temp_dir.mkdir()
        except Exception as e:
            logger.error(f"Error cleaning temp files: {e}")