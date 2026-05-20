import yfinance as yf
import feedparser
from dotenv import load_dotenv

load_dotenv()

WATCHLIST = {
    "S&P 500":      "^GSPC",
    "Nasdaq":       "^IXIC",
    "Dow Jones":    "^DJI",
    "Russell 2000": "^RUT",
    "10Y Yield":    "^TNX",
    "VIX":          "^VIX",
    "ES Futures":   "ES=F",
    "Apple":        "AAPL",
    "Nvidia":       "NVDA",
    "Microsoft":    "MSFT",
    "Gold":         "GC=F",
    "Oil (WTI)":    "CL=F",
}

NEWS_FEEDS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
]

def fetch_quotes():
    quotes = []
    for name, ticker in WATCHLIST.items():
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if len(hist) < 2:
                continue
            prev = hist["Close"].iloc[-2]
            last = hist["Close"].iloc[-1]
            week_ago = hist["Close"].iloc[0]
            change = last - prev
            pct = (change / prev) * 100
            week_pct = ((last - week_ago) / week_ago) * 100
            quotes.append({
                "name": name,
                "ticker": ticker,
                "price": last,
                "change": change,
                "pct": pct,
                "week_pct": week_pct,
                "arrow": "▲" if change >= 0 else "▼",
                "color": "#2ecc71" if change >= 0 else "#e74c3c",
            })
        except Exception as e:
            print(f"[!] Error fetching {ticker}: {e}")
    return quotes


def fetch_headlines(max_per_feed=5):
    headlines = []
    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_per_feed]:
                headlines.append(entry.title)
        except Exception as e:
            print(f"[!] Error fetching news from {url}: {e}")
    return headlines