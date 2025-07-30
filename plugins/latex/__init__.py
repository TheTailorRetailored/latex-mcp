from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict
from .engine import (
    compile_latex_source, cleanup_old_files, TEMPLATES, validate_source
)
from .snippets import (
    list_available_snippets, get_snippet_info, render_snippet
)

class CompileResult(TypedDict):
    url: str
    log_url: str
    filename: str
    engine: str
    hash: str
    cached: bool

def register(mcp):
    @mcp.tool
    def compile_latex(source: str,
                      filename: Optional[str] = None,
                      engine: str = "xelatex",
                      enable_cache: bool = True,
                      passes: int = 2) -> CompileResult:
        """Compile LaTeX to PDF. Returns {url, log_url, filename, hash, engine, cached}"""
        # Run automatic cleanup before compilation
        cleanup_old_files()
        return compile_latex_source(source, filename, engine, enable_cache, passes)


    @mcp.tool
    def list_templates() -> List[Dict[str,str]]:
        """List templates available on server."""
        out = []
        for t in TEMPLATES.glob("*.tex"):
            desc = "No description"
            for line in t.read_text(encoding="utf-8").splitlines()[:10]:
                if line.strip().startswith("% Description:"):
                    desc = line.split(":",1)[1].strip(); break
            out.append({"name": t.stem, "filename": t.name, "description": desc})
        return out

    @mcp.tool
    def get_template(name: str) -> str:
        """Return template source by name."""
        p = TEMPLATES / f"{name}.tex"
        if not p.exists(): raise FileNotFoundError(f"Template '{name}' not found")
        return p.read_text(encoding="utf-8")

    @mcp.tool
    def list_snippets() -> List[Dict[str, Any]]:
        """List all available LaTeX snippets/macros with their descriptions."""
        return list_available_snippets()

    @mcp.tool
    def get_snippet_info(name: str) -> Dict[str, Any]:
        """Get detailed information about a snippet including parameters and usage."""
        return get_snippet_info(name)

    @mcp.tool
    def render_snippet(name: str, **parameters) -> str:
        """Render a LaTeX snippet with the provided parameters."""
        return render_snippet(name, **parameters)


