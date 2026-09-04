# References and Supporting Files

## References

- **Flask Documentation** – https://flask.palletsprojects.com/
- **Flask‑CORS** – https://flask-cors.readthedocs.io/
- **OpenAI API Reference** – https://platform.openai.com/docs/api-reference
- **Docker Documentation** – https://docs.docker.com/
- **Docker‑Compose Documentation** – https://docs.docker.com/compose/
- **MongoDB Python Driver (PyMongo)** – https://pymongo.readthedocs.io/
- **mongomock** – https://github.com/mongomock/mongomock
- **AsyncIO** – https://docs.python.org/3/library/asyncio.html
- **Vite (if needed for frontend)** – https://vitejs.dev/

## Supporting Files

| File | Description |
|------|-------------|
| `app.py` | Entry point for the Flask application, sets up CORS and registers blueprints. |
| `config.py` | Central configuration handling environment variables. |
| `db.py` | MongoDB connection manager with fallback to `mongomock`. |
| `openai_client.py` | Wrapper around OpenAI API calls with mock fallback. |
| `routes/chat.py` | Blueprint defining `/api/chat` endpoint. |
| `routes/chat_batch.py` | Blueprint for batch chat processing (`/api/chat-batch`). |
| `templates/index.html` | Modern, dark‑theme UI for interacting with the API. |
| `Dockerfile` | Container definition for the Flask app. |
| `docker-compose.yml` | Docker‑Compose setup for the app and a MongoDB service. |
| `requirements.txt` | Python dependencies. |
| `README.md` | Project overview, setup, and usage instructions. |
| `.env.example` *(removed)* | Example environment file (no longer needed). |
| `test_api.py` *(removed)* | Temporary test script (removed). |

Feel free to add any additional resources or files as the project evolves.
