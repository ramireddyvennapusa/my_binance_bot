# src/limit_orders.py
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity, validate_price

logger = setup_logger()

def place_limit_order(symbol: str, side: str, quantity, price, time_in_force="GTC"):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    price = validate_price(price)
    side = side.upper()
    if side not in ("BUY","SELL"):
        raise ValueError("side must be BUY or SELL")

    client = get_client()
    logger.info(f"Placing LIMIT order: {symbol} {side} {quantity} @ {price}")
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce=time_in_force,
            quantity=quantity,
            price=str(price)
        )
        logger.info(f"Limit order result: {order}")
        return order
    except Exception as e:
        logger.exception("Error placing limit order")
        raise
