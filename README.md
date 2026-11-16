
# Zentra

A lightweight conversational AI application that connects a FastAPI backend with a React frontend and uses a LangGraph workflow to power thread-aware chatbot responses with Groq-hosted LLM inference.

Zentra acts as a central hub for conversations: users send messages from the frontend, the backend routes the request through a stateful chat graph, and the model returns a response while preserving memory for each thread.

## Overview

This project is designed as a simple but extensible conversational AI app. It demonstrates:

- a FastAPI backend for API handling
- a React + Vite frontend for user interaction
- LangGraph-based orchestration for chat logic
- Groq-backed LLM inference through `langchain_groq`
- thread-based memory using `InMemorySaver`
- local development support with CORS for frontend-backend communication

## Features

- Multi-turn chat support using a LangGraph workflow
- Thread-based memory separation via `thread_id`
- FastAPI endpoint for chat requests
- Simple React interface for sending and receiving messages
- Easy local setup for development and experimentation
- Extensible foundation for future AI app features

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain
- Groq LLM API
- python-dotenv

### Frontend
- React
- Vite
- JavaScript

## Architecture

The project is organized into three main parts:

1. Backend logic in `app/chatbot.py`
   - builds a LangGraph state graph
   - creates the LLM connection using `ChatGroq`
   - stores memory with `InMemorySaver`
   - exposes `get_chat_response(message, thread_id)`

2. API layer in `app/myapi.py`
   - defines the `ChatRequest` schema
   - handles POST requests at `/chat`
   - returns the AI reply as JSON

3. Frontend in `frontend/`
   - React app runs with Vite
   - sends user input to the backend
   - displays the assistant response in the browser

## Project Structure

```text
Zentra/
├── app/
│   ├── chatbot.py         # LangGraph-based chat workflow and LLM integration
│   └── myapi.py           # FastAPI app and /chat endpoint
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── initial_flow.md
├── README.md
├── package-lock.json
├── st_UI.py
├── .gitignore
└── LICENSE (if present)
```

## How It Works

1. A user types a message in the React frontend.
2. The frontend sends a POST request to `http://127.0.0.1:8000/chat`.
3. The backend validates the payload:
   - `message`
   - `thread_id`
4. The backend calls `get_chat_response(message, thread_id)`.
5. The LangGraph workflow sends the message to the Groq-backed model.
6. The generated response is returned to the frontend.
7. The conversation memory is preserved separately for each thread.

## Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

The backend uses `python-dotenv` to load environment variables, so the Groq API key must be available when the app starts.

## Running the Application

### 1. Start the backend

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic langgraph langchain-groq python-dotenv
```

Start the API:

```bash
uvicorn app.myapi:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the frontend

Open a new terminal and navigate to the frontend folder:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

## API Endpoint

### POST /chat

Request body:

```json
{
  "message": "Hello! Can you help me?",
  "thread_id": "user1"
}
```

Example response:

```json
{
  "reply": "Hello! Yes, I can help you."
}
```

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Summarize how this app works.",
    "thread_id": "user1"
  }'
```

## Notes

- Memory is currently in-memory only (`InMemorySaver`) and is not persistent across restarts.
- The frontend is configured to call the backend at `http://127.0.0.1:8000/chat`.
- CORS is currently scoped for local development on `http://localhost:5173`.
- The project is intentionally lightweight and extensible.

## Future Improvements

- Add persistent storage for conversations
- Add user authentication and profiles
- Add file uploads and document-based Q&A
- Add tool calling and external API integrations
- Improve deployment configuration for production
- Add logging, monitoring, and error handling

## License

This project does not currently include a dedicated license file in the repository. Please verify repository policy before using it in production or redistributing it externally.

## Summary

Zentra is a compact conversational AI starter project combining a Python backend, a React frontend, and a LangGraph-powered LLM workflow. It is suitable for learning, prototyping, and extending into a more advanced AI assistant application.


#Zentra
A central hub for conversations.
