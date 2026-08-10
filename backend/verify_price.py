"""Verification script after live price fix."""
import httpx

print("=== LIVE PRICE ENDPOINT TEST ===")
symbols = ["AAPL", "INFY", "RELIANCE"]
for sym in symbols:
    try:
        r = httpx.get(f"http://localhost:8000/api/price/{sym}", timeout=15)
        d = r.json()
        print(f"  {sym}: price={d.get('price')}  change_pct={d.get('change_pct')}%  src={d.get('source')}")
    except Exception as e:
        print(f"  {sym}: ERROR - {e}")

print()
print("=== FULL ANALYZE ENDPOINT TEST (INFY) ===")
r2 = httpx.post("http://localhost:8000/api/analyze", json={"symbol": "INFY"}, timeout=90)
d2 = r2.json()
print(f"  current_price  : {d2.get('current_price')}")
print(f"  change_pct     : {d2.get('change_pct')}%")
print(f"  market_state   : {d2.get('market_state')}")
sys_status = d2.get("system_status", {})
print(f"  cache_status   : {sys_status.get('cache_status')}")
print(f"  yfinance_status: {sys_status.get('yfinance_status')}")
print(f"  exec_time_sec  : {sys_status.get('execution_time_sec')}")
