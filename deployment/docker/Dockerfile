FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    APP_ROOT=/app \
    PORT=8080 \
    COMPILED_DIR=/app/compiled \
    LOGS_DIR=/app/compiled/logs \
    TEMPLATES_DIR=/app/templates \
    LATEX_BASE_URL="http://localhost:8080" \
    LATEX_MAX_FILE_AGE_HOURS=24 \
    HOME=/app

# Base deps + TeX + latexmk + Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    latexmk \
    texlive-base texlive-latex-base texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-fonts-extra \
    texlive-xetex texlive-luatex \
    texlive-pictures texlive-plain-generic \
    fonts-noto-core ca-certificates curl tini python3 python3-pip \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_ROOT}

# Python dependencies
RUN pip3 install --no-cache-dir fastmcp>=2.10 jinja2>=3.1 pydantic>=2.7 pyyaml>=6.0 uvicorn>=0.30

# Copy application files
COPY server.py ${APP_ROOT}/
COPY plugins/ ${APP_ROOT}/plugins/
COPY mcp_core/ ${APP_ROOT}/mcp_core/

# Create required directories
RUN mkdir -p ${COMPILED_DIR} ${LOGS_DIR} ${TEMPLATES_DIR}

EXPOSE ${PORT}
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["python3","/app/server.py"]