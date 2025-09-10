# src/binance_client.py
import os
from binance.client import Client  # Correct import

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("BINANCE_USE_TESTNET", "true").lower() in ("1", "true", "yes")
    if not api_key or not api_secret:
        raise EnvironmentError("Set BINANCE_API_KEY and BINANCE_API_SECRET in environment variables.")
    client = Client(api_key, api_secret)
    # Enable futures endpoints
    client.FUTURES_URL = client.API_URL  # keep attribute
    if use_testnet:
        # python-binance testnet config
        client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'
        client.API_URL_V2 = 'https://testnet.binancefuture.com/fapi/v2'
        client.FUTURES_URL = 'https://testnet.binancefuture.com'
    return client
