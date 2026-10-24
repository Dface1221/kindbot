import re

from app.models.expertise import Expertise


def slugify(text: str) -> str:
    """Generate a URL- and filesystem-safe slug from text."""
    if not text:
        return "unnamed-skill"
    text = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return slug or "unnamed-skill"


def compile_skill(expertise: Expertise) -> str:
    """
    Compile a validated Expertise model into a structured, readable SKILL.md document.
    """
    lines = []

    lines.append(f"# {expertise.title or 'Untitled Skill'}")
    lines.append("")

    lines.append("## Purpose")
    lines.append(expertise.purpose or "No purpose specified.")
    lines.append("")

    lines.append("## When to Use")
    lines.append(expertise.when_to_use or "Not specified.")
    lines.append("")

    if expertise.tools:
        lines.append("## Tools")
        for tool in expertise.tools:
            lines.append(f"- {tool}")
        lines.append("")

    if expertise.preconditions:
        lines.append("## Preconditions")
        for item in expertise.preconditions:
            lines.append(f"- {item}")
        lines.append("")

    if expertise.steps:
        lines.append("## Procedure")
        for step in expertise.steps:
            lines.append(f"{step.number}. {step.instruction}")
            if step.rationale:
                lines.append(f"   - Why: {step.rationale}")
        lines.append("")

    if expertise.decision_rules:
        lines.append("## Decision Rules")
        for rule in expertise.decision_rules:
            lines.append(f"- {rule}")
        lines.append("")

    if expertise.warnings:
        lines.append("## Safety Warnings")
        for warning in expertise.warnings:
            lines.append(f"- ⚠️ {warning}")
        lines.append("")

    if expertise.common_mistakes:
        lines.append("## Common Mistakes")
        for mistake in expertise.common_mistakes:
            lines.append(f"- {mistake}")
        lines.append("")

    if expertise.failure_conditions:
        lines.append("## Failure Conditions")
        for failure in expertise.failure_conditions:
            lines.append(f"- {failure}")
        lines.append("")

    lines.append("## Source")
    lines.append(f"Language: {expertise.source_language or 'unknown'}")
    lines.append("")

    return "\n".join(lines)
