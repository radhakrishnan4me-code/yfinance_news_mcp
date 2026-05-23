from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def register_topics_summary(mcp: FastMCP):
    @mcp.tool()
    def get_news_topics_summary(
        symbol: str = Field(..., description="Yahoo ticker"),
        limit: int = Field(50, description="Max news items to fetch before clustering")
    ) -> List[Dict[str, Any]]:
        """Convert lots of raw news metadata into topics/clusters for AI."""
        news_items = fetch_symbol_news(symbol, limit=limit)
        
        topics = {
            "Earnings": {"keywords": ["earnings", "q1", "q2", "q3", "q4", "dividend", "profit", "revenue"], "count": 0, "samples": []},
            "Macro & Policy": {"keywords": ["rbi", "rate", "policy", "inflation", "gdp", "tax", "government"], "count": 0, "samples": []},
            "Company Actions": {"keywords": ["merger", "acquisition", "board", "ceo", "management", "stake"], "count": 0, "samples": []},
            "Other": {"keywords": [], "count": 0, "samples": []}
        }
        
        for item in news_items:
            headline = item.headline.lower()
            matched = False
            
            for topic_name, data in topics.items():
                if topic_name == "Other":
                    continue
                
                if any(kw in headline for kw in data["keywords"]):
                    topics[topic_name]["count"] += 1
                    if len(topics[topic_name]["samples"]) < 3:
                        topics[topic_name]["samples"].append(item.headline)
                    matched = True
                    break
            
            if not matched:
                topics["Other"]["count"] += 1
                if len(topics["Other"]["samples"]) < 3:
                    topics["Other"]["samples"].append(item.headline)
                    
        results = []
        for topic_name, data in topics.items():
            if data["count"] > 0:
                results.append({
                    "topic_name": topic_name,
                    "keywords": data["keywords"],
                    "news_count": data["count"],
                    "sample_headlines": data["samples"]
                })
                
        return results
