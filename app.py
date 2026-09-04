"""
app.py – Application entry point.

Responsibilities:
  - Create the Flask app
  - Register route blueprints
  - Seed the database on startup
  - Serve the demo UI at /
"""

from flask import Flask, render_template
from flask_cors import CORS
from config import DEBUG, PORT
from db import init_db
from routes.chat import chat_bp
from routes.chat_batch import chat_batch_bp

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (e.g. from VS Code Live Server)

# ── Register blueprints ───────────────────────────────────────────────────────
app.register_blueprint(chat_bp)
app.register_blueprint(chat_batch_bp)


# ── Demo UI ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Startup ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=DEBUG, port=PORT)
