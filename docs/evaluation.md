# Skill Evaluation Methodology

## Heuristic Fidelity Scoring

Expert to Skill evaluates generated skills using an automated structural heuristic check.

### Checks Performed

1. **Procedure Extracted:** Confirms at least 2 sequential steps have been extracted.
2. **Tools Preserved:** Verifies that tools mentioned in the source material are captured in the tools list.
3. **Safety Warnings Preserved:** Checks that critical safety notices or cautions are identified.
4. **Decision Rules Preserved:** Verifies that conditional branch logic ("if X, then Y") is extracted.
5. **Failure Conditions Identified:** Confirms that error states or criteria indicating procedure failure are captured.

### Scope & Disclaimer

This evaluation is an automated structural heuristic. It does not replace subject matter expert review, nor does it guarantee factual validity, execution safety, or operational accuracy.
