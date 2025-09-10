# src/advanced/stop_limit.py
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity, validate_price

logger = setup_logger()

def place_stop_limit(symbol: str, side: str, quantity, stop_price, limit_price, time_in_force="GTC"):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    stop_price = validate_price(stop_price)
    limit_price = validate_price(limit_price)
    side = side.upper()
    if side not in ("BUY","SELL"):
        raise ValueError("side must be BUY or SELL")

    client = get_client()
    logger.info(f"Placing STOP-LIMIT: {symbol} {side} {quantity}, stop={stop_price}, limit={limit_price}")
    try:
        # Using STOP (trigger) + LIMIT type
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            stopPrice=str(stop_price),
            price=str(limit_price),
            quantity=quantity,
            timeInForce=time_in_force
        )
        logger.info(f"Stop-Limit order result: {order}")
        return order
    except Exception as e:
        logger.exception("Error placing stop-limit order")
        raise
