# Failure Modes & Error Handling

Expert to Skill handles failure modes robustly without silently inventing AI output or failing silently.

## Handled Failure Modes

1. **Missing Server Credentials (`GEMINI_API_KEY`):**
   - The application starts normally, but generation returns HTTP 503 explaining that `GEMINI_API_KEY` is required.
2. **Empty Input Demonstration:**
   - Validated upfront with HTTP 400 bad request error.
3. **API or Network Connectivity Issues:**
   - Caught and surfaced cleanly as HTTP 502 with descriptive message.
4. **Markdown-Fenced JSON or Malformed Output:**
   - Sanitized via regex fence stripping; malformed JSON raises descriptive syntax errors rather than crashing.
5. **Schema Non-Compliance:**
   - Validated through Pydantic; schema mismatches raise validation errors before compilation.
