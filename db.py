"""
db.py – MongoDB connection singleton.

Uses a real MongoClient when MongoDB is reachable,
falls back to mongomock (in-memory) for local development / testing
when no MongoDB server is available.
"""

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME


def _create_client():
    """
    Try to connect to the real MongoDB server.
    If the server is unreachable, fall back to mongomock.
    """
    try:
        real_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        # Force a connection check
        real_client.admin.command("ping")
        print(f"[db] Connected to MongoDB at {MONGO_URI}")
        return real_client
    except Exception as exc:
        print(f"[db] MongoDB unavailable ({exc}). Using in-memory mongomock.")
        import mongomock
        return mongomock.MongoClient()


# Module-level singleton – created once at import time
_client = _create_client()
_db = _client[DB_NAME]


def get_prompts_collection():
    """Return the 'prompts' collection."""
    return _db["prompts"]


def get_history_collection():
    """Return the 'history' collection."""
    return _db["history"]


def init_db():
    """
    Seed the database with the Education_Prompt document
    if it does not already exist.
    """
    prompts = get_prompts_collection()
    if not prompts.find_one({"_id": "Education_Prompt"}):
        prompts.insert_one({
            "_id": "Education_Prompt",
            "template": (
                "You are an expert in education domain. "
                "Answer the following: {{userInput}}"
            )
        })
        print("[db] Education_Prompt inserted.")
    else:
        print("[db] Education_Prompt already exists.")
