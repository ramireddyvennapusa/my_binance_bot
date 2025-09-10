# src/market_orders.py
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity

logger = setup_logger()

def place_market_order(symbol: str, side: str, quantity):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    side = side.upper()
    if side not in ("BUY","SELL"):
        raise ValueError("side must be BUY or SELL")

    client = get_client()
    logger.info(f"Placing MARKET order: {symbol} {side} {quantity}")
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
            reduceOnly=False
        )
        logger.info(f"Market order result: {order}")
        return order
    except Exception as e:
        logger.exception("Error placing market order")
        raise
