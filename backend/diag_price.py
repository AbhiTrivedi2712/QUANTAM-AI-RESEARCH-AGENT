"""
Quick diagnostic script — checks what price yfinance actually returns for AAPL and INFY.NS.
Run: python diag_price.py
"""
import yfinance as yf
import requests
from requests.adapters import HTTPAdapter

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", 5.0)
        super().__init__(*args, **kwargs)
    def send(self, request, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
adapter = TimeoutHTTPAdapter(timeout=10.0)
session.mount("https://", adapter)
session.mount("http://", adapter)

def diag(symbol):
    print(f"\n=== {symbol} PRICE DIAGNOSTIC ===")
    try:
        ticker = yf.Ticker(symbol, session=session)
        info = ticker.info

        market_state = info.get("marketState", "UNKNOWN")
        reg_price     = info.get("regularMarketPrice")
        cur_price     = info.get("currentPrice")
        pre_price     = info.get("preMarketPrice")
        post_price    = info.get("postMarketPrice")
        prev_close    = info.get("previousClose")
        reg_change    = info.get("regularMarketChange")
        reg_change_pct= info.get("regularMarketChangePercent")

        print(f"  marketState             : {market_state}")
        print(f"  regularMarketPrice      : {reg_price}")
        print(f"  currentPrice            : {cur_price}")
        print(f"  preMarketPrice          : {pre_price}")
        print(f"  postMarketPrice         : {post_price}")
        print(f"  previousClose           : {prev_close}")
        print(f"  regularMarketChange     : {reg_change}")
        print(f"  regularMarketChangePct  : {reg_change_pct}")

        hist = ticker.history(period="1y", interval="1d")
        hist = hist.dropna(subset=["Close"]) if not hist.empty else hist
        if not hist.empty:
            last_close = float(hist["Close"].iloc[-1])
            last_date  = str(hist.index[-1])
            print(f"  history last Close      : {last_close}")
            print(f"  history last date       : {last_date}")
        else:
            print("  history                 : EMPTY")

        # Determine what the backend would actually serve
        if market_state == "PRE" and pre_price:
            chosen = float(pre_price)
            label  = "PRE-MARKET"
        elif market_state in ("POST", "POSTPOST") and post_price:
            chosen = float(post_price)
            label  = "POST-MARKET"
        else:
            chosen = float(reg_price) if reg_price else (float(cur_price) if cur_price else last_close)
            label  = "REGULAR/FALLBACK"

        print(f"\n  >>> BACKEND WOULD SERVE : {chosen:.2f}  ({label})")

    except Exception as e:
        print(f"  ERROR: {e}")

diag("AAPL")
diag("INFY.NS")
diag("RELIANCE.NS")
