FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as non-root security user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8003

CMD ["python3", "app.py"]
