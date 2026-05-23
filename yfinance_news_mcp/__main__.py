import uvicorn
from yfinance_news_mcp.server import app
from yfinance_news_mcp.config import settings

def main():
    print(f"Starting yfinance-news-mcp on {settings.mcp_host}:{settings.mcp_port} with Streamable HTTP")
    fastapi_app = app.streamable_http_app()
    uvicorn.run(fastapi_app, host=settings.mcp_host, port=settings.mcp_port)

if __name__ == "__main__":
    main()
