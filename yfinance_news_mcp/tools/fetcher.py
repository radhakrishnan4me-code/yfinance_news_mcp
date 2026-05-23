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
            # yfinance returns providerPublishTime as unix timestamp
            pub_time = datetime.fromtimestamp(item.get("providerPublishTime", 0), tz=timezone.utc)
            
            if since and pub_time < since:
                continue

            # some short summary from the available text or just title if empty
            summary_text = item.get("summary", "")
            if not summary_text:
                summary_text = "No summary available."

            news_items.append(NewsItem(
                symbol=symbol,
                headline=item.get("title", "No Title"),
                source=item.get("publisher", "Unknown Publisher"),
                published_at=pub_time,
                url=item.get("link", ""),
                summary=summary_text,
                categories=[item.get("type", "STORY")]
            ))
            
            if len(news_items) >= limit:
                break
        except Exception as e:
            print(f"Error parsing news item for {symbol}: {e}")
            continue

    return news_items
