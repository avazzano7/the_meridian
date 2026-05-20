from meridian.market_data import fetch_quotes, fetch_headlines

quotes = fetch_quotes()
for q in quotes:
    print(f"{q['name']}: {q['price']:.2f} {q['arrow']} {q['pct']:.2f}%")

print("\nHeadlines:")
headlines = fetch_headlines()
for h in headlines:
    print(f"  - {h}")