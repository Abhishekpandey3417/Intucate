import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "intucate_db"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Flask
DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
