from exchange_factory import make_exchange

def scan_all(venue="okx", bases=None):
    ex = make_exchange(venue)
    ex.load_markets()

    bases = bases or ["BTC", "ETH", "SOL", "ADA", "XRP"]
    signals = []

    for base in bases:
        symbol = f"{base}/USDT"
        if symbol not in ex.markets:
            continue
        try:
            ohlcv = ex.fetch_ohlcv(symbol, timeframe="1m", limit=2)
            if not ohlcv:
                continue
            ts, open_, high, low, close, vol = ohlcv[-1]
            direction = "buy" if close > open_ else "sell"
            signals.append({
                "symbol": symbol,
                "price": close,
                "direction": direction,
                "ts": ts
            })
        except Exception as e:
            print("SCAN ERROR:", symbol, e)

    return {"count": len(signals), "items": signals}
