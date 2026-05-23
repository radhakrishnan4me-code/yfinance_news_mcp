from typing import List, Dict, Optional, Any
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance_news_mcp.config import settings
from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def register_index_news(mcp: FastMCP):
    @mcp.tool()
    def get_index_and_sector_news(
        index: str = Field(..., description="Logical name like NIFTY50, BANKNIFTY"),
        include_constituents: bool = Field(False, description="If true, pull news for top constituents")
    ) -> Dict[str, Any]:
        """Focus on NSE index and sector news."""
        yahoo_symbol = settings.nse_indexes.get(index)
        if not yahoo_symbol:
            # Fallback if not found in mapping
            yahoo_symbol = index

        index_news = fetch_symbol_news(yahoo_symbol, limit=15)
        
        results = {
            "index_news": [item.model_dump(mode="json") for item in index_news],
            "constituents_news": {}
        }
        
        if include_constituents:
            # Map index to a watchlist if exists
            watchlist_key = index.lower()
            constituents = settings.watchlists.get(f"nse_{watchlist_key}", [])
            if not constituents and "nse_top_5" in settings.watchlists:
                constituents = settings.watchlists["nse_top_5"]
            
            for constituent in constituents:
                c_news = fetch_symbol_news(constituent, limit=5)
                results["constituents_news"][constituent] = [item.model_dump(mode="json") for item in c_news]
                
        return results
