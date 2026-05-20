import yfinance as yf
import pandas as pd
import requests


def get_sp500_tickers():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    response = requests.get(url)
    df = pd.read_csv(pd.io.common.StringIO(response.text))
    return df["Symbol"].str.replace(".", "-", regex=False).tolist()


def fetch_outliers(day_threshold=5.0, week_threshold=10.0):
    print("Fetching S&P 500 tickers from Wikipedia...")
    tickers = get_sp500_tickers()

    print(f"Downloading price data for {len(tickers)} tickers...")
    data = yf.download(
        tickers,
        period="5d",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
    )

    day_gainers, day_losers, week_gainers, week_losers = [], [], [], []

    for ticker in tickers:
        try:
            closes = data[ticker]["Close"].dropna()
            if ticker == "AAPL":
                print(f"AAPL closes:\n{closes}")
                print(f"Number of rows: {len(closes)}")


            if len(closes) < 2:
                continue
            prev = closes.iloc[-2]
            last = closes.iloc[-1]
            week_start = closes.iloc[0]
            day_pct = ((last - prev) / prev) * 100
            week_pct = ((last - week_start) / week_start) * 100
            entry = {
                "ticker": ticker,
                "price": last,
                "day_pct": day_pct,
                "week_pct": week_pct,
            }

            if day_pct >= day_threshold:
                day_gainers.append(entry)
            elif day_pct <= -day_threshold:
                day_losers.append(entry)

            if week_pct >= week_threshold:
                week_gainers.append(entry)
            elif week_pct <= -week_threshold:
                week_losers.append(entry)

        except Exception as e:
            continue

    return {
        "day_gainers": sorted(day_gainers,  key=lambda x: x["day_pct"],  reverse=True)[:10],
        "day_losers": sorted(day_losers,   key=lambda x: x["day_pct"])[:10],
        "week_gainers": sorted(week_gainers, key=lambda x: x["week_pct"], reverse=True)[:10],
        "week_losers": sorted(week_losers,  key=lambda x: x["week_pct"])[:10],
        "day_threshold": day_threshold,
        "week_threshold": week_threshold,
    }