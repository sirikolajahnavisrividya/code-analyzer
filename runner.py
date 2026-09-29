"""Runs code in a separate process: temp dir, empty env, timeout, output cap, POSIX memory/CPU limits.
NOTE: network is NOT blocked at process level. For untrusted public use, run this in Docker with --network none."""
import os, shutil, subprocess, sys, tempfile, time

ENABLED = os.getenv("ENABLE_EXECUTION", "true").lower() == "true"
PY = sys.executable
# language -> (filename, compile cmd or None, run cmd, required tool)
CFG = {
 "python": ("main.py", None, [PY, "main.py"], PY),
 "javascript": ("main.js", None, ["node", "main.js"], "node"),
 "ruby": ("main.rb", None, ["ruby", "main.rb"], "ruby"),
 "php": ("main.php", None, ["php", "main.php"], "php"),
 "go": ("main.go", None, ["go", "run", "main.go"], "go"),
 "c": ("main.c", ["gcc", "main.c", "-o", "prog"], ["./prog"], "gcc"),
 "cpp": ("main.cpp", ["g++", "main.cpp", "-o", "prog"], ["./prog"], "g++"),
}

def available(lang):
    return ENABLED and lang in CFG and shutil.which(CFG[lang][3]) is not None

def _limits():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
        resource.setrlimit(resource.RLIMIT_AS, (512 * 2**20,) * 2)
    except ImportError:
        pass  # Windows has no 'resource'

def _exec(cmd, cwd, stdin, timeout):
    env = {"PATH": os.environ.get("PATH", ""), "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
    kw = {"preexec_fn": _limits} if os.name == "posix" else {}
    p = subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=timeout, env=env, **kw)
    return p

def run_code(lang, code, stdin="", timeout=5):
    if lang not in CFG or not available(lang):
        return {"available": False, "message": "Execution unavailable for this language in the current environment."}
    fname, comp, run, _ = CFG[lang]
    d = tempfile.mkdtemp(prefix="acr_")
    t0 = time.time()
    try:
        open(os.path.join(d, fname), "w", encoding="utf-8").write(code)
        if comp:
            c = _exec(comp, d, "", 20)
            if c.returncode != 0:
                return {"available": True, "status": "Compilation failed", "stdout": "", "stderr": c.stderr[:5000], "exit_code": c.returncode, "time": round(time.time() - t0, 3)}
        p = _exec(run, d, stdin, timeout)
        return {"available": True, "status": "Completed" if p.returncode == 0 else "Runtime error", "stdout": p.stdout[:20000],
                "stderr": p.stderr[:5000], "exit_code": p.returncode, "time": round(time.time() - t0, 3)}
    except subprocess.TimeoutExpired:
        return {"available": True, "status": f"Timed out after {timeout}s (process killed)", "stdout": "", "stderr": "", "exit_code": None, "time": timeout}
    except Exception as e:
        return {"available": True, "status": "Execution failure", "stdout": "", "stderr": str(e), "exit_code": None, "time": 0}
    finally:
        shutil.rmtree(d, ignore_errors=True)
