"""
routes/chat_batch.py – POST /api/chat-batch

Assessment Step 6:
  - Accept { "userInputs": ["...", "...", ...] }
  - Fetch Education_Prompt template from MongoDB
  - Process each string INDEPENDENTLY and ASYNCHRONOUSLY with ChatGPT
  - Store all request/response pairs in history collection
  - Return { "responses": ["...", "...", ...] } in the SAME ORDER
"""

import asyncio
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from db import get_prompts_collection, get_history_collection
from openai_client import call_openai_async

chat_batch_bp = Blueprint("chat_batch", __name__)


async def _process_single(user_input: str, template: str) -> dict:
    """
    Render the prompt for one input string and call the OpenAI API.
    Returns a dict ready to be inserted into the history collection.
    """
    final_prompt = template.replace("{{userInput}}", user_input)
    ai_response = await call_openai_async(final_prompt)
    return {
        "original_input": user_input,
        "rendered_prompt": final_prompt,
        "response": ai_response,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@chat_batch_bp.route("/api/chat-batch", methods=["POST"])
async def chat_batch():
    # ── Validate request body ─────────────────────────────────────────────────
    data = request.get_json(silent=True)
    if not data or "userInputs" not in data:
        return jsonify({"error": "Request body must contain 'userInputs' list."}), 400

    user_inputs = data["userInputs"]
    if not isinstance(user_inputs, list) or len(user_inputs) == 0:
        return jsonify({"error": "'userInputs' must be a non-empty list of strings."}), 400

    # ── Fetch prompt template from MongoDB ────────────────────────────────────
    prompt_doc = get_prompts_collection().find_one({"_id": "Education_Prompt"})
    if not prompt_doc:
        return jsonify({"error": "Prompt template not found in database."}), 500

    template: str = prompt_doc.get("template", "")

    # ── Process all inputs CONCURRENTLY (non-blocking) ────────────────────────
    # asyncio.gather preserves the ORDER of results matching the input list
    tasks = [_process_single(inp, template) for inp in user_inputs]
    results = await asyncio.gather(*tasks)

    # ── Store all request/response pairs in history ───────────────────────────
    get_history_collection().insert_many(list(results))

    # ── Return responses in the same order as the inputs ─────────────────────
    return jsonify({"responses": [r["response"] for r in results]}), 200
