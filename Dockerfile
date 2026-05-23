FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV MCP_PORT=8816

WORKDIR /app

# Install dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY yfinance_news_mcp/ ./yfinance_news_mcp/

# Install the project
RUN pip install --no-cache-dir .

EXPOSE 8816

CMD ["python", "-m", "yfinance_news_mcp"]
