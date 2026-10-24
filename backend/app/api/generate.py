from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.compiler import compile_skill, slugify
from app.services.evaluator import evaluate_skill
from app.services.extractor import extract_expertise
from app.services.gemma import is_api_configured

router = APIRouter(prefix="/api/skills", tags=["skills"])


class GenerateRequest(BaseModel):
    demonstration: str


@router.post("/generate")
def generate_skill(request: GenerateRequest):
    """
    Extract expertise from source instructions using hosted Gemma 4,
    validate, compile to SKILL.md, and run heuristic fidelity checks.
    """
    if not request.demonstration.strip():
        raise HTTPException(status_code=400, detail="Demonstration text cannot be empty.")

    if not is_api_configured():
        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured on the server. "
                "Please configure GEMINI_API_KEY in the server environment to generate skills with hosted Gemma 4."
            ),
        )

    try:
        expertise = extract_expertise(request.demonstration)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    skill_markdown = compile_skill(expertise)

    confidences = [step.confidence for step in expertise.steps]
    overall_confidence = (sum(confidences) / len(confidences)) if confidences else 0.0
    needs_review = overall_confidence < 0.8

    evaluation = evaluate_skill(expertise, request.demonstration)

    return {
        "status": "generated",
        "skill_id": slugify(expertise.title),
        "expertise": expertise.model_dump(),
        "skill_markdown": skill_markdown,
        "confidence": round(overall_confidence, 2),
        "needs_review": needs_review,
        "evaluation": evaluation,
    }
