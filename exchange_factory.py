import ccxt
import os

def make_exchange(venue: str):
    venue = venue.lower()
    if venue == "okx":
        api_key = os.getenv("OKX_API_KEY")
        secret = os.getenv("OKX_SECRET")
        password = os.getenv("OKX_PASSWORD")
        cfg = {}
        if api_key and secret and password:
            cfg = {"apiKey": api_key, "secret": secret, "password": password}
        ex = ccxt.okx(cfg)
        ex.options = {"defaultType": "spot"}
        return ex
    elif venue == "binance":
        return ccxt.binance()
    elif venue == "bybit":
        return ccxt.bybit()
    elif venue == "kucoin":
        return ccxt.kucoin()
    else:
        raise ValueError(f"Unsupported venue: {venue}")
