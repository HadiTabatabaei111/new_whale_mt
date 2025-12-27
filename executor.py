import os

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

def _safe_amount(ex, symbol, fallback=0.001):
    m = ex.markets.get(symbol, {})
    limits = m.get("limits", {})
    amin = (limits.get("amount", {}) or {}).get("min", None)
    if amin and isinstance(amin, (int, float)):
        return max(fallback, amin)
    return fallback

def execute_signal(ex, sig):
    symbol = sig["symbol"]
    side = sig["direction"]
    amount = _safe_amount(ex, symbol)

    if DRY_RUN:
        return {
            "status": "dry_run",
            "symbol": symbol,
            "side": side,
            "amount": amount
        }

    try:
        order = ex.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=amount
        )
        return {"status": "executed", "order": order}
    except Exception as e:
        return {"status": "error", "error": str(e)}
