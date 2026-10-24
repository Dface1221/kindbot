import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models.expertise import Expertise
from app.services.compiler import compile_skill, slugify
from app.services.extractor import extract_expertise
from app.services.evaluator import evaluate_skill
from app.services.gemma import get_model_name, is_api_configured


app = FastAPI(
    title="Expert to Skill API",
    description="An AI-powered tool that transforms practical knowledge, instructions, and documented procedures into structured, reusable SKILL.md files using Google's hosted Gemma 4 model.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    demonstration: str


@app.get("/")
def root():
    return {
        "name": "Expert to Skill",
        "description": "An AI-powered tool that transforms practical knowledge and instructions into structured, reusable SKILL.md files using Google's hosted Gemma 4 model.",
        "version": "0.2.0",
        "model": get_model_name(),
        "api_configured": is_api_configured(),
        "endpoints": {
            "web_ui": "/demo",
            "health": "/health",
            "api_docs": "/docs",
            "generate": "/api/skills/generate",
            "compile": "/api/skills/compile",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "expert-to-skill-backend",
        "version": "0.2.0",
        "model": get_model_name(),
        "api_configured": is_api_configured(),
    }


@app.get("/api/skills/status")
def status():
    return {
        "service": "expert-to-skill",
        "model": get_model_name(),
        "api_configured": is_api_configured(),
    }


@app.post("/api/skills/compile")
def compile_expertise(expertise: Expertise):
    skill_markdown = compile_skill(expertise)

    return {
        "skill_id": slugify(expertise.title),
        "status": "compiled",
        "skill_markdown": skill_markdown,
    }


@app.post("/api/skills/generate")
def generate_skill(request: GenerateRequest):
    if not request.demonstration or not request.demonstration.strip():
        raise HTTPException(
            status_code=400,
            detail="Demonstration text cannot be empty.",
        )

    if not is_api_configured():
        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured on the server. "
                "Please configure GEMINI_API_KEY in the server environment or .env file "
                "to generate skills using the hosted Gemma 4 model."
            ),
        )

    try:
        expertise = extract_expertise(request.demonstration)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Hosted Gemma 4 generation error: {str(exc)}",
        ) from exc

    skill_markdown = compile_skill(expertise)

    confidences = [step.confidence for step in expertise.steps]
    overall_confidence = (
        sum(confidences) / len(confidences) if confidences else 0.0
    )
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


@app.get("/demo", response_class=HTMLResponse)
def demo():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Expert to Skill</title>
<style>
* {
    box-sizing: border-box;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #0b1120;
    color: #e2e8f0;
    margin: 0;
    padding: 30px 20px;
    line-height: 1.5;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
}
header {
    text-align: center;
    margin-bottom: 30px;
}
h1 {
    font-size: 2.2rem;
    color: #f8fafc;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.tagline {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 760px;
    margin: 0 auto 12px;
}
.badge-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    font-size: 0.85rem;
}
.badge {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 4px 12px;
    border-radius: 9999px;
    color: #cbd5e1;
}
.badge.ready {
    background: #064e3b;
    border-color: #059669;
    color: #6ee7b7;
}
.badge.warn {
    background: #78350f;
    border-color: #d97706;
    color: #fde68a;
}
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}
@media (max-width: 900px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
.card {
    background: #151e32;
    border: 1px solid #1e293b;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.card h2 {
    font-size: 1.3rem;
    margin-top: 0;
    margin-bottom: 14px;
    color: #f1f5f9;
}
textarea {
    width: 100%;
    height: 320px;
    background: #090e1a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px;
    font-size: 0.95rem;
    line-height: 1.5;
    resize: vertical;
    font-family: inherit;
}
textarea:focus {
    outline: none;
    border-color: #6366f1;
}
.btn-group {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}
button.primary {
    flex: 1;
    padding: 14px 20px;
    background: #6366f1;
    color: white;
    border: 0;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}
button.primary:hover:not(:disabled) {
    background: #4f46e5;
}
button.primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
button.secondary {
    padding: 14px 18px;
    background: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 10px;
    font-size: 0.95rem;
    cursor: pointer;
}
button.secondary:hover {
    background: #334155;
}
.score-box {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
    padding: 14px;
    background: #090e1a;
    border-radius: 10px;
    border: 1px solid #1e293b;
}
.score {
    font-size: 2.4rem;
    font-weight: 800;
    color: #10b981;
}
.score.review {
    color: #f59e0b;
}
.status-pill {
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}
.status-pass {
    background: #064e3b;
    color: #6ee7b7;
}
.status-review {
    background: #78350f;
    color: #fde68a;
}
.disclaimer {
    background: #182234;
    border-left: 4px solid #6366f1;
    padding: 10px 14px;
    border-radius: 6px;
    font-size: 0.82rem;
    color: #94a3b8;
    margin-bottom: 18px;
}
.check-list {
    margin-bottom: 20px;
}
.check {
    padding: 8px 10px;
    border-bottom: 1px solid #1e293b;
    font-size: 0.9rem;
}
.check:last-child {
    border-bottom: none;
}
.action-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
}
.action-btn {
    padding: 8px 14px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #e2e8f0;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
}
.action-btn:hover {
    background: #334155;
}
pre {
    white-space: pre-wrap;
    word-break: break-word;
    background: #090e1a;
    border: 1px solid #334155;
    padding: 16px;
    border-radius: 10px;
    max-height: 440px;
    overflow-y: auto;
    font-size: 0.88rem;
    color: #cbd5e1;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
.alert-error {
    background: #451a1a;
    border: 1px solid #b91c1c;
    color: #fca5a5;
    padding: 14px;
    border-radius: 8px;
    font-size: 0.95rem;
}
.spinner {
    display: inline-block;
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 0.8s linear infinite;
    margin-right: 8px;
    vertical-align: middle;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>⚡ Expert to Skill</h1>
        <p class="tagline">An AI-powered tool that transforms practical knowledge, instructions, and documented procedures into structured, reusable <code>SKILL.md</code> files using Google's hosted Gemma 4 model.</p>
        <div class="badge-row">
            <span class="badge" id="modelBadge">Model: Loading...</span>
            <span class="badge" id="apiBadge">API Status: Checking...</span>
        </div>
    </header>

    <div class="grid">
        <div class="card">
            <h2>Source Procedure / Knowledge</h2>
            <p style="color: #94a3b8; font-size: 0.88rem; margin-top: -6px; margin-bottom: 12px;">
                Enter a documented workflow, expert demonstration, or operating procedure:
            </p>
            <textarea id="demoText">When reviewing a pull request before merging to main, first verify that all automated CI checks and tests have passed. Check out the branch locally to inspect the changes for unintended file edits, sensitive credentials, or leftover debug prints. Run the local integration test suite against the target branch. Confirm that documentation and test coverage are updated for any changed functionality. If any automated check fails or sensitive credentials are found, immediately request changes and do not approve the pull request. Once all requirements are satisfied, approve the pull request using a squash merge.</textarea>

            <div class="btn-group">
                <button class="primary" onclick="generateSkill()" id="submitBtn">
                    ✨ Generate Reusable Skill
                </button>
                <button class="secondary" onclick="loadAlternativeExample()" title="Load alternative example">
                    Load Example
                </button>
            </div>
        </div>

        <div class="card">
            <h2>Generated Skill Artifact</h2>
            <div id="outputArea">
                <p style="color: #64748b; font-style: italic; margin-top: 30px;">
                    Provide instructions on the left and click "Generate Reusable Skill" to compile a validated SKILL.md.
                </p>
            </div>
        </div>
    </div>
</div>

<script>
let lastSkillMarkdown = "";
let lastSkillTitle = "skill";

async function checkStatus() {
    try {
        const res = await fetch("/health");
        const data = await res.json();
        document.getElementById("modelBadge").innerText = "Model: " + (data.model || "gemma-4-26b-a4b-it");
        const apiBadge = document.getElementById("apiBadge");
        if (data.api_configured) {
            apiBadge.innerText = "Hosted API: Configured";
            apiBadge.className = "badge ready";
        } else {
            apiBadge.innerText = "Hosted API: Key Missing";
            apiBadge.className = "badge warn";
        }
    } catch (e) {
        document.getElementById("apiBadge").innerText = "API: Unavailable";
    }
}
checkStatus();

function loadAlternativeExample() {
    const motorcycleExample = "When my motorcycle does not start, I first turn off the ignition. I inspect the battery terminals for corrosion. Then I set my multimeter to DC voltage and measure the battery. If the voltage is very low, I charge or replace the battery. I never short the battery terminals.";
    const prExample = "When reviewing a pull request before merging to main, first verify that all automated CI checks and tests have passed. Check out the branch locally to inspect the changes for unintended file edits, sensitive credentials, or leftover debug prints. Run the local integration test suite against the target branch. Confirm that documentation and test coverage are updated for any changed functionality. If any automated check fails or sensitive credentials are found, immediately request changes and do not approve the pull request. Once all requirements are satisfied, approve the pull request using a squash merge.";
    const current = document.getElementById("demoText").value;
    document.getElementById("demoText").value = current.includes("motorcycle") ? prExample : motorcycleExample;
}

async function generateSkill() {
    const btn = document.getElementById("submitBtn");
    const output = document.getElementById("outputArea");
    const text = document.getElementById("demoText").value.trim();

    if (!text) {
        output.innerHTML = `<div class="alert-error">Please provide a procedure or demonstration text before generating.</div>`;
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span>Hosted Gemma 4 is compiling...`;
    output.innerHTML = `
        <div style="text-align: center; padding: 40px 10px; color: #94a3b8;">
            <div class="spinner" style="width: 28px; height: 28px; margin-bottom: 12px;"></div>
            <p><strong>Extracting structured expertise with hosted Gemma 4...</strong></p>
            <p style="font-size: 0.85rem; color: #64748b;">Validating fields, evaluating heuristic fidelity, and compiling SKILL.md...</p>
        </div>
    `;

    try {
        const response = await fetch("/api/skills/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ demonstration: text })
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = data.detail || (data.message || "Failed to generate skill");
            throw new Error(errorMsg);
        }

        lastSkillMarkdown = data.skill_markdown || "";
        lastSkillTitle = data.skill_id || "skill";
        const evalData = data.evaluation || {};
        const fidelity = evalData.fidelity_percent || 0;
        const isPass = evalData.status === "PASS";

        const checksHtml = (evalData.checks || []).map(c => `
            <div class="check">
                ${c.passed ? "✅" : "⚠️"} <strong>${escapeHtml(c.name)}</strong>
                <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 8px;">${escapeHtml(c.detail)}</span>
            </div>
        `).join("");

        output.innerHTML = `
            <div class="score-box">
                <div class="score ${isPass ? '' : 'review'}">${fidelity}%</div>
                <div>
                    <span class="status-pill ${isPass ? 'status-pass' : 'status-review'}">
                        ${isPass ? "✓ CERTIFIED STRUCTURE" : "⚠ EXPERT REVIEW SUGGESTED"}
                    </span>
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">
                        Confidence: ${(data.confidence * 100).toFixed(0)}% • Steps: ${data.expertise.steps ? data.expertise.steps.length : 0}
                    </div>
                </div>
            </div>

            <div class="disclaimer">
                <strong>Heuristic Fidelity Check:</strong> ${escapeHtml(evalData.disclaimer || "Structural verification check only; does not guarantee operational safety or factual validity.")}
            </div>

            <h3 style="margin-top: 0; color: #f8fafc;">${escapeHtml(data.expertise.title || "Untitled Skill")}</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; margin-bottom: 14px;">${escapeHtml(data.expertise.purpose || "")}</p>

            <details style="margin-bottom: 16px; background: #090e1a; padding: 10px 14px; border-radius: 8px; border: 1px solid #1e293b;">
                <summary style="cursor: pointer; font-weight: 600; color: #94a3b8;">Structural Verification Details (${(evalData.checks || []).length} checks)</summary>
                <div class="check-list" style="margin-top: 10px;">
                    ${checksHtml}
                </div>
            </details>

            <div class="action-bar">
                <button class="action-btn" onclick="copySkill(this)">📋 Copy SKILL.md</button>
                <button class="action-btn" onclick="downloadSkill()">⬇️ Download SKILL.md</button>
            </div>

            <pre id="skillPre">${escapeHtml(data.skill_markdown)}</pre>
        `;
    } catch (err) {
        output.innerHTML = `
            <div class="alert-error">
                <strong>Generation Error:</strong><br>
                ${escapeHtml(err.message)}
            </div>
        `;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `✨ Generate Reusable Skill`;
    }
}

function copySkill(btn) {
    if (!lastSkillMarkdown) return;
    navigator.clipboard.writeText(lastSkillMarkdown).then(() => {
        const orig = btn.innerText;
        btn.innerText = "✓ Copied!";
        setTimeout(() => { btn.innerText = orig; }, 2000);
    }).catch(err => {
        alert("Could not copy to clipboard: " + err);
    });
}

function downloadSkill() {
    if (!lastSkillMarkdown) return;
    const blob = new Blob([lastSkillMarkdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = (lastSkillTitle || "skill") + ".SKILL.md";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function escapeHtml(text) {
    if (!text) return "";
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}
</script>
</body>
</html>
"""
