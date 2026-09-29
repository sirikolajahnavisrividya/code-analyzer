import { useState } from "react";
import Editor from "@monaco-editor/react";
import { LANGS, sampleFor, fileName } from "./samples.js";
const API = "http://localhost:8000";
const post = async (path, body) => {
  try { const r = await fetch(API + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }); return await r.json(); }
  catch { return { error: "Backend unavailable. Is it running on port 8000?" }; }
};
const copy = t => navigator.clipboard.writeText(t);

export default function App() {
  const init = localStorage.getItem("acr_lang") || "python";
  const [lang, setLang] = useState(init);
  const [code, setCode] = useState(sampleFor(init));
  const [saved, setSaved] = useState(sampleFor(init));
  const [stdin, setStdin] = useState("");
  const [rev, setRev] = useState(null), [out, setOut] = useState(null);
  const [busy, setBusy] = useState(""), [filter, setFilter] = useState("all");

  const change = l => {
    if (code !== saved && !confirm("Discard your unsaved code?")) return;
    localStorage.setItem("acr_lang", l); setLang(l); setCode(sampleFor(l)); setSaved(sampleFor(l)); setRev(null); setOut(null);
  };
  const review = async () => { setBusy("review"); setRev(await post("/review", { language: lang, code })); setBusy(""); };
  const run = async () => { setBusy("run"); setOut(await post("/run", { language: lang, code, stdin })); setBusy(""); };
  const issues = rev?.issues?.filter(i => filter === "all" || i.category === filter) || [];

  return (<div className="app">
    <div className="grid" />
    <header className="hero">
      <h1>AI Code Reviewer</h1>
      <p className="tag">Understand your code. Find the risks. Fix it. Run it.</p>
      <p className="sub">AI-powered security, quality and performance analysis for modern developers.</p>
      <a className="btn primary" href="#editor">Start Reviewing</a>
      <button className="btn" onClick={() => setCode(sampleFor(lang))}>Load Sample</button>
    </header>
    <section id="editor" className="card">
      <div className="bar">
        <select value={lang} onChange={e => change(e.target.value)}>{Object.entries(LANGS).map(([k, v]) => <option key={k} value={k}>{v[0]}</option>)}</select>
        <span className="file">{fileName(lang)}</span>
        <span className="spacer" />
        <button className="btn" onClick={() => setCode(sampleFor(lang))}>Load Sample</button>
        <button className="btn" onClick={() => { setCode(""); setRev(null); setOut(null); }}>Reset</button>
        <button className="btn" onClick={() => copy(code)}>Copy</button>
        <button className="btn" disabled={!!busy} onClick={run}>{busy === "run" ? "Running…" : "▶ Run Code"}</button>
        <button className="btn primary" disabled={!!busy} onClick={review}>{busy === "review" ? "Analyzing…" : "Review Code"}</button>
      </div>
      <Editor height="380px" theme="vs-dark" language={LANGS[lang][2]} value={code} onChange={v => setCode(v || "")} options={{ minimap: { enabled: false }, fontSize: 14 }} />
      {!code.trim() && <p className="muted pad">Paste or write your code to begin.</p>}
      <textarea className="stdin" placeholder="Input (stdin) for your program…" value={stdin} onChange={e => setStdin(e.target.value)} />
    </section>

    {out && <section className="card pad fade"><h2>Program Output</h2>
      <p className="muted">Real output from a sandboxed process. Not AI-generated.</p>
      {out.error ? <p className="err">{out.error}</p> : out.available === false ? <p className="warn"><b>{out.message}</b></p> : <>
        <pre className="term">{out.stdout || "(no output)"}</pre>
        {out.stderr && <pre className="term err">{out.stderr}</pre>}
        <p className="muted">Status: {out.status} · Time: {out.time}s · Exit code: {String(out.exit_code)}</p></>}
    </section>}

    {rev?.error && <section className="card pad err">{rev.error}</section>}
    {rev && !rev.error && <div className="fade">
      <section className="card pad row">
        <div className="score" style={{ "--s": rev.score }}><b>{rev.score}</b>/100</div>
        <div><h2>Overall Code Quality Score</h2>
          <p className="muted">Calculated from the severity of detected issues. Not a scientific measure.</p>
          <p className={rev.syntax.valid ? "ok" : "err"}>{rev.syntax.valid ? "✓ Syntax Valid" : `✕ Syntax Error (line ${rev.syntax.line}): ${rev.syntax.message}`}</p>
          {rev.syntax.note && <p className="muted">{rev.syntax.note}</p>}
          <p>Algorithm Complexity: <b>{rev.complexity}</b> <span className="muted">({rev.complexity_note})</span></p>
          <p className="muted">Analysis: {rev.analysis_mode}. Checks are pattern-based, not exhaustive.</p></div>
      </section>
      <div className="cards">{[["Total Issues", "total"], ["Security", "security"], ["Quality", "quality"], ["Performance", "performance"]].map(([l, k]) =>
        <div key={k} className={"stat " + k}><b>{rev.summary[k]}</b><span>{l}</span></div>)}</div>
      <section className="card pad"><h2>Detected Issues</h2>
        <div className="tabs">{["all", "security", "quality", "performance"].map(f => <button key={f} className={"btn " + (filter === f ? "primary" : "")} onClick={() => setFilter(f)}>{f}</button>)}</div>
        {!issues.length && <p className="ok">No issues in this category.</p>}
        {issues.map((i, n) => <div key={n} className="issue">
          <div><span className={"pill " + i.category}>{i.category}</span> <span className={"pill sev-" + i.severity}>{i.severity.toUpperCase()}</span> <span className="muted">Line {i.line}</span></div>
          <h3>{i.title}</h3><pre className="term">{i.code}</pre>
          <p><b>Why it's a problem:</b> {i.why}</p><p><b>How to fix it:</b> {i.recommendation}</p>
          {i.fix_code && <><pre className="term good">{i.fix_code}</pre><button className="btn" onClick={() => copy(i.fix_code)}>Copy Fix</button></>}
        </div>)}</section>
      <section className="card pad"><h2>Improved Code</h2>
        {rev.manual_review && <p className="warn">Manual review recommended: {rev.manual_items.join(", ")} could not be fixed automatically.</p>}
        <pre className="term good">{rev.improved_code}</pre>
        <button className="btn primary" onClick={() => copy(rev.improved_code)}>Copy Improved Code</button></section>
      {rev.learn.length > 0 && <section className="card pad"><h2>Learn From This Review</h2><ul>{rev.learn.map((l, i) => <li key={i}>{l}</li>)}</ul></section>}
    </div>}
    <footer className="muted pad">Code execution is sandboxed with a timeout and limited resources. Do not run untrusted code you don't understand.</footer>
  </div>);
}
