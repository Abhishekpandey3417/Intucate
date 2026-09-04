"""
routes/chat.py – POST /api/chat

Assessment Steps 1-5:
  1. Accept { "userInput": "..." }
  2. Fetch Education_Prompt template from MongoDB
  3. Call ChatGPT API with rendered prompt
  4. Store request/response pair in history collection
  5. Return { "response": "..." }
"""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from db import get_prompts_collection, get_history_collection
from openai_client import call_openai_sync

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    # ── Step 1: Validate request body ────────────────────────────────────────
    data = request.get_json(silent=True)
    if not data or "userInput" not in data:
        return jsonify({"error": "Request body must contain 'userInput' field."}), 400

    user_input: str = data["userInput"].strip()
    if not user_input:
        return jsonify({"error": "'userInput' must not be empty."}), 400

    # ── Step 2: Fetch prompt template from MongoDB ────────────────────────────
    prompt_doc = get_prompts_collection().find_one({"_id": "Education_Prompt"})
    if not prompt_doc:
        return jsonify({"error": "Prompt template not found in database."}), 500

    template: str = prompt_doc.get("template", "")
    final_prompt: str = template.replace("{{userInput}}", user_input)

    # ── Step 3: Call ChatGPT API ──────────────────────────────────────────────
    ai_response: str = call_openai_sync(final_prompt)

    # ── Step 4: Store request/response pair in history ────────────────────────
    get_history_collection().insert_one({
        "original_input": user_input,
        "rendered_prompt": final_prompt,
        "response": ai_response,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    # ── Step 5: Return response ───────────────────────────────────────────────
    return jsonify({"response": ai_response}), 200
