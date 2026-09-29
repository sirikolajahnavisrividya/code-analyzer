from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer.code_analyzer import analyze
from execution.runner import run_code, available, CFG

LANGS = ["python","javascript","typescript","java","c","cpp","csharp","go","rust","php","ruby","kotlin","swift","sql"]
app = FastAPI(title="AI Code Reviewer")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

class Req(BaseModel):
    language: str = "python"
    code: str
    stdin: str = ""

@app.get("/")
def root():
    return {"name": "AI Code Reviewer", "languages": LANGS, "execution": {l: available(l) for l in LANGS}}

@app.post("/review")
def review(r: Req):
    if not r.code.strip(): return {"error": "Code is empty."}
    if r.language not in LANGS: return {"error": f"Unsupported language: {r.language}"}
    try: return analyze(r.language, r.code)
    except Exception as e: return {"error": f"Analysis failed: {e}"}

@app.post("/run")
def run(r: Req):
    if not r.code.strip(): return {"available": True, "status": "Empty code", "stdout": "", "stderr": "Nothing to run."}
    return run_code(r.language, r.code, r.stdin)
