# LaTeX MCP Server

A small Model Context Protocol server that compiles LaTeX documents and serves the resulting PDFs. It also exposes a handful of document templates and reusable snippets.

The project is usable but lightly maintained: I am not currently developing new features for it.

## Tools

- `compile_latex` compiles a complete document with pdfLaTeX, XeLaTeX or LuaLaTeX.
- `list_templates` and `get_template` expose the bundled document templates.
- `list_snippets`, `get_snippet_info` and `render_snippet` work with the bundled equation, figure and multiple-choice snippets.

Compiled files are cached by source and engine, then removed after a configurable period.

## Run with Docker

Build from the repository root:

```bash
docker build -f deployment/docker/Dockerfile -t latex-mcp .
docker run --rm -p 8083:8080 latex-mcp
```

The MCP HTTP endpoint is then available at `http://localhost:8083/mcp`.

Docker Compose configuration is under `deployment/docker/`:

```bash
docker compose -f deployment/docker/docker-compose.yml up --build
```

## Run directly

This requires Python 3.11+ and a TeX distribution providing `pdflatex`, `xelatex` or `lualatex`.

```bash
python -m pip install .
python server.py
```

Configuration is available through three environment variables:

- `PORT` — HTTP port, defaulting to `8080`.
- `LATEX_BASE_URL` — public base URL used in PDF and log links.
- `LATEX_MAX_FILE_AGE_HOURS` — compiled-file retention, defaulting to 24 hours.

## Security boundary

LaTeX is a programmable language, and rejecting a short list of commands does not make arbitrary documents safe. Shell escape is disabled and the server performs some basic source validation, but this is not a hardened multi-tenant sandbox.

Use it with trusted inputs, preferably inside a disposable container with no secrets, restricted resources and no unnecessary network or filesystem access. Do not expose the HTTP service publicly without adding authentication and further isolation.

## Maintained alternatives

If this server no longer fits your workflow, these more active projects cover adjacent use cases:

- [mcp-latex-server](https://github.com/RobertoDure/mcp-latex-server) — LaTeX file creation, editing and project management.
- [latex-mcp](https://github.com/SepineTam/latex-mcp) — LaTeX compilation inside Docker.
- [texflow-mcp](https://github.com/aaronsb/texflow-mcp) — structured document authoring with an MCP compiler.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

Deployment examples for Docker, systemd and Nginx live under `deployment/`.

## Licence

MIT
