from datetime import datetime, timezone
import yfinance as yf
from pydantic import BaseModel
from typing import List, Optional

class NewsItem(BaseModel):
    symbol: str
    headline: str
    source: str
    published_at: datetime
    url: str
    summary: str
    categories: List[str]

def fetch_symbol_news(symbol: str, limit: int = 20, since: Optional[datetime] = None) -> List[NewsItem]:
    """
    Fetches news metadata for a single symbol using yfinance.
    """
    try:
        ticker = yf.Ticker(symbol)
        raw_news = ticker.news
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []

    news_items = []
    if not raw_news:
        return []

    for item in raw_news:
        try:
            # yfinance returns nested content now
            content = item.get("content", item)
            
            # pubDate is ISO format string, fallback to old timestamp if needed
            pub_date_str = content.get("pubDate", "")
            if pub_date_str:
                pub_time = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            else:
                pub_time = datetime.fromtimestamp(content.get("providerPublishTime", 0), tz=timezone.utc)
            
            if since and pub_time < since:
                continue

            # some short summary from the available text or just title if empty
            summary_text = content.get("summary", "")
            if not summary_text:
                summary_text = "No summary available."
                
            provider = content.get("provider", {})
            source = provider.get("displayName", "Unknown Publisher") if isinstance(provider, dict) else content.get("publisher", "Unknown Publisher")
            
            url_obj = content.get("clickThroughUrl", {})
            url = url_obj.get("url", "") if isinstance(url_obj, dict) else content.get("link", "")

            news_items.append(NewsItem(
                symbol=symbol,
                headline=content.get("title", "No Title"),
                source=source,
                published_at=pub_time,
                url=url,
                summary=summary_text,
                categories=[content.get("contentType", content.get("type", "STORY"))]
            ))
            
            if len(news_items) >= limit:
                break
        except Exception as e:
            print(f"Error parsing news item for {symbol}: {e}")
            continue

    return news_items
