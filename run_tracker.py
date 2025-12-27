from flask import Flask, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)
SIGNAL_STORE = {}
DB_FILE = "signals.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS signals (
        id TEXT PRIMARY KEY,
        symbol TEXT,
        price REAL,
        direction TEXT,
        ts INTEGER,
        status TEXT,
        reason TEXT
    )""")
    conn.commit()
    conn.close()

def save_signal(sig):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?)",
              (sig["id"], sig["symbol"], sig["price"], sig["direction"],
               sig["ts"], sig.get("status","pending"), sig.get("reason")))
    conn.commit()
    conn.close()

@app.get("/api/signals")
def api_signals():
    return jsonify({"items": list(SIGNAL_STORE.values())})

@app.get("/api/history")
def api_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM signals ORDER BY ts DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify({"items":[{
        "id":r[0],"symbol":r[1],"price":r[2],"direction":r[3],
        "ts":r[4],"status":r[5],"reason":r[6]} for r in rows]})

@app.get("/api/validation_summary")
def api_validation_summary():
    total = len(SIGNAL_STORE)
    accepted = sum(1 for v in SIGNAL_STORE.values() if v.get("status")=="accepted")
    rejected = total - accepted
    return jsonify({"total_signals": total, "accepted": accepted, "rejected": rejected})

@app.get("/dashboard")
def dashboard():
    return send_from_directory(".", "dashboard.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)