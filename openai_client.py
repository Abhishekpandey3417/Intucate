"""
openai_client.py – OpenAI client helpers (sync + async).

Provides:
  - call_openai_sync(prompt)  → str
  - call_openai_async(prompt) → str  (awaitable coroutine)

Both return a mock string when the OpenAI API is unavailable
(no key, no credits, network error, etc.) so the rest of the
app can keep running without crashing.
"""

from openai import OpenAI, AsyncOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

# Shared client instances (reused across all requests)
_sync_client = OpenAI(api_key=OPENAI_API_KEY)
_async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def call_openai_sync(prompt: str) -> str:
    """
    Send a single prompt to the ChatGPT API and return the response text.
    Falls back to a mock string on any exception.
    """
    try:
        completion = _sync_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as exc:
        print(f"[openai] Sync call failed: {exc}. Returning mock response.")
        return f"[Mock] AI response for: {prompt[:80]}..."


async def call_openai_async(prompt: str) -> str:
    """
    Async version of call_openai_sync – used for concurrent batch processing.
    Falls back to a mock string on any exception.
    """
    try:
        completion = await _async_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as exc:
        print(f"[openai] Async call failed: {exc}. Returning mock response.")
        return f"[Mock] AI response for: {prompt[:80]}..."
