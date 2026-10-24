# Expert to Skill - Backend

FastAPI backend service powering **Expert to Skill**, integrating Google's hosted Gemma 4 model via `google-genai` to extract structured expertise and compile reusable `SKILL.md` files.

## Quick Start

```bash
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
