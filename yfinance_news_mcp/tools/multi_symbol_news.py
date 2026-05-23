from datetime import datetime
from typing import Optional, List, Dict
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def register_multi_symbol_news(mcp: FastMCP):
    @mcp.tool()
    def get_multi_symbol_news(
        symbols: List[str] = Field(..., description="List of Yahoo tickers"),
        limit_per_symbol: int = Field(10, description="Max number of articles per symbol"),
        since: Optional[str] = Field(None, description="ISO8601 datetime string")
    ) -> Dict[str, List[dict]]:
        """Fetch news for multiple symbols in one call."""
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            except ValueError:
                pass

        results = {}
        for symbol in symbols:
            items = fetch_symbol_news(symbol, limit=limit_per_symbol, since=since_dt)
            results[symbol] = [item.model_dump(mode="json") for item in items]
            
        return results
