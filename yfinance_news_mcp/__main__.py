import uvicorn
from yfinance_news_mcp.server import app
from yfinance_news_mcp.config import settings

def main():
    print(f"Starting yfinance-news-mcp on {settings.mcp_host}:{settings.mcp_port}")
    # Run using the FastMCP's built-in run method or uvicorn
    # app.run(transport="sse") uses uvicorn under the hood.
    app.settings.port = settings.mcp_port
    app.settings.host = settings.mcp_host
    app.run(transport="sse")

if __name__ == "__main__":
    main()
