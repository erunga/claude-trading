# scripts/research.py

import os
import requests
from datetime import datetime, timedelta, timezone
import json
from dotenv import load_dotenv

load_dotenv()

ALPACA_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_BASE_URL")

def get_bars(symbol, timeframe="1Day", limit=100):
    """Fetch historical price bars for a symbol.

    Without an explicit start date, the API defaults to a window that can be
    as narrow as a single trading day, which isn't enough to compute 20/50-day
    moving averages — so we request a range wide enough to comfortably cover
    50 trading days.
    """
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
    start = (datetime.now(timezone.utc) - timedelta(days=110)).strftime("%Y-%m-%d")
    params = {
        "timeframe": timeframe,
        "limit": limit,
        "adjustment": "raw",
        "start": start,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_account():
    """Get current portfolio status."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"{BASE_URL}/v2/account"
    response = requests.get(url, headers=headers)
    return response.json()

def get_positions():
    """Get all open positions."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"{BASE_URL}/v2/positions"
    response = requests.get(url, headers=headers)
    return response.json()

def get_orders(after=None, until=None, status="all", limit=100):
    """Get orders, optionally filtered by a date window."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"{BASE_URL}/v2/orders"
    params = {"status": status, "limit": limit}
    if after:
        params["after"] = after
    if until:
        params["until"] = until
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_quote(symbol):
    """Get the latest quote (bid/ask) for a symbol."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest"
    response = requests.get(url, headers=headers)
    return response.json()

def get_news(symbol):
    """Get recent news for a symbol."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"https://data.alpaca.markets/v1beta1/news"
    params = {
        "symbols": symbol,
        "limit": 5,
        "sort": "desc"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "account"
    symbol = sys.argv[2] if len(sys.argv) > 2 else None
    
    if action == "bars" and symbol:
        print(json.dumps(get_bars(symbol)))
    elif action == "quote" and symbol:
        print(json.dumps(get_quote(symbol)))
    elif action == "news" and symbol:
        print(json.dumps(get_news(symbol)))
    elif action == "positions":
        print(json.dumps(get_positions()))
    elif action == "orders":
        after = sys.argv[2] if len(sys.argv) > 2 else None
        until = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(get_orders(after=after, until=until)))
    else:
        print(json.dumps(get_account()))