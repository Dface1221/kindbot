from typing import Any, Dict
from app.models.expertise import Expertise


def evaluate_skill(expertise: Expertise, demonstration: str) -> Dict[str, Any]:
    """
    Evaluate extracted expertise against the source demonstration using heuristic structural checks.

    NOTE: This is a structural heuristic for consistency and completeness;
    it does NOT independently verify factual accuracy, operational safety, or real-world validity.
    """
    text = demonstration.lower()

    checks = []

    # 1. Procedure
    checks.append({
        "name": "Procedure extracted",
        "passed": len(expertise.steps) >= 2,
        "detail": f"{len(expertise.steps)} procedural steps extracted",
    })

    # 2. Tools
    if expertise.tools:
        tool_found = any(tool.lower() in text for tool in expertise.tools)
    else:
        tool_found = True

    checks.append({
        "name": "Tools preserved",
        "passed": tool_found,
        "detail": f"{len(expertise.tools)} tool(s) identified",
    })

    # 3. Safety
    safety_present = bool(expertise.warnings)
    checks.append({
        "name": "Safety information preserved",
        "passed": safety_present,
        "detail": f"{len(expertise.warnings)} warning(s) extracted",
    })

    # 4. Decision rules
    decision_present = bool(expertise.decision_rules)
    checks.append({
        "name": "Decision rules preserved",
        "passed": decision_present,
        "detail": f"{len(expertise.decision_rules)} decision rule(s)",
    })

    # 5. Failure conditions
    failure_present = bool(expertise.failure_conditions)
    checks.append({
        "name": "Failure conditions identified",
        "passed": failure_present,
        "detail": f"{len(expertise.failure_conditions)} failure condition(s)",
    })

    passed = sum(1 for c in checks if c["passed"])
    fidelity = passed / len(checks)

    critical_gaps = [
        c["name"] for c in checks if not c["passed"]
    ]

    return {
        "fidelity_score": round(fidelity, 2),
        "fidelity_percent": round(fidelity * 100),
        "status": "PASS" if fidelity >= 0.8 and not critical_gaps else "REVIEW",
        "evaluation_type": "heuristic",
        "disclaimer": (
            "This fidelity score is an automated structural heuristic and does not "
            "independently verify factual accuracy or operational safety. Expert review is recommended."
        ),
        "checks": checks,
        "critical_gaps": critical_gaps,
    }
