from __future__ import annotations
import hashlib, json, os, re, subprocess, uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict

ROOT = Path(__file__).parent
COMPILED = ROOT / "compiled"
LOGS     = ROOT / "logs"
TEMPLATES= ROOT / "templates"

BASE_URL = os.environ.get("LATEX_BASE_URL", "https://mcp.lachlanbridges.com")
MAX_AGE_HOURS = int(os.environ.get("LATEX_MAX_FILE_AGE_HOURS", "24"))

for d in (COMPILED, LOGS, TEMPLATES):
    d.mkdir(exist_ok=True, parents=True)

DANGEROUS = (
    r"\\write18", r"\\immediate\\write18", r"\\openin", r"\\openout",
    r"\\newwrite", r"\\newread", r"\\input\{/", r"\\include\{/"
)
DANGEROUS_RE = re.compile("|".join(DANGEROUS))

ALLOWED_ENGINES = {"pdflatex", "xelatex", "lualatex"}

def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def _sanitize_name(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in ("-", "_")) or "doc"

def validate_source(src: str) -> None:
    if DANGEROUS_RE.search(src):
        raise ValueError("Blocked potentially dangerous LaTeX command.")
    if "\\documentclass" not in src:       raise ValueError("Missing \\documentclass")
    if "\\begin{document}" not in src:     raise ValueError("Missing \\begin{document}")
    if "\\end{document}" not in src:       raise ValueError("Missing \\end{document}")

def cleanup_old_files(hours: int = MAX_AGE_HOURS) -> Dict[str,int]:
    cutoff = datetime.now() - timedelta(hours=hours)
    removed = {"pdf":0, "log":0}
    for p in COMPILED.glob("*.pdf"):
        if datetime.fromtimestamp(p.stat().st_mtime) < cutoff:
            p.unlink(missing_ok=True); removed["pdf"] += 1
    for p in LOGS.glob("*.txt"):
        if datetime.fromtimestamp(p.stat().st_mtime) < cutoff:
            p.unlink(missing_ok=True); removed["log"] += 1
    return removed

def compile_latex_source(
    source: str,
    filename: Optional[str] = None,
    engine: str = "xelatex",
    enable_cache: bool = True,
    passes: int = 2
) -> Dict[str, str | bool]:
    validate_source(source)
    if engine not in ALLOWED_ENGINES:
        raise ValueError(f"Unsupported engine: {engine}")

    # Cache key
    key = _hash(source + engine)
    pdf_existing = next(COMPILED.glob(f"*_{key}.pdf"), None)
    if enable_cache and pdf_existing:
        name = pdf_existing.stem
        return {
            "url":     f"{BASE_URL}/latex/compiled/{pdf_existing.name}",
            "log_url": f"{BASE_URL}/latex/logs/{name}.txt",
            "filename": pdf_existing.name,
            "cached": True,
            "engine": engine,
            "hash": key,
        }

    base = _sanitize_name(filename or "doc")
    job  = f"{base}_{key}"
    tex  = COMPILED / f"{job}.tex"
    pdf  = COMPILED / f"{job}.pdf"
    log  = LOGS / f"{job}.txt"

    tex.write_text(source, encoding="utf-8")

    # Compile (multiple passes, no shell-escape)
    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape",
           f"-output-directory={COMPILED}", str(tex)]
    outs = []
    for _ in range(max(1, passes)):
        res = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
        outs.append(("stdout", res.stdout))
        outs.append(("stderr", res.stderr))
        if res.returncode != 0:
            break

    # Write combined log (keep, do NOT delete)
    log_txt = f"Engine: {engine}\nJob: {job}\n\n"
    for k,v in outs:
        if v:
            log_txt += f"--- {k.upper()} ---\n{v}\n"
    log.write_text(log_txt, encoding="utf-8")

    if not pdf.exists():
        raise RuntimeError(f"Compilation failed. See log: {BASE_URL}/latex/logs/{job}.txt")

    return {
        "url":     f"{BASE_URL}/latex/compiled/{pdf.name}",
        "log_url": f"{BASE_URL}/latex/logs/{job}.txt",
        "filename": pdf.name,
        "cached": False,
        "engine": engine,
        "hash": key,
    }
