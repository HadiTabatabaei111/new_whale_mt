import ccxt

def pumpdump_scan(venue="okx", bases=None, threshold=1.0):
    ex = ccxt.okx()
    ex.load_markets()

    bases = bases or ["BTC", "ETH", "SOL", "ADA", "XRP", "DOGE", "LTC", "BNB"]
    prev_prices = {}
    pumpdump_list = []

    for base in bases:
        symbol = f"{base}/USDT"
        try:
            ticker = ex.fetch_ticker(symbol)
            price = ticker["last"]

            if symbol in prev_prices:
                prev = prev_prices[symbol]
                change_pct = (price - prev) / prev * 100
                if abs(change_pct) >= threshold:
                    pumpdump_list.append({
                        "symbol": symbol,
                        "price": price,
                        "change_pct": round(change_pct, 2),
                        "direction": "pump" if change_pct > 0 else "dump"
                    })
            prev_prices[symbol] = price
        except Exception as e:
            print("PumpDump ERROR:", symbol, e)

    return {"count": len(pumpdump_list), "items": pumpdump_list}
