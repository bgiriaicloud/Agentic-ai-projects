# =============================================================================
# PRODUCTION MULTI-STAGE DOCKERFILE FOR HEALTHCARE MULTI-AGENT PLATFORM (GCP)
# Complies with HIPAA Security Rule, Non-Root User Execution & Minimal Attack Surface
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Dependency Builder
# -----------------------------------------------------------------------------
FROM python:3.11-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Hardened Runtime Container
# -----------------------------------------------------------------------------
FROM python:3.11-slim as runtime

WORKDIR /app

# Create dedicated non-root healthcare user (UID 1001)
RUN useradd -m -u 1001 hcareuser && \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python site-packages from builder
COPY --from=builder /root/.local /home/hcareuser/.local
COPY --chown=hcareuser:hcareuser . .

# Set Environment Variables
ENV PATH=/home/hcareuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8005 \
    ENVIRONMENT=production

USER hcareuser

EXPOSE 8005

# Container Healthcheck (every 30s)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8005/api/healthz || exit 1

# Start FastAPI Uvicorn Server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8005"]
