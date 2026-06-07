# OSED regulatory connector — container image for hosting as a REMOTE MCP
# connector (claude.ai / Claude Cowork). Serves the same six tools the Claude
# Code plugin runs over stdio, here over streamable HTTP.
#
#   docker build -t osed-connector connectors/regulatory
#   docker run -p 8000:8000 \
#     -e COURTLISTENER_API_KEY=... -e REGULATIONS_GOV_API_KEY=... \
#     osed-connector
#   # → MCP endpoint at http://localhost:8000/mcp
#
# The two keys are OPTIONAL: the keyless tools (Federal Register, eCFR, US Code)
# work without them; the keyed tools return an explicit not-found if their key
# is absent. See DEPLOY.md for hosting + how to add this as a remote connector.

FROM python:3.11-slim

# Avoid .pyc clutter; unbuffered logs for container platforms.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    MCP_PATH=/mcp

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir .

# Run as a non-root user.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# PORT is read at runtime (Cloud Run / Fly / Render inject their own).
CMD ["osed-connectors-http"]
