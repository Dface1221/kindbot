import json
import os
import re
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# Load environment variables from .env if present (root or backend)
_repo_root = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(_repo_root / ".env")
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

DEFAULT_MODEL = "gemma-4-26b-a4b-it"


def get_model_name() -> str:
    """Return the configured Gemma 4 model identifier."""
    return os.environ.get("GEMMA_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_api_key() -> str:
    """Retrieve the Gemini API key from the environment."""
    return os.environ.get("GEMINI_API_KEY", "").strip()


def is_api_configured() -> bool:
    """Check if a non-empty Gemini API key is configured."""
    return bool(get_api_key())


def _clean_json_text(raw_text: str) -> str:
    """Extract clean JSON text from raw model output, handling markdown blocks."""
    text = raw_text.strip()
    # Remove markdown code fences if present
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fence_match:
        text = fence_match.group(1).strip()
    return text


def generate_json(prompt: str) -> Dict[str, Any]:
    """
    Generate structured JSON using Google's hosted Gemma 4 model via google-genai.
    Preserves the standard generate_json interface.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured on the server. "
            "Please configure GEMINI_API_KEY in your server environment or .env file "
            "to use the hosted Gemma 4 model."
        )

    model_name = get_model_name()

    try:
        from google import genai
        from google.genai import types
        from google.genai.errors import APIError
    except ImportError as exc:
        raise RuntimeError(
            "The 'google-genai' SDK is not installed. Please install dependencies from backend/requirements.txt."
        ) from exc

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
    except APIError as exc:
        raise RuntimeError(
            f"Hosted Gemma 4 API error (HTTP {exc.code}): {exc.message}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            f"Failed to communicate with hosted Gemma 4 API ({model_name}): {str(exc)}"
        ) from exc

    if not response or not response.text or not response.text.strip():
        raise RuntimeError(
            f"Hosted Gemma 4 model '{model_name}' returned an empty response."
        )

    cleaned_text = _clean_json_text(response.text)

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Hosted Gemma 4 returned malformed JSON: {cleaned_text[:500]}"
        ) from exc

    if isinstance(data, list):
        # Handle cases where model wraps root object in a list: [{ "title": ... }]
        dict_items = [item for item in data if isinstance(item, dict)]
        if dict_items:
            matching = [d for d in dict_items if "title" in d or "steps" in d or "purpose" in d]
            data = matching[0] if matching else dict_items[0]
        else:
            raise RuntimeError("Hosted Gemma 4 returned a JSON list containing no objects.")

    if not isinstance(data, dict):
        raise RuntimeError(
            f"Hosted Gemma 4 returned JSON of type '{type(data).__name__}' instead of a JSON object."
        )

    return data
