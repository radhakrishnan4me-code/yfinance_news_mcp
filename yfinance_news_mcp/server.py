from mcp.server.fastmcp import FastMCP

from yfinance_news_mcp.tools.symbol_news import register_symbol_news
from yfinance_news_mcp.tools.multi_symbol_news import register_multi_symbol_news
from yfinance_news_mcp.tools.index_news import register_index_news
from yfinance_news_mcp.tools.mcx_news import register_mcx_news
from yfinance_news_mcp.tools.topics_summary import register_topics_summary
from yfinance_news_mcp.tools.search_news import register_search_news

def create_server() -> FastMCP:
    mcp = FastMCP("yfinance-news-mcp")
    
    register_symbol_news(mcp)
    register_multi_symbol_news(mcp)
    register_index_news(mcp)
    register_mcx_news(mcp)
    register_topics_summary(mcp)
    register_search_news(mcp)
    
    return mcp

app = create_server()
