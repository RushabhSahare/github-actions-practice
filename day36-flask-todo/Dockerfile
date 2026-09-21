# Build stage: compile dependencies into a venv
FROM python:3.8-slim AS builder

WORKDIR /app

# gcc and libpq-dev are only needed to build psycopg2-binary wheels if no prebuilt wheel matches; kept minimal and dropped after this stage
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Final stage: clean slim image, no build tools
FROM python:3.8-slim

RUN useradd --create-home appuser
WORKDIR /app

# Bring in only the installed venv, not the build tools
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

USER appuser

EXPOSE 5000

CMD ["python", "run.py"]
