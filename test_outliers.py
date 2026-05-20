from meridian.outliers import fetch_outliers

print("\nFetching outliers...")
outliers = fetch_outliers()

print(f"\nDay Gainers (>{outliers['day_threshold']}%):")
for s in outliers["day_gainers"]:
    print(f"  {s['ticker']}: +{s['day_pct']:.2f}%")

print(f"\nDay Losers (<-{outliers['day_threshold']}%):")
for s in outliers["day_losers"]:
    print(f"  {s['ticker']}: {s['day_pct']:.2f}%")


print(f"\nWeek Gainers (>{outliers['week_threshold']}%):")
for s in outliers["week_gainers"]:
    print(f"  {s['ticker']}: +{s['week_pct']:.2f}%")

print(f"\nWeek Losers (<-{outliers['week_threshold']}%):")
for s in outliers["week_losers"]:
    print(f"  {s['ticker']}: {s['week_pct']:.2f}%")