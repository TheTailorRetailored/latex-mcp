# Docker Deployment

## Quick Start

Build and run the LaTeX MCP Server using Docker.

### Option 1: Simple Build (Recommended)

```bash
# Build using pre-built texlive image (faster)
docker build -f Dockerfile.simple -t mcp-latex-simple ../..

# Run the container
docker run -d --name mcp-latex-server --restart unless-stopped -p 8083:8080 mcp-latex-simple
```

### Option 2: Docker Compose

```bash
# Standalone service
docker-compose -f docker-compose-standalone.yml up -d

# Or with the snippet version
docker-compose -f docker-compose-snippet.yml up -d
```

## Configuration

The container can be configured with environment variables:

- `PORT` - Server port (default: 8080)
- `LATEX_BASE_URL` - Base URL for compiled files
- `LATEX_MAX_FILE_AGE_HOURS` - File cleanup age in hours (default: 24)

## Health Check

The container includes a health check that verifies the MCP server is responding:

```bash
curl http://localhost:8083/
```

## Volumes

Optional persistent volumes:
- `/app/compiled` - Compiled PDF files
- `/app/compiled/logs` - Compilation logs