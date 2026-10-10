"""Thin LLM wrapper. Everything else in the project calls ask_llm() and nothing else,
so swapping providers (or models) later means editing only this file."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Override with GEMINI_MODEL in .env if the default isn't available to your keys.
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Comma-separated list in .env: GEMINI_API_KEYS=key1,key2
KEYS = [k.strip() for k in os.getenv("GEMINI_API_KEYS", "").split(",") if k.strip()]


def ask_llm(prompt: str, system: str | None = None) -> str:
    """Send a prompt, return the reply text. Falls through to the next key on failure
    (expired key, quota hit, etc.)."""
    if not KEYS:
        raise RuntimeError("No keys found. Set GEMINI_API_KEYS in your .env file.")

    config = types.GenerateContentConfig(system_instruction=system) if system else None
    last_error = None

    for key in KEYS:
        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            return response.text
        except Exception as e:  # try the next key
            last_error = e

    raise RuntimeError(f"All keys failed. Last error: {last_error}")
