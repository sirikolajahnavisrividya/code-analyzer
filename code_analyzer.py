"""Deterministic, regex-based static analysis + safe auto-fixes.
Rule: (languages or None=all, regex, category, severity, title, why, fix_text, fix_code, (sub_pattern, replacement) or None)"""
import ast, re

RULES = [
 (None, r"(password|passwd|secret|api_?key|token)\s*=\s*['\"][^'\"]+['\"]", "security", "high",
  "Hardcoded secret", "Secrets in source code leak through version control and shared files.",
  "Load the secret from an environment variable.", "value = os.environ['MY_SECRET']  # or process.env.MY_SECRET", None),
 (None, r"http://", "security", "low", "Insecure HTTP URL", "HTTP traffic is unencrypted and can be read or modified.",
  "Use https:// instead.", "https://example.com", (r"http://", "https://")),
 (None, r"TODO|FIXME", "quality", "low", "TODO/FIXME left in code", "Unfinished work is easy to forget.", "Finish it or track it in an issue.", "", None),
 (None, r"select\s+\*", "performance", "low", "SELECT * used", "Fetching every column wastes memory and bandwidth.",
  "List only the columns you need.", "SELECT id, name FROM users WHERE ...", None),
 (["python","javascript","typescript","ruby","php"], r"\beval\s*\(", "security", "high", "eval() on dynamic input",
  "eval runs any text as code, so an attacker can run their own code.", "Parse data safely (json.loads / ast.literal_eval / JSON.parse).",
  "value = ast.literal_eval(text)   # JSON.parse(text) in JS", None),
 (["python"], r"\bexec\s*\(", "security", "high", "exec() usage", "exec runs arbitrary code.", "Avoid it; call functions directly.", "", None),
 (["python"], r"except\s*:", "quality", "medium", "Bare except", "Catches every error, hiding real bugs (even Ctrl+C).",
  "Catch specific exceptions.", "except ValueError as e:\n    print(e)", (r"except\s*:", "except Exception as e:")),
 (["python"], r"(execute\(|query\s*=).*(\+|%|\.format|f['\"])", "security", "high", "Possible SQL injection",
  "User input is inserted straight into the query, so an attacker can change the query.", "Use parameterized queries.",
  "query = \"SELECT * FROM users WHERE name = ?\"\ncursor.execute(query, (username,))", None),
 (["python"], r"hashlib\.(md5|sha1)", "security", "medium", "Weak hash", "MD5/SHA1 are broken for passwords.", "Use hashlib.sha256 or bcrypt/argon2 for passwords.",
  "hashlib.sha256(data).hexdigest()", (r"hashlib\.(md5|sha1)", "hashlib.sha256")),
 (["python"], r"os\.system\(|subprocess\..*shell\s*=\s*True", "security", "high", "Command injection risk",
  "Shell commands built from input let attackers run other commands.", "Pass an argument list without shell=True.",
  "subprocess.run(['ls', path], check=True)", None),
 (["python"], r"pickle\.loads?\(", "security", "high", "Unsafe deserialization", "Unpickling untrusted data can run code.", "Use JSON.", "json.loads(data)", None),
 (["javascript","typescript"], r"\.innerHTML\s*=", "security", "high", "XSS via innerHTML", "Untrusted text is parsed as HTML, so scripts can run.",
  "Use textContent.", "el.textContent = userInput;", (r"\.innerHTML\s*=", ".textContent =")),
 (["javascript","typescript"], r"\bvar\s+", "quality", "low", "var used", "var is function-scoped and error-prone.", "Use let or const.", "const x = 1;", (r"\bvar\s+", "let ")),
 (["javascript","typescript"], r"\bany\b", "quality", "low", "'any' type", "any disables type checking.", "Use a real type or unknown.", "let x: unknown;", None),
 (["c","cpp"], r"\b(gets|strcpy|strcat|sprintf)\s*\(", "security", "high", "Unsafe C string function (buffer overflow)",
  "These functions do not check buffer size, so long input overwrites memory.", "Use bounded versions.",
  "fgets(buf, sizeof buf, stdin);\nsnprintf(buf, sizeof buf, \"%s\", src);", (r"\bstrcpy\(([^,]+),", r"strncpy(\1,")),
 (["c","cpp"], r"\bmalloc\s*\(", "quality", "medium", "Manual memory (check free())", "Missing free() causes memory leaks.", "Call free() on every path, or use RAII in C++.", "free(ptr);", None),
 (["c","cpp"], r"printf\s*\(\s*[a-z_]+\s*\)", "security", "high", "Format string bug", "User text used as a format lets attackers read memory.", "Use a fixed format.", 'printf("%s", text);', None),
 (["java","csharp","kotlin"], r"\.equals\(|!!", "quality", "medium", "Possible null handling issue", "Calling methods on null crashes the program.", "Check for null or use safe calls (?.).", "if (x != null) { ... }", None),
 (["go"], r"\b_\s*,?\s*(:?=)?\s*[a-zA-Z.]+\(.*\)\s*$", "quality", "medium", "Ignored error (Go)", "Discarding errors hides failures.", "Check err != nil.", "if err != nil { return err }", None),
 (["rust"], r"\bunsafe\s*\{|\.unwrap\(\)|\.clone\(\)", "quality", "medium", "unsafe / unwrap / clone", "These bypass Rust safety, can panic, or copy data.", "Use ? and borrowing.", "let v = f()?;", None),
 (["swift"], r"\w+!\s|as!", "quality", "medium", "Force unwrap", "Crashes when the value is nil.", "Use if let / guard let.", "if let v = x { }", None),
 (["php"], r"\$_(GET|POST|REQUEST)", "security", "high", "Unsanitized user input", "Request data is untrusted (XSS/SQL injection).", "Validate, and use htmlspecialchars / prepared statements.",
  "echo htmlspecialchars($_GET['q'], ENT_QUOTES);", None),
 (["sql"], r"delete\s+from\s+\w+\s*;|update\s+\w+\s+set[^;]*;(?!.*where)", "security", "high", "DELETE/UPDATE without WHERE", "Affects every row in the table.", "Add a WHERE clause.", "DELETE FROM users WHERE id = 5;", None),
]

LEARN = {
 "SQL": "SQL injection: attacker-controlled text changes the meaning of your query. Parameters keep data separate from code.",
 "eval": "eval runs text as code, so any input becomes a possible attack.",
 "buffer": "Buffer overflow: writing past the end of an array corrupts memory and can be exploited.",
 "Bare": "Catch specific exceptions so real bugs are not silently hidden.",
 "XSS": "XSS: untrusted text is rendered as HTML/JS in the browser. Use textContent.",
 "Hardcoded": "Never commit secrets; keep them in environment variables.",
}

def syntax_check(lang, code):
    if lang == "python":
        try: ast.parse(code)
        except SyntaxError as e:
            return {"valid": False, "line": e.lineno, "message": e.msg, "checked": True}
    elif lang == "json":
        pass
    else:  # only balance check for other languages
        pairs = {")": "(", "]": "[", "}": "{"}; st = []
        for i, ln in enumerate(code.splitlines(), 1):
            for ch in ln:
                if ch in "([{": st.append((ch, i))
                elif ch in pairs:
                    if not st or st[-1][0] != pairs[ch]:
                        return {"valid": False, "line": i, "message": f"Unmatched '{ch}'", "checked": False}
                    st.pop()
        if st: return {"valid": False, "line": st[-1][1], "message": f"Unclosed '{st[-1][0]}'", "checked": False}
        return {"valid": True, "checked": False, "note": "Basic bracket check only; full syntax check needs the language compiler."}
    return {"valid": True, "checked": lang == "python"}

def complexity(lang, code):
    depth = mx = 0
    if lang == "python":
        try:
            def walk(n, d):
                nonlocal mx
                for c in ast.iter_child_nodes(n):
                    nd = d + isinstance(c, (ast.For, ast.While))
                    mx = max(mx, nd); walk(c, nd)
            walk(ast.parse(code), 0)
        except SyntaxError: return "Unknown"
    else:
        for ln in code.splitlines():
            if re.search(r"\b(for|while)\b", ln): depth += 1; mx = max(mx, depth)
            depth = max(0, depth - ln.count("}") ) if "}" in ln else depth
    return {0: "O(1) / depends on called functions", 1: "Approximately O(n)", 2: "Potentially O(n²) or higher"}.get(mx, "Potentially O(n³) or higher")

def analyze(lang, code):
    lines = code.splitlines(); issues = []
    for langs, pat, cat, sev, title, why, fix, fixcode, sub in RULES:
        if langs and lang not in langs: continue
        for i, ln in enumerate(lines, 1):
            if re.search(pat, ln, re.I):
                issues.append({"line": i, "category": cat, "severity": sev, "title": title, "code": ln.strip(),
                    "why": why, "recommendation": fix, "fix_code": fixcode, "_sub": sub})
    if lang == "python":  # nested loops (performance) via AST
        if complexity(lang, code).startswith("Potentially"):
            issues.append({"line": 1, "category": "performance", "severity": "medium", "title": "Nested loops",
                "code": "for ... in ...:\n    for ... in ...:", "why": "Work grows with the square of the input size.",
                "recommendation": "Use a set/dict for lookups instead of an inner loop.", "fix_code": "seen = set(items)\nfor x in other:\n    if x in seen: ...", "_sub": None})
    # improved code: apply only safe substitutions
    improved, manual = list(lines), []
    for it in issues:
        sub = it.pop("_sub")
        if sub:
            new = re.sub(sub[0], sub[1], improved[it["line"] - 1], flags=re.I)
            if new != improved[it["line"] - 1]: improved[it["line"] - 1] = new; continue
        manual.append(it["title"])
    weight = {"high": 15, "medium": 8, "low": 3}
    score = max(0, 100 - sum(weight[i["severity"]] for i in issues))
    learn = sorted({v for k, v in LEARN.items() if any(k in i["title"] for i in issues)})
    return {"language": lang, "syntax": syntax_check(lang, code), "score": score, "issues": issues,
            "summary": {"total": len(issues), **{c: sum(i["category"] == c for i in issues) for c in ("security", "quality", "performance")}},
            "complexity": complexity(lang, code), "complexity_note": "Estimate based on static structure only.",
            "improved_code": "\n".join(improved), "manual_review": bool(manual), "manual_items": sorted(set(manual)),
            "learn": learn, "analysis_mode": "rule-based (deterministic)"}
