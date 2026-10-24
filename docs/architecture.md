# Expert to Skill Architecture

## Overview

Expert to Skill converts unstructured procedural knowledge and human instructions into validated, reusable `SKILL.md` documents using Google's hosted Gemma 4 model.

## Pipeline Components

1. **Extraction (`app.services.extractor`):**
   - Receives human instructions or procedure descriptions.
   - Formats instructions with `app/prompts/extraction.txt`.
   - Sends payload to Google's hosted `gemma-4-26b-a4b-it` model via `app.services.gemma` and `google-genai`.
   - Receives structured JSON adhering to the target schema.

2. **Validation (`app.models.expertise`):**
   - Validates JSON into the `Expertise` Pydantic model.
   - Enforces types, step order, confidence scores, preconditions, tools, warnings, decision rules, and failure conditions.

3. **Compilation (`app.services.compiler`):**
   - Deterministically generates standard Markdown `SKILL.md` from the validated `Expertise` object.
   - Produces clear, readable sections: Purpose, When to Use, Tools, Preconditions, Procedure, Decision Rules, Safety Warnings, Common Mistakes, Failure Conditions, and Source.

4. **Heuristic Evaluation (`app.services.evaluator`):**
   - Runs structural consistency checks (procedure length, tools identified, warnings extracted, decision rules captured, failure conditions detected).
   - Generates a structural fidelity percentage and pass/review recommendation.
   - Displays clear disclaimers that this is a structural heuristic rather than a guarantee of operational correctness.
