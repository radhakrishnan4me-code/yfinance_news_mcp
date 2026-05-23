from datetime import datetime
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from yfinance_news_mcp.tools.fetcher import fetch_symbol_news, NewsItem

def register_symbol_news(mcp: FastMCP):
    @mcp.tool()
    def get_symbol_news(
        symbol: str = Field(..., description="Yahoo ticker like SBIN.NS, ^NSEI, CRUDEOIL.NS"),
        limit: int = Field(20, description="Max number of articles"),
        since: Optional[str] = Field(None, description="ISO8601 datetime string. Only return news newer than this.")
    ) -> List[dict]:
        """Fetch recent news metadata for a single symbol."""
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            except ValueError:
                pass # Invalid date, ignore

        items = fetch_symbol_news(symbol, limit=limit, since=since_dt)
        return [item.model_dump(mode="json") for item in items]
