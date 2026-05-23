import pytest
from yfinance_news_mcp.tools.fetcher import fetch_symbol_news

def test_fetch_symbol_news():
    # Use a well-known symbol that generally has news
    news = fetch_symbol_news("RELIANCE.NS", limit=2)
    assert isinstance(news, list)
    if news:
        item = news[0]
        assert item.symbol == "RELIANCE.NS"
        assert hasattr(item, "headline")
        assert hasattr(item, "url")
        assert hasattr(item, "summary")

def test_fetch_invalid_symbol():
    # Try an invalid symbol
    news = fetch_symbol_news("INVALID_SYMBOL_123", limit=2)
    assert news == []
