from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance_news_mcp.config import settings
from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def register_mcx_news(mcp: FastMCP):
    @mcp.tool()
    def get_mcx_news_snapshot(
        assets: Optional[List[str]] = Field(None, description="Logical assets like MCX_CRUDEOIL, MCX_NATURALGAS")
    ) -> List[Dict[str, Any]]:
        """Concentrate on MCX Crude Oil and MCX Natural Gas news."""
        if assets is None:
            assets = ["MCX_CRUDEOIL", "MCX_NATURALGAS"]

        results = []
        for asset in assets:
            yahoo_symbol = settings.mcx_assets.get(asset, asset)
            news_items = fetch_symbol_news(yahoo_symbol, limit=10)
            
            results.append({
                "asset_id": asset,
                "symbol": yahoo_symbol,
                "news": [item.model_dump(mode="json") for item in news_items]
            })
            
        return results
