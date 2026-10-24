from fastapi import APIRouter
from app.models.expertise import Expertise
from app.services.compiler import compile_skill, slugify

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.post("/compile")
def compile_expertise(expertise: Expertise):
    """Compile structured expertise into a SKILL.md document."""
    skill_markdown = compile_skill(expertise)

    return {
        "skill_id": slugify(expertise.title),
        "status": "compiled",
        "skill_markdown": skill_markdown,
    }
