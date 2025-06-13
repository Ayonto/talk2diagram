# Talk2Diagram Backend

This is the FastAPI backend for Talk2Diagram that processes natural language input and generates Manim animations.

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from https://ollama.com
3. **Manim** - Mathematical Animation Engine

## Setup Instructions

### 1. Install Ollama and Model
```bash
# Install Ollama (visit https://ollama.com for your platform)
# Then pull the required model:
ollama pull codellama:7b
```

### 2. Install Manim
```bash
# Install Manim (Mathematical Animation Engine)
pip install manim

# For better performance, you might also need:
# - FFmpeg (for video processing)
# - LaTeX (for math rendering)
```

### 3. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the Backend
```bash
cd backend
python main.py
or 
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `POST /api/generate` - Generate animation from text
- `GET /api/health` - Check service status
- `GET /media/{filename}` - Serve generated videos

## Testing

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show a sine wave animation",
    "history": []
  }'
```

## Troubleshooting

1. **Ollama not running**: Make sure Ollama is installed and the service is running
2. **Model not found**: Run `ollama pull codellama:7b` to download the model
3. **Manim errors**: Ensure Manim is properly installed with `manim --version`
4. **Permission errors**: Make sure the backend has write permissions for temporary files