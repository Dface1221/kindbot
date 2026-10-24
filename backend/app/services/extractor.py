from pathlib import Path
from pydantic import ValidationError

from app.models.expertise import Expertise
from app.services.gemma import generate_json


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent / "prompts" / "extraction.txt"
)


def extract_expertise(demonstration: str) -> Expertise:
    """
    Extract structured procedural expertise from a human demonstration or instruction
    using Google's hosted Gemma 4 model and validate against the Expertise schema.
    """
    if not demonstration or not demonstration.strip():
        raise ValueError("Demonstration text cannot be empty.")

    template = PROMPT_PATH.read_text(encoding="utf-8")

    prompt = template.replace(
        "{demonstration}",
        demonstration.strip(),
    )

    result = generate_json(prompt)

    try:
        return Expertise.model_validate(result)
    except ValidationError as exc:
        raise RuntimeError(
            f"Extraction output failed schema validation: {exc}"
        ) from exc
