FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy app
COPY ingest_data.py .

# Use uv
ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]