# Talk2Diagram

Talk2Diagram is an innovative application that converts natural language descriptions into visual diagrams. It combines the power of language models with visualization tools to create dynamic and interactive diagrams based on user input.

## Features

- Natural language to diagram conversion
- Real-time diagram generation
- Interactive user interface
- Support for various diagram types
- Fast and responsive design

## Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Axios for API communication

### Backend
- Python
- FastAPI
- Language Model Integration
- Manim for diagram generation

## Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- npm package manager

## Getting Started

### Frontend Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd talk2diagram
```

2. Install frontend dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. As of now the project uses Ollama. <br>
* Install Ollama and pull the model `deepseek-coder-v2:latest` or any model of your choice ( coding specific )
* change the model name in `self.model = "deepseek-coder-v2:latest"` under `llm_service.py` file

**Must start the ollama server**
```bash
ollama serve
```

The backend API will be available at `http://localhost:8000`

## Development

### Frontend Development

- Run development server: `npm run dev`


### Backend Development

The backend consists of several key components:
- `main.py`: FastAPI application entry point
- `llm_service.py`: Language model integration
- `manim_service.py`: Diagram generation service
- `models.py`: Data models

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
