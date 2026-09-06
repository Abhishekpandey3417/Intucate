# Intucate

## Overview
Intucate is a **Flask‑based AI Education API** that demonstrates the full technical‑assessment workflow:

1. Accept a user question (`POST /api/chat`).
2. Retrieve a prompt template from MongoDB.
3. Render the prompt and call the OpenAI ChatGPT API.
4. Store the request/response pair in a `history` collection.
5. Return the AI response.
6. Support a batch endpoint (`POST /api/chat-batch`) that processes many inputs concurrently with `asyncio.gather`.

The project also ships a **premium‑looking browser UI** (`templates/index.html`) that lets reviewers test the endpoints directly from Chrome.
The Project is deployed at Url-https://intucate-3.onrender.com

## Features
- **Modular architecture** – Blueprint‑based routes, separate `config`, `db`, and `openai_client` modules.
- **MongoDB fallback** – Uses `mongomock` when a real MongoDB server is unavailable (great for local testing).
- **OpenAI fallback** – Returns a mock response when the API key is missing or credits are exhausted.
- **Async batch processing** – Handles many requests concurrently without blocking.
- **CORS enabled** – UI can be served from any origin (e.g., VS Code Live Server).
- **Docker ready** – Simple `Dockerfile` and `docker‑compose.yml` for production deployment.

## Prerequisites
- Python **3.13** (or 3.12+) installed.
- Optionally, **Docker** and **Docker‑Compose** for containerized deployment.
- An **OpenAI API key** (place it in `.env` as `OPENAI_API_KEY`).
- (Optional) A running MongoDB instance; otherwise the app will use the in‑memory `mongomock`.

## Quick Start (local development)
```bash
# Clone the repo (already on your machine)
cd C:/Users/Lenovo/OneDrive/Desktop/Intucate

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate   # on Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Copy environment example and fill in your key
cp .env.example .env
# Edit .env → set OPENAI_API_KEY=your_key   (optional – mock fallback works without it)

# Run the app
python app.py
```
Visit **http://127.0.0.1:5000** in Chrome. Use the UI to send a single question or a batch of questions.

## Testing the API with `curl`
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"userInput":"What is the capital of France?"}'
```
Batch endpoint:
```bash
curl -X POST http://127.0.0.1:5000/api/chat-batch \
     -H "Content-Type: application/json" \
     -d '{"userInputs":["Q1","Q2"]}'
```

## Docker Deployment
A production‑ready Docker image is provided.
```bash
# Build the image
docker build -t intucate .

# Run with Docker Compose (includes a MongoDB service)
docker compose up -d
```
The service will be reachable at **http://localhost:5000**.

## Project Structure
```
Intucate/
├─ app.py                # Flask entry point
├─ config.py             # Environment variables
├─ db.py                 # MongoDB (or mongomock) singleton
├─ openai_client.py      # Sync/async OpenAI helpers with fallback
├─ routes/
│   ├─ __init__.py
│   ├─ chat.py           # /api/chat
│   └─ chat_batch.py     # /api/chat-batch
├─ templates/
│   └─ index.html        # Interactive demo UI
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env.example
└─ README.md             # <- you are reading it!
```

## References & Supporting Files
- **Flask** – https://flask.palletsprojects.com/
- **MongoDB** – https://www.mongodb.com/
- **Mongomock** – https://github.com/mongomock/mongomock
- **OpenAI Python SDK** – https://github.com/openai/openai-python
- **Flask‑CORS** – https://flask-cors.readthedocs.io/
- **Docker** – https://www.docker.com/

---
*This repository is ready for the technical assessment and can be easily deployed to any environment.*
