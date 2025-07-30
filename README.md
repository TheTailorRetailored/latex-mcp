# LaTeX MCP Server

A Model Context Protocol (MCP) server for LaTeX compilation and document generation.

## Features

- **LaTeX Compilation**: Compile LaTeX source to PDF using various engines (pdflatex, xelatex, lualatex)
- **Template System**: Manage reusable LaTeX templates
- **Snippets/Macros**: Use predefined LaTeX components (equations, figures, multiple choice questions, etc.)
- **Automatic Cleanup**: Old files are automatically cleaned up during compilation
- **Caching**: Compiled documents are cached to avoid recompilation
- **Security**: Dangerous LaTeX commands are blocked

## MCP Tools

### Core Tools
- `compile_latex` - Compile LaTeX source to PDF
- `list_templates` - List available LaTeX templates  
- `get_template` - Get template source code

### Snippets System
- `list_snippets` - List available LaTeX snippets/macros
- `get_snippet_info` - Get detailed info about a snippet including parameters
- `render_snippet` - Render a snippet with provided parameters

## Available Snippets

- **multiple_choice** - Creates multiple choice questions with 4 options
- **equation** - Creates numbered equations with optional labels
- **figure** - Creates figures with captions and optional labels

## Installation

### Docker (Recommended)

1. Build the image:
```bash
docker build -f Dockerfile.simple -t mcp-latex-simple .
```

2. Run the container:
```bash
docker run -d --name mcp-latex-server --restart unless-stopped -p 8083:8080 mcp-latex-simple
```

### Manual Installation

1. Install system dependencies:
```bash
# Install LaTeX
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# Install Python dependencies
pip install fastmcp jinja2 pydantic pyyaml uvicorn
```

2. Run the server:
```bash
python server.py
```

## Configuration

Set environment variables:
- `PORT` - Server port (default: 8080)
- `LATEX_BASE_URL` - Base URL for compiled files
- `LATEX_MAX_FILE_AGE_HOURS` - File cleanup age in hours (default: 24)

## Usage with Claude

Configure Claude Desktop to connect to your MCP server:
- URL: `https://your-domain.com/`
- Transport: HTTP

## API

The server exposes a Model Context Protocol interface on the configured port and path.

## Security

- Dangerous LaTeX commands are blocked
- File system access is restricted
- No shell escapes allowed during compilation
- Automatic cleanup prevents disk space issues

## Development

See the included configuration files:
- `docker-compose-standalone.yml` - Docker Compose setup
- `mcp-latex.service` - Systemd service
- `nginx-include.conf` - Nginx configuration