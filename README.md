# Expert to Skill

> **Transform practical knowledge, instructions, and documented procedures into structured, reusable `SKILL.md` files using Google's hosted Gemma 4 model.**

**Expert to Skill** is an AI-powered compiler for practical knowledge. Complex operational workflows, troubleshooting checklists, and expert instructions are often trapped in informal notes, chat messages, or documentation. Expert to Skill extracts the underlying procedural expertise, validates it against strict schemas, and deterministically compiles it into reusable, standardized `SKILL.md` agent skill files.

---

## Key Features

- **Hosted Gemma 4 Integration:** Powered by Google's hosted `gemma-4-26b-a4b-it` model via the official `google-genai` Python SDK.
- **Strict Schema Validation:** Extracted procedural steps, decision rules, tools, preconditions, and safety warnings are validated with Pydantic before compilation.
- **Deterministic Compilation:** Consistent, clean Markdown output (`SKILL.md`) with standardized sections ready for AI agent execution.
- **Structural Heuristic Evaluation:** Automated heuristic verification scoring extracted procedures against source material to flag critical gaps.
- **Interactive Web Interface:** Built-in web UI at `/demo` featuring one-click sample loading, real-time generation, clipboard copying, and direct file download.
- **Clean REST API:** FastAPI backend with endpoints for generation, compilation, and health checks.

---

## Architecture Pipeline

```text
Documented Procedure / Knowledge
              │
              ▼
    Google Hosted Gemma 4
     (gemma-4-26b-a4b-it)
              │
              ▼
   Structured JSON Expertise
              │
              ▼
    Pydantic Schema Validation
              │
              ▼
    Deterministic Compiler
              │
              ▼
           SKILL.md
              │
              ▼
 Heuristic Structural Verification
              │
              ▼
  Copy / Download / Integrate
```

---

## Tech Stack

- **Model:** Google Gemma 4 (`gemma-4-26b-a4b-it`) hosted via Google Gemini API
- **SDK:** `google-genai` (official Google Gen AI Python SDK)
- **Backend:** Python, FastAPI, Uvicorn, Pydantic v2
- **Testing:** Pytest
- **Frontend / UI:** Responsive single-page web interface served via FastAPI

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API key (obtainable at [Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/gagandeepun24-crypto/apprentice-ai.git
cd apprentice-ai
```

### 2. Configure Environment Variables

Copy the example environment file and add your `GEMINI_API_KEY`:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
GEMINI_API_KEY=your_google_ai_studio_api_key_here
GEMMA_MODEL=gemma-4-26b-a4b-it
HOST=127.0.0.1
PORT=8000
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Run the Application

Start the backend server:

```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```

Access the application:

- **Interactive Web UI:** [http://127.0.0.1:8000/demo](http://127.0.0.1:8000/demo)
- **API Documentation (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service metadata, configuration status, and route catalog |
| `GET` | `/health` | Health check returning status and model readiness |
| `GET` | `/demo` | Interactive web UI |
| `GET` | `/api/skills/status` | Model status and API configuration state |
| `POST` | `/api/skills/generate` | Extract, validate, compile, and heuristically evaluate a skill |
| `POST` | `/api/skills/compile` | Compile pre-validated `Expertise` JSON into `SKILL.md` |

---

## Running Tests

Execute the test suite using `pytest`:

```bash
PYTHONPATH=backend pytest backend/tests
```

---

## Evaluation Notice

The included validation evaluation is an **automated structural heuristic** designed to verify procedural step extraction, decision rules, tools, and warnings. It does **not** independently verify real-world factual correctness or operational safety. Human expert review is recommended before executing compiled skills in production environments.

---

## Maintainer & Attribution

- **Current Maintainer:** aadil ([@dface1221](https://github.com/dface1221))
- **Original Foundation:** Inherited and migrated from the Apprentice project originally built by **Team Jupyter** (Gagan Deep U N, Dhanya S, Dhanush Gowda, Dhanush K Urs) for HackFest@MLH.
- **License:** [MIT License](LICENSE) — Copyright (c) 2026 Apprentice Contributors.
