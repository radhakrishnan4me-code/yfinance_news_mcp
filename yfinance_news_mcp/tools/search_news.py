from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def register_search_news(mcp: FastMCP):
    @mcp.tool()
    def search_news(
        query: str = Field(..., description="Search phrase, e.g. 'RBI rate hike'"),
        symbol: Optional[str] = Field(None, description="Optional symbol to scope the search"),
        limit: int = Field(20, description="Max results")
    ) -> List[Dict[str, Any]]:
        """Search news metadata by keyword and optionally symbol."""
        # Note: yfinance doesn't have a direct global news search without a ticker.
        # If symbol is not provided, we can fallback to a broad market index like ^NSEI as a proxy for "general news".
        search_symbol = symbol if symbol else "^NSEI"
        
        # Fetch a larger pool to search within
        news_items = fetch_symbol_news(search_symbol, limit=100)
        
        results = []
        query_lower = query.lower()
        
        for item in news_items:
            # Check headline and summary for matches
            if query_lower in item.headline.lower() or query_lower in item.summary.lower():
                results.append(item.model_dump(mode="json"))
                if len(results) >= limit:
                    break
                    
        return results
