# yfinance-news-mcp

An HTTP-compatible Model Context Protocol (MCP) server that exposes rich, structured financial news tools tailored for AI analysis and n8n integration. 

This project focuses on the **Indian Markets**, specifically:
- NSE equities and indices (NIFTY, BANKNIFTY, etc.)
- MCX commodities (Crude Oil, Natural Gas)

The server exposes an **HTTP / SSE Transport** using the official `mcp` Python SDK's FastMCP wrapper.

> **Disclaimer**: This project is for informational and educational purposes only. It does not constitute financial advice. Data is sourced from Yahoo Finance and is subject to their terms of service. This project only fetches news metadata and summaries—no full article bodies are stored or returned to respect copyright limits.

## Available Tools

1. **`get_symbol_news`**: Fetch recent news metadata for a single symbol (e.g., `SBIN.NS`, `^NSEI`, `CRUDEOIL.NS`).
2. **`get_multi_symbol_news`**: Fetch news for multiple symbols in one call.
3. **`get_index_and_sector_news`**: Focus on NSE index news. Supports pulling news for top constituents.
4. **`get_mcx_news_snapshot`**: Quickly fetch a snapshot for MCX Crude Oil and Natural Gas.
5. **`get_news_topics_summary`**: Locally cluster news headlines into topics (Earnings, Macro & Policy, Company Actions) for AI summaries.
6. **`search_news`**: Substring search on recent news metadata by keyword and symbol.

## Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/yfinance-news-mcp.git
cd yfinance-news-mcp

# Install dependencies
pip install .

# Run the server
python -m yfinance_news_mcp
```
The server will start on `http://0.0.0.0:8816`.

## Portainer Setup & Deployment

To deploy this via Portainer using Docker Compose:

1. **Build the image**:
   (If your Portainer agent has access to build from a Git repo, or build it locally and push to a registry).
   Alternatively, build locally:
   ```bash
   docker build -t yfinance-news-mcp:latest .
   ```
2. **Deploy via Portainer Stacks**:
   Copy the contents of `docker-compose.yml` into a new Portainer Stack.
   ```yaml
   version: "3.9"
   services:
     yfinance-news-mcp:
       image: yfinance-news-mcp:latest
       container_name: yfinance-news-mcp
       environment:
         MCP_PORT: "8816"
       ports:
         - "8816:8816"
       restart: unless-stopped
   ```
   Click "Deploy the stack".
3. **Test the Endpoint**:
   Once running, you can test if the SSE endpoint is accessible:
   ```bash
   curl -N http://<server-ip>:8816/sse
   ```
   *(Note: FastMCP automatically exposes `/sse` for Server-Sent Events by default. Check the endpoint based on the exact version you're using. n8n will hit this URL).*

## n8n MCP Client Tool Configuration

You can easily integrate this server into an **n8n** workflow using the MCP Client node.

1. Add a **Model Context Protocol (MCP)** Client node to your n8n workflow.
2. Configure the **Connection Details**:
   - **Transport**: `SSE` / `Streamable HTTP`
   - **URL**: `http://yfinance-news-mcp:8816/sse` (if running in the same Docker network) or `http://<your-vps-ip>:8816/sse`.
3. Select a tool, for example, `get_mcx_news_snapshot`.
4. Provide the required JSON arguments.
   - For `get_news_topics_summary`, pass `{"symbol": "^NSEI"}` to get an aggregated view of index topics.
5. Execute the node! It will parse the Pydantic schema and provide strongly-typed outputs to the rest of your n8n workflow.
