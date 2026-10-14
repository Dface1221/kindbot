# Apprentice

> **Show it once. It writes the skill.**

**Apprentice is a compiler for human expertise.**

People often know how to perform complex tasks without having that knowledge written down in a structured, reusable form. Apprentice lets an expert demonstrate a procedure through video, image, or text, uses **Gemma 4** to extract the underlying expertise, and compiles that knowledge into a reusable `SKILL.md`.

The generated skill can then be validated, tested through teach-back scenarios, scored for fidelity, reviewed by a human, and published to the **Skill Commons**.

---

## The Problem

A large amount of valuable knowledge exists only in people's heads.

An expert may be able to demonstrate:

- How to perform a particular procedure
- How to use a tool
- How to follow a specialized workflow
- How to avoid common mistakes
- What small details matter in practice

But this knowledge is often trapped in:

- Demonstration videos
- Informal training
- Conversations
- Personal experience
- Unstructured documentation

Simply summarizing a demonstration isn't enough.

The real challenge is:

> **How can we turn a human demonstration into a structured, reusable capability for an AI agent?**

---

## Our Solution

Apprentice treats human expertise like source code.

```text
Human Demonstration
        │
        ▼
   Video / Image / Text
        │
        ▼
      Gemma 4
        │
        ▼
Structured Expertise
        │
        ▼
 Deterministic Compiler
        │
        ▼
      SKILL.md
        │
        ▼
     Validation
        │
        ▼
     Teach-Back
        │
        ▼
   Fidelity Score
        │
        ▼
  Human Approval
        │
        ▼
   Skill Commons
```

### The key idea

**Gemma understands.  
Apprentice compiles.  
The validator checks.  
Teach-back tests.  
A human approves.**

---

## How It Works

### 1. Demonstrate

The user provides a demonstration through video, image, or text.

For video demonstrations, Apprentice extracts representative frames and sends the visual information to Gemma.

### 2. Extract Expertise

Gemma converts the demonstration into structured expertise:

```json
{
  "title": "Tying a Necktie",
  "purpose": "To create a secure knot in a necktie",
  "when_to_use": "Formal or semi-formal attire",
  "tools_needed": [
    "Necktie",
    "Collared shirt"
  ],
  "steps": [
    {
      "step": 1,
      "instruction": "Drape the tie around the neck...",
      "reason": "To establish the correct starting position."
    }
  ],
  "warnings": [],
  "common_mistakes": [],
  "expert_tips": []
}
```

### 3. Compile

The structured expertise is converted into a standard `SKILL.md` artifact.

Example:

```markdown
---
name: tying-a-necktie
description: To create a secure knot in a necktie
---

# Tying a Necktie

## Purpose

To create a secure knot in a necktie.

## When to Use

When dressing in formal or semi-formal attire.

## Tools Needed

- Necktie
- Collared shirt

## Procedure

1. Drape the tie around the neck...
2. Cross the wide end...
3. Wrap the wide end...
```

The compiler is deterministic: the LLM does not control the final file structure.

### 4. Validate

The generated skill can be checked for required structure and expected content.

### 5. Teach-Back

Apprentice generates five scenarios designed to test whether the skill contains enough information to answer practical questions.

The answering model receives:

```text
SKILL.md
+
Scenario
+
Answer
```

It does **not** receive the original demonstration.

This is important because otherwise the model could rely on the original knowledge even if the generated skill was incomplete.

### 6. Fidelity Score

The teach-back results are converted into a simple fidelity score.

```text
5 / 5  → 100%
4 / 5  → 80%
3 / 5  → 60%
2 / 5  → 40%
1 / 5  → 20%
0 / 5  → 0%
```

The score is a signal of how faithfully the generated skill preserves the demonstrated knowledge.

### 7. Human Approval

AI-generated expertise is not automatically treated as authoritative.

A human reviews the generated skill and approves it before publication.

### 8. Skill Commons

Approved skills can be stored and downloaded as reusable artifacts.

---

# Why This Is Different

Apprentice is **not just a video summarizer**.

A summarizer might produce:

> "A person demonstrates how to tie a necktie."

Apprentice produces:

```text
Purpose
When to use
Tools
Ordered procedure
Reasons
Warnings
Common mistakes
Expert tips
```

And then turns that knowledge into a reusable `SKILL.md`.

The goal is not merely to describe what happened.

The goal is to **capture a capability**.

---

# Why Gemma 4?

Gemma 4 provides the semantic intelligence needed to interpret human demonstrations.

We use Gemma for tasks such as:

- Understanding demonstrated procedures
- Extracting structured expertise
- Generating teach-back scenarios
- Answering scenarios using the generated skill

We intentionally keep other parts of the system deterministic.

This separation makes the architecture easier to inspect and reason about:

```text
             Gemma 4
                │
       Semantic understanding
                │
                ▼
      Structured Expertise
                │
       Deterministic code
                │
        ┌───────┴────────┐
        ▼                ▼
   SKILL.md          Validation
                           │
                           ▼
                       Teach-back
                           │
                           ▼
                     Fidelity Score
```

---

# Current Video Pipeline

For video demonstrations, Apprentice currently uses OpenCV to:

1. Load the uploaded video
2. Sample representative frames
3. Resize frames when necessary
4. Encode them as JPEG images
5. Send those visual frames to Gemma 4
6. Extract structured expertise

This means the current video pipeline genuinely analyzes the **visual content of the uploaded video**.

### Current limitation

The current Gemma 4 video path does not process the video's audio track.

If spoken instructions are essential to a demonstration, a future version can add a dedicated speech-to-text stage before combining the transcript with the visual analysis.

We do not treat audio understanding as implemented functionality in the current version.

---

# Tech Stack

## AI

- **Gemma 4 31B**
- Google Gemini API / `google-genai`

## Backend

- Python
- FastAPI
- Pydantic
- OpenCV

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

## Output

- Markdown
- `SKILL.md`

---

# Project Structure

```text
apprentice/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── services/
│   │   │   ├── gemma_provider.py
│   │   │   ├── expertise_extractor.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/
│   │   │   └── models.py
│   │   │
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── skills/
    └── <generated-skills>/
```

---

# Getting Started

## Prerequisites

- Python 3.10+
- Node.js
- npm
- A Google Gemini API key with access to Gemma 4

---

## Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create/activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Start the backend:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Build for production:

```bash
npm run build
```

---

# API

Main endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Backend health |
| `GET /api/gemma/status` | Check Gemma connection |
| `POST /api/upload` | Upload demonstration |
| `POST /api/extract` | Extract structured expertise |
| `POST /api/compile` | Generate `SKILL.md` |
| `POST /api/validate` | Validate generated skill |
| `POST /api/teachback/questions` | Generate teach-back scenarios |
| `POST /api/teachback/answer` | Answer a scenario using the skill |
| `POST /api/teachback/evaluate` | Evaluate an answer |
| `POST /api/teachback/run` | Run the full teach-back |
| `POST /api/skills/approve` | Approve/publish a skill |
| `GET /api/skills` | List published skills |
| `GET /api/skills/{skill_id}` | View a skill |
| `GET /api/skills/{skill_id}/download` | Download a skill |

---

# Example

Suppose an expert demonstrates how to tie a necktie.

### Input

```text
How to tie a necktie demonstration video
```

### Gemma extraction

```text
Title:
Tying a Necktie

Tools:
- Necktie
- Collared shirt

Steps:
1. Position the tie
2. Cross the wide end
3. Wrap the wide end
4. Bring it through the neck loop
5. Pull through the front loop
6. Tighten
```

### Compiler output

```text
skills/
└── tying-a-necktie/
    └── SKILL.md
```

### Result

The demonstration has been converted from informal human knowledge into a structured, reusable skill artifact.

---

# Design Principles

### 1. Human expertise first

The system starts with something a person already knows how to do.

### 2. AI for understanding

Gemma handles semantic interpretation rather than controlling the entire application.

### 3. Deterministic compilation

The final skill structure is generated through predictable application logic.

### 4. Verification over blind trust

Generated skills are validated and tested rather than automatically trusted.

### 5. Human-in-the-loop

The expert remains the final authority.

### 6. Open artifacts

The result is an inspectable Markdown file rather than knowledge locked inside the application.

---

# Limitations

The current prototype has several limitations:

- Video analysis currently focuses on sampled visual frames.
- Audio from videos is not currently analyzed by the Gemma 4 video path.
- Demonstrations need to contain sufficiently observable procedural information.
- Implicit knowledge that is not visible or explained may be missed.
- Fidelity scoring is a prototype signal rather than a formal guarantee of correctness.
- Human review remains important for high-stakes expertise.

Apprentice is currently intended as a prototype for capturing and packaging procedural knowledge, not as an autonomous authority.

---

# Future Work

Potential extensions include:

- Audio transcription + visual fusion
- Temporal reasoning across longer demonstrations
- Skill versioning
- Expert corrections and feedback loops
- Skill dependencies
- Skill composition
- Richer fidelity evaluation
- Collaborative Skill Commons
- Agent runtime integration
- Offline/local inference
- Skill provenance and version history

---

# Demo Flow

For a hackathon demonstration:

```text
1. Upload a demonstration
        ↓
2. Gemma analyzes it
        ↓
3. Structured expertise appears
        ↓
4. Compile into SKILL.md
        ↓
5. Show the generated skill
        ↓
6. Run/preview teach-back
        ↓
7. Show fidelity score
        ↓
8. Human approves
        ↓
9. Skill appears in Skill Commons
```

### The one-line story

> **Show it once. It writes the skill.**

---

# Team Jupyter

Built for **HackFest@MLH**.

Apprentice explores a simple idea:

> **What if teaching an AI agent could be as natural as teaching another person?**

Instead of manually writing every instruction, an expert demonstrates what they know — and Apprentice turns that demonstration into a reusable skill.



