def validate_signals(ex, store):
    validated = {}
    for sid, sig in store.items():
        symbol = sig.get("symbol")
        if symbol not in ex.markets:
            status = "rejected"
            reason = "symbol not in markets"
        else:
            price = sig.get("price")
            status = "accepted" if (isinstance(price, (int, float)) and price > 0) else "rejected"
            reason = None if status == "accepted" else "invalid price"

        validated[sid] = {
            "id": sid,
            "symbol": symbol,
            "price": sig.get("price"),
            "direction": sig.get("direction"),
            "ts": sig.get("ts"),
            "status": status,
            "reason": reason
        }
    return validated
