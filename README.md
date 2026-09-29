# AI Code Reviewer
Rule-based multi-language code review (security / quality / performance), improved code, complexity estimate and sandboxed Run Code.
Frontend: React + Vite + Monaco. Backend: FastAPI.

## Setup (Windows CMD)
Terminal 1 (backend):
    cd AI-Code-Reviewer\backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Terminal 2 (frontend):
    cd AI-Code-Reviewer\frontend
    npm install
    npm run dev
Open http://localhost:5173

## Execution
Run Code works for languages whose tool is installed: Python, Node (JavaScript), Ruby, PHP, Go, gcc (C), g++ (C++).
Others show "Execution unavailable for this language in the current environment." (`GET /` lists what is detected).
Isolation: separate process, temp folder, stripped environment (no secrets), 5 s timeout, output cap, CPU/memory limits on Linux/macOS.
Limitation: network is not blocked and Windows has no memory limit. For untrusted users run the backend in Docker with `--network none`, or set ENABLE_EXECUTION=false.

## Test
- Python sample: Review -> hardcoded secret, SQL injection, bare except, weak hash, nested loops. Run -> prints Result.
- C sample: Review -> strcpy + malloc issues. Run needs gcc installed.
- SQL sample: DELETE without WHERE, SELECT *.
- `print(x)` in Python -> Run shows a real NameError; `def f(:` -> Syntax Error with line.

## Troubleshooting
"Backend unavailable" = backend not running on port 8000. Port busy = change the port in uvicorn and API in App.jsx.
