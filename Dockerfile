# Use a slim, official Python runtime as a parent image
FROM python:3.11-slim as builder

# Set shell and basic env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies into a local directory
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy python dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Add local bin to PATH for the application user
ENV PATH=/root/.local/bin:$PATH

# Create and switch to a non-privileged system user for container security hardening
RUN useradd -u 10001 -r -g   nogroup appuser && \
    chown -R appuser:nogroup /app
USER appuser

# Expose port for Cloud Run SSE endpoint
ENV PORT=8080
EXPOSE 8080

# Command to run the MCP server using SSE transport (suitable for production Cloud Run deployment)
# FastMCP runs as an ASGI web application under the hood when transport is set to sse.
CMD ["fastmcp", "run", "mcp_server.py:mcp", "--port", "8080", "--transport", "sse"]
